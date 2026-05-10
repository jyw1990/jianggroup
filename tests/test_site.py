#!/usr/bin/env python3
"""
Jiang Group Website — Test Suite
Run with: python3 tests/test_site.py
Tests structure, data integrity, and HTML correctness.
"""

import os
import json
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errors = []
passed = 0

def ok(msg):
    global passed
    passed += 1
    print(f"  ✅ {msg}")

def fail(msg):
    errors.append(msg)
    print(f"  ❌ {msg}")

def assert_true(cond, msg):
    if cond: ok(msg)
    else: fail(msg)

def assert_file(path, label=None):
    full = os.path.join(ROOT, path)
    assert_true(os.path.isfile(full), label or f"File exists: {path}")
    return full

def read_json(path):
    with open(os.path.join(ROOT, path)) as f:
        return json.load(f)

def read_html(path):
    with open(os.path.join(ROOT, path)) as f:
        return f.read()

print("\n── File Structure ──────────────────────────────────")
assert_file("index.html")
assert_file("pages/people/index.html")
assert_file("pages/alumni/index.html")
assert_file("pages/research/index.html")
assert_file("pages/publications/index.html")
assert_file("pages/photos/index.html")
assert_file("pages/contact/index.html")
assert_file("assets/css/style.css")
assert_file("assets/js/main.js")
assert_file("assets/images/logo.png")

print("\n── Data Files ──────────────────────────────────────")
assert_file("data/news.json")
assert_file("data/people.json")
assert_file("data/alumni.json")
assert_file("data/research.json")
assert_file("data/publications.json")
assert_file("data/photos.json")

print("\n── news.json ───────────────────────────────────────")
news = read_json("data/news.json")
assert_true(isinstance(news, list), "news.json is a list")
assert_true(len(news) > 0, "news.json has entries")
for i, n in enumerate(news):
    assert_true("id" in n, f"news[{i}] has id")
    assert_true("date" in n, f"news[{i}] has date")
    assert_true("month" in n, f"news[{i}] has month")
    assert_true("text" in n, f"news[{i}] has text")
    assert_true(isinstance(n.get("image"), (str, type(None))), f"news[{i}] image is str or null")
    # Validate date format
    assert_true(re.match(r'\d{4}-\d{2}-\d{2}', n["date"]), f"news[{i}] date format YYYY-MM-DD")

print("\n── people.json ─────────────────────────────────────")
people = read_json("data/people.json")
assert_true("pi" in people, "people.json has pi")
assert_true("postdocs" in people, "people.json has postdocs")
assert_true("phd_students" in people, "people.json has phd_students")
assert_true("masters_students" in people, "people.json has masters_students")
assert_true("undergrad_students" in people, "people.json has undergrad_students")
assert_true("highschool_students" in people, "people.json has highschool_students")

pi = people["pi"]
for field in ["name","title","email","bio"]:
    assert_true(field in pi, f"PI has {field}")

for category, required in [
    ("postdocs",          ["id","name","email","bio","photo"]),
    ("phd_students",      ["id","name","email","bio","photo"]),
    ("masters_students",  ["id","name","email","department","photo"]),
    ("undergrad_students",["id","name","email","department","photo"]),
]:
    for i, m in enumerate(people.get(category, [])):
        for f in required:
            assert_true(f in m, f"{category}[{i}] has {f}")

print("\n── alumni.json ─────────────────────────────────────")
alumni = read_json("data/alumni.json")
assert_true("masters_students" in alumni, "alumni.json has masters_students")
assert_true("undergrad_students" in alumni, "alumni.json has undergrad_students")
assert_true("highschool_students" in alumni, "alumni.json has highschool_students")

for category, required in [
    ("masters_students",  ["id","name","department","years","exit_year","photo"]),
    ("undergrad_students",["id","name","department","years","exit_year","photo"]),
    ("highschool_students",["id","name","school","years","exit_year","photo"]),
]:
    arr = alumni.get(category, [])
    for i, m in enumerate(arr):
        for f in required:
            assert_true(f in m, f"alumni.{category}[{i}] has {f}")
    # Check sorted descending by exit_year
    if len(arr) > 1:
        years = [m["exit_year"] for m in arr]
        assert_true(years == sorted(years, reverse=True), f"alumni.{category} ordered by exit_year desc")

print("\n── research.json ───────────────────────────────────")
research = read_json("data/research.json")
assert_true(isinstance(research, list), "research.json is a list")
assert_true(len(research) > 0, "research.json has entries")
for i, r in enumerate(research):
    for f in ["id","title","carousel_title","carousel_subtitle","references"]:
        assert_true(f in r, f"research[{i}] has {f}")
    assert_true(isinstance(r["references"], list), f"research[{i}].references is list")
    for j, ref in enumerate(r["references"]):
        assert_true("citation" in ref, f"research[{i}].references[{j}] has citation")
        assert_true("url" in ref, f"research[{i}].references[{j}] has url")

print("\n── publications.json ───────────────────────────────")
pubs = read_json("data/publications.json")
assert_true(isinstance(pubs, list), "publications.json is a list")
assert_true(len(pubs) > 0, "publications.json has entries")
years = [p["year"] for p in pubs]
assert_true(years == sorted(years, reverse=True), "publications ordered newest first")
for i, section in enumerate(pubs):
    assert_true("year" in section, f"pub section {i} has year")
    assert_true("entries" in section, f"pub section {i} has entries")
    assert_true(isinstance(section["entries"], list), f"pub section {i} entries is list")
    for j, e in enumerate(section["entries"]):
        for f in ["id","authors","title","journal","details"]:
            assert_true(f in e, f"pub[{i}].entries[{j}] has {f}")

print("\n── photos.json ─────────────────────────────────────")
photos = read_json("data/photos.json")
assert_true(isinstance(photos, list), "photos.json is a list")
for i, p in enumerate(photos):
    for f in ["id","date","display_date","caption","images"]:
        assert_true(f in p, f"photos[{i}] has {f}")
    assert_true(isinstance(p["images"], list), f"photos[{i}].images is list")

print("\n── HTML: index.html ────────────────────────────────")
idx = read_html("index.html")
assert_true('<nav class="site-nav"' in idx, "index.html has nav")
assert_true('class="carousel"' in idx, "index.html has carousel")
assert_true('id="newsContainer"' in idx, "index.html has newsContainer")
assert_true('assets/js/main.js' in idx, "index.html loads main.js")
assert_true('assets/css/style.css' in idx, "index.html loads style.css")
assert_true('site-footer' in idx, "index.html has footer")
assert_true('pages/people/index.html' in idx, "index.html links to people page")
assert_true('pages/research/index.html' in idx, "index.html links to research page")
assert_true('viewport' in idx, "index.html has viewport meta")

print("\n── HTML: All pages have nav + footer ───────────────")
pages = [
    "pages/people/index.html",
    "pages/alumni/index.html",
    "pages/research/index.html",
    "pages/publications/index.html",
    "pages/photos/index.html",
    "pages/contact/index.html",
]
for page in pages:
    html = read_html(page)
    name = page.split("/")[1]
    assert_true('<nav class="site-nav"' in html, f"{name}: has nav")
    assert_true('site-footer' in html, f"{name}: has footer")
    assert_true('assets/js/main.js' in html or '../../assets/js/main.js' in html, f"{name}: loads main.js")
    assert_true('viewport' in html, f"{name}: has viewport meta")
    assert_true('../../index.html' in html, f"{name}: links back to home")

print("\n── CSS checks ──────────────────────────────────────")
css = read_html("assets/css/style.css")
assert_true('--penn-blue' in css, "CSS defines --penn-blue")
assert_true('@media' in css, "CSS has responsive media queries")
assert_true('.carousel' in css, "CSS has carousel styles")
assert_true('.site-nav' in css, "CSS has nav styles")
assert_true('.site-footer' in css, "CSS has footer styles")
assert_true('.people-grid' in css, "CSS has people-grid")

print("\n── JS checks ───────────────────────────────────────")
js = read_html("assets/js/main.js")
assert_true('fetchData' in js, "JS has fetchData function")
assert_true('initNav' in js, "JS has initNav function")
assert_true('initCarousel' in js, "JS has initCarousel function")
assert_true('renderFooter' in js, "JS has renderFooter function")
assert_true('navToggle' in js, "JS handles mobile nav toggle")

print("\n── GitHub Pages config ─────────────────────────────")
assert_file(".nojekyll", ".nojekyll exists (disables Jekyll processing)")

print(f"\n{'='*52}")
total = passed + len(errors)
print(f"Results: {passed}/{total} passed, {len(errors)} failed")
if errors:
    print("\nFailed tests:")
    for e in errors: print(f"  • {e}")
    sys.exit(1)
else:
    print("All tests passed! ✅")
    sys.exit(0)
