# arkbndy.github.io

Personal academic website of **Dr. Arka Bandyopadhyay** — theoretical condensed-matter physicist, Universität Würzburg.

Plain HTML, CSS and a single JavaScript file. No build step, no framework, no npm.
GitHub Pages serves it exactly as it sits in the repository.

---

## 1. Putting it online (about ten minutes, once)

1. Go to <https://github.com/new> and create a repository named **exactly**
   `arkbndy.github.io` — the name is what makes GitHub Pages serve it at that address.
   Set it to **Public**. Do **not** tick "Add a README".
2. On the empty repository page, click **uploading an existing file**.
3. Drag in *everything* from this folder. Two things are easy to miss:
   - the hidden file `.nojekyll` (turn on hidden files in your file manager: `Cmd+Shift+.` on macOS, `Ctrl+H` on Linux)
   - the `.github` folder, which carries the ORCID automation
   If drag-and-drop skips them, see the `git` route below — it is more reliable.
4. Click **Commit changes**.
5. Open **Settings → Pages**. Under *Build and deployment* set Source to
   **Deploy from a branch**, branch **main**, folder **/ (root)**. Save.
6. Wait about a minute, then open **https://arkbndy.github.io** — it is live.

### The `git` route (recommended, and required to keep updating easily)

```bash
cd path/to/this/folder
git init
git add -A
git commit -m "Personal academic website"
git branch -M main
git remote add origin https://github.com/arkbndy/arkbndy.github.io.git
git push -u origin main
```

Then do step 5 above. Every later change is just:

```bash
git add -A && git commit -m "what changed" && git push
```

Changes appear on the live site within a minute or two.

---

## 2. The one thing to do first

`assets/img/portrait.jpg` is a placeholder. Replace it with a photograph of
yourself — the same one from your Würzburg page works well. Keep the filename
and keep it roughly portrait-shaped (around 560 × 630 pixels is plenty).
Nothing else needs touching for the site to look finished.

---

## 3. Editing the site

| I want to… | Edit this |
|---|---|
| Change my bio, title, or the lede paragraph | `index.html` — the `<!-- HERO -->` block |
| Add or rewrite a research theme | `research.html` — the numbered `theme-block` sections |
| Add a publication by hand | `data/publications.json` |
| Post a news item | `data/news.json` |
| Update the CV page | `cv.html` |
| Replace the CV PDF | `files/Arka_Bandyopadhyay_CV.pdf` (keep the filename) |
| Change colours or spacing | `assets/css/style.css` — the `:root` block at the top |

### Adding a publication by hand

Add an object at the **top** of the `peer_reviewed` array in `data/publications.json`:

```json
{
  "id": "shortuniquename2026",
  "title": "Title of the paper",
  "authors": "First Author, Arka Bandyopadhyay, Last Author",
  "journal": "Physical Review B",
  "volume": "114",
  "pages": "105406",
  "year": 2026,
  "doi": "10.1103/xxxx",
  "arxiv": "2511.15337",
  "role": "Corresponding author",
  "award": "Editors' Suggestion",
  "tags": ["quantum-geometry"],
  "selected": true,
  "summary": "One sentence on why this paper matters. Only shown for selected papers."
}
```

Everything except `title`, `authors`, `journal`, `year` and `id` is optional.
Write your name exactly as `Arka Bandyopadhyay` and it is bolded automatically.

**Tags** drive the filter chips on the publications page. The available ones are
`quantum-geometry`, `topology`, `flat-bands`, `non-hermitian`, `oxides`,
`2d-materials`, `review`. Add a new tag by also adding a chip button in
`publications.html`.

**`selected: true`** puts a paper in the "Six papers that say what I do" block on
the home page. Six is a good number; ten is too many.

### Adding a news item

At the top of `data/news.json`:

```json
{ "date": "2026-11", "text": "Something happened. <strong>Bold</strong> and <em>italic</em> work.", "link": "https://doi.org/…" }
```

`link` is optional. Keep the newest item first. A news feed whose last entry is a
year old reads worse than no news feed at all — one entry every couple of months
is enough.

---

## 4. The ORCID automation

`.github/workflows/sync-orcid.yml` runs `scripts/sync_orcid.py` at 06:15 UTC on
the first of every month, and whenever you trigger it by hand from the repository's
**Actions** tab.

The script reads your ORCID record, finds DOIs that are not yet on the site,
looks up the details on Crossref, and commits them to `data/publications.json`.

Two things worth knowing:

- **It never overwrites what is already there.** Your `role`, `award`, `tags`,
  `selected` and `summary` fields are safe.
- **New entries arrive marked `"needs_review": true` with empty tags.** They show
  up on the site immediately but will not be filtered by any chip until you add
  tags. Delete the `needs_review` flag once you have annotated one.

So the routine is: keep ORCID current, and about once a quarter open
`data/publications.json`, find the `needs_review` entries and add tags and an
authorship role.

To run it yourself:

```bash
python3 scripts/sync_orcid.py
```

Standard library only — no `pip install` needed.

**If the monthly run fails to push:** go to Settings → Actions → General →
Workflow permissions and select *Read and write permissions*.

---

## 5. Using your own domain

If you buy a domain later (say `arkabandyopadhyay.com`):

1. Create a file called `CNAME` in the root of the repository containing just the
   domain, no `https://` and no trailing slash.
2. At your registrar, add four `A` records for the bare domain pointing to
   `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`,
   and a `CNAME` record for `www` pointing to `arkbndy.github.io`.
3. In Settings → Pages, enter the domain and tick **Enforce HTTPS**.
4. Search for `arkbndy.github.io` in the `.html` files and `sitemap.xml` and
   replace it with the new domain — those are the canonical URLs and the
   structured data that Google Scholar and search engines read.

---

## 6. What is where

```
index.html            Home: hero, record, five research themes, selected papers, news, contact
research.html         The five research programmes in depth, each with a figure
publications.html     Full record with search and topic filters; preprints listed separately
news.html             Full news feed
cv.html               Web CV
data/publications.json  All publication data (the ORCID job writes here)
data/news.json          All news entries
assets/css/style.css    Everything visual, including light/dark themes
assets/js/site.js       Theme toggle, mobile menu, list rendering and filtering
assets/img/portrait.jpg REPLACE THIS with your photo
files/…CV.pdf           The downloadable CV
scripts/sync_orcid.py   ORCID → Crossref → publications.json
.github/workflows/      The monthly schedule
.nojekyll               Tells GitHub Pages to serve the files as-is
```

---

## 7. Notes on the design choices

- **No citation counts, no h-index.** None of the physicist sites surveyed while
  building this displayed them, and in physics self-reported metrics read poorly.
  The Google Scholar link carries that information for anyone who wants it.
- **Preprints are listed separately** from refereed work, clearly labelled.
- **Numbering descends**, so paper 41 stays paper 41 when new ones arrive on top.
- **Nothing below the doctorate appears anywhere** on the site, by request.
- **Works with JavaScript disabled** for everything except the publication and
  news lists, which are rendered from JSON.
- Light and dark themes follow the visitor's system setting; the toggle in the
  header overrides it and remembers the choice.
