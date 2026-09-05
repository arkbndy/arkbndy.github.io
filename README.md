# arkbndy.github.io

Personal academic website of **Dr. Arka Bandyopadhyay** — theoretical condensed-matter physicist, Universität Würzburg.

Live at <https://arkbndy.github.io>.

Plain HTML, CSS and one JavaScript file. Nothing is compiled at serve time and there
is no framework or npm dependency: GitHub Pages publishes the files exactly as they
sit in the repository. The five HTML pages are *generated* from one Python script so
that the header, footer, metadata and structure can never drift apart — see §3.

---

## 1. Everyday updating

```bash
git add -A && git commit -m "what changed" && git push
```

Changes appear on the live site within a minute or two. On Windows, GitHub Desktop
does the same thing: **Commit to main**, then **Push origin**.

---

## 2. Where to change what

| I want to… | Edit this | Then |
|---|---|---|
| Change any wording on any page | `scripts/build_pages.py` | rebuild (§3) |
| Add or rewrite a research pillar | `scripts/build_pages.py` — `PILLARS` (cards) and `DETAIL` (full sections) | rebuild |
| Add or edit a collaborator | `scripts/build_pages.py` — `GROUPS` | rebuild |
| Add a publication by hand | `data/publications.json` | nothing — it is read at runtime |
| Post a news item | `data/news.json` | nothing |
| Change colours, spacing, type | `assets/css/style.css` — the `:root` block at the top | nothing |
| Change list rendering or filtering | `assets/js/site.js` | nothing |

**Do not edit the `.html` files directly.** They are build output and the next
rebuild overwrites them.

---

## 3. Rebuilding the pages

```bash
python3 scripts/build_pages.py
```

Standard library only. It prints the files it wrote and the collaborator count.
It regenerates `index.html`, `research.html`, `publications.html`, `news.html`
and `cv.html` from a single page template, so a change to the navigation, the
footer, the OpenGraph tags or the JSON-LD block happens once and applies to all five.

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
  "tags": ["geometry"],
  "selected": true,
  "summary": "One sentence on why this paper matters. Only shown for selected papers."
}
```

Everything except `title`, `authors`, `journal`, `year` and `id` is optional.
The name `Arka Bandyopadhyay` is bolded automatically wherever it appears.

**Tags** drive the filter chips on the publications page and the paper counts on
the research page. Every paper must carry exactly one of the five pillar tags:

| Tag | Pillar |
|---|---|
| `geometry` | Quantum geometry & unconventional transport |
| `topology` | Topology, flat bands & kagome quantum matter |
| `magnetism` | Magnetism, correlations & spin–orbit physics |
| `interfaces` | Interfaces & materials-realistic quantum matter |
| `materials` | Low-dimensional & chemically designed materials |

Two optional secondary tags may be added alongside a pillar tag: `review` and
`applied`. The human-readable pillar names live in the `pillars` map at the top of
`data/publications.json`; the chips are declared in `build_pages.py`.

**`role`** is what produces the "as first or joint-first author" and "as
corresponding author" counts on the home page. Anything matching *first* or
*corresponding* is counted — the numbers are never written by hand anywhere.

**`selected: true`** puts a paper in the "Six papers, five threads" block on the
home page, together with its `summary`. Six is a good number; ten is too many.

### Adding a news item

At the top of `data/news.json`:

```json
{ "date": "2026-11", "text": "Something happened. <strong>Bold</strong> and <em>italic</em> work.", "link": "https://doi.org/…" }
```

`link` is optional. Keep the newest item first. The home page shows the four most
recent; `news.html` shows all of them. A news feed whose last entry is a year old
reads worse than no news feed at all — one entry every couple of months is enough.

---

## 4. The ORCID automation

`.github/workflows/sync-orcid.yml` runs `scripts/sync_orcid.py` at 06:15 UTC on
the first of every month, and whenever you trigger it by hand from the repository's
**Actions** tab.

The script reads the ORCID record, finds DOIs that are not yet on the site, looks up
the details on Crossref, and commits them to `data/publications.json`.

Two things worth knowing:

- **It never overwrites what is already there.** The `role`, `award`, `tags`,
  `selected` and `summary` fields are safe.
- **New entries arrive marked `"needs_review": true` with empty tags.** They appear
  in the "All" list immediately but are not matched by any filter chip and are not
  counted towards a pillar until a pillar tag is added. Delete the `needs_review`
  flag once the entry has been annotated.

So the routine is: keep ORCID current, and about once a quarter open
`data/publications.json`, find the `needs_review` entries, and add a pillar tag and
an authorship role.

To run it by hand:

```bash
python3 scripts/sync_orcid.py
```

Standard library only — no `pip install` needed.

**If the monthly run fails to push:** Settings → Actions → General → Workflow
permissions → *Read and write permissions*.

---

## 5. Using a custom domain

If a domain is bought later (say `arkabandyopadhyay.com`):

1. Create a file called `CNAME` in the repository root containing just the domain,
   no `https://` and no trailing slash.
2. At the registrar, add four `A` records for the bare domain pointing to
   `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`,
   and a `CNAME` record for `www` pointing to `arkbndy.github.io`.
3. In Settings → Pages, enter the domain and tick **Enforce HTTPS**.
4. Replace `arkbndy.github.io` in `scripts/build_pages.py` (the `SITE` dictionary),
   `sitemap.xml` and `robots.txt`, then rebuild. Those are the canonical URLs and
   the structured data that search engines read.

---

## 6. What is where

```
scripts/build_pages.py   THE SOURCE OF ALL PAGE COPY — generates the five .html files
scripts/sync_orcid.py    ORCID → Crossref → publications.json

data/publications.json   All publication data, tags and pillar labels (ORCID job writes here)
data/news.json           All news entries

assets/css/style.css     Everything visual, including the light/dark themes
assets/js/site.js        Theme toggle, mobile menu, list rendering, filtering, all counts
assets/img/portrait.jpg  Photograph
assets/img/favicon.svg   Favicon

index.html               GENERATED — home
research.html            GENERATED — five pillars in depth, plus collaborators
publications.html        GENERATED — full record, search and filters, preprints separately
news.html                GENERATED — full news feed
cv.html                  GENERATED — web CV

.github/workflows/       The monthly ORCID schedule
sitemap.xml, robots.txt  Search-engine files
.nojekyll                Tells GitHub Pages to serve the files as-is
```

---

## 7. Notes on the design choices

- **All displayed numbers are computed from `data/publications.json`** — the paper
  count, the first-author count, the corresponding-author count, the number under
  review, and the per-pillar counts. Nothing is typed by hand, so nothing can go stale.
- **No citation counts, no h-index.** In physics, self-reported metrics read poorly.
  The Google Scholar link carries that information for anyone who wants it.
- **Manuscripts under review are listed separately** from refereed work, clearly
  labelled, and never counted in the peer-reviewed total.
- **Numbering descends** and is computed once over the whole record, so paper 41
  stays paper 41 when new papers arrive on top and when a filter is applied.
- **Nothing below the doctorate appears anywhere** on the site, by request, and
  there is no downloadable CV file.
- **The site states plainly that the experiments are collaborators' work.**
- **Works with JavaScript disabled** for everything except the publication and news
  lists, which are rendered from JSON.
- Light and dark themes follow the visitor's system setting; the toggle in the
  header overrides it and remembers the choice in `localStorage`.
