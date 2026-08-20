#!/usr/bin/env python3
"""Оценка проработанности демо-лендингов/демок v2.

Учитывает inline CSS/JS внутри HTML, дизайн-токены, семантику, SEO-инфраструктуру
(sitemap/robots/security.txt), оптимизацию изображений (webp), README,
доступность. Эталон — paffo (должен набрать 85+).
"""

import json
import re
import sys
from pathlib import Path

BASE = Path("/tmp/demo_eval")


def size(p):
    try:
        return p.stat().st_size
    except OSError:
        return 0


def read(p):
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def analyze(repo_dir):
    s = {}
    files = list(repo_dir.rglob("*"))
    html_files = [f for f in files if f.suffix == ".html"]
    css_files = [f for f in files if f.suffix == ".css"]
    js_files = [f for f in files if f.suffix == ".js"]
    img_files = [f for f in files if f.suffix.lower() in
                 (".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".avif")]
    readme = next((f for f in files if f.name.lower() == "readme.md"), None)

    all_html = "".join(read(h) for h in html_files[:8])

    # --- inline CSS/JS внутри HTML ---
    inline_css = 0
    for m in re.finditer(r"<style[^>]*>(.*?)</style>", all_html, re.S):
        inline_css += len(m.group(1))
    inline_js = 0
    for m in re.finditer(r"<script(?![^>]*src)[^>]*>(.*?)</script>", all_html, re.S):
        inline_js += len(m.group(1))
    external_css = sum(size(c) for c in css_files)
    external_js = sum(size(j) for j in js_files)
    total_css = inline_css + external_css
    total_js = inline_js + external_js
    css_text = "".join(read(c) for c in css_files) + \
        "".join(m.group(1) for m in re.finditer(r"<style[^>]*>(.*?)</style>", all_html, re.S))
    js_text = "".join(read(j) for j in js_files) + \
        "".join(m.group(1) for m in re.finditer(r"<script(?![^>]*src)[^>]*>(.*?)</script>", all_html, re.S))

    # --- 1. README (0..10)
    r = 0
    if readme:
        rtext = read(readme).lower()
        rlen = size(readme)
        if rlen > 1500:
            r += 5
        elif rlen > 300:
            r += 3
        else:
            r += 1
        if any(k in rtext for k in ("how to run", "запуск", "usage", "open index")):
            r += 2
        if any(k in rtext for k in ("screenshot", "скриншот", "preview", "demo", "github pages")):
            r += 2
        if any(k in rtext for k in ("feature", "возможност", "stack", "технолог")):
            r += 1
    s["readme"] = r

    # --- 2. SEO-мета (0..12)
    seo = 0
    t = re.search(r"<title>(.*?)</title>", all_html, re.S)
    if t and len(t.group(1).strip()) > 5:
        seo += 2
    if 'name="description"' in all_html:
        seo += 2
    if 'property="og:title"' in all_html:
        seo += 2
    if 'property="og:image"' in all_html:
        seo += 2
    if 'name="twitter:card"' in all_html:
        seo += 1
    if 'rel="canonical"' in all_html:
        seo += 1
    if 'rel="icon"' in all_html:
        seo += 1
    if 'lang="ru"' in all_html or 'lang="en"' in all_html or 'lang=' in all_html:
        seo += 1
    s["seo"] = seo

    # --- 3. Семантика HTML (0..8)
    sem = 0
    for tag in ("<header", "<main", "<footer", "<nav"):
        if tag in all_html:
            sem += 1.5
    for tag in ("<section", "<article"):
        if tag in all_html:
            sem += 1
    s["semantics"] = min(8, sem)

    # --- 4. CSS: токены + адаптив + анимации + объём (0..20)
    c = 0
    if total_css > 15000:
        c += 4
    elif total_css > 4000:
        c += 3
    elif total_css > 800:
        c += 2
    else:
        c += 1
    if re.search(r":root\s*\{", css_text):
        c += 5
    elif re.search(r"--[a-z-]+\s*:", css_text):
        c += 4
    if "@media" in css_text:
        c += 3
    if re.search(r"\.dark|data-theme|prefers-color-scheme", css_text):
        c += 3
    if "@keyframes" in css_text:
        c += 2
    if "scroll-behavior" in css_text or "backdrop-filter" in css_text or "clamp(" in css_text:
        c += 2
    if "focus" in css_text and (":focus-visible" in css_text or ":focus" in css_text):
        c += 1
    s["css"] = min(20, c)

    # --- 5. JS: объём + модульность (0..10)
    j = 0
    if total_js > 12000:
        j += 4
    elif total_js > 2500:
        j += 3
    elif total_js > 400:
        j += 2
    else:
        j += 1
    if len(js_files) > 1:
        j += 3
    elif len(js_files) == 1 and external_js > 2000:
        j += 2
    if inline_js > 0 and total_js > 4000:
        j += 1
    if re.search(r"localStorage|sessionStorage", js_text):
        j += 1
    if re.search(r"addEventListener", js_text):
        j += 1
    s["js"] = min(10, j)

    # --- 6. PWA/манифест (0..8)
    pwa = 0
    if any(f.name in ("manifest.json", "manifest.webmanifest") for f in files):
        pwa += 3
    if any("service-worker" in f.name or f.name == "sw.js" for f in files):
        pwa += 3
    if 'rel="manifest"' in all_html:
        pwa += 1
    if any(f.suffix == ".png" and "icon" in f.name.lower() for f in files):
        pwa += 1
    s["pwa"] = pwa

    # --- 7. Изображения: webp + OG + кол-во (0..10)
    og = 0
    webp_count = len([f for f in img_files if f.suffix.lower() == ".webp"])
    if webp_count > 3:
        og += 4
    elif webp_count > 0:
        og += 2
    if re.search(r'property="og:image"', all_html):
        og += 2
    if len(img_files) >= 5:
        og += 2
    if readme and readme.read_text(encoding="utf-8", errors="replace").count("![") > 0:
        og += 2
    s["images"] = min(10, og)

    # --- 8. Доступность (0..10)
    a = 0
    alt_count = len(re.findall(r'<img[^>]*\salt="', all_html))
    img_count = len(re.findall(r"<img", all_html))
    if img_count and alt_count >= img_count * 0.8:
        a += 4
    elif img_count == 0:
        a += 2
    if "aria-" in all_html or 'role="' in all_html:
        a += 2
    if re.search(r'<label[^>]*>', all_html):
        a += 2
    if "font-display" in css_text or "preconnect" in all_html or "preload" in all_html:
        a += 1
    if ":focus-visible" in css_text or "outline" in css_text:
        a += 1
    s["a11y"] = min(10, a)

    # --- 9. Инфраструктура сайта (0..8)
    inf = 0
    if (repo_dir / "sitemap.xml").exists():
        inf += 2
    if (repo_dir / "robots.txt").exists():
        inf += 2
    if (repo_dir / ".well-known" / "security.txt").exists():
        inf += 2
    if (repo_dir / "CNAME").exists():
        inf += 1
    if (repo_dir / "404.html").exists():
        inf += 1
    s["infra"] = inf

    # --- 10. Структура проекта (0..4)
    st = 0
    if css_files or inline_css > 0:
        st += 1
    if js_files or inline_js > 0:
        st += 1
    if len(html_files) > 1:
        st += 1
    if readme:
        st += 1
    s["structure"] = st

    total = sum(v for v in s.values())
    s["total"] = total
    s["html_kb"] = round(sum(size(h) for h in html_files) / 1024, 1)
    s["css_kb"] = round(total_css / 1024, 1)
    s["js_kb"] = round(total_js / 1024, 1)
    s["webp"] = webp_count
    return s


def main():
    results = []
    for repo_dir in sorted(BASE.iterdir()):
        if not repo_dir.is_dir() or repo_dir.name.startswith("."):
            continue
        try:
            r = analyze(repo_dir)
            r["repo"] = repo_dir.name
            results.append(r)
        except Exception as e:
            print(f"ERR {repo_dir.name}: {e}", file=sys.stderr)

    results.sort(key=lambda x: x["total"], reverse=True)
    print(f"{'Репозиторий':<18} {'Итог':>5}  RDM SEO Сем CSS  JS PWA IMG A11 Inf Стр")
    print("-" * 76)
    for r in results:
        print(f"{r['repo']:<18} {r['total']:>5}  {r['readme']:>3} {r['seo']:>3} "
              f"{r['semantics']:>3.0f} {r['css']:>3} {r['js']:>3} {r['pwa']:>3} "
              f"{r['images']:>3} {r['a11y']:>3.0f} {r['infra']:>3} {r['structure']:>3}")

    with open("/tmp/demo_eval_scores.json", "w") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()