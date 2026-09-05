#!/usr/bin/env python3
"""
Keep data/publications.json current from ORCID.

What it does
------------
1. Reads every work on the ORCID record.
2. Collects the DOIs and compares them with what is already in
   data/publications.json (both the peer_reviewed and preprints lists).
3. For each genuinely new DOI it asks Crossref for authors, title, journal,
   volume, pages and year, and appends a new entry.
4. Rewrites the file with entries sorted newest-first.

What it deliberately does NOT do
--------------------------------
It never touches an entry that is already in the file. Curated fields —
role, award, tags, selected, summary, note — are yours and are preserved
exactly. New entries arrive with `"needs_review": true` and empty tags so
you can see at a glance what to annotate.

Only Crossref type "journal-article", "book-chapter" and "proceedings-article"
are added, so arXiv postings of papers you have already published do not
create duplicates.

Standard library only. Run:  python3 scripts/sync_orcid.py
"""

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ORCID = os.environ.get("ORCID_ID", "0000-0003-3386-4289")
CONTACT = os.environ.get("CROSSREF_MAILTO", "arka.bandyopadhyay@uni-wuerzburg.de")
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBS = os.path.join(HERE, "data", "publications.json")

UA = "arkbndy.github.io publication sync (mailto:%s)" % CONTACT
ADD_TYPES = {"journal-article", "book-chapter", "proceedings-article"}


def get_json(url, accept="application/json", tries=3):
    for attempt in range(tries):
        req = urllib.request.Request(url, headers={"Accept": accept, "User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < tries - 1:
                time.sleep(4 * (attempt + 1))
                continue
            raise
        except urllib.error.URLError:
            if attempt < tries - 1:
                time.sleep(4 * (attempt + 1))
                continue
            raise
    return None


def norm(doi):
    return (doi or "").strip().lower().replace("https://doi.org/", "")


def orcid_dois():
    data = get_json("https://pub.orcid.org/v3.0/%s/works" % ORCID)
    found = set()
    for group in data.get("group", []):
        for eid in (group.get("external-ids") or {}).get("external-id", []):
            if eid.get("external-id-type") == "doi":
                found.add(norm(eid.get("external-id-value")))
    found.discard("")
    return found


def crossref(doi):
    try:
        msg = get_json("https://api.crossref.org/works/%s" % urllib.parse.quote(doi))
    except Exception as exc:                      # noqa: BLE001
        print("  ! Crossref lookup failed for %s (%s)" % (doi, exc))
        return None
    return (msg or {}).get("message")


def authors_of(m):
    names = []
    for a in m.get("author", []) or []:
        given = a.get("given", "")
        family = a.get("family", "")
        full = (given + " " + family).strip()
        names.append(full or a.get("name", ""))
    if len(names) > 11:
        names = names[:10] + ["et al."]
    return ", ".join(n for n in names if n)


def year_of(m):
    for key in ("published-print", "published-online", "issued", "created"):
        parts = (m.get(key) or {}).get("date-parts") or []
        if parts and parts[0] and parts[0][0]:
            return int(parts[0][0])
    return 0


def entry_from(m, doi):
    title = (m.get("title") or [""])[0]
    journal = (m.get("container-title") or [""])[0]
    slug = "".join(ch for ch in title.lower() if ch.isalnum() or ch == " ").split()
    return {
        "id": (slug[0] if slug else "work") + str(year_of(m)) + doi[-4:],
        "title": title,
        "authors": authors_of(m),
        "journal": journal,
        "volume": m.get("volume", "") or "",
        "pages": (m.get("page") or "").split("-")[0],
        "year": year_of(m),
        "doi": doi,
        "tags": [],
        "needs_review": True,
    }


def main():
    with open(PUBS, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    known = {norm(p.get("doi")) for p in data["peer_reviewed"] + data["preprints"]}
    known.discard("")

    try:
        remote = orcid_dois()
    except Exception as exc:                      # noqa: BLE001
        print("ORCID fetch failed: %s" % exc)
        return 1

    new = sorted(remote - known)
    print("ORCID lists %d DOIs; %d already on the site; %d new." %
          (len(remote), len(remote & known), len(new)))

    added = 0
    for doi in new:
        m = crossref(doi)
        time.sleep(1.2)                            # be polite to Crossref
        if not m:
            continue
        ctype = m.get("type", "")
        if ctype not in ADD_TYPES:
            print("  - skipping %s (type: %s)" % (doi, ctype))
            continue
        item = entry_from(m, doi)
        if not item["title"]:
            continue
        data["peer_reviewed"].append(item)
        added += 1
        print("  + %s (%s)" % (item["title"][:70], item["year"]))

    if not added:
        print("Nothing to add.")
        return 0

    data["peer_reviewed"].sort(key=lambda p: (-int(p.get("year") or 0), p.get("title", "")))
    data["generated"] = time.strftime("%Y-%m-%d")

    with open(PUBS, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    print("Added %d entr%s. Review the ones marked needs_review." %
          (added, "y" if added == 1 else "ies"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
