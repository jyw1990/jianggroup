# Jiang Group Website — Update Manual

This document explains how to instruct Claude to update the website.
The site is a static HTML/CSS/JS site hosted on GitHub Pages at:
**https://jyw1990.github.io/jianggroup/**

All content lives in `data/*.json` files. You never need to edit HTML directly.

---

## How Updates Work

1. Tell Claude what you want to change (using the formats below).
2. Claude edits the relevant JSON file(s), runs the test suite, and commits to GitHub.
3. GitHub Pages deploys automatically within ~1 minute.

---

## 1. News Updates

**Add a news item:**
> "Add a news item for [MM/YYYY]: [text of the news]. [Optional: attach an image]"

**Example:**
> "Add a news item for 03/2025: Alice Smith joined the group as a Ph.D. student in Bioengineering."

**With image:**
> "Add a news item for 06/2025: We won the Best Paper Award. [attach image]"

**Notes:**
- News older than 3 years is automatically archived (hidden from the home page).
- You do not need to manually remove old news.

---

## 2. People Updates

### 2.1 Add a new member

For **Postdoctoral Scholars** or **Ph.D. Students**, provide:
> "Add a new postdoc/PhD student named [Full Name], email [email], bio: [paragraph]. [attach photo]"

For **Master's** or **Undergraduate Students**, provide:
> "Add a new master's/undergrad student named [Full Name], department [dept], email [email]. [attach photo]"

For **High School Students**, provide:
> "Add a new high school student named [Full Name], school [School Name]. [attach photo]"

### 2.2 Update an existing member
> "Update [Full Name]'s [field] to [new value]."

**Example:**
> "Update Yewei Huang's email to newemail@seas.upenn.edu."
> "Update Yuhang Ye's bio to: [new bio text]."

### 2.3 Remove a member
> "Remove [Full Name] from the People page."

### 2.4 Move a member to Alumni
> "Move [Full Name] to Alumni. They were here from [start year] to [exit year]."

**Example:**
> "Move Lingfeng Tang to Alumni. He was here from 2023 to 2025."

Alumni are automatically sorted by exit year (newest first).

---

## 3. Research Updates

> "Add a new research area titled [Title]. Description: [paragraph]. The carousel subtitle is: [short phrase]. [attach research image] [attach carousel image if different]"

> "Update the research area '[existing title]': [what to change]."

**Read More links** on the carousel automatically point to the research page anchor.

---

## 4. Publications Updates

**From Google Scholar (most common):**
> "Update the publications page. New publication: [full citation as it appears on Google Scholar]."

**Manual entry:**
> "Add a publication to [year]: Authors: [authors]. Title: [title]. Journal: [journal name]. Details: [vol, pages, year]. URL: [link]."

**Example:**
> "Add a 2025 publication: Authors: Huang Y. & Jiang Y.* Title: Stretchable neural probes. Journal: Nature Nanotechnology. Details: 20, 100–110 (2025). URL: https://nature.com/..."

---

## 5. Photos Updates

> "Add a photo for [Month, Year]: '[Caption text]'. [attach photo(s)]"

**Example:**
> "Add a photo for May, 2025: 'Lab retreat in the Poconos!' [attach image]"

Multiple images for one event are supported — just attach them all.

---

## Adding Images

When you provide an image with an update, Claude will:
1. Save it under the appropriate `assets/images/` subfolder.
2. Update the relevant JSON to reference it.

**Image subfolders:**
- People photos: `assets/images/people/`
- Alumni photos: `assets/images/alumni/`
- Research images: `assets/images/research/`
- Photo gallery: `assets/images/photos/`

---

## Running Tests

After any update, Claude runs:
```
python3 tests/test_site.py
```
All 500+ tests must pass before committing.

---

## File Reference

| File | Purpose |
|------|---------|
| `data/news.json` | Home page news items |
| `data/people.json` | Current lab members |
| `data/alumni.json` | Former lab members |
| `data/research.json` | Research areas + carousel |
| `data/publications.json` | Publications list |
| `data/photos.json` | Photo gallery |
| `assets/css/style.css` | All styles |
| `assets/js/main.js` | Shared JS (nav, carousel, data loading) |

---

## Commit Message Convention

Claude uses this format for commits:
```
v[N]: [summary of changes]
```
**Examples:**
- `v2: Add news item 03/2025 – Alice Smith joined as PhD student`
- `v3: Move Lingfeng Tang to alumni (2023–2025)`
- `v4: Add 2025 Nature Nanotechnology publication`
