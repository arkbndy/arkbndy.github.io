#!/usr/bin/env python3
"""
Assemble the five site pages from one template.

Run from the repository root:  python3 scripts/build_pages.py
Edit the copy here, not in the generated .html files.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

SITE = "https://arkbndy.github.io/"
NAME = "Arka Bandyopadhyay"

NAV = [("index.html", "Home"), ("research.html", "Research"),
       ("publications.html", "Publications"), ("news.html", "News"),
       ("cv.html", "CV"), ("index.html#contact", "Contact")]

JSONLD = """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Arka Bandyopadhyay",
  "givenName": "Arka",
  "familyName": "Bandyopadhyay",
  "jobTitle": "Postdoctoral Researcher in Theoretical Condensed Matter Physics",
  "email": "mailto:arka.bandyopadhyay@uni-wuerzburg.de",
  "url": "https://arkbndy.github.io/",
  "image": "https://arkbndy.github.io/assets/img/portrait.jpg",
  "affiliation": {
    "@type": "Organization",
    "name": "Julius-Maximilians-Universit\\u00e4t W\\u00fcrzburg",
    "department": "Institute for Theoretical Physics and Astrophysics"
  },
  "memberOf": { "@type": "Organization", "name": "Cluster of Excellence ct.qmat" },
  "knowsAbout": ["Quantum materials","Theoretical condensed matter physics","Quantum geometry",
    "Berry curvature","Nonlinear Hall effect","Topological materials","Flat bands","Kagome lattices",
    "Altermagnetism","Electronic correlations","Spin-orbit coupling","Oxide interfaces",
    "Density functional theory","Wannier functions","Quantum transport","Two-dimensional materials"],
  "identifier": "https://orcid.org/0000-0003-3386-4289",
  "sameAs": [
    "https://orcid.org/0000-0003-3386-4289",
    "https://scholar.google.com/citations?user=EcM27vQAAAAJ",
    "https://github.com/arkbndy",
    "https://www.physik.uni-wuerzburg.de/en/cqm/team/postdocs/dr-arka-bandyopadhyay/"
  ]
}
</script>"""

FOOTER = """
<footer class="site-footer">
  <div class="wrap footer-inner">
    <p>&copy; <span id="year">2026</span> Arka Bandyopadhyay &middot; W&uuml;rzburg</p>
    <div class="idlinks">
      <a href="https://orcid.org/0000-0003-3386-4289" target="_blank" rel="noopener">ORCID 0000-0003-3386-4289</a>
      <a href="https://scholar.google.com/citations?user=EcM27vQAAAAJ" target="_blank" rel="noopener">Google Scholar</a>
      <a href="https://github.com/arkbndy" target="_blank" rel="noopener">GitHub</a>
    </div>
  </div>
</footer>"""


def header(current):
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ''
        items.append('        <li><a href="%s"%s>%s</a></li>' % (href, cur, label))
    return """
<header class="site-header">
  <div class="wrap nav">
    <a class="brand" href="index.html"><b>Arka Bandyopadhyay</b><span>Quantum Materials Theory</span></a>
    <nav aria-label="Primary">
      <ul class="nav-links" id="nav-links">
%s
      </ul>
    </nav>
    <button class="icon-btn theme-toggle" type="button" aria-label="Switch colour theme">
      <svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
      <svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
    </button>
    <button class="icon-btn nav-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="nav-links">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
    </button>
  </div>
</header>"""  % "\n".join(items)


def page(filename, title, description, body, current, extra_head=""):
    canonical = SITE + ("" if filename == "index.html" else filename)
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<meta name="author" content="Arka Bandyopadhyay">
<link rel="canonical" href="%(canonical)s">

<meta property="og:type" content="profile">
<meta property="og:site_name" content="Arka Bandyopadhyay">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(canonical)s">
<meta property="og:image" content="%(site)sassets/img/portrait.jpg">
<meta name="twitter:card" content="summary">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
%(extra)s
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
%(header)s
<main id="main">
%(body)s
</main>
%(footer)s
<script src="assets/js/site.js"></script>
</body>
</html>
""" % dict(title=title, desc=description, canonical=canonical, site=SITE,
           extra=extra_head, header=header(current), body=body, footer=FOOTER)
    (ROOT / filename).write_text(html, encoding="utf-8")
    return filename


# =========================================================================
#  Figures
# =========================================================================

MAP_SVG = """<svg viewBox="0 0 960 250" role="img" aria-labelledby="maptitle mapdesc">
  <title id="maptitle">How the research programme fits together</title>
  <desc id="mapdesc">Five linked stages: materials and structure; symmetry and electronic structure;
  quantum geometry, topology, magnetism and correlations; emergent states and unconventional transport;
  measurable signatures. A feedback arrow runs from measurable signatures back to the models.</desc>
  <defs>
    <marker id="mArrow" markerWidth="9" markerHeight="9" refX="7" refY="3.2" orient="auto">
      <path d="M0,0 L7,3.2 L0,6.4 z" style="fill:var(--accent)"/>
    </marker>
  </defs>
  <text x="480" y="26" text-anchor="middle" style="fill:var(--accent);font:650 12px var(--sans);letter-spacing:.22em">QUANTUM MATERIALS</text>
  <line x1="60" y1="38" x2="900" y2="38" style="stroke:var(--accent-line);stroke-width:1"/>

  <g style="fill:var(--surface);stroke:var(--rule);stroke-width:1">
    <rect x="20"  y="62" width="168" height="104" rx="8"/>
    <rect x="208" y="62" width="168" height="104" rx="8"/>
    <rect x="396" y="62" width="168" height="104" rx="8"/>
    <rect x="584" y="62" width="168" height="104" rx="8"/>
    <rect x="772" y="62" width="168" height="104" rx="8"/>
  </g>

  <g style="fill:var(--ink);font:600 13px var(--sans)" text-anchor="middle">
    <text x="104" y="94">Materials</text><text x="104" y="112">&amp; structure</text>
    <text x="292" y="94">Symmetry &amp;</text><text x="292" y="112">electronic structure</text>
    <text x="480" y="94">Quantum geometry,</text><text x="480" y="112">topology, magnetism</text>
    <text x="668" y="94">Anomalous &amp; nonlinear</text><text x="668" y="112">electronic response</text>
    <text x="856" y="94">Measurable</text><text x="856" y="112">signatures</text>
  </g>
  <g style="fill:var(--muted);font:400 10.5px var(--sans)" text-anchor="middle">
    <text x="104" y="136">crystal chemistry,</text><text x="104" y="150">interfaces, molecules</text>
    <text x="292" y="136">first-principles, Wannier,</text><text x="292" y="150">tight-binding models</text>
    <text x="480" y="136">Berry curvature, quantum</text><text x="480" y="150">metric, flat bands, order</text>
    <text x="668" y="136">nonlinear Hall, anomalous</text><text x="668" y="150">Hall and Nernst effects</text>
    <text x="856" y="136">transport, ARPES,</text><text x="856" y="150">spectroscopy</text>
  </g>

  <g style="stroke:var(--accent);stroke-width:1.6;fill:none" marker-end="url(#mArrow)">
    <path d="M190 114 H204"/><path d="M378 114 H392"/><path d="M566 114 H580"/><path d="M754 114 H768"/>
  </g>

  <path d="M856 168 V212 H292 V178" style="stroke:var(--accent-line);stroke-width:1.4;fill:none;stroke-dasharray:5 4" marker-end="url(#mArrow)"/>
  <text x="574" y="234" text-anchor="middle" style="fill:var(--muted);font:italic 400 11.5px var(--serif)">what experiment sees feeds back into which mechanism the model must contain</text>
</svg>"""

FIG_GEOMETRY = """<svg viewBox="0 0 360 240" role="img" aria-label="Berry curvature distributed asymmetrically over a Fermi surface, converting a drive at frequency omega into a transverse current at twice omega">
  <defs>
    <radialGradient id="gPos"><stop offset="0" stop-color="#b4553f" stop-opacity=".85"/><stop offset="1" stop-color="#b4553f" stop-opacity="0"/></radialGradient>
    <radialGradient id="gNeg"><stop offset="0" stop-color="#1c6b66" stop-opacity=".85"/><stop offset="1" stop-color="#1c6b66" stop-opacity="0"/></radialGradient>
    <marker id="gArr" markerWidth="9" markerHeight="9" refX="7" refY="3.2" orient="auto"><path d="M0,0 L7,3.2 L0,6.4 z" style="fill:var(--accent)"/></marker>
  </defs>
  <rect x="72" y="40" width="216" height="140" rx="10" style="fill:none;stroke:var(--rule);stroke-width:1.2"/>
  <text x="82" y="58" style="fill:var(--muted);font:500 10px var(--sans)">Brillouin zone</text>
  <ellipse cx="140" cy="112" rx="50" ry="42" fill="url(#gPos)"/>
  <ellipse cx="220" cy="112" rx="50" ry="42" fill="url(#gNeg)"/>
  <path d="M106 112 a34 34 0 1 0 68 0 a34 34 0 1 0 -68 0" style="fill:none;stroke:var(--ink-2);stroke-width:1;opacity:.45"/>
  <path d="M186 112 a34 34 0 1 0 68 0 a34 34 0 1 0 -68 0" style="fill:none;stroke:var(--ink-2);stroke-width:1;opacity:.45"/>
  <text x="140" y="117" text-anchor="middle" style="fill:var(--ink);font:600 14px var(--sans)">+&#937;</text>
  <text x="220" y="117" text-anchor="middle" style="fill:var(--ink);font:600 14px var(--sans)">&#8722;&#937;</text>
  <path d="M16 112 H64" style="stroke:var(--accent);stroke-width:1.8;fill:none" marker-end="url(#gArr)"/>
  <text x="16" y="100" style="fill:var(--ink-2);font:600 11px var(--sans)">E(&#969;)</text>
  <path d="M180 224 V192" style="stroke:var(--accent);stroke-width:1.8;fill:none" marker-end="url(#gArr)"/>
  <text x="190" y="219" style="fill:var(--ink-2);font:600 11px var(--sans)">J&#8869;(0, 2&#969;)</text>
  <text x="298" y="112" style="fill:var(--muted);font:italic 400 11px var(--serif)">D &#8733; &#8747; f &#8706;&#937;/&#8706;k</text>
</svg>"""

FIG_KAGOME = """<svg viewBox="0 0 360 240" role="img" aria-label="A kagome lattice and its band structure, showing a flat band above two dispersive bands that touch at a Dirac point">
  <g style="stroke:var(--accent);stroke-width:1.4;fill:none;opacity:.92">
    <path d="M16 172 L46 120 L76 172 Z"/><path d="M76 172 L106 120 L136 172 Z"/>
    <path d="M46 120 L76 68 L106 120 Z"/><path d="M106 120 L136 68 L166 120 Z"/>
    <path d="M76 68 L106 16 L136 68 Z"/>
    <path d="M46 120 H166"/><path d="M16 172 H136"/><path d="M76 68 H136"/>
  </g>
  <g style="fill:var(--accent)">
    <circle cx="46" cy="120" r="3.6"/><circle cx="106" cy="120" r="3.6"/><circle cx="166" cy="120" r="3.6"/>
    <circle cx="16" cy="172" r="3.6"/><circle cx="76" cy="172" r="3.6"/><circle cx="136" cy="172" r="3.6"/>
    <circle cx="76" cy="68" r="3.6"/><circle cx="136" cy="68" r="3.6"/><circle cx="106" cy="16" r="3.6"/>
  </g>
  <path d="M214 204 V30 M214 204 H344" style="stroke:var(--rule);stroke-width:1.2;fill:none"/>
  <path d="M221 60 H340" style="stroke:var(--accent);stroke-width:2.8;fill:none"/>
  <path d="M221 176 Q280 60 340 176" style="stroke:var(--ink-2);stroke-width:1.5;fill:none;opacity:.7"/>
  <path d="M221 60 Q280 176 340 60" style="stroke:var(--ink-2);stroke-width:1.5;fill:none;opacity:.7"/>
  <circle cx="280" cy="118" r="3.2" style="fill:var(--ink-2)"/>
  <text x="343" y="54" text-anchor="end" style="fill:var(--accent);font:600 10.5px var(--sans)">flat band</text>
  <text x="290" y="113" style="fill:var(--muted);font:500 10px var(--sans)">band touching</text>
  <text x="207" y="38" text-anchor="end" style="fill:var(--muted);font:500 11px var(--sans)">E</text>
  <text x="344" y="222" text-anchor="end" style="fill:var(--muted);font:500 11px var(--sans)">k</text>
</svg>"""

FIG_DECIMATION = """<svg viewBox="0 0 360 240" role="img" aria-label="Real-space decimation reduces a lattice to an energy-dependent effective lattice; in the non-Hermitian case the complex eigenvalues coalesce at exceptional points">
  <defs><marker id="dArr" markerWidth="9" markerHeight="9" refX="7" refY="3.2" orient="auto"><path d="M0,0 L7,3.2 L0,6.4 z" style="fill:var(--accent)"/></marker></defs>
  <text x="18" y="20" style="fill:var(--muted);font:500 10px var(--sans)">lattice</text>
  <path d="M18 44 H178" style="stroke:var(--rule);stroke-width:1.4;fill:none"/>
  <g style="fill:var(--accent)"><circle cx="18" cy="44" r="5"/><circle cx="98" cy="44" r="5"/><circle cx="178" cy="44" r="5"/></g>
  <g style="fill:var(--muted);opacity:.5"><circle cx="58" cy="44" r="3.8"/><circle cx="138" cy="44" r="3.8"/></g>
  <path d="M200 44 H242" style="stroke:var(--accent);stroke-width:1.7;fill:none" marker-end="url(#dArr)"/>
  <text x="221" y="34" text-anchor="middle" style="fill:var(--accent);font:600 9.5px var(--sans)">decimate</text>
  <text x="264" y="20" style="fill:var(--muted);font:500 10px var(--sans)">effective</text>
  <path d="M264 44 H342" style="stroke:var(--accent);stroke-width:2;fill:none"/>
  <g style="fill:var(--accent)"><circle cx="264" cy="44" r="5"/><circle cx="303" cy="44" r="5"/><circle cx="342" cy="44" r="5"/></g>
  <text x="303" y="66" text-anchor="middle" style="fill:var(--muted);font:italic 400 10px var(--serif)">t(E), &#949;(E)</text>
  <path d="M18 86 H342" style="stroke:var(--rule);stroke-width:1;stroke-dasharray:4 4;opacity:.7"/>
  <path d="M34 166 H336 M184 106 V230" style="stroke:var(--rule);stroke-width:1.2"/>
  <path d="M100 166 C100 118 184 118 184 166 C184 214 268 214 268 166" style="stroke:var(--accent);stroke-width:2;fill:none"/>
  <path d="M100 166 C100 214 184 214 184 166 C184 118 268 118 268 166" style="stroke:var(--ink-2);stroke-width:2;fill:none;opacity:.7"/>
  <circle cx="100" cy="166" r="5" style="fill:var(--accent)"/><circle cx="268" cy="166" r="5" style="fill:var(--accent)"/>
  <text x="100" y="190" text-anchor="middle" style="fill:var(--ink-2);font:600 10.5px var(--sans)">EP</text>
  <text x="268" y="152" text-anchor="middle" style="fill:var(--ink-2);font:600 10.5px var(--sans)">EP</text>
  <text x="340" y="159" text-anchor="end" style="fill:var(--muted);font:500 10px var(--sans)">Re E</text>
  <text x="191" y="116" style="fill:var(--muted);font:500 10px var(--sans)">Im E</text>
</svg>"""

FIG_MAGNETISM = """<svg viewBox="0 0 360 240" role="img" aria-label="Two magnetic sublattices in rotated crystal environments, and bands whose spin splitting reverses between two directions in the Brillouin zone">
  <defs><marker id="sUp" markerWidth="8" markerHeight="8" refX="4" refY="1" orient="auto"><path d="M0,6 L4,0 L8,6" style="fill:none;stroke:#b4553f;stroke-width:1.6"/></marker></defs>
  <g style="stroke:var(--rule);stroke-width:1.2;fill:none">
    <g transform="rotate(16 56 74)"><rect x="34" y="52" width="44" height="44" rx="4"/></g>
    <g transform="rotate(-16 130 74)"><rect x="108" y="52" width="44" height="44" rx="4"/></g>
  </g>
  <g style="stroke:#b4553f;stroke-width:2;fill:none"><path d="M56 92 V56" marker-end="url(#sUp)"/></g>
  <g style="stroke:var(--accent);stroke-width:2;fill:none"><path d="M130 56 V92" marker-end="url(#sUp)"/></g>
  <text x="93" y="122" text-anchor="middle" style="fill:var(--muted);font:500 10px var(--sans)">opposite spins, rotated environments</text>
  <text x="93" y="24" text-anchor="middle" style="fill:var(--ink);font:600 11px var(--sans)">no net magnetisation</text>

  <path d="M210 200 V150 M210 200 H344" style="stroke:var(--rule);stroke-width:1.2"/>
  <path d="M210 158 Q244 186 278 158" style="stroke:#b4553f;stroke-width:2;fill:none"/>
  <path d="M210 172 Q244 200 278 172" style="stroke:var(--accent);stroke-width:2;fill:none"/>
  <path d="M278 172 Q311 200 344 172" style="stroke:#b4553f;stroke-width:2;fill:none"/>
  <path d="M278 158 Q311 186 344 158" style="stroke:var(--accent);stroke-width:2;fill:none"/>
  <line x1="278" y1="150" x2="278" y2="200" style="stroke:var(--rule);stroke-width:1;stroke-dasharray:3 3"/>
  <text x="244" y="216" text-anchor="middle" style="fill:var(--muted);font:500 10px var(--sans)">&#915;&#8594;X</text>
  <text x="311" y="216" text-anchor="middle" style="fill:var(--muted);font:500 10px var(--sans)">&#915;&#8594;Y</text>
  <text x="203" y="145" text-anchor="end" style="fill:var(--muted);font:500 11px var(--sans)">E</text>
  <text x="277" y="140" text-anchor="middle" style="fill:var(--ink);font:600 11px var(--sans)">spin splitting reverses with direction</text>
</svg>"""

FIG_INTERFACE = """<svg viewBox="0 0 360 240" role="img" aria-label="Oxygen octahedra tilting across an oxide interface, altering the local spin-orbit environment of the layer above">
  <defs><marker id="iArr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" style="fill:var(--accent)"/></marker></defs>
  <rect x="20" y="24" width="320" height="92" rx="4" style="fill:var(--accent);opacity:.05"/>
  <rect x="20" y="124" width="320" height="92" rx="4" style="fill:var(--muted);opacity:.06"/>
  <path d="M20 120 H340" style="stroke:var(--accent);stroke-width:1.8;stroke-dasharray:6 4"/>
  <text x="336" y="114" text-anchor="end" style="fill:var(--accent);font:600 10px var(--sans)">interface</text>
  <g style="stroke:var(--accent);stroke-width:1.5;fill:none">
    <g transform="rotate(11 64 70)"><path d="M42 70 L64 48 L86 70 L64 92 Z"/><path d="M42 70 H86 M64 48 V92"/></g>
    <g transform="rotate(-11 140 70)"><path d="M118 70 L140 48 L162 70 L140 92 Z"/><path d="M118 70 H162 M140 48 V92"/></g>
    <g transform="rotate(11 216 70)"><path d="M194 70 L216 48 L238 70 L216 92 Z"/><path d="M194 70 H238 M216 48 V92"/></g>
    <g transform="rotate(-11 292 70)"><path d="M270 70 L292 48 L314 70 L292 92 Z"/><path d="M270 70 H314 M292 48 V92"/></g>
  </g>
  <g style="stroke:var(--ink-2);stroke-width:1.4;fill:none;opacity:.55">
    <path d="M42 170 L64 148 L86 170 L64 192 Z"/><path d="M42 170 H86 M64 148 V192"/>
    <path d="M118 170 L140 148 L162 170 L140 192 Z"/><path d="M118 170 H162 M140 148 V192"/>
    <path d="M194 170 L216 148 L238 170 L216 192 Z"/><path d="M194 170 H238 M216 148 V192"/>
    <path d="M270 170 L292 148 L314 170 L292 192 Z"/><path d="M270 170 H314 M292 148 V192"/>
  </g>
  <g style="stroke:var(--accent);stroke-width:1.8;fill:none">
    <path d="M102 56 V84" marker-end="url(#iArr)"/><path d="M178 84 V56" marker-end="url(#iArr)"/><path d="M254 56 V84" marker-end="url(#iArr)"/>
  </g>
  <text x="26" y="42" style="fill:var(--muted);font:500 10px var(--sans)">tilted; spin&#8211;orbit-entangled state reconstructed</text>
  <text x="26" y="210" style="fill:var(--muted);font:500 10px var(--sans)">bulk-like substrate</text>
</svg>"""

FIG_MATERIALS = """<svg viewBox="0 0 360 240" role="img" aria-label="A square-and-octagon carbon network and an anisotropic Dirac cone">
  <g style="stroke:var(--accent);stroke-width:1.4;fill:none;opacity:.92">
    <rect x="30" y="30" width="36" height="36"/><rect x="104" y="30" width="36" height="36"/>
    <rect x="30" y="104" width="36" height="36"/><rect x="104" y="104" width="36" height="36"/>
    <path d="M66 48 H104 M66 122 H104 M48 66 V104 M122 66 V104"/>
    <path d="M30 48 H12 M140 48 H158 M30 122 H12 M140 122 H158 M48 30 V12 M122 30 V12 M48 140 V158 M122 140 V158"/>
  </g>
  <g style="fill:var(--accent)">
    <circle cx="30" cy="30" r="3.2"/><circle cx="66" cy="30" r="3.2"/><circle cx="30" cy="66" r="3.2"/><circle cx="66" cy="66" r="3.2"/>
    <circle cx="104" cy="30" r="3.2"/><circle cx="140" cy="30" r="3.2"/><circle cx="104" cy="66" r="3.2"/><circle cx="140" cy="66" r="3.2"/>
    <circle cx="30" cy="104" r="3.2"/><circle cx="66" cy="104" r="3.2"/><circle cx="30" cy="140" r="3.2"/><circle cx="66" cy="140" r="3.2"/>
    <circle cx="104" cy="104" r="3.2"/><circle cx="140" cy="104" r="3.2"/><circle cx="104" cy="140" r="3.2"/><circle cx="140" cy="140" r="3.2"/>
  </g>
  <text x="12" y="184" style="fill:var(--muted);font:500 10px var(--sans)">square-and-octagon carbon network</text>
  <path d="M204 206 L272 122 L340 206" style="stroke:var(--accent);stroke-width:1.8;fill:none"/>
  <path d="M204 38 L272 122 L340 38" style="stroke:var(--accent);stroke-width:1.8;fill:none"/>
  <ellipse cx="272" cy="206" rx="68" ry="14" style="fill:none;stroke:var(--rule);stroke-width:1.1"/>
  <ellipse cx="272" cy="38" rx="68" ry="14" style="fill:none;stroke:var(--rule);stroke-width:1.1"/>
  <circle cx="272" cy="122" r="4" style="fill:var(--accent)"/>
  <text x="282" y="119" style="fill:var(--muted);font:500 10px var(--sans)">Dirac point</text>
</svg>"""

CARD_FIGS = {"geometry": FIG_GEOMETRY, "topology": FIG_KAGOME, "magnetism": FIG_MAGNETISM,
             "interfaces": FIG_INTERFACE, "materials": FIG_MATERIALS}

# ---- counts, computed from data/publications.json so nothing is typed twice ----
_DATA = json.loads((ROOT / "data" / "publications.json").read_text(encoding="utf-8"))
_PILLAR_KEYS = ["geometry", "topology", "magnetism", "interfaces", "materials"]


def _tally(key):
    """(published, under review, in preparation) for one pillar."""
    pub = sum(1 for x in _DATA["peer_reviewed"] if key in x.get("tags", []))
    ur = prep = 0
    for x in _DATA["preprints"]:
        if key not in x.get("tags", []):
            continue
        if str(x.get("journal", "")).lower().startswith("under review"):
            ur += 1
        else:
            prep += 1
    return pub, ur, prep


def count_line(key):
    pub, ur, prep = _tally(key)
    bits = ["%d paper%s" % (pub, "" if pub == 1 else "s")]
    if ur:
        bits.append("%d under review" % ur)
    if prep:
        bits.append("%d in preparation" % prep)
    return " &middot; ".join(bits)


PILLARS = [
 ("geometry", "01", "Quantum geometry &amp; unconventional transport", count_line("geometry"),
  "Berry curvature, the quantum metric and the transverse responses they generate — nonlinear Hall, "
  "anomalous Hall and Nernst — in materials where symmetry allows them."),
 ("topology", "02", "Topology, flat bands &amp; kagome quantum matter", count_line("topology"),
  "Where flat bands come from in kagome and other line-graph lattices, when they carry non-trivial topology, "
  "and what exactly solvable lattice methods reveal that numerics alone do not."),
 ("magnetism", "03", "Magnetism, correlations &amp; spin–orbit physics", count_line("magnetism"),
  "Magnetic order and spin–orbit coupling decide which anomalous and nonlinear responses are allowed. "
  "Altermagnetism, magnetic Weyl semimetals, molecular magnetism — and correlated methods as an "
  "expanding direction."),
 ("interfaces", "04", "Interfaces &amp; materials-realistic quantum matter", count_line("interfaces"),
  "Complex-oxide heterostructures, where a structural distortion of a few degrees reorganises the "
  "electronic and magnetic state, tested directly against spectroscopy and transport."),
 ("materials", "05", "Low-dimensional &amp; chemically designed materials", count_line("materials"),
  "The largest part of my record: predicting two-dimensional and molecular lattices from first "
  "principles, and working out where their Dirac points, nodal lines and band gaps come from."),
]


def pillar_cards():
    out = []
    for key, n, title, count, blurb in PILLARS:
        out.append("""        <a class="pillar-card" href="research.html#%s">
          <span class="n">%s</span>
          <h3>%s</h3>
          <p>%s</p>
          <span class="count">%s</span>
          <span class="more">Read more &rarr;</span>
        </a>""" % (key, n, title, blurb, count))
    return "\n".join(out)


# =========================================================================
#  Home
# =========================================================================
HOME = """
<section class="hero">
  <div class="wrap">
    <div class="hero-grid">
      <div>
        <p class="kicker">Theoretical Condensed-Matter Physicist</p>
        <h1>Arka Bandyopadhyay</h1>
        <p class="keywords">Quantum materials &middot; topology &amp; Dirac physics &middot; quantum geometry &middot; magnetism &middot; unconventional transport</p>
        <p class="affil">Computational Quantum Materials, Institute for Theoretical Physics and Astrophysics<br>
          Julius-Maximilians-Universit&auml;t W&uuml;rzburg &middot; Cluster of Excellence <em>ct.qmat</em></p>
        <p class="lede">I am a theoretical condensed-matter physicist working on quantum materials. My
          research examines how the electronic structure and symmetry of a material give rise to
          topological, quantum-geometric and magnetic properties, and how those show up in transport and
          spectroscopy. I am drawn to lattices where geometry does something specific &mdash; Dirac and
          nodal-line systems away from the honeycomb, kagome and other line-graph flat bands, oxide interfaces
          where a few degrees of octahedral tilt decide which spin&ndash;orbit-entangled state the layer
          settles into. The work is done
          with first-principles and Wannier-based calculations, symmetry-adapted tight-binding models,
          quantum transport and, increasingly, many-body methods. Several projects run with experimental groups,
          where the calculations either identify the mechanism behind a measurement or point to a signature
          worth looking for.</p>
        <div class="actions">
          <a class="btn btn--primary" href="research.html">Research programme</a>
          <a class="btn" href="publications.html">Publications</a>
          <a class="btn" href="cv.html">CV</a>
          <a class="btn" href="mailto:arka.bandyopadhyay@uni-wuerzburg.de">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 7 10 6 10-6"/></svg>
            Email</a>
        </div>
      </div>
      <div class="portrait-frame">
        <img class="portrait" src="assets/img/portrait.jpg" width="560" height="627"
             alt="Arka Bandyopadhyay">
      </div>
    </div>
  </div>
</section>

<section class="section" style="padding-block:0 clamp(2.4rem,5vw,3.4rem)">
  <div class="wrap"><div class="record" id="record"></div></div>
</section>

<section class="section section--tint" id="programme">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Research programme</p>
      <h2>Five threads, one way of working</h2>
      <p>The threads below are separate research directions, not variations on a single question. What they
        share is a way of working: start from the structure and symmetry of a specific material, build an
        electronic-structure model faithful enough to be quantitative, and follow it through to a response a
        measurement can resolve.</p>
      <p>They also overlap in practice. The symmetry analysis that decides whether a nonlinear Hall
        response is allowed at all is the same one that decides which magnetic orders can give an
        anomalous Hall effect, and the tight-binding and Wannier machinery is shared across all five.</p>
    </div>
    <figure class="map">
      <div class="map-scroll" tabindex="0" role="group" aria-label="Diagram: how the research programme moves from structure to measurement (scrollable)">%(map)s</div>
      <figcaption>The chain most of my projects follow. Structure and chemistry set the local symmetry and
        which orbitals matter; those decide what topology, Berry curvature and magnetic order are possible;
        and those fix what a transport or spectroscopy measurement can see. The return arrow matters as much
        as the forward one: a measurement that resists explanation is often what selects the next
        model.</figcaption>
    </figure>
    <div class="pillars" style="margin-top:var(--s5)">
%(cards)s
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Selected work</p>
      <h2>Six papers, five threads</h2>
      <p>Chosen to show the range of the programme rather than the journals. One line on each says what it
        establishes; the complete record is on the <a href="publications.html">publications page</a>.</p>
    </div>
    <div class="selected" id="selected-pubs"></div>
    <div class="actions" style="margin-top:var(--s4)">
      <a class="btn" href="publications.html">Full publication record &rarr;</a>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Recent</p><h2>News</h2></div>
    <ul class="timeline news-compact" data-news="4"></ul>
    <noscript>
      <p class="nojs">The news feed is generated from a data file, which needs JavaScript. Recent papers
        and talks are listed on <a href="https://orcid.org/0000-0003-3386-4289" rel="noopener">ORCID</a>.</p>
    </noscript>

    <div class="actions" style="margin-top:var(--s2)"><a class="btn" href="news.html">All updates &rarr;</a></div>
  </div>
</section>

<section class="section" id="contact">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Get in touch</p>
      <h2>Contact</h2>
      <p>I am always glad to hear from researchers working on quantum materials, unconventional transport,
        topology, magnetism and related problems &mdash; particularly where theory can work closely with
        experiment or with materials design. A material worth calculating, a measurement that resists
        explanation, or a question you want to think through are all good reasons to write.</p>
    </div>
    <div class="contact-grid">
      <address>
        <strong>Dr. Arka Bandyopadhyay</strong><br>
        Institute for Theoretical Physics and Astrophysics<br>
        Computational Quantum Materials<br>
        Julius-Maximilians-Universit&auml;t W&uuml;rzburg<br>
        Am Hubland, 97074 W&uuml;rzburg, Germany<br>
        Building M1 (Informatik/Physik), Room 03.017
      </address>
      <div>
        <p><a href="mailto:arka.bandyopadhyay@uni-wuerzburg.de">arka.bandyopadhyay@uni-wuerzburg.de</a><br>
           <a href="mailto:arkbndy@gmail.com">arkbndy@gmail.com</a></p>
        <div class="idlinks" style="margin-top:var(--s3)">
          <a href="https://orcid.org/0000-0003-3386-4289" target="_blank" rel="noopener">ORCID</a>
          <a href="https://scholar.google.com/citations?user=EcM27vQAAAAJ" target="_blank" rel="noopener">Google Scholar</a>
          <a href="https://github.com/arkbndy" target="_blank" rel="noopener">GitHub</a>
          <a href="https://www.physik.uni-wuerzburg.de/en/cqm/team/postdocs/dr-arka-bandyopadhyay/" target="_blank" rel="noopener">Group page</a>
        </div>
      </div>
    </div>
  </div>
</section>
""" % {"map": MAP_SVG, "cards": pillar_cards()}


# =========================================================================
#  Research
# =========================================================================
DETAIL = [
 dict(key="geometry", n="01", figs=[(FIG_GEOMETRY,
      "Berry curvature distributed asymmetrically over the Fermi surface. Weighted by the equilibrium "
      "occupation and summed over the zone, its momentum derivative gives the Berry-curvature dipole. "
      "Where the point group "
      "allows that dipole to be non-zero, a drive at &omega; produces a second-order transverse current "
      "with a rectified and a 2&omega; component, and no magnetic field is needed.")],
   title="Quantum geometry &amp; unconventional transport",
   thesis="Band energies are only half the story: the wavefunctions carry a geometry of their own, and "
          "it shows up directly in what a sample conducts.",
   body="""<p>Berry curvature and the quantum metric describe how Bloch states change across the
     Brillouin zone. Where symmetry permits, that geometry appears in transport. The nonlinear Hall
     effect is the clearest case. In a non-magnetic metal, time-reversal symmetry forbids a linear
     anomalous Hall response, but a second-order one survives when inversion symmetry is broken
     <em>and</em> the point group leaves a Berry-curvature dipole non-zero &mdash; a Fermi-surface
     quantity whose contribution scales with the scattering time. In magnetic metals that keep the product of
     inversion and time reversal, the picture changes: a scattering-time-independent term set by the
     quantum metric can lead, alongside disorder-induced contributions that scale differently again
     &mdash; skew scattering as &tau;<sup>2</sup>, side-jump-like terms as &tau;<sup>0</sup>. Establishing which mechanism applies in a given
     compound is part of the problem, not a detail.</p>
     <p>My contribution has been to move these ideas from model Hamiltonians to specific materials, and
     to look for handles that change the geometry itself rather than merely the band filling: gating,
     strain, structural chirality, and the choice of molecular building block.</p>""",
   highlights=[
     "A perpendicular electric field reverses the sign of the Berry-curvature dipole in silicene, germanene and stanene and changes its magnitude, making a quantum-geometric quantity gate-tunable",
     "Strain plays the same role in layered phosphorene; structural chirality provides an independent handle in tellurium-based systems",
     "Not every transverse response is geometric &mdash; refraction of carriers at an internal interface produces one without Berry curvature at all",
     "Current work extends this to metal&ndash;organic frameworks, where the lattice geometry follows from the choice of linker",
   ],
   papers=[
     ("Non-linear Hall effects: mechanisms and materials", "Materials Today Electronics <strong>8</strong>, 100101 (2024) &mdash; first and corresponding author"),
     ("Berry curvature dipole and its strain engineering in layered phosphorene", "Materials Today Electronics <strong>6</strong>, 100076 (2023) &mdash; first and corresponding author"),
     ("Electrically switchable giant Berry curvature dipole in silicene, germanene and stanene", "2D Materials <strong>9</strong>, 035013 (2022) &mdash; first author"),
     ("Refraction-induced transverse charge transport", "Phys. Rev. B <strong>114</strong>, 105406 (2026) &mdash; corresponding author; Editors&rsquo; Suggestion"),
   ]),

 dict(key="topology", n="02", figs=[(FIG_KAGOME,
      "Destructive interference on the kagome lattice quenches one band entirely. It is not isolated: "
      "it meets a dispersive band quadratically at the zone centre, while the two dispersive bands cross "
      "linearly at K. Which side of the pair the flat band lies on follows the sign of the hopping."),
      (FIG_DECIMATION,
      "Decimation removes sites exactly, leaving an effective lattice with energy-dependent hoppings. "
      "Made non-Hermitian, its spectrum moves into the complex plane, and eigenvalues together with "
      "their eigenvectors can coalesce at exceptional points.")],
   title="Topology, flat bands &amp; kagome quantum matter",
   thesis="Some lattices are generous: their connectivity alone tells you where the flat band is. "
          "Whether it carries topology is then a question about the terms you add.",
   body="""<p>A flat band has no dispersion, so kinetic energy is quenched and whatever else is present
     sets the scale. On the kagome lattice &mdash; the line graph of the honeycomb &mdash; the flat band
     comes from compact states that live on the hexagonal plaquettes and interfere destructively at the
     apex sites, so its origin is structural rather than accidental. With uniform nearest-neighbour
     hopping that argument carries across the whole line-graph family; longer-range hopping and orbital
     multiplicity lift the flatness, which is what makes the multi-orbital case interesting. With coupled
     kagome layers we traced the flat bands to that origin and worked out when interlayer coupling
     separates the nearly flat band from the dispersive ones, and when what remains is topologically
     non-trivial.</p>
     <p>The same interest in exactly solvable structure runs through my work on real-space decimation,
     which eliminates sites exactly and turns a numerical parameter scan into conditions on
     energy-dependent effective hoppings. It extends naturally to non-Hermitian lattices, where the two usual
     ingredients typically do different things: balanced gain and loss bring eigenvalues <em>and their
     eigenvectors</em> together at exceptional points, while non-reciprocal hopping gives the spectrum a
     non-zero point-gap winding, and with it skin modes that pile up at a boundary.</p>""",
   highlights=[
     "Line-graph origin of the flat bands in coupled kagome lattices, and the condition on interlayer coupling for the separated band to stay topologically non-trivial",
     "Exact decimation gives analytic conditions &mdash; evaluated at the flat-band energy &mdash; for flat bands, and for skin modes in decorated non-reciprocal lattices",
     "Exceptional points located analytically in a dice-lattice Haldane model",
     "With W&uuml;rzburg experimental groups, a minimal two-dimensional multi-orbital kagome model realised in a grown system and tested by photoemission (manuscript in preparation)",
   ],
   papers=[
     ("Origin of flat bands and non-trivial topology in coupled kagome lattices", "Communications Physics <strong>8</strong>, 519 (2025) &mdash; joint first author"),
     ("Non-Hermitian topology and flat bands via an exact real-space decimation scheme", "Phys. Rev. B <strong>110</strong>, 085431 (2024) &mdash; joint first author"),
     ("Non-Hermiticity induced exceptional points and skin effect in the Haldane model on a dice lattice", "Phys. Rev. B <strong>107</strong>, 035403 (2023)"),
   ]),

 dict(key="magnetism", n="03", figs=[(FIG_MAGNETISM,
      "In an altermagnet the two magnetic sublattices are related by a rotation, and not by a "
      "translation or by inversion. The net magnetisation vanishes by symmetry, yet the bands acquire a "
      "spin splitting that is even in momentum and changes sign between directions. Drawn here for a "
      "d<sub><i>x</i>&sup2;&minus;<i>y</i>&sup2;</sub> form factor; other wave symmetries put the nodal "
      "directions elsewhere.")],
   title="Magnetism, correlations &amp; spin&ndash;orbit physics",
   thesis="Magnetic order, spin&ndash;orbit coupling and interactions do not merely shift bands &mdash; "
          "they change which responses are allowed at all.",
   body="""<p>Magnetism has become a larger part of my work, and electronic correlations are the newest
     addition to it. Magnetic order lowers symmetry, and what survives determines whether an anomalous Hall
     or Nernst response can exist at all, how spin and orbital degrees of freedom mix, and whether a flat
     band can become a correlated state.
     Altermagnetism is an instructive case: a collinear order whose net magnetisation vanishes by
     symmetry in the absence of spin&ndash;orbit coupling, and which nonetheless produces a
     momentum-dependent spin splitting. The reason is that the two sublattices are connected by a rotation
     or rotoreflection and <em>not</em> by a translation or by inversion &mdash; either of which would
     restore spin degeneracy. The splitting is even in momentum and survives without spin&ndash;orbit
     coupling, which is what separates it from Rashba- and Dresselhaus-type splitting. Our review restates
     those symmetry conditions in the language of crystal chemistry, so that they can be applied when
     screening candidate compounds.</p>
     <p>Alongside this I work on magnetism at the molecular scale, where ligand-field chemistry and
     crystal packing set the spin state. I am now applying correlated methods &mdash; dynamical mean-field
     theory and the functional renormalisation group &mdash; to flat-band and kagome problems. That work is
     under way rather than concluded, and I describe it as a direction rather than a result.</p>""",
   highlights=[
     "Altermagnetism restated as chemical and symmetry criteria that can guide the search for candidate materials",
     "Anomalous Hall and Nernst responses tuned by composition in magnetic Weyl semimetals",
     "Spin-state switching in manganese(III) complexes, where ligand-field chemistry and crystal packing set the magnetic state",
     "Magnon&ndash;electromagnon anomalies in rare-earth-doped BiFeO<sub>3</sub> films &mdash; manuscript under review",
     "Correlated approaches (DMFT via w2dynamics, FRG via divERGe) applied to flat-band and kagome systems &mdash; work in progress",
   ],
   papers=[
     ("Altermagnetism from the viewpoint of chemistry", "Chem. Soc. Rev. (2026)"),
     ("Tunable anomalous Hall and Nernst effects in magnetic Weyl semimetals Co<sub>2&minus;<i>x</i></sub>Cr<sub><i>x</i></sub>MnGe", "J. Phys.: Condens. Matter <strong>37</strong>, 365702 (2025)"),
     ("Spin-state switching: chemical modulation and the impact of intermolecular interactions in manganese(III) complexes", "Dalton Trans. <strong>52</strong>, 11335 (2023)"),
   ]),

 dict(key="interfaces", n="04", figs=[(FIG_INTERFACE,
      "Octahedral rotations propagate across a complex-oxide interface. The changed "
      "metal&ndash;oxygen&ndash;metal angles alter orbital overlap, bandwidth and crystal-field splitting "
      "in the layer above, and so the state it settles into.")],
   title="Interfaces &amp; materials-realistic quantum matter",
   thesis="At an oxide interface a few degrees of octahedral tilt can decide which "
          "spin&ndash;orbit-entangled ground state the layer settles into.",
   body="""<p>Where two perovskite oxides meet, the oxygen octahedra do not simply join: the tilt
     pattern of one propagates into the other over several unit cells. Changing the
     metal&ndash;oxygen&ndash;metal angles changes the orbital overlaps and so the bandwidth, while the
     accompanying local distortion lowers the site symmetry and splits the t<sub>2g</sub> manifold. The
     atomic spin&ndash;orbit coupling itself is fixed; what the tilt moves is the balance between it, the
     crystal field and the bandwidth &mdash; and that balance decides which spin&ndash;orbit-entangled
     state the layer settles into, and how it conducts.</p>
     <p>Working with groups performing X-ray spectroscopy, photoemission and transport, we established a
     route from the measured tilt coupling to the reconstructed spin&ndash;orbit-entangled state. This is the part
     of my work where theory is most tightly constrained by experiment: the calculations are done for
     the structure that was actually grown, not an idealised one. The experimental measurements are my
     collaborators&rsquo; work; my contribution is the electronic-structure modelling and its
     interpretation.</p>""",
   highlights=[
     "Octahedral tilt coupling related to spin&ndash;orbit reconstruction at a complex-oxide interface, published in <em>Nature Communications</em>",
     "Berry-curvature-dipole nonlinear Hall response predicted for oxide heterostructures",
     "Antiferromagnetic tunnel barriers producing discrete tunnelling-magnetoresistance states &mdash; manuscript under review",
   ],
   papers=[
     ("An unconventional pathway to correlate the octahedral tilt coupling and spin&ndash;orbit reconstruction at oxide interfaces", "Nature Communications <strong>17</strong>, 332 (2026) &mdash; joint first author"),
     ("Berry curvature dipole-induced non-linear Hall effect in oxide heterostructures", "J. Mater. Chem. C <strong>14</strong>, 11561 (2026)"),
   ]),

 dict(key="materials", n="05", figs=[(FIG_MATERIALS,
      "Dirac cones do not require a honeycomb. Square-and-octagon carbon networks host anisotropic "
      "cones and nodal lines. A node is located by the jump in the Zak phase &mdash; symmetry-quantised to "
      "0 or &pi; &mdash; between one-dimensional cuts on either side of it.")],
   title="Low-dimensional &amp; chemically designed materials",
   thesis="Dirac physics does not require a honeycomb &mdash; and much of what I ask later about "
          "topology and transport began as a question about which lattices could exist at all.",
   body="""<p>This is the largest part of my published record and, in a real sense, the origin of the
     rest. Beginning in my doctoral work, this line has predicted two-dimensional carbon, silicon and
     nitride networks built from squares, octagons and acetylenic links and worked out what their
     electrons do &mdash; some of it led by me, some by colleagues whose electronic-structure analysis I
     contributed to:
     S-graphene, whose two Dirac cones survive distortion; 8-16-4 graphyne, a square-lattice nodal-line
     semimetal whose nodal lines are located by a symmetry-quantised Zak phase along
     one-dimensional cuts of the Brillouin zone; the dumbbell C<sub>3</sub>NX family and its
     quasi-one-dimensional derivatives. Two reviews map the wider landscape and have each received an IOP
     India Top Cited Paper Award; I led the first and was second author on the second.</p>
     <p>The same first-principles workflow, pointed at a device figure of merit rather than a topological
     invariant, produced an earlier interdisciplinary thread on lithium storage, supercapacitance,
     thermoelectrics, photocatalysis and redox polymers. It is not where my current questions lie, but it
     shaped how I judge whether a predicted material is worth an experimentalist&rsquo;s time.</p>""",
   highlights=[
     "S-graphene and 8-16-4 graphyne: Dirac cones and nodal lines away from the honeycomb lattice",
     "The dumbbell C<sub>3</sub>NX family (X = C, Si, Ge) and its quasi-one-dimensional derivatives",
     "Semiconductor device responses from first principles &mdash; negative differential resistance, rectification, gas sensing &mdash; via non-equilibrium Green-function (NEGF) transport",
     "Functional properties with chemists: lithium storage, supercapacitance, thermoelectrics, photocatalysis and &pi;-conjugated redox polymers",
   ],
   papers=[
     ("8-16-4 graphyne: square-lattice two-dimensional nodal line semimetal with a nontrivial topological Zak index", "Phys. Rev. B <strong>103</strong>, 075137 (2021) &mdash; first author"),
     ("The topology and robustness of two Dirac cones in S-graphene: a tight binding approach", "Scientific Reports <strong>10</strong>, 2502 (2020) &mdash; first author"),
     ("A review on role of tetra-rings in the graphene systems and their possible applications", "Rep. Prog. Phys. <strong>83</strong>, 056501 (2020) &mdash; first author; IOP India Top Cited Paper Award"),
   ]),
]


def pillar_sections():
    out = []
    for d in DETAIL:
        figs = "\n".join(
            '        <figure><div class="box">%s</div><figcaption>%s</figcaption></figure>' % (svg, cap)
            for svg, cap in d["figs"])
        hl = "\n".join("          <li>%s</li>" % h for h in d["highlights"])
        pp = "\n".join('            <li>%s <span class="venue">%s</span></li>' % (t, v) for t, v in d["papers"])
        out.append("""    <article class="pillar" id="%(key)s">
      <div>
        <span class="n">%(n)s</span>
        <h2>%(title)s</h2>
        <p class="pillar-count">%(count)s</p>
        <p class="thesis">%(thesis)s</p>
        %(body)s
        <ul class="highlights">
%(hl)s
        </ul>
        <div class="keypapers">
          <h3>Representative papers</h3>
          <ul>
%(pp)s
          </ul>
        </div>
      </div>
      <div class="figure">
%(figs)s
      </div>
    </article>""" % dict(key=d["key"], n=d["n"], title=d["title"], thesis=d["thesis"],
                         count=count_line(d["key"]), body=d["body"], hl=hl, pp=pp, figs=figs))
    return "\n".join(out)


# =========================================================================
#  Collaborators
# =========================================================================
GS = "https://scholar.google.com/citations?user=%s"
GROUPS = [
 ("Universit&auml;t W&uuml;rzburg", [
  ("Ronny Thomale", "Professor of Theoretical Physics", GS % "RJ8vWeoAAAAJ", "GS"),
  ("Giorgio Sangiovanni", "Professor of Theoretical Physics", GS % "SeCV78UAAAAJ", "GS"),
  ("Ralph Claessen", "Professor of Experimental Physics", GS % "t8wpk5sAAAAJ", "GS"),
  ("J&ouml;rg Sch&auml;fer", "Professor of Experimental Physics", GS % "25yzQPYAAAAJ", "GS"),
  ("Lennart Klebl", "Institute for Theoretical Physics and Astrophysics",
   "https://www.physik.uni-wuerzburg.de/tp1/team/postdocs/dr-lennart-klebl/", "WEB"),
  ("Manish Verma", "Computational Quantum Materials", GS % "7EljkOAAAAAJ", "GS")]),
 ("Indian Institute of Science, Bengaluru", [
  ("Awadhesh Narayan", "Associate Professor, Solid State and Structural Chemistry Unit", GS % "kHOQvgQAAAAJ", "GS"),
  ("Diptiman Sen", "Professor, Centre for High Energy Physics", GS % "4TZdOPIAAAAJ", "GS"),
  ("Sujit Das", "Assistant Professor, Materials Research Centre", GS % "L8j4ld8AAAAJ", "GS"),
  ("Satish Patil", "Professor of Polymer Chemistry", GS % "Tyfe7LcAAAAJ", "GS"),
  ("Bhagwati Prasad", "Department of Materials Engineering", GS % "8lDnePMAAAAJ", "GS"),
  ("Abhishake Mondal", "Associate Professor, Solid State and Structural Chemistry Unit", GS % "wZkA5s0AAAAJ", "GS"),
  ("Naga Phani B. Aetukuri", "Solid State and Structural Chemistry Unit", GS % "Te2ZTYgAAAAJ", "GS"),
  ("N. Ravishankar", "Professor, Materials Research Centre", GS % "v5FUPi4AAAAJ", "GS"),
  ("S. B. Krupanidhi", "Materials Research Centre", GS % "ieUCCasAAAAJ", "GS"),
  ("Nesta Benno Joseph", "Solid State and Structural Chemistry Unit", GS % "3cfchUgAAAAJ", "GS"),
  ("Ronika Sarkar", "Department of Physics", GS % "WuKSGW8AAAAJ", "GS"),
  ("Md Afsar Reja", "Solid State and Structural Chemistry Unit", None, None)]),
 ("Kolkata and West Bengal", [
  ("Debnarayan Jana", "Professor of Physics, University of Calcutta", GS % "43SR0GsAAAAJ", "GS"),
  ("Arunava Chakrabarti", "Professor of Physics, University of Kalyani",
   "https://scispace.com/authors/arunava-chakrabarti-7pqvtc1c09", "WEB"),
  ("Dirtha Sanyal", "Variable Energy Cyclotron Centre", GS % "ReD7dBWTPcwC", "GS"),
  ("Atanu Nandy", "Acharya Prafulla Chandra College", GS % "9eE-LGcAAAAJ", "GS"),
  ("Subhadip Nath", "Assistant Professor of Physics, Krishnagar Government College", GS % "kwKfWjwAAAAJ", "GS"),
  ("Debaprem Bhattacharya", "Government College of Engineering &amp; Textile Technology, Berhampore", GS % "7LZ-wgQAAAAJ", "GS")]),
 ("Across India", [
  ("Ajit C. Balram", "Institute of Mathematical Sciences, Chennai", GS % "T1vffdAAAAAJ", "GS"),
  ("Amrita Mukherjee", "Tata Institute of Fundamental Research", None, None),
  ("Supriya Ghosal", "Theoretical Sciences Unit, JNCASR, Bengaluru", GS % "QIltrEEAAAAJ", "GS"),
  ("Deep Mondal", "Indian Institute of Technology Bombay", GS % "TbMI07YAAAAJ", "GS"),
  ("Anju Ahlawat", "Institute of Sciences, SAGE University, Indore", GS % "A72iJqMAAAAJ", "GS"),
  ("Basanta Roul", "Central Research Laboratory, Bharat Electronics, Bengaluru", GS % "0eUYcSQAAAAJ", "GS"),
  ("Suman Chowdhury", "Department of Physics &amp; Astrophysics, University of Delhi", GS % "Do_yowMAAAAJ", "GS")]),
 ("International partners", [
  ("Claudia Felser", "Director, Max Planck Institute for Chemical Physics of Solids, Dresden", GS % "QOdCHXMAAAAJ", "GS"),
  ("T. Venky Venkatesan", "Center for Quantum Research and Technology, University of Oklahoma", GS % "brdyAZ4AAAAJ", "GS"),
  ("Rajeev Ahuja", "Uppsala University", GS % "OqyvV_oAAAAJ", "GS"),
  ("Faxian Xiu", "Department of Physics, Fudan University", GS % "0QMB9ZUAAAAJ", "GS"),
  ("Simon Moser", "Professor of Experimental Physics, Ruhr-Universit&auml;t Bochum", GS % "WCSgzGwAAAAJ", "GS"),
  ("Hendrik Bentmann", "Associate Professor, Center for Quantum Spintronics, NTNU Trondheim", GS % "tNbD2eMAAAAJ", "GS"),
  ("Domenico Di Sante", "University of Bologna", GS % "EVyjBUYAAAAJ", "GS"),
  ("Carmine Ortix", "University of Salerno", GS % "5tgyU54AAAAJ", "GS"),
  ("Enze Zhang", "School of Physics, Nanjing University", GS % "fp_HNTAAAAAJ", "GS"),
  ("Moritz Hoesch", "PETRA III, Deutsches Elektronen-Synchrotron (DESY), Hamburg", GS % "PtrvJRoAAAAJ", "GS"),
  ("Manuel Valvidares", "ALBA Synchrotron Light Source, Barcelona", GS % "n21FAZYAAAAJ", "GS"),
  ("Akbar Ali Mohamad", "Assistant Professor of Chemistry, Khalifa University, Abu Dhabi", GS % "f9iY8woAAAAJ", "GS"),
  ("Md. Mohi Uddin", "Professor of Physics, Chittagong University of Engineering &amp; Technology", GS % "VkzVBBkAAAAJ", "GS"),
  ("Anumita Bose", "Condensed Matter Theory, SISSA, Trieste", GS % "-iKh_vkAAAAJ", "GS"),
  ("Ayan Banerjee", "Max Planck Institute for the Science of Light, Erlangen", GS % "AGIwnYEAAAAJ", "GS")]),
]


def collaborators():
    blocks, total = [], 0
    for title, people in GROUPS:
        total += len(people)
        rows = []
        for name, aff, url, badge in people:
            link = ('<a class="gs" href="%s" target="_blank" rel="noopener" title="%s profile for %s">%s</a>'
                    % (url, "Google Scholar" if badge == "GS" else "Homepage", name, badge)) if url else ''
            rows.append('          <li><div><span class="who">%s</span><span class="where">%s</span></div>%s</li>'
                        % (name, aff, link))
        blocks.append("""      <details class="collab-group">
        <summary>%s <span class="n">%d</span></summary>
        <ul class="collab-list">
%s
        </ul>
      </details>""" % (title, len(people), "\n".join(rows)))
    return "\n".join(blocks), total


COLLAB_HTML, COLLAB_N = collaborators()

RESEARCH = """
<section class="section">
  <div class="wrap">
    <div class="section-head prose">
      <p class="eyebrow">Research</p>
      <h1>Quantum materials, from structure to signal</h1>
      <p>In a quantum material the lattice does more than hold the atoms in place. The crystal structure
        fixes which orbitals lie near the Fermi level; the symmetry of that structure decides which
        responses are allowed to be non-zero; spin&ndash;orbit coupling and magnetic order reshape the
        bands; and where a band is flat, interactions set the remaining energy scale. My work follows that
        chain in specific compounds, and asks which transport or spectroscopic signature distinguishes one
        mechanism from another.</p>
      <p>The chain runs through more than one discipline. Coordination and crystal chemistry set orbital
        overlap and local symmetry; an oxide interface changes octahedral tilts and with them the
        spin&ndash;orbit-entangled state a layer settles into; the choice of molecular linker sets lattice geometry directly. That
        is why a substantial part of my work is done with chemists and materials scientists &mdash; not as
        an aside, but because those are the practical handles on electronic structure.</p>
      <p>Several projects run in close collaboration with experimental groups, and the exchange goes both
        ways. In one direction, first-principles calculations and microscopic models are used to interpret
        measured transport and spectra and to identify which mechanism is responsible. In the other, a
        model points to a signature, a parameter regime or a candidate compound that can then be tested. I
        do not perform experiments myself &mdash; the transport, photoemission, X-ray spectroscopy and
        synthesis behind the work below are my collaborators&rsquo;.</p>
    </div>

    <div class="keypapers prose" style="margin-bottom:var(--s6)">
      <h2>How the programme developed</h2>
      <ul>
        <li>Predicting two-dimensional carbon and nitride lattices, and finding Dirac cones away from the honeycomb</li>
        <li>Nodal lines and Zak phases in those lattices</li>
        <li>Berry curvature and the quantum metric, and the nonlinear and anomalous transport they produce</li>
        <li>Flat bands traced to line-graph structure, with kagome systems as the testbed, and exact real-space methods extended to non-Hermitian lattices</li>
        <li>Magnetism and spin&ndash;orbit coupling in real compounds and at oxide interfaces &mdash; correlated methods now being added</li>
      </ul>
    </div>

%(sections)s
  </div>
</section>

<section class="section section--tint" id="collaborators">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">People</p>
      <h2>Collaborators</h2>
      <p>My research has benefited enormously from collaboration across theory, experiment and materials
        synthesis. The longest-running are with <strong>Prof. Debnarayan Jana</strong> at the University of
        Calcutta, which goes back to my doctoral work, and <strong>Prof. Awadhesh Narayan</strong> at the
        Indian Institute of Science. In W&uuml;rzburg I work with <strong>Prof. Ronny Thomale</strong> and
        <strong>Prof. Giorgio Sangiovanni</strong>. The groups below span condensed-matter theory,
        photoemission and X-ray spectroscopy, transport measurement, thin-film growth and synthetic
        chemistry.</p>
    </div>
%(collab)s
  </div>
</section>

<section class="section">
  <div class="wrap prose">
    <p class="eyebrow">Methods</p>
    <h2>How the work is done</h2>
    <div class="tool-grid" style="margin-top:var(--s4)">
      <div class="tool-card"><h3>Electronic structure</h3>
        <p>Density-functional theory (Quantum ESPRESSO, VASP, SIESTA, OpenMX); Wannier functions and
          quantum-geometric quantities (Wannier90, WannierTools, WannierBerri).</p></div>
      <div class="tool-card"><h3>Models &amp; symmetry</h3>
        <p>Symmetry-adapted tight-binding models, real-space decimation and renormalisation, topological
          invariants, non-Hermitian formulations.</p></div>
      <div class="tool-card"><h3>Transport &amp; many-body</h3>
        <p>non-equilibrium Green-function (NEGF) transport; Boltzmann and quantum-geometric response theory; dynamical
          mean-field theory (<a href="https://github.com/w2dynamics/w2dynamics" target="_blank" rel="noopener">w2dynamics</a>)
          and functional renormalisation group (<a href="https://git.rwth-aachen.de/frg/divERGe" target="_blank" rel="noopener">divERGe</a>).</p></div>
      <div class="tool-card"><h3>Computing</h3>
        <p>Python (NumPy, SciPy, Matplotlib), Fortran, Mathematica, Linux and HPC workflows.</p></div>
    </div>
    <p style="margin-top:var(--s4);color:var(--muted);font-size:.92rem">I am glad to discuss any of these
      with someone who wants to learn them.</p>
  </div>
</section>
""" % {"sections": pillar_sections(), "collab": COLLAB_HTML}


# =========================================================================
#  Publications
# =========================================================================
CHIPS = [("all", "All")] + [(k, t) for k, _n, t, _c, _b in
         [(p[0], p[1], p[2], p[3], p[4]) for p in PILLARS]]
CHIP_LABELS = {"geometry": "Quantum geometry", "topology": "Topology &amp; flat bands",
               "magnetism": "Magnetism &amp; correlations", "interfaces": "Interfaces",
               "materials": "Low-dimensional materials"}

PUBLICATIONS = """
<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Publications</p>
      <h1>Complete record</h1>
      <p>Peer-reviewed papers, newest first, numbered so that each keeps its number as the list grows.
        Every entry links to the DOI, and to the arXiv posting where one exists. The filters follow the
        five research threads. Also on
        <a href="https://orcid.org/0000-0003-3386-4289" target="_blank" rel="noopener">ORCID</a> and
        <a href="https://scholar.google.com/citations?user=EcM27vQAAAAJ" target="_blank" rel="noopener">Google Scholar</a>.</p>
    </div>

    <div class="pubtools">
      <div class="search">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
        <label for="pub-search" class="skip">Search publications</label>
        <input id="pub-search" type="search" placeholder="Search title, author, journal or year&hellip;" autocomplete="off">
      </div>
      <div class="chips" role="group" aria-label="Filter publications by research thread">
        <button class="chip" type="button" data-tag="all" aria-pressed="true">All</button>
        <button class="chip" type="button" data-tag="geometry" aria-pressed="false">Quantum geometry</button>
        <button class="chip" type="button" data-tag="topology" aria-pressed="false">Topology &amp; flat bands</button>
        <button class="chip" type="button" data-tag="magnetism" aria-pressed="false">Magnetism &amp; correlations</button>
        <button class="chip" type="button" data-tag="interfaces" aria-pressed="false">Interfaces</button>
        <button class="chip" type="button" data-tag="materials" aria-pressed="false">Low-dimensional materials</button>
        <button class="chip" type="button" data-tag="review" aria-pressed="false">Reviews</button>
        <button class="chip" type="button" data-tag="applied" aria-pressed="false">Energy &amp; devices</button>
      </div>
    </div>

    <p class="pubcount" id="pub-count" role="status"></p>
    <div id="pub-list"></div>
    <noscript>
      <p class="nojs">This list is generated from a data file, which needs JavaScript. The complete,
        identical record is available on
        <a href="https://orcid.org/0000-0003-3386-4289" rel="noopener">ORCID</a> and
        <a href="https://scholar.google.com/citations?user=EcM27vQAAAAJ" rel="noopener">Google Scholar</a>.</p>
    </noscript>

  </div>
</section>

<section class="section section--tint">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Not yet refereed</p>
      <h2>Manuscripts under review and in preparation</h2>
      <p>Listed separately, and clearly labelled, so that the refereed record above stands on its own.
        Where a journal is named, the manuscript is currently under consideration there &mdash; not
        accepted. Manuscripts still in preparation are marked as such.</p>
    </div>
    <div id="preprint-list"></div>
    <noscript>
      <p class="nojs">This list is generated from a data file, which needs JavaScript. The complete,
        identical record is available on
        <a href="https://orcid.org/0000-0003-3386-4289" rel="noopener">ORCID</a> and
        <a href="https://scholar.google.com/citations?user=EcM27vQAAAAJ" rel="noopener">Google Scholar</a>.</p>
    </noscript>

  </div>
</section>
"""

# =========================================================================
#  News
# =========================================================================
NEWS = """
<section class="section">
  <div class="wrap prose">
    <div class="section-head">
      <p class="eyebrow">Updates</p>
      <h1>News</h1>
      <p>Papers, awards, talks and research visits.</p>
    </div>
    <ul class="timeline" data-news="0"></ul>
    <noscript>
      <p class="nojs">The news feed is generated from a data file, which needs JavaScript. Recent papers
        and talks are listed on <a href="https://orcid.org/0000-0003-3386-4289" rel="noopener">ORCID</a>.</p>
    </noscript>

  </div>
</section>
"""

# =========================================================================
#  CV
# =========================================================================
CV = """
<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Curriculum vitae</p>
      <h1>Arka Bandyopadhyay</h1>
      <p>Theoretical condensed-matter physicist &mdash; quantum materials, topology and quantum geometry,
        magnetism, and unconventional transport.</p>
      <div class="actions" style="margin-top:var(--s3)">
        <a class="btn btn--primary" href="publications.html">Publication record</a>
        <a class="btn" href="research.html">Research programme</a>
      </div>
    </div>

    <div class="cv-block">
      <h2>Research profile</h2>
      <p>I am a theoretical condensed-matter physicist working on quantum materials. My research examines
        how the electronic structure and symmetry of a material give rise to topological, quantum-geometric
        and magnetic properties, and how these are reflected in transport and spectroscopic measurements. I
        am particularly interested in cases where lattice geometry, spin&ndash;orbit coupling, magnetic
        order or electronic correlations qualitatively change the underlying electronic states: Dirac and
        nodal-line systems outside the honeycomb lattice, kagome and other line-graph flat bands, non-Hermitian
        lattices, and complex-oxide interfaces.</p>
      <p>The methods are first-principles electronic structure and Wannier-based modelling,
        symmetry-adapted tight-binding Hamiltonians, quantum transport and, increasingly, many-body
        approaches &mdash; applied to specific compounds rather than idealised Hamiltonians. The work also
        meets materials chemistry and computational materials science, where bonding, coordination geometry,
        interfaces and molecular design give concrete control over electronic structure. Several projects
        run with experimental groups &mdash; I do not perform experiments myself; the calculations serve
        either to identify the mechanism behind a measurement or to propose a signature worth testing.</p>
    </div>

    <div class="cv-block">
      <h2>Positions</h2>
      <div class="cv-entry">
        <div><span class="what">Postdoctoral Researcher</span><br><span class="where">Julius-Maximilians-Universit&auml;t W&uuml;rzburg, Germany</span></div>
        <div class="when">Oct 2024 &ndash; present</div>
        <p class="detail">Topological and quantum-geometric electronic structure of quantum materials in the
          Computational Quantum Materials group, within the DFG Cluster of Excellence <em>ct.qmat</em>: kagome
          and flat-band systems, anomalous and nonlinear transport, and magnetic quantum materials, treated
          with first-principles and Wannier-based models alongside correlated methods. Several projects are
          carried out jointly with theory and experimental groups in W&uuml;rzburg. Independent direction:
          quantum-geometric transport in metal&ndash;organic frameworks, where the choice of linker sets the
          lattice geometry. Mentoring of junior researchers.</p>
      </div>
      <div class="cv-entry">
        <div><span class="what">Visiting Researcher</span><br><span class="where">Indian Institute of Science, Bengaluru</span></div>
        <div class="when">May &ndash; Sep 2024</div>
        <p class="detail">First-principles electronic-structure calculations on magnetic complex-oxide
          interfaces, carried out with the experimental groups measuring them.</p>
      </div>
      <div class="cv-entry">
        <div><span class="what">IISc-IoE Postdoctoral Fellow</span><br><span class="where">Indian Institute of Science, Bengaluru</span></div>
        <div class="when">May 2022 &ndash; May 2024</div>
        <p class="detail">Berry-curvature dipoles and nonlinear Hall response, flat bands in coupled kagome
          lattices, and non-Hermitian topology treated by exact real-space decimation. Started the
          collaborations with oxide-interface and transport experimentalists from which several later papers
          came.</p>
      </div>
      <div class="cv-entry">
        <div><span class="what">Research Associate</span><br><span class="where">Indian Institute of Science, Bengaluru</span></div>
        <div class="when">Jul 2021 &ndash; May 2022</div>
        <p class="detail">Dirac and nodal-line electronic structure in non-honeycomb two-dimensional
          lattices; Berry-curvature dipoles across a quantum spin Hall transition.</p>
      </div>
    </div>

    <div class="cv-block">
      <h2>Academics</h2>
      <div class="cv-entry">
        <div><span class="what">Highest degree &mdash; Ph.D. in Physics</span><br><span class="where">University of Calcutta, India</span></div>
        <div class="when">Awarded Apr 2022</div>
        <p class="detail">Thesis: <em>Electronic and optical properties of graphene allotropes</em>.
          Supervisor: Prof. Debnarayan Jana.</p>
      </div>
    </div>

    <div class="cv-block">
      <h2>Awards &amp; distinctions</h2>
      <div class="cv-entry"><div><span class="what">Physical Review B Editors&rsquo; Suggestion</span><br><span class="where">for &ldquo;Refraction-induced transverse charge transport&rdquo;</span></div><div class="when">2026</div></div>
      <div class="cv-entry"><div><span class="what">IOP India Top Cited Paper Award</span><br><span class="where">for &ldquo;Emerging properties of carbon based 2D material beyond graphene&rdquo;</span></div><div class="when">2025</div></div>
      <div class="cv-entry"><div><span class="what">Journal of Materials Chemistry C cover article</span><br><span class="where">nodal flexible-surface three-dimensional carbon network</span></div><div class="when">2024</div></div>
      <div class="cv-entry"><div><span class="what">IOP India Top Cited Paper Award</span><br><span class="where">for &ldquo;A review on role of tetra-rings in the graphene systems&rdquo;</span></div><div class="when">2023</div></div>
      <div class="cv-entry"><div><span class="what">IOP Trusted Reviewer</span></div><div class="when">2023</div></div>
      <div class="cv-entry"><div><span class="what">Best Oral Presentation</span><br><span class="where">Functional Oxides: Materials and Devices (FOMAD), Indian Institute of Science</span></div><div class="when">2023</div></div>
      <div class="cv-entry"><div><span class="what">IISc Institute of Eminence Postdoctoral Fellowship</span></div><div class="when">2022 &ndash; 2024</div></div>
      <div class="cv-entry"><div><span class="what">CSIR-UGC National Eligibility Test &mdash; All India Rank 85</span><br><span class="where">with UGC Junior Research Fellowship; University Research Fellowship, University of Calcutta</span></div><div class="when">2019</div></div>
    </div>

    <div class="cv-block">
      <h2>Invited talks &amp; academic visits</h2>
      <div class="cv-entry"><div><span class="what">Invited Talk, <a href="https://sscu50.in/" target="_blank" rel="noopener">SSCU-50</a> <span class="flag">upcoming</span></span><br><span class="where">Emergent materials for energy and photonics &mdash; fifty years of the Solid State and Structural Chemistry Unit, Indian Institute of Science, Bengaluru</span></div><div class="when">Dec 2026</div></div>
      <div class="cv-entry"><div><span class="what">Departmental Seminar</span><br><span class="where">Solid State and Structural Chemistry Unit, Indian Institute of Science, Bengaluru</span></div><div class="when">Jan 2026</div></div>
      <div class="cv-entry"><div><span class="what">Departmental Seminar</span><br><span class="where">Theoretical Sciences Unit, JNCASR, Bengaluru</span></div><div class="when">Jan 2026</div></div>
      <div class="cv-entry"><div><span class="what">Resource Person, CMQF-2026 National Seminar</span><br><span class="where">Sidho-Kanho-Birsha University, Purulia</span></div><div class="when">2026</div></div>
      <div class="cv-entry"><div><span class="what">Academic visit &amp; seminar</span><br><span class="where">Department of Quantum Matter Physics, University of Geneva</span></div><div class="when">Apr 2025</div></div>
      <div class="cv-entry"><div><span class="what">Departmental Seminar</span><br><span class="where">Institute for Theoretical Physics and Astrophysics, Universit&auml;t W&uuml;rzburg</span></div><div class="when">Jun 2024</div></div>
      <div class="cv-entry"><div><span class="what">Invited enrichment lecture</span><br><span class="where">C. K. Majumdar Memorial Workshop in Physics</span></div><div class="when">2022</div></div>
    </div>

    <div class="cv-block">
      <h2>Teaching &amp; mentoring</h2>
      <p>I have mentored doctoral and junior researchers at W&uuml;rzburg, IISc and the University of
        Calcutta on theoretical and computational projects &mdash; problem formulation, numerical
        implementation, analysis, and the preparation of manuscripts and presentations. Several of these
        projects led to co-authored publications.</p>
      <p class="detail" style="margin-top:var(--s2)">Courses I am prepared to teach:</p>
      <div class="tool-grid" style="margin-top:var(--s2)">
        <div class="tool-card"><h3>Core</h3><p>Quantum Mechanics &middot; Condensed Matter and Solid State Physics &middot; Mathematical Physics &middot; Computational Physics.</p></div>
        <div class="tool-card"><h3>Advanced</h3><p>Electronic Structure Theory and DFT &middot; Topological Quantum Matter &middot; Quantum Transport &middot; Low-Dimensional and Semiconductor Physics &middot; Introduction to Many-Body Physics.</p></div>
      </div>
    </div>

    <div class="cv-block">
      <h2>Professional service</h2>
      <p>Referee for 14 journals including <em>Physical Review Letters</em>, <em>Physical Review B</em>,
        <em>New Journal of Physics</em>, <em>Communications Physics</em> and <em>2D Materials</em> &mdash;
        34 review reports to date. Session Chair, NAMMA Psi-k Workshop and Conference (2023). Invited
        lecturer and resource person at national workshops.</p>
    </div>

    <div class="cv-block">
      <h2>Technical expertise</h2>
      <div class="tool-grid">
        <div class="tool-card"><h3>Electronic structure</h3><p>Density-functional theory including DFT+<em>U</em>, spin&ndash;orbit coupling and collinear and non-collinear magnetism.<br><span class="codes">Quantum ESPRESSO &middot; VASP &middot; SIESTA &middot; OpenMX; Gaussian and ORCA for molecular and coordination complexes</span></p></div>
        <div class="tool-card"><h3>Wannier &amp; quantum-geometric response</h3><p>Wannier interpolation; Berry curvature, Berry-curvature dipole and quantum metric; anomalous, nonlinear and thermoelectric transport coefficients; topological invariants.<br><span class="codes">Wannier90 &middot; WannierBerri &middot; WannierTools</span></p></div>
        <div class="tool-card"><h3>Model Hamiltonians &amp; transport</h3><p>Symmetry-adapted tight-binding models; real-space decimation and renormalisation; equilibrium and non-equilibrium Green-function (NEGF) quantum transport; non-Hermitian formulations.</p></div>
        <div class="tool-card"><h3>Many-body methods</h3><p>Dynamical mean-field theory and the functional renormalisation group, applied to flat-band and kagome problems &mdash; an expanding part of the work.<br><span class="codes">w2dynamics &middot; divERGe</span></p></div>
        <div class="tool-card"><h3>Scientific computing</h3><p>Python (NumPy, SciPy, Matplotlib) &middot; Fortran &middot; Mathematica &middot; Linux and HPC workflows &middot; LaTeX.</p></div>
        <div class="tool-card"><h3>Languages</h3><p>English &middot; Bengali &middot; Hindi.</p></div>
      </div>
    </div>
  </div>
</section>
"""

# =========================================================================
#  Build
# =========================================================================
DESC_HOME = ("Arka Bandyopadhyay is a theoretical condensed-matter physicist at Universität Würzburg "
             "working on quantum materials: topology and Dirac physics, quantum geometry and nonlinear "
             "transport, kagome flat bands, magnetism and complex-oxide interfaces.")

written = [
  page("index.html", "Arka Bandyopadhyay — Quantum Materials Theory", DESC_HOME, HOME,
       "index.html", JSONLD),
  page("research.html", "Research — Arka Bandyopadhyay",
       "Research programme: quantum geometry and unconventional transport; topology, flat bands and "
       "kagome quantum matter; magnetism and spin-orbit physics; complex-oxide interfaces; and "
       "low-dimensional, chemically designed materials.", RESEARCH, "research.html"),
  page("publications.html", "Publications — Arka Bandyopadhyay",
       "Complete publication record of Arka Bandyopadhyay: peer-reviewed papers with DOI and arXiv "
       "links, filterable by research thread, plus manuscripts under review and in preparation.", PUBLICATIONS,
       "publications.html"),
  page("news.html", "News — Arka Bandyopadhyay",
       "Recent papers, awards, invited talks and research visits.", NEWS, "news.html"),
  page("cv.html", "CV — Arka Bandyopadhyay",
       "Curriculum vitae of Arka Bandyopadhyay, theoretical condensed-matter physicist working on "
       "quantum materials: positions, doctorate, awards, invited talks, teaching and expertise.",
       CV, "cv.html"),
]
print("built:", ", ".join(written))
print("collaborators:", COLLAB_N, "in", len(GROUPS), "groups")
