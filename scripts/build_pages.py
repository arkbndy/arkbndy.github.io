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
    "https://www.linkedin.com/in/arka-bandyopadhyay-315293381/",
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
      <a href="https://www.linkedin.com/in/arka-bandyopadhyay-315293381/" target="_blank" rel="noopener">LinkedIn</a>
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

MAP_SVG = """<svg viewBox="0 0 1080 280" role="img" aria-labelledby="maptitle mapdesc">
  <title id="maptitle">The conceptual architecture of the research programme</title>
  <desc id="mapdesc">Six linked levels: materials and structure; symmetry and electronic structure;
  Dirac states and topology; lattice geometry and flat bands; quantum geometry; unconventional transport
  and measurable response. A band beneath them marks magnetism and electronic correlations, which modify
  every level, and a return arrow runs from measurement back to the models.</desc>
  <defs>
    <marker id="mArrow" markerWidth="9" markerHeight="9" refX="7" refY="3.2" orient="auto">
      <path d="M0,0 L7,3.2 L0,6.4 z" style="fill:var(--accent)"/>
    </marker>
    <marker id="mArrowSoft" markerWidth="8" markerHeight="8" refX="6.4" refY="2.9" orient="auto">
      <path d="M0,0 L6.4,2.9 L0,5.8 z" style="fill:var(--accent-line)"/>
    </marker>
  </defs>

  <text x="540" y="24" text-anchor="middle" style="fill:var(--accent);font:650 13px var(--sans);letter-spacing:.2em">QUANTUM MATERIALS</text>
  <line x1="40" y1="36" x2="1040" y2="36" style="stroke:var(--accent-line);stroke-width:1"/>

  <g style="fill:var(--surface);stroke:var(--rule);stroke-width:1">
    <rect x="16"  y="56" width="158" height="102" rx="8"/>
    <rect x="194" y="56" width="158" height="102" rx="8"/>
    <rect x="372" y="56" width="158" height="102" rx="8"/>
    <rect x="550" y="56" width="158" height="102" rx="8"/>
    <rect x="728" y="56" width="158" height="102" rx="8"/>
    <rect x="906" y="56" width="158" height="102" rx="8"/>
  </g>

  <g style="fill:var(--ink);font:600 14px var(--sans)" text-anchor="middle">
    <text x="95"  y="86">Structure &amp;</text><text x="95"  y="103">chemistry</text>
    <text x="273" y="86">Symmetry &amp;</text><text x="273" y="103">electronic structure</text>
    <text x="451" y="86">Dirac states</text><text x="451" y="103">&amp; topology</text>
    <text x="629" y="86">Lattice geometry</text><text x="629" y="103">&amp; flat bands</text>
    <text x="807" y="86">Quantum</text><text x="807" y="103">geometry</text>
    <text x="985" y="86">Unconventional</text><text x="985" y="103">transport</text>
  </g>
  <g style="fill:var(--muted);font:400 11.5px var(--sans)" text-anchor="middle">
    <text x="95"  y="126">bonding, coordination,</text><text x="95"  y="139">interfaces, molecules</text>
    <text x="273" y="126">first-principles, Wannier,</text><text x="273" y="139">tight-binding models</text>
    <text x="451" y="126">nodal lines, Berry</text><text x="451" y="139">and Zak phases</text>
    <text x="629" y="126">kagome, line graphs,</text><text x="629" y="139">van Hove singularities</text>
    <text x="807" y="126">Berry curvature,</text><text x="807" y="139">quantum metric</text>
    <text x="985" y="126">nonlinear Hall, anomalous</text><text x="985" y="139">Hall and Nernst</text>
  </g>

  <g style="stroke:var(--accent);stroke-width:1.6;fill:none" marker-end="url(#mArrow)">
    <path d="M176 107 H190"/><path d="M354 107 H368"/><path d="M532 107 H546"/>
    <path d="M710 107 H724"/><path d="M888 107 H902"/>
  </g>

  <rect x="16" y="196" width="1048" height="40" rx="8" style="fill:var(--accent-soft);stroke:var(--accent-line);stroke-width:1"/>
  <text x="540" y="221" text-anchor="middle" style="fill:var(--accent-2);font:600 13.5px var(--sans)">Magnetism &amp; electronic correlations &mdash; reshaping symmetry, bands and response at every level</text>
  <g style="stroke:var(--accent-line);stroke-width:1.3;fill:none;stroke-dasharray:4 4" marker-end="url(#mArrowSoft)">
    <path d="M273 194 V166"/><path d="M451 194 V166"/><path d="M629 194 V166"/>
    <path d="M807 194 V166"/><path d="M985 194 V166"/>
  </g>

  <path d="M1040 158 V178 H95 V166" style="stroke:var(--accent-line);stroke-width:1.3;fill:none;stroke-dasharray:5 4" marker-end="url(#mArrowSoft)"/>
  <text x="540" y="264" text-anchor="middle" style="fill:var(--muted);font:italic 400 13px var(--serif)">what a measurement resolves decides which mechanism the next model has to contain</text>
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

FIG_TOPOLOGY = """<svg viewBox="0 0 360 240" role="img" aria-label="A closed nodal ring in a two-dimensional Brillouin zone. A one-dimensional cut passing through the ring carries a Zak phase of pi; a cut outside the ring carries zero. Beside it, a Dirac cone.">
  <defs>
    <marker id="tArr" markerWidth="8" markerHeight="8" refX="6.2" refY="2.8" orient="auto"><path d="M0,0 L6.2,2.8 L0,5.6 z" style="fill:var(--muted)"/></marker>
    <radialGradient id="tRing"><stop offset=".55" stop-color="#1c6b66" stop-opacity="0"/><stop offset="1" stop-color="#1c6b66" stop-opacity=".16"/></radialGradient>
  </defs>

  <rect x="34" y="34" width="192" height="146" rx="8" style="fill:none;stroke:var(--rule);stroke-width:1.2"/>
  <text x="44" y="52" style="fill:var(--muted);font:500 10px var(--sans)">Brillouin zone</text>

  <ellipse cx="118" cy="112" rx="46" ry="32" fill="url(#tRing)"/>
  <ellipse cx="118" cy="112" rx="46" ry="32" style="fill:none;stroke:var(--accent);stroke-width:2.4"/>
  <circle cx="118" cy="112" r="2" style="fill:var(--ink-2)"/>
  <text x="118" y="128" text-anchor="middle" style="fill:var(--muted);font:500 10px var(--sans)">&#915;</text>
  <text x="140" y="70" text-anchor="middle" style="fill:var(--accent-2);font:600 10.5px var(--sans)">nodal ring</text>

  <g style="stroke:var(--ink-2);stroke-width:1.1;opacity:.55;stroke-dasharray:4 3">
    <path d="M104 58 V170"/><path d="M196 58 V170"/>
  </g>
  <g style="fill:var(--accent)">
    <circle cx="104" cy="82" r="3.4"/><circle cx="104" cy="142" r="3.4"/>
  </g>
  <g style="stroke:var(--muted);stroke-width:1;fill:none" marker-end="url(#tArr)">
    <path d="M46 168 H70"/><path d="M46 168 V146"/>
  </g>
  <text x="74" y="171" style="fill:var(--muted);font:500 10px var(--sans)">k<tspan dy="2" font-size="8">x</tspan></text>
  <text x="40" y="146" text-anchor="end" style="fill:var(--muted);font:500 10px var(--sans)">k<tspan dy="2" font-size="8">y</tspan></text>

  <g style="stroke:var(--muted);stroke-width:1;fill:none" marker-end="url(#tArr)">
    <path d="M104 176 V194"/><path d="M196 176 V194"/>
  </g>
  <text x="104" y="211" text-anchor="middle" style="fill:var(--ink);font:600 12px var(--serif)">&#947; = &#960;</text>
  <text x="196" y="211" text-anchor="middle" style="fill:var(--ink);font:600 12px var(--serif)">&#947; = 0</text>
  <text x="104" y="226" text-anchor="middle" style="fill:var(--muted);font:400 9.5px var(--sans)">cut through the ring</text>
  <text x="196" y="226" text-anchor="middle" style="fill:var(--muted);font:400 9.5px var(--sans)">cut outside it</text>

  <g transform="translate(266,58)">
    <path d="M0 74 L26 24 L52 74" style="fill:none;stroke:var(--ink-2);stroke-width:1.3"/>
    <path d="M0 -26 L26 24 L52 -26" style="fill:none;stroke:var(--ink-2);stroke-width:1.3"/>
    <ellipse cx="26" cy="24" rx="26" ry="7" style="fill:none;stroke:var(--accent);stroke-width:1.2;opacity:.7"/>
    <circle cx="26" cy="24" r="2.6" style="fill:var(--accent)"/>
    <text x="26" y="94" text-anchor="middle" style="fill:var(--muted);font:400 10px var(--sans)">a point on the ring</text>
    <text x="26" y="107" text-anchor="middle" style="fill:var(--muted);font:400 10px var(--sans)">is a Dirac cone</text>
  </g>
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

FIG_MAGNETISM = """<svg viewBox="0 0 360 240" role="img" aria-label="Left: two magnetic sublattices with opposite spins sitting in environments related by a rotation. Right: the resulting spin splitting across the Brillouin zone, positive along one axis, negative along the other, with nodal lines along the diagonals">
  <defs>
    <radialGradient id="mUp"><stop offset="0" stop-color="#b4553f" stop-opacity=".72"/><stop offset=".72" stop-color="#b4553f" stop-opacity=".18"/><stop offset="1" stop-color="#b4553f" stop-opacity="0"/></radialGradient>
    <radialGradient id="mDn"><stop offset="0" stop-color="#1c6b66" stop-opacity=".72"/><stop offset=".72" stop-color="#1c6b66" stop-opacity=".18"/><stop offset="1" stop-color="#1c6b66" stop-opacity="0"/></radialGradient>
    <marker id="mUpTip" markerWidth="8" markerHeight="8" refX="4" refY="1.2" orient="auto"><path d="M0,6 L4,0 L8,6" style="fill:none;stroke:#b4553f;stroke-width:1.7"/></marker>
    <marker id="mDnTip" markerWidth="8" markerHeight="8" refX="4" refY="4.8" orient="auto"><path d="M0,0 L4,6 L8,0" style="fill:none;stroke:var(--accent);stroke-width:1.7"/></marker>
    <marker id="mRot" markerWidth="8" markerHeight="8" refX="6" refY="2.8" orient="auto"><path d="M0,0 L6,2.8 L0,5.6 z" style="fill:var(--muted)"/></marker>
  </defs>

  <!-- real space -->
  <rect x="26" y="42" width="126" height="126" rx="6" style="fill:none;stroke:var(--rule);stroke-width:1.2"/>
  <g transform="rotate(28 62 78)">
    <rect x="42" y="58" width="40" height="40" rx="5" style="fill:var(--paper-2);stroke:var(--rule);stroke-width:1.2"/>
  </g>
  <g transform="rotate(-28 116 132)">
    <rect x="96" y="112" width="40" height="40" rx="5" style="fill:var(--paper-2);stroke:var(--rule);stroke-width:1.2"/>
  </g>
  <path d="M62 94 V62" style="stroke:#b4553f;stroke-width:2.2;fill:none" marker-end="url(#mUpTip)"/>
  <path d="M116 114 V146" style="stroke:var(--accent);stroke-width:2.2;fill:none" marker-end="url(#mDnTip)"/>
  <path d="M84 92 A 34 34 0 0 1 102 116" style="fill:none;stroke:var(--muted);stroke-width:1.2;stroke-dasharray:3 3" marker-end="url(#mRot)"/>
  <text x="106" y="90" style="fill:var(--muted);font:italic 500 11px var(--serif)">rotation</text>
  <text x="89" y="188" text-anchor="middle" style="fill:var(--ink);font:600 10.5px var(--sans)">sublattices related by a rotation,</text>
  <text x="89" y="202" text-anchor="middle" style="fill:var(--ink);font:600 10.5px var(--sans)">not a translation or inversion</text>
  <text x="89" y="222" text-anchor="middle" style="fill:var(--muted);font:400 10px var(--sans)">net magnetisation zero</text>

  <!-- momentum space -->
  <rect x="206" y="42" width="132" height="132" rx="6" style="fill:none;stroke:var(--rule);stroke-width:1.2"/>
  <g style="stroke:var(--rule);stroke-width:1;stroke-dasharray:4 4">
    <path d="M206 42 L338 174"/><path d="M338 42 L206 174"/>
  </g>
  <ellipse cx="302" cy="108" rx="30" ry="17" fill="url(#mUp)"/>
  <ellipse cx="242" cy="108" rx="30" ry="17" fill="url(#mUp)"/>
  <ellipse cx="272" cy="72"  rx="17" ry="27" fill="url(#mDn)"/>
  <ellipse cx="272" cy="144" rx="17" ry="27" fill="url(#mDn)"/>
  <text x="308" y="112" text-anchor="middle" style="fill:#b4553f;font:700 12px var(--sans)">+&#916;</text>
  <text x="272" y="78"  text-anchor="middle" style="fill:var(--accent);font:700 12px var(--sans)">&#8722;&#916;</text>
  <circle cx="272" cy="108" r="2" style="fill:var(--ink-2)"/>
  <text x="266" y="120" text-anchor="end" style="fill:var(--muted);font:500 10px var(--sans)">&#915;</text>
  <text x="333" y="120" text-anchor="end" style="fill:var(--muted);font:500 10px var(--sans)">k<tspan dy="2" font-size="8">x</tspan></text>
  <text x="290" y="56" style="fill:var(--muted);font:500 10px var(--sans)">k<tspan dy="2" font-size="8">y</tspan></text>
  <text x="272" y="188" text-anchor="middle" style="fill:var(--ink);font:600 10.5px var(--sans)">spin splitting changes sign</text>
  <text x="272" y="202" text-anchor="middle" style="fill:var(--ink);font:600 10.5px var(--sans)">between directions</text>
  <text x="272" y="222" text-anchor="middle" style="fill:var(--muted);font:400 10px var(--sans)">&#916; = E<tspan dy="2" font-size="8">&#8593;</tspan><tspan dy="-2"> &#8722; E</tspan><tspan dy="2" font-size="8">&#8595;</tspan><tspan dy="-2">; nodes on the diagonals</tspan></text>
</svg>"""

FIG_CORRELATIONS = """<svg viewBox="0 0 360 240" role="img" aria-label="Top: the Dyson equation drawn as diagrams, with the full propagator equal to the bare propagator plus the bare propagator dressed by a self-energy. Bottom: the second-order self-energy, two interaction vertices joined by a particle-hole bubble.">
  <text x="24" y="30" style="fill:var(--muted);font:500 10px var(--sans)">Dyson equation</text>

  <g style="stroke:var(--ink-2);fill:none;stroke-width:2.6">
    <path d="M24 66 H80"/>
  </g>
  <path d="M46 60 L58 66 L46 72 z" style="fill:var(--ink-2)"/>
  <text x="94" y="71" text-anchor="middle" style="fill:var(--ink-2);font:600 15px var(--serif)">=</text>

  <g style="stroke:var(--ink-2);fill:none;stroke-width:1.4">
    <path d="M108 66 H164"/>
  </g>
  <path d="M130 61 L140 66 L130 71 z" style="fill:var(--ink-2)"/>
  <text x="178" y="71" text-anchor="middle" style="fill:var(--ink-2);font:600 15px var(--serif)">+</text>

  <g style="stroke:var(--ink-2);fill:none;stroke-width:1.4">
    <path d="M192 66 H219"/><path d="M249 66 H286"/>
  </g>
  <path d="M198 61 L208 66 L198 71 z" style="fill:var(--ink-2)"/>
  <path d="M262 61 L272 66 L262 71 z" style="fill:var(--ink-2)"/>
  <circle cx="234" cy="66" r="15" style="fill:var(--accent-soft);stroke:var(--accent);stroke-width:1.6"/>
  <text x="234" y="71" text-anchor="middle" style="fill:var(--accent-2);font:600 13px var(--serif)">&#931;</text>

  <text x="52"  y="92" text-anchor="middle" style="fill:var(--muted);font:italic 500 11.5px var(--serif)">G</text>
  <text x="136" y="92" text-anchor="middle" style="fill:var(--muted);font:italic 500 11.5px var(--serif)">G<tspan dy="2" font-size="8">0</tspan></text>
  <text x="234" y="94" text-anchor="middle" style="fill:var(--muted);font:400 9.5px var(--sans)">self-energy</text>

  <line x1="24" y1="112" x2="336" y2="112" style="stroke:var(--rule-soft);stroke-width:1"/>
  <text x="24" y="132" style="fill:var(--muted);font:500 10px var(--sans)">second-order self-energy</text>

  <ellipse cx="180" cy="158" rx="48" ry="19" style="fill:none;stroke:var(--accent);stroke-width:1.6"/>
  <path d="M172 135 L184 139 L172 143 z" style="fill:var(--accent)"/>
  <path d="M188 181 L176 177 L188 173 z" style="fill:var(--accent)"/>

  <g style="stroke:var(--gold);stroke-width:1.6;fill:none">
    <path d="M132 190 q5 -3.75 0 -7.5 q-5 -3.75 0 -7.5 q5 -3.75 0 -7.5 q-5 -3.75 0 -7.5"/>
    <path d="M228 190 q5 -3.75 0 -7.5 q-5 -3.75 0 -7.5 q5 -3.75 0 -7.5 q-5 -3.75 0 -7.5"/>
  </g>
  <text x="120" y="178" text-anchor="end" style="fill:var(--gold);font:italic 600 12.5px var(--serif)">U</text>
  <text x="240" y="178" style="fill:var(--gold);font:italic 600 12.5px var(--serif)">U</text>

  <path d="M64 192 H296" style="stroke:var(--ink-2);stroke-width:1.4;fill:none"/>
  <path d="M92 187 L102 192 L92 197 z" style="fill:var(--ink-2)"/>
  <path d="M258 187 L268 192 L258 197 z" style="fill:var(--ink-2)"/>
  <circle cx="132" cy="192" r="3.6" style="fill:var(--ink)"/>
  <circle cx="228" cy="192" r="3.6" style="fill:var(--ink)"/>

  <text x="180" y="222" text-anchor="middle" style="fill:var(--muted);font:400 10px var(--sans)">the loop is a particle&#8211;hole pair; U is the local interaction</text>
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

# Card figure for theme 04: the local d orbitals that carry the moment, and the
# self-energy through which the interaction between two electrons in them is felt.
FIG_ORBITAL_SE = """<svg viewBox="0 0 360 240" role="img" aria-label="Left: a d orbital with four alternating lobes holding two electrons of opposite spin, whose local Coulomb repulsion U is drawn as a wavy line. Right: the self-energy diagram, a propagator dressed by two interaction vertices joined by a particle-hole loop.">
  <text x="20" y="26" style="fill:var(--muted);font:500 10.5px var(--sans)">local d orbital</text>
  <text x="212" y="26" style="fill:var(--muted);font:500 10.5px var(--sans)">self-energy &#931;</text>
  <line x1="192" y1="14" x2="192" y2="212" style="stroke:var(--rule-soft);stroke-width:1"/>

  <!-- four-lobe d orbital; opposite lobes share the sign of the wavefunction -->
  <g transform="translate(92,94)" style="stroke-width:1.4">
    <ellipse cx="0" cy="-26" rx="13" ry="26" transform="rotate(45)"
             style="fill:var(--accent-soft);stroke:var(--accent)"/>
    <ellipse cx="0" cy="-26" rx="13" ry="26" transform="rotate(225)"
             style="fill:var(--accent-soft);stroke:var(--accent)"/>
    <ellipse cx="0" cy="-26" rx="13" ry="26" transform="rotate(135)"
             style="fill:var(--gold-soft);stroke:var(--gold)"/>
    <ellipse cx="0" cy="-26" rx="13" ry="26" transform="rotate(315)"
             style="fill:var(--gold-soft);stroke:var(--gold)"/>
    <circle cx="0" cy="0" r="2.8" style="fill:var(--ink);stroke:none"/>
    <text x="18"  y="-14" text-anchor="middle" style="fill:var(--accent-2);font:600 12px var(--sans);stroke:none">+</text>
    <text x="-18" y="-14" text-anchor="middle" style="fill:var(--gold);font:600 13px var(--sans);stroke:none">&#8722;</text>
  </g>

  <!-- two electrons of opposite spin in that shell, repelling through U -->
  <g style="stroke:var(--ink);stroke-width:1.8;fill:none;stroke-linecap:round">
    <path d="M64 186 V158"/><path d="M60 163 L64 157 L68 163"/>
    <path d="M120 158 V186"/><path d="M116 181 L120 187 L124 181"/>
  </g>
  <g style="stroke:var(--gold);stroke-width:1.6;fill:none">
    <path d="M72 172 q5 -4 10 0 q5 4 10 0 q5 -4 10 0 q5 4 10 0"/>
  </g>
  <text x="92" y="154" text-anchor="middle" style="fill:var(--gold);font:italic 600 12.5px var(--serif)">U</text>
  <text x="92" y="212" text-anchor="middle" style="fill:var(--muted);font:400 10px var(--sans)">two electrons, one shell</text>

  <!-- second-order self-energy: two U vertices joined by a particle-hole loop -->
  <ellipse cx="276" cy="112" rx="40" ry="17" style="fill:none;stroke:var(--accent);stroke-width:1.6"/>
  <path d="M269 91 L280 95 L269 99 z" style="fill:var(--accent)"/>
  <path d="M283 133 L272 129 L283 125 z" style="fill:var(--accent)"/>

  <g style="stroke:var(--gold);stroke-width:1.6;fill:none">
    <path d="M236 142 q4.5 -3.5 0 -7 q-4.5 -3.5 0 -7 q4.5 -3.5 0 -7"/>
    <path d="M316 142 q4.5 -3.5 0 -7 q-4.5 -3.5 0 -7 q4.5 -3.5 0 -7"/>
  </g>
  <text x="228" y="132" text-anchor="end" style="fill:var(--gold);font:italic 600 12px var(--serif)">U</text>
  <text x="326" y="132" style="fill:var(--gold);font:italic 600 12px var(--serif)">U</text>

  <path d="M208 144 H344" style="stroke:var(--ink-2);stroke-width:1.5;fill:none"/>
  <path d="M218 139 L228 144 L218 149 z" style="fill:var(--ink-2)"/>
  <path d="M320 139 L330 144 L320 149 z" style="fill:var(--ink-2)"/>
  <circle cx="236" cy="144" r="3.4" style="fill:var(--ink)"/>
  <circle cx="316" cy="144" r="3.4" style="fill:var(--ink)"/>
  <text x="276" y="212" text-anchor="middle" style="fill:var(--muted);font:400 10px var(--sans)">what dresses the propagator</text>
</svg>"""

CARD_FIGS = {"geometry": FIG_GEOMETRY, "kagome": FIG_KAGOME, "topology": FIG_TOPOLOGY,
             "magnetism": FIG_ORBITAL_SE, "materials": FIG_MATERIALS}

# ---- counts, computed from data/publications.json so nothing is typed twice ----
_DATA = json.loads((ROOT / "data" / "publications.json").read_text(encoding="utf-8"))
_PILLAR_KEYS = ["geometry", "kagome", "topology", "magnetism", "materials"]


def _tally(key):
    """(primary papers, cross-listed papers, under review, in preparation)."""
    prim = sum(1 for x in _DATA["peer_reviewed"] if x.get("primary") == key)
    cross = sum(1 for x in _DATA["peer_reviewed"]
                if key in x.get("tags", []) and x.get("primary") != key)
    ur = prep = 0
    for x in _DATA["preprints"]:
        if x.get("primary") != key:
            continue
        if str(x.get("journal", "")).lower().startswith("under review"):
            ur += 1
        else:
            prep += 1
    return prim, cross, ur, prep


def count_line(key):
    prim, cross, ur, prep = _tally(key)
    bits = ["%d paper%s" % (prim, "" if prim == 1 else "s")]
    if cross:
        bits.append("%d cross-listed" % cross)
    if ur:
        bits.append("%d under review" % ur)
    if prep:
        bits.append("%d in preparation" % prep)
    return " &middot; ".join(bits)


# key, number, title, central question, one- or two-sentence description
PILLARS = [
 ("geometry", "01", "Quantum geometry &amp; unconventional transport",
  "How does the geometry of quantum states show up in measurable electronic transport?",
  "Berry curvature, the Berry-curvature dipole and the quantum metric, and the transverse responses they "
  "produce: nonlinear Hall, anomalous Hall and Nernst. My current flagship direction, and the one where "
  "symmetry, gating, strain and chemistry become handles on transport."),

 ("kagome", "02", "Kagome, flat bands &amp; line-graph physics",
  "How does lattice geometry alone generate flat bands and singular electronic structure?",
  "Kagome and other line-graph lattices, where connectivity fixes where a flat band sits, and where "
  "quenched kinetic energy, van Hove singularities and geometrical frustration make topology, magnetism "
  "and interactions matter at once."),

 ("topology", "03", "Topology &amp; Dirac quantum matter",
  "How do lattice structure, symmetry and band connectivity generate Dirac states and topological phases?",
  "Dirac cones and nodal lines away from the honeycomb, Berry and Zak phases, and symmetry-protected "
  "electronic states. Exact real-space methods carry the same analysis into non-Hermitian lattices, with "
  "their exceptional points and skin modes."),

 ("magnetism", "04", "Magnetism &amp; correlated quantum matter",
  "How do magnetic order and electronic correlations reconstruct topology, quantum geometry and transport?",
  "Magnetic quantum materials, altermagnetism, anomalous Hall and Nernst response, and "
  "spin&ndash;orbit-coupled magnetism at oxide interfaces and in molecular systems. Correlated methods are "
  "now being brought to bear. The most rapidly expanding part of the programme."),

 ("materials", "05", "Materials discovery &amp; functional materials",
  "Which materials are worth calculating, and what makes their electronic structure useful?",
  "Predicting low-dimensional and molecular lattices from first principles and working out what their "
  "electrons do. With chemists, the same calculations follow through to energy storage, catalysis, "
  "sensing and optical response. The broadest and longest-running part of my record."),
]

CORE_KEYS = ["geometry", "kagome", "topology", "magnetism"]


def pillar_cards(keys, wide=False):
    """Every card is the same size. Theme 05 uses the wide variant: one full-width
    band, which reads as a different tier without being a different size."""
    out = []
    for key, n, title, question, blurb in PILLARS:
        if key not in keys:
            continue
        cls = "pillar-card" + (" pillar-card--wide" if wide else "")
        out.append("""        <a class="%s" href="research.html#%s">
          <span class="card-fig" aria-hidden="true">%s</span>
          <span class="n">%s</span>
          <h3>%s</h3>
          <p class="q">%s</p>
          <p>%s</p>
          <span class="count">%s</span>
          <span class="more">Read more &rarr;</span>
        </a>""" % (cls, key, CARD_FIGS[key], n, title, question, blurb, count_line(key)))
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
        <p class="keywords">Quantum materials &middot; quantum geometry &amp; transport &middot; kagome &amp; flat bands &middot; topology &amp; Dirac matter &middot; magnetism &amp; correlations</p>
        <p class="affil">Computational Quantum Materials, Institute for Theoretical Physics and Astrophysics<br>
          Julius-Maximilians-Universit&auml;t W&uuml;rzburg &middot; Cluster of Excellence <em>ct.qmat</em></p>
        <div class="lede">
          <p>I am a theoretical condensed-matter physicist working on quantum materials. I study how the
            geometry and topology of electronic states show up in measurable transport, how lattice
            geometry, symmetry and orbital structure give rise to Dirac states, flat bands and topological
            phases, and how magnetism and correlations reshape that physics.</p>
          <p>My work combines first-principles electronic-structure calculations and Wannier-based methods
            with symmetry-guided low-energy models, topological analysis, quantum transport and many-body
            approaches. Moving between realistic materials and minimal models lets me isolate microscopic
            mechanisms and connect them to experimentally accessible signatures.</p>
          <p>Much of this happens close to experiment. My projects often grow out of collaborations with
            experimentalists across disciplines, where theoretical prediction, synthesis and targeted
            measurement come together. I am drawn to problems where an unusual observation can be traced
            to a microscopic mechanism, or where a theoretical idea can be turned into a concrete
            prediction.</p>
        </div>
        <div class="actions">
          <a class="btn btn--primary" href="research.html">Research programme</a>
          <a class="btn" href="publications.html">Publications</a>
          <a class="btn" href="cv.html">CV</a>
          <a class="btn" href="mailto:arka.bandyopadhyay@uni-wuerzburg.de">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 7 10 6 10-6"/></svg>
            Email</a>
        </div>
      </div>
      <div class="portrait-col">
        <div class="portrait-frame">
          <img class="portrait" src="assets/img/portrait.jpg" width="560" height="627"
               alt="Arka Bandyopadhyay">
        </div>
        <div class="idlinks idlinks--stack">
          <a href="https://orcid.org/0000-0003-3386-4289" target="_blank" rel="noopener">ORCID</a>
          <a href="https://scholar.google.com/citations?user=EcM27vQAAAAJ" target="_blank" rel="noopener">Google Scholar</a>
          <a href="https://www.linkedin.com/in/arka-bandyopadhyay-315293381/" target="_blank" rel="noopener">LinkedIn</a>
          <a href="https://www.physik.uni-wuerzburg.de/en/cqm/team/postdocs/dr-arka-bandyopadhyay/" target="_blank" rel="noopener">Group page</a>
        </div>
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
      <h2>One programme, five entry points</h2>
      <p>Structure and chemistry set the symmetry and the orbitals; those decide which Dirac states and
        topological phases are possible; lattice geometry decides where flat bands sit; and where the
        geometry of the wavefunctions is strong enough, it shows up in what the material conducts.
        Magnetism and electronic correlations act on every level rather than at one point in the
        chain.</p>
      <p>This is the architecture, not a chronology. Different projects enter it at different places. The
        four themes below make up the core quantum-materials programme; the fifth is the broader materials
        work the rest grew out of.</p>
    </div>
    <figure class="map">
      <div class="map-scroll" tabindex="0" role="group" aria-label="Diagram: how the research programme moves from structure to measurement (scrollable)">%(map)s</div>
      <figcaption>The conceptual architecture, not a fixed sequence. Magnetism and electronic
        correlations are drawn as a band rather than a stage because they modify every level. The return
        arrow matters as much as the forward one: a measurement that resists explanation is often what
        selects the next model.</figcaption>
    </figure>
    <div class="tier-head" style="margin-top:var(--s6)">
      <h3>Core quantum-materials programme</h3>
      <p>Where my current questions are. Each count gives the papers for which that theme is the primary
        one, then the papers that sit primarily elsewhere but genuinely belong here too.</p>
    </div>
    <div class="pillars">
%(cards)s
    </div>

    <div class="tier-head tier-head--quiet">
      <h3>Interdisciplinary materials research</h3>
      <p>The broader materials work with chemists and materials scientists that the rest grew out of.</p>
    </div>
    <div class="pillars pillars--single">
%(cards5)s
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Selected work</p>
      <h2>Six papers</h2>
      <p>Six that give the clearest sense of what I do, weighted towards recent work. One line on each
        says what it establishes. The full record, including the larger body of materials work, is on the
        <a href="publications.html">publications page</a>.</p>
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
        topology, magnetism and related problems, particularly where theory can work closely with experiment
        or with materials design. A material worth calculating, an unexplained measurement, a question
        worth thinking through together, or simply a hello are all good reasons to write.</p>
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
          <a href="https://www.linkedin.com/in/arka-bandyopadhyay-315293381/" target="_blank" rel="noopener">LinkedIn</a>
          <a href="https://github.com/arkbndy" target="_blank" rel="noopener">GitHub</a>
          <a href="https://www.physik.uni-wuerzburg.de/en/cqm/team/postdocs/dr-arka-bandyopadhyay/" target="_blank" rel="noopener">Group page</a>
        </div>
      </div>
    </div>
  </div>
</section>
""" % {"map": MAP_SVG, "cards": pillar_cards(CORE_KEYS),
           "cards5": pillar_cards(["materials"], wide=True)}


# =========================================================================
#  Research
# =========================================================================
DETAIL = [
 dict(key="geometry", n="01",
   title="Quantum geometry &amp; unconventional transport",
   question="How does the geometry of quantum states show up in measurable electronic transport?",
   figs=[(FIG_GEOMETRY,
      "Berry curvature distributed asymmetrically over the Fermi surface. Weighted by the equilibrium "
      "occupation and summed over the zone, its momentum derivative gives the Berry-curvature dipole. "
      "Where the point group allows that dipole to be non-zero, a drive at &omega; produces a "
      "second-order transverse current with a rectified and a 2&omega; component, and no magnetic field "
      "is needed.")],
   thesis="Band energies are only half the story: the wavefunctions carry a geometry of their own, and "
          "it shows up directly in what a sample conducts.",
   body="""<p>Berry curvature and the quantum metric are the two halves of the quantum geometric tensor,
     and both leave signatures in transport. The nonlinear Hall effect is the clearest case. In a
     non-magnetic metal, time-reversal symmetry forbids a linear anomalous Hall response, but a
     second-order one survives when inversion symmetry is broken <em>and</em> the point group leaves a
     Berry-curvature dipole non-zero. That dipole is a Fermi-surface quantity, and its contribution scales
     with the scattering time. In magnetic metals that keep the product of inversion and time reversal, the
     picture changes. The Berry curvature is then forced to vanish by that symmetry, and what remains is a
     scattering-time-independent term set by the quantum-metric dipole, alongside disorder-induced
     contributions with their own scaling in the scattering time. Which mechanism applies in a given
     compound is the question, not a footnote.</p>
     <p>My own contribution has been the step from model Hamiltonians to specific materials, and the
     search for handles that change the geometry itself instead of the band filling: an electric field,
     strain, structural chirality, the choice of molecular building block.</p>""",
   highlights=[
     "In gated silicene, germanene and stanene the Berry-curvature dipole can be reversed in sign and changed in magnitude, turning a quantum-geometric quantity into something a device can set",
     "Strain does the same in layered phosphorene, and structural chirality gives an independent handle in tellurium-based systems",
     "Not every transverse response is geometric &mdash; refraction of carriers at an internal interface produces one with no Berry curvature at all",
     "Current work extends this to metal&ndash;organic frameworks, where the linker sets the lattice geometry, and to the field-tunable quantum metric in few-layer phosphorene",
   ],
   papers=[
     ("Non-linear Hall effects: mechanisms and materials", "Materials Today Electronics <strong>8</strong>, 100101 (2024) &middot; first and corresponding author"),
     ("Berry curvature dipole and its strain engineering in layered phosphorene", "Materials Today Electronics <strong>6</strong>, 100076 (2023) &middot; first and corresponding author"),
     ("Electrically switchable giant Berry curvature dipole in silicene, germanene and stanene", "2D Materials <strong>9</strong>, 035013 (2022) &middot; first author"),
     ("Refraction-induced transverse charge transport", "Phys. Rev. B <strong>114</strong>, 105406 (2026) &middot; corresponding author; Editors&rsquo; Suggestion"),
   ],
   methods="Wannier interpolation and quantum-geometric response theory (Wannier90, WannierBerri), "
           "symmetry analysis of the response tensors, semiclassical Boltzmann transport.",
   connections="Anomalous Hall and Nernst responses in magnetic systems belong here as much as to "
               "<a href=\"#magnetism\">magnetism and correlated quantum matter</a>. The link to "
               "<a href=\"#kagome\">kagome and flat-band physics</a> runs through the band touchings: "
               "the quadratic contact between a line-graph flat band and its neighbour is exactly the kind "
               "of near-degeneracy where Berry curvature and the quantum metric become large.",
   expt="With the Fudan group, band-structure input and Berry-phase analysis for quantum-oscillation "
        "measurements on tellurium nanowires; the oxide-heterostructure prediction is written so that a "
        "second-harmonic transport measurement can test it directly."),

 dict(key="kagome", n="02",
   title="Kagome, flat bands &amp; line-graph physics",
   question="How does lattice geometry alone generate flat bands and singular electronic structure?",
   figs=[(FIG_KAGOME,
      "Destructive interference on the kagome lattice quenches one band entirely. It is not isolated: it "
      "meets a dispersive band quadratically at the zone centre, while the two dispersive bands cross "
      "linearly at K. Which side of the pair the flat band lies on follows the sign of the hopping.")],
   thesis="Some lattices are generous: their connectivity alone tells you where the flat band is. What "
          "happens to it afterwards is where the physics starts.",
   body="""<p>A flat band has no dispersion, so kinetic energy is quenched and whatever else is present
     sets the scale: interactions, spin&ndash;orbit coupling, magnetic order. On the kagome lattice, the
     line graph of the honeycomb, the flat band comes from compact states living on the hexagonal
     plaquettes that interfere destructively at the apex sites. Its origin is therefore structural, not
     accidental. With uniform nearest-neighbour hopping the argument carries across the whole
     line-graph family; longer-range hopping and orbital multiplicity lift the flatness, which is exactly
     what makes the multi-orbital case worth studying.</p>
     <p>Kagome systems also carry Dirac points and van Hove singularities in the same band structure, so
     one lattice puts geometrical frustration, topology and correlations in the same place. It is a newer
     direction for me than the others, and the one I expect to grow.</p>""",
   highlights=[
     "Line-graph origin of the flat bands in coupled kagome lattices, and the condition on interlayer coupling for the separated band to stay topologically non-trivial",
     "Exact real-space decimation gives analytic conditions for flat bands in decorated lattices, evaluated at the flat-band energy",
     "With W&uuml;rzburg experimental groups, a minimal two-dimensional multi-orbital kagome model realised in a grown system and tested by photoemission (manuscript in preparation)",
     "Correlated methods, dynamical mean-field theory and the functional renormalisation group, are being applied to flat-band and kagome problems",
   ],
   papers=[
     ("Origin of flat bands and non-trivial topology in coupled kagome lattices", "Communications Physics <strong>8</strong>, 519 (2025) &middot; joint first author"),
     ("Non-Hermitian topology and flat bands via an exact real-space decimation scheme", "Phys. Rev. B <strong>110</strong>, 085431 (2024) &middot; joint first author"),
     ("Application of the real space decimation method in determining intricate electronic phases of matter: a review", "Phys. Chem. Chem. Phys. <strong>25</strong>, 9706 (2023)"),
   ],
   methods="Symmetry-adapted tight-binding models, line-graph and real-space decimation arguments, "
           "Wannier-based multi-orbital models, and DMFT (w2dynamics) and FRG (divERGe) for the "
           "interacting problem.",
   connections="A flat band is where interactions matter most, which is the entry to "
               "<a href=\"#magnetism\">magnetism and correlated quantum matter</a>; the touching points "
               "it cannot avoid are where the quantum geometry of "
               "<a href=\"#geometry\">theme 01</a> lives; and the decimation machinery is shared with "
               "<a href=\"#topology\">topology and Dirac quantum matter</a>.",
   expt="The multi-orbital kagome project is a direct experiment&ndash;theory collaboration: the model is "
        "built for the grown system and compared with photoemission, and the theory identifies which "
        "orbital content the measured bands require."),

 dict(key="topology", n="03",
   title="Topology &amp; Dirac quantum matter",
   question="How do lattice structure, symmetry and band connectivity generate Dirac states and topological phases?",
   figs=[(FIG_TOPOLOGY,
      "Dirac cones do not require a honeycomb. A nodal ring is located by the jump in the Zak phase, "
      "symmetry-quantised to 0 or &pi;, between a one-dimensional cut that passes through the ring and "
      "one that does not. Every point on the ring is itself a Dirac crossing."),
     (FIG_DECIMATION,
      "Decimation removes sites exactly, leaving an effective lattice with energy-dependent hoppings. "
      "Made non-Hermitian, its spectrum moves into the complex plane, and eigenvalues together with their "
      "eigenvectors can coalesce at exceptional points.")],
   thesis="Dirac physics is a statement about connectivity and symmetry, not about hexagons.",
   body="""<p>This is where my work started and it remains the backbone of the programme. Square,
     octagonal and acetylenic carbon and nitride lattices host anisotropic Dirac cones and nodal lines.
     What certifies them is a Zak phase along a one-dimensional cut, quantised to 0 or &pi; by inversion
     or chiral symmetry, and the Berry phase picked up around a node. Both depend on the symmetry of the
     lattice, not on any particular chemistry. Working out which lattices can support which phases, and how a
     structural or chemical change moves a system across a topological transition, is the recurring
     question.</p>
     <p>The same interest in exactly solvable structure led to real-space decimation, which eliminates
     sites exactly and turns a numerical parameter scan into conditions on energy-dependent effective
     hoppings.</p>""",
   sub=dict(title="Non-Hermitian topology",
     body="""<p>Decimation extends naturally to lattices with gain, loss or non-reciprocal hopping, where
       the two usual ingredients typically do different things: balanced gain and loss bring eigenvalues
       <em>and their eigenvectors</em> together at exceptional points, while non-reciprocal hopping gives
       the spectrum a non-zero point-gap winding and with it skin modes that pile up at a boundary. The
       method locates both analytically, including in decorated lattices that carry flat bands.</p>""",
     highlights=[
       "Exceptional points located analytically in a dice-lattice Haldane model",
       "Closed conditions for skin modes in decorated non-reciprocal lattices, and for non-Hermitian flat bands",
     ]),
   highlights=[
     "8-16-4 graphyne: a square-lattice two-dimensional nodal-line semimetal, with the nodes certified by a symmetry-quantised Zak phase",
     "S-graphene: two Dirac cones that survive distortion, in a non-hexagonal carbon lattice",
     "Berry-curvature dipoles tracked across a quantum spin Hall transition",
     "A review of the Su&ndash;Schrieffer&ndash;Heeger model, from the fundamentals through to its responses",
   ],
   papers=[
     ("8-16-4 graphyne: square-lattice two-dimensional nodal line semimetal with a nontrivial topological Zak index", "Phys. Rev. B <strong>103</strong>, 075137 (2021) &middot; first author"),
     ("The topology and robustness of two Dirac cones in S-graphene: a tight binding approach", "Scientific Reports <strong>10</strong>, 2502 (2020) &middot; first author"),
     ("Non-Hermiticity induced exceptional points and skin effect in the Haldane model on a dice lattice", "Phys. Rev. B <strong>107</strong>, 035403 (2023)"),
     ("Su&ndash;Schrieffer&ndash;Heeger model: from fundamentals to responses", "Int. J. Theor. Phys. <strong>64</strong>, 125 (2025)"),
   ],
   methods="Tight-binding and first-principles band structure, Zak and Berry phase calculation, "
           "topological invariants (Wannier90, WannierTools), real-space decimation and renormalisation, "
           "non-Hermitian formulations.",
   connections="The lattices studied here come out of <a href=\"#materials\">materials discovery</a>; the "
               "Berry phases that certify the phases are the same objects that drive transport in "
               "<a href=\"#geometry\">quantum geometry and transport</a>; the decimation methods carry over to the flat-band "
               "problems of <a href=\"#kagome\">kagome and flat-band physics</a>.",
   expt="Predicted Dirac and nodal-line materials are characterised in a form photoemission and transport "
        "can test: band velocities, node positions, and the response expected from each. None of these "
        "lattices has been synthesised yet, so the predictions stand as an invitation rather than a "
        "comparison."),

 dict(key="magnetism", n="04",
   title="Magnetism &amp; correlated quantum matter",
   question="How do magnetic order and electronic correlations reconstruct topology, quantum geometry and transport?",
   figs=[(FIG_MAGNETISM,
      "In an altermagnet the two magnetic sublattices are related by a rotation, and not by a translation "
      "or by inversion. The net magnetisation vanishes by symmetry, yet the bands acquire a spin "
      "splitting that is even in momentum and changes sign between directions. Drawn here for a "
      "d<sub><i>x</i>&sup2;&minus;<i>y</i>&sup2;</sub> form factor; other wave symmetries put the nodal "
      "directions elsewhere."),
     (FIG_INTERFACE,
      "Octahedral rotations propagate across a complex-oxide interface. The changed "
      "metal&ndash;oxygen&ndash;metal angles alter orbital overlap, bandwidth and crystal-field splitting "
      "in the layer above, and so the state it settles into."),
     (FIG_CORRELATIONS,
      "Correlations enter through the self-energy: the propagator that a measurement sees is the bare one "
      "dressed by &Sigma;. Dynamical mean-field theory computes &Sigma; on a site and solves for it "
      "self-consistently; the functional renormalisation group instead follows how the interaction itself "
      "changes as the energy scale is lowered. This part of the work is under way rather than "
      "concluded.")],
   thesis="Magnetic order and interactions decide which responses a material is allowed to have at all, "
          "not merely where its bands sit.",
   body="""<p>Magnetic order lowers symmetry, and what survives decides whether an anomalous Hall or
     Nernst response can appear at all, how spin and orbital degrees of freedom mix, and what an interacting
     flat band settles into. Altermagnetism is the instructive case: a collinear order whose net
     magnetisation vanishes by symmetry in the absence of spin&ndash;orbit coupling, yet whose sublattices
     are connected by a rotation, or by a rotation combined with a translation, and not by a translation or
     an inversion on their own. The splitting that results is even in momentum, carries a d-, g- or
     i-wave form factor, and changes sign between momentum directions with symmetry-enforced nodes. It
     also survives without spin&ndash;orbit coupling, which is what makes it a workable screening
     criterion.</p>
     <p>The same theme runs through complex-oxide interfaces, where a few degrees of octahedral tilt
     change the bandwidth and site symmetry and so the spin&ndash;orbit-entangled state the layer settles
     into, and through molecular magnets, where ligand-field chemistry sets the spin state. Correlations
     are the newest addition: dynamical mean-field theory and the functional renormalisation group are
     being applied to flat-band and kagome problems. That work is a direction rather than a result.</p>""",
   highlights=[
     "Altermagnetism restated as chemical and symmetry criteria that can guide the search for candidate compounds",
     "Anomalous Hall and Nernst responses tuned by composition in magnetic Weyl semimetals",
     "Octahedral tilt coupling related to spin&ndash;orbit reconstruction at a complex-oxide interface, published in <em>Nature Communications</em>",
     "Spin-state switching in manganese(III) complexes, where ligand-field chemistry and crystal packing set the magnetic state",
     "Antiferromagnetic tunnel barriers giving discrete tunnelling-magnetoresistance states, and magnon&ndash;electromagnon anomalies in rare-earth-doped BiFeO<sub>3</sub> films, both under review",
   ],
   papers=[
     ("Altermagnetism from the viewpoint of chemistry", "Chem. Soc. Rev. (2026)"),
     ("An unconventional pathway to correlate the octahedral tilt coupling and spin&ndash;orbit reconstruction at oxide interfaces", "Nature Communications <strong>17</strong>, 332 (2026) &middot; joint first author"),
     ("Tunable anomalous Hall and Nernst effects in magnetic Weyl semimetals Co<sub>2&minus;<i>x</i></sub>Cr<sub><i>x</i></sub>MnGe", "J. Phys.: Condens. Matter <strong>37</strong>, 365702 (2025)"),
     ("Spin-state switching: chemical modulation and the impact of intermolecular interactions in manganese(III) complexes", "Dalton Trans. <strong>52</strong>, 11335 (2023)"),
   ],
   methods="Spin-polarised and non-collinear DFT with DFT+<em>U</em> and spin&ndash;orbit coupling, "
           "magnetic symmetry analysis, Wannier-based anomalous transport coefficients, and dynamical "
           "mean-field theory (w2dynamics) and functional renormalisation group (divERGe).",
   connections="Anomalous Hall and Nernst responses are quantum-geometric quantities, so this thread "
               "shares its transport machinery with <a href=\"#geometry\">quantum geometry and transport</a>; correlated flat "
               "bands connect it to <a href=\"#kagome\">kagome and flat-band physics</a>; and the altermagnetism criteria "
               "are chemical, which links it to <a href=\"#materials\">materials discovery</a>.",
   expt="This is where theory is most tightly constrained by measurement. Working with groups performing "
        "X-ray spectroscopy, photoemission and transport, we established a route from the measured tilt "
        "coupling at an oxide interface to the reconstructed spin&ndash;orbit-entangled state, with "
        "calculations done for the structure that was actually grown. The experiments are my "
        "collaborators&rsquo; work; my contribution is the electronic-structure modelling and its "
        "interpretation."),

 dict(key="materials", n="05",
   title="Materials discovery &amp; functional materials",
   question="Which materials are worth calculating, and what makes their electronic structure useful?",
   figs=[(FIG_MATERIALS,
      "Square-and-octagon carbon networks: Dirac physics away from the honeycomb, and the starting point "
      "for much of the later work on topology and transport.")],
   thesis="Someone has to propose the material. For a large part of my record, that has been the work.",
   body="""<p>This is the broadest and longest-running part of my publication record, and the origin of
     the rest. Beginning in my doctoral work, this line has predicted two-dimensional carbon, silicon and
     nitride networks built from squares, octagons and acetylenic links and worked out what their
     electrons do &mdash; some of it led by me, some by colleagues whose electronic-structure analysis I
     contributed to. Alongside the Dirac and nodal-line results, the same first-principles workflow,
     pointed at a device figure of merit rather than an invariant, produced a long interdisciplinary
     thread with chemists and materials scientists.</p>
     <p>It is not where my current questions lie, but it is what taught me to judge whether a predicted
     material is worth an experimentalist&rsquo;s time, and it is the reason chemical and structural
     control appears everywhere else in the programme.</p>""",
   subgroups=[
     ("Low-dimensional &amp; Dirac materials",
      "Graphene allotropes and graphynes, silicene and germanene, dumbbell C<sub>3</sub>NX networks; "
      "structural and chemical engineering of Dirac states."),
     ("Energy &amp; functional materials",
      "Lithium adsorption and battery anodes, supercapacitive and redox materials, photocatalysis and "
      "energy storage, largely with synthetic chemists."),
     ("Sensing, optical &amp; electronic functionality",
      "Gas sensing, optical and nonlinear-optical response, thermoelectrics, negative differential "
      "resistance and rectification via Green-function transport."),
   ],
   highlights=[
     "Two reviews survey this field and have each received an IOP India Top Cited Paper Award; I led the first and was second author on the second",
     "A nodal flexible-surface three-dimensional carbon network, proposed as a lithium anode; a cover article in <em>Journal of Materials Chemistry C</em>",
     "The dumbbell C<sub>3</sub>NX family (X = C, Si, Ge) and its quasi-one-dimensional derivatives",
     "Negative differential resistance, rectification and gas sensing, computed from first principles with non-equilibrium Green-function (NEGF) transport",
   ],
   papers=[
     ("A review on role of tetra-rings in the graphene systems and their possible applications", "Rep. Prog. Phys. <strong>83</strong>, 056501 (2020) &middot; first author; IOP India Top Cited Paper Award"),
     ("Emerging properties of carbon based 2D material beyond graphene", "J. Phys.: Condens. Matter <strong>34</strong>, 053001 (2022) &middot; IOP India Top Cited Paper Award"),
     ("Intriguing topological signatures in a newly predicted family of dumbbell C<sub>3</sub>NX (X = C, Si, Ge) and its quasi-one-dimensional derivatives", "Applied Materials Today <strong>40</strong>, 102360 (2024)"),
   ],
   methods="Density-functional theory (Quantum ESPRESSO, VASP, SIESTA, OpenMX; Gaussian and ORCA for "
           "molecular systems), phonon and stability analysis, optical response, and NEGF device transport.",
   connections="The lattices proposed here are the ones whose topology is analysed in "
               "<a href=\"#topology\">topology and Dirac quantum matter</a>, and the chemical control demonstrated here is what "
               "makes the interfaces and molecular systems of <a href=\"#magnetism\">magnetism and correlated quantum matter</a> "
               "tractable.",
   expt="Predictions are reported with the quantities a synthetic or measurement group needs: stability, "
        "expected spectra, device characteristics. Several of these projects were carried out directly "
        "with chemists, and the redox-polymer and lithium-storage work began on their side of the "
        "problem."),
]


def pillar_sections(keys):
    out = []
    for d in DETAIL:
        if d["key"] not in keys:
            continue
        figs = "\n".join(
            '        <figure><div class="box">%s</div><figcaption>%s</figcaption></figure>' % (svg, cap)
            for svg, cap in d["figs"])
        hl = "\n".join("          <li>%s</li>" % h for h in d["highlights"])
        pp = "\n".join('            <li>%s <span class="venue">%s</span></li>' % (t, v)
                       for t, v in d["papers"])

        sub = ""
        if d.get("sub"):
            sb = d["sub"]
            sub_hl = "\n".join("            <li>%s</li>" % h for h in sb["highlights"])
            sub = """
        <div class="subtheme">
          <h3>%s</h3>
          %s
          <ul class="highlights">
%s
          </ul>
        </div>""" % (sb["title"], sb["body"], sub_hl)

        groups = ""
        if d.get("subgroups"):
            rows = "\n".join(
                '            <div><h3 class="sg">%s</h3><p>%s</p></div>' % (t, b) for t, b in d["subgroups"])
            groups = """
        <div class="subgroups">
%s
        </div>""" % rows

        out.append("""    <article class="pillar" id="%(key)s">
      <div>
        <span class="n">%(n)s</span>
        <h2>%(title)s</h2>
        <p class="pillar-count">%(count)s</p>
        <p class="question">%(question)s</p>
        <p class="thesis">%(thesis)s</p>
        %(body)s%(sub)s%(groups)s
        <ul class="highlights">
%(hl)s
        </ul>
        <div class="keypapers">
          <h3>Representative papers</h3>
          <ul>
%(pp)s
          </ul>
        </div>
        <dl class="meta-pairs">
          <dt>Methods</dt><dd>%(methods)s</dd>
          <dt>With experiment</dt><dd>%(expt)s</dd>
          <dt>Connects to</dt><dd>%(connections)s</dd>
        </dl>
      </div>
      <div class="figure">
%(figs)s
      </div>
    </article>""" % dict(key=d["key"], n=d["n"], title=d["title"], thesis=d["thesis"],
                         question=d["question"], count=count_line(d["key"]), body=d["body"],
                         sub=sub, groups=groups, hl=hl, pp=pp, figs=figs,
                         methods=d["methods"], expt=d["expt"], connections=d["connections"]))
    return "\n".join(out)


# =========================================================================
#  Collaborators
# =========================================================================
GS = "https://scholar.google.com/citations?user=%s"

# One list, ordered by how long and how closely we have worked together.
PEOPLE = [
 ("Prof. Awadhesh Narayan", "Solid State and Structural Chemistry Unit, Indian Institute of Science", GS % "kHOQvgQAAAAJ", "GS"),
 ("Prof. Ronny Thomale", "Theoretical Physics, Universit&auml;t W&uuml;rzburg", GS % "RJ8vWeoAAAAJ", "GS"),
 ("Prof. Giorgio Sangiovanni", "Theoretical Physics, Universit&auml;t W&uuml;rzburg", GS % "SeCV78UAAAAJ", "GS"),
 ("Prof. Debnarayan Jana", "Physics, University of Calcutta", GS % "43SR0GsAAAAJ", "GS"),
 ("Prof. Diptiman Sen", "Centre for High Energy Physics, Indian Institute of Science", GS % "4TZdOPIAAAAJ", "GS"),
 ("Prof. Ralph Claessen", "Experimental Physics, Universit&auml;t W&uuml;rzburg", None, None),
 ("Prof. Claudia Felser", "Director, Max Planck Institute for Chemical Physics of Solids, Dresden", None, None),

 ("Prof. Ajit C. Balram", "Institute of Mathematical Sciences, Chennai", GS % "T1vffdAAAAAJ", "GS"),
 ("Prof. Sujit Das", "Materials Research Centre, Indian Institute of Science", GS % "L8j4ld8AAAAJ", "GS"),
 ("Prof. Satish Patil", "Polymer Chemistry, Indian Institute of Science", GS % "Tyfe7LcAAAAJ", "GS"),
 ("Prof. Abhishake Mondal", "Solid State and Structural Chemistry Unit, Indian Institute of Science", GS % "wZkA5s0AAAAJ", "GS"),
 ("Prof. Bhagwati Prasad", "Department of Materials Engineering, Indian Institute of Science", None, None),
 ("Prof. Naga Phani B. Aetukuri", "Solid State and Structural Chemistry Unit, Indian Institute of Science", GS % "Te2ZTYgAAAAJ", "GS"),
 ("Prof. N. Ravishankar", "Materials Research Centre, Indian Institute of Science", GS % "v5FUPi4AAAAJ", "GS"),
 ("Prof. S. B. Krupanidhi", "Materials Research Centre, Indian Institute of Science", None, None),

 ("Prof. T. Venky Venkatesan", "Center for Quantum Research and Technology, University of Oklahoma", GS % "brdyAZ4AAAAJ", "GS"),
 ("Prof. J&ouml;rg Sch&auml;fer", "Experimental Physics, Universit&auml;t W&uuml;rzburg", None, None),
 ("Prof. Simon Moser", "Experimental Physics, Ruhr-Universit&auml;t Bochum", None, None),
 ("Prof. Hendrik Bentmann", "Center for Quantum Spintronics, NTNU Trondheim", None, None),
 ("Prof. Rajeev Ahuja", "Uppsala University", GS % "OqyvV_oAAAAJ", "GS"),
 ("Prof. Faxian Xiu", "Department of Physics, Fudan University", GS % "0QMB9ZUAAAAJ", "GS"),
 ("Prof. Domenico Di Sante", "University of Bologna", GS % "EVyjBUYAAAAJ", "GS"),
 ("Prof. Carmine Ortix", "University of Salerno", None, None),
 ("Prof. Udo Schwingenschl&ouml;gl", "Materials Science and Applied Physics, King Abdullah University of Science and Technology (KAUST)", None, None),

 ("Prof. Arunava Chakrabarti", "Physics, University of Kalyani", None, None),
 ("Prof. Md. Mohi Uddin", "Physics, Chittagong University of Engineering &amp; Technology", None, None),
 ("Prof. Mohamad Akbar Ali", "Chemistry, Khalifa University, Abu Dhabi", None, None),
 ("Dr. N. V. R. Nulakani", "Department of Chemistry, Khalifa University, Abu Dhabi", GS % "7N4Ovi4AAAAJ", "GS"),
 ("Dr. Dirtha Sanyal", "Variable Energy Cyclotron Centre, Kolkata", GS % "ReD7dBWTPcwC", "GS"),
 ("Dr. Moritz Hoesch", "PETRA III, Deutsches Elektronen-Synchrotron (DESY), Hamburg", None, None),
 ("Dr. Manuel Valvidares", "ALBA Synchrotron Light Source, Barcelona", None, None),
 ("Dr. Jayjit Kumar Dey", "Deutsches Elektronen-Synchrotron (DESY), Hamburg", None, None),
 ("Dr. Anju Ahlawat", "Institute of Sciences, SAGE University, Indore", None, None),
 ("Dr. Arup Kumar Mandal", "UGC-DAE Consortium for Scientific Research, Indore", "https://www.researchgate.net/scientific-contributions/Arup-Kumar-Mandal-2241663034", "WEB"),
 ("Dr. Basanta Roul", "Central Research Laboratory, Bharat Electronics, Bengaluru", None, None),
 ("Prof. Subhadip Nath", "Physics, Krishnagar Government College", None, None),
 ("Dr. Atanu Nandy", "Acharya Prafulla Chandra College", None, None),
 ("Dr. Debaprem Bhattacharya", "Government College of Engineering &amp; Textile Technology, Berhampore", None, None),
 ("Dr. Susmita Jana", "Indian Institute of Technology Madras", GS % "QYQhf_YAAAAJ", "GS"),
 ("Dr. Mainak Dey Sarkar", "Department of Physics, University of Calcutta", None, None),
 ("Dr. Suman Chowdhury", "Department of Physics &amp; Astrophysics, University of Delhi", GS % "Do_yowMAAAAJ", "GS"),
 ("Dr. Deep Mondal", "Indian Institute of Technology Bombay", None, None),
 ("Dr. Anumita Bose", "Condensed Matter Theory, SISSA, Trieste", GS % "-iKh_vkAAAAJ", "GS"),
 ("Dr. Ayan Banerjee", "Max Planck Institute for the Science of Light, Erlangen", GS % "AGIwnYEAAAAJ", "GS"),
 ("Dr. Subarna Das", "Max Planck Institute for Chemical Physics of Solids, Dresden", GS % "2EW9jrsAAAAJ", "GS"),
 ("Dr. Enze Zhang", "School of Physics, Nanjing University", None, None),
 ("Dr. Lennart Klebl", "Institute for Theoretical Physics and Astrophysics, Universit&auml;t W&uuml;rzburg", None, None),
 ("Dr. Manish Verma", "Computational Quantum Materials, Universit&auml;t W&uuml;rzburg", None, None),
 ("Dr. Bing Liu", "Experimental Physics IV, Universit&auml;t W&uuml;rzburg", None, None),
 ("Dr. Nesta Benno Joseph", "Solid State and Structural Chemistry Unit, Indian Institute of Science", GS % "3cfchUgAAAAJ", "GS"),
 ("Dr. Ronika Sarkar", "Department of Physics, Indian Institute of Science", GS % "WuKSGW8AAAAJ", "GS"),
 ("Dr. Supriya Ghosal", "Theoretical Sciences Unit, JNCASR, Bengaluru", None, None),
 ("Dr. Nayana Devaraj", "Solid State and Structural Chemistry Unit, Indian Institute of Science", GS % "IHa8JmMAAAAJ", "GS"),
 ("Dr. Md Afsar Reja", "Solid State and Structural Chemistry Unit, Indian Institute of Science", GS % "Tn5Njx8AAAAJ", "GS"),
 ("Dr. Sarbajit Mazumdar", "Theoretical Physics I, Universit&auml;t W&uuml;rzburg", GS % "1YhOrqwAAAAJ", "GS"),
 ("Dr. Amrita Mukherjee", "Tata Institute of Fundamental Research, Mumbai", None, None),
]


def collaborators():
    rows = []
    for name, aff, url, badge in PEOPLE:
        link = ('<a class="gs" href="%s" target="_blank" rel="noopener" title="%s profile for %s">%s</a>'
                % (url, "Google Scholar" if badge == "GS" else "Homepage", name, badge)) if url else ''
        where = '<span class="where">%s</span>' % aff if aff else ''
        rows.append('        <li><div><span class="who">%s</span>%s</div>%s</li>'
                    % (name, where, link))
    return '      <ul class="collab-list">\n%s\n      </ul>' % "\n".join(rows), len(PEOPLE)


COLLAB_HTML, COLLAB_N = collaborators()

RESEARCH = """
<section class="section">
  <div class="wrap">
    <div class="section-head section-head--lede">
      <p class="eyebrow">Research</p>
      <h1>Quantum materials, from structure to signal</h1>
      <p>In a quantum material the lattice does more than hold the atoms in place. The crystal structure
        fixes which orbitals lie near the Fermi level, and the symmetry of that structure decides which
        responses are allowed to be non-zero at all.</p>
      <p>Spin&ndash;orbit coupling and magnetic order then reshape the bands, and where a band is flat,
        interactions set the remaining energy scale. My work follows that chain in specific compounds, and
        asks which transport or spectroscopic signature tells one mechanism from another.</p>
      <p>That chain runs through more than one discipline, and in practice the influence tends to run one
        way. Chemical environment, bonding, coordination geometry and interfaces set the local symmetry,
        the orbital content and the strength of spin&ndash;orbit and magnetic coupling, and those in turn
        shape the topology, the quantum geometry and the transport.</p>
      <p>An oxide interface changes octahedral tilts; the choice of molecular linker sets a lattice
        geometry directly. That is why a substantial part of my work is done with chemists and materials
        scientists: they hold the practical handles on electronic structure.</p>
      <p>Several projects run in close collaboration with experimental groups, and the exchange goes both
        ways. In one direction, first-principles calculations and microscopic models are used to interpret
        measured transport and spectra and to identify which mechanism is responsible. In the other, a
        model points to a signature, a parameter regime or a candidate compound that can then be tested.
        The transport, photoemission, X-ray spectroscopy and synthesis behind the work below are my
        collaborators&rsquo;; what I bring is the electronic structure and the modelling that connects it
        to what they measure.</p>
    </div>

    <div class="evolution prose">
      <h2>How the questions evolved</h2>
      <p>My work began with a fairly concrete question: how lattice geometry and chemical structure
        determine the electronic properties of low-dimensional materials. Predicting square, octagonal and
        acetylenic carbon and nitride lattices led naturally to Dirac states and to the invariants that
        certify them, and from there to Berry-phase physics: first as a way of labelling a phase, then as
        something a sample can be made to show.</p>
      <p>Once the Berry phase is a physical quantity rather than a label, how it is distributed across the
        Brillouin zone begins to matter, and that distribution is what the Berry curvature and the quantum
        metric describe. Quantum geometry and unconventional transport grew out of that step.</p>
      <p>Kagome and line-graph systems arrived from a different direction and turned out to be a
        complementary setting, where connectivity alone restructures the spectrum and puts flat bands,
        Dirac points and van Hove singularities in one place. My current research increasingly asks how
        magnetic order and electronic correlations modify these geometric and topological responses. None
        of this was planned in advance; each step was the question the previous answer raised.</p>
    </div>

    <nav class="theme-nav" aria-label="Jump to a research theme">
      <a href="#geometry"><span>01</span> Quantum geometry &amp; transport</a>
      <a href="#kagome"><span>02</span> Kagome &amp; flat bands</a>
      <a href="#topology"><span>03</span> Topology &amp; Dirac matter</a>
      <a href="#magnetism"><span>04</span> Magnetism &amp; correlations</a>
      <a href="#materials"><span>05</span> Materials discovery</a>
    </nav>

    <div class="tier-head">
      <h2>Core quantum-materials programme</h2>
    </div>

%(sections)s

    <div class="tier-head tier-head--quiet">
      <h2>Interdisciplinary materials research</h2>
      <p>The broader materials work, done largely with chemists and materials scientists.</p>
    </div>

%(sections5)s
  </div>
</section>

<section class="section section--tint" id="collaborators">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">People</p>
      <h2>Collaborators &amp; co-authors</h2>
      <p>My research has benefited enormously from long-standing, active collaboration across theory,
        experiment and materials synthesis. Very little of it would exist without the groups I have been
        part of: in W&uuml;rzburg, at the Indian Institute of Science and at the University of Calcutta. I
        am grateful to have worked inside them. Listed below are co-authors on published work and
        colleagues I am currently working with.</p>
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
""" % {"sections": pillar_sections(CORE_KEYS), "sections5": pillar_sections(["materials"]),
       "collab": COLLAB_HTML}


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
      <p>Newest first; the numbers stay fixed as the list grows. Each entry links to its DOI, and to
        arXiv where one exists. Review articles and one book chapter are included and labelled as such.
        A paper that belongs to two themes appears under both filters. &ldquo;Joint first author&rdquo;
        is the paper&rsquo;s own equal-contribution designation. Also on
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
        <button class="chip" type="button" data-tag="kagome" aria-pressed="false">Kagome &amp; flat bands</button>
        <button class="chip" type="button" data-tag="topology" aria-pressed="false">Topology &amp; Dirac matter</button>
        <button class="chip" type="button" data-tag="magnetism" aria-pressed="false">Magnetism &amp; correlations</button>
        <button class="chip" type="button" data-tag="materials" aria-pressed="false">Materials discovery</button>
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
      <p>Theoretical condensed-matter physicist. Quantum materials: quantum geometry and unconventional
        transport, kagome and flat-band physics, topology and Dirac matter, magnetism and electronic
        correlations.</p>
      <div class="actions" style="margin-top:var(--s3)">
        <a class="btn btn--primary" href="publications.html">Publication record</a>
        <a class="btn" href="research.html">Research programme</a>
      </div>
    </div>

    <div class="cv-block">
      <h2>Research profile</h2>
      <p>I am a theoretical condensed-matter physicist working on quantum materials. My research examines
        how the electronic structure and symmetry of a material give rise to topological, quantum-geometric
        and magnetic properties, and how these are reflected in transport and spectroscopic measurements.
        Four directions carry most of the current work: quantum geometry and unconventional transport;
        kagome, flat-band and line-graph physics; topology and Dirac quantum matter, including its
        non-Hermitian extension; and magnetism with electronic correlations, which is expanding fastest.
        A broader, longer-running line in materials discovery underpins all of them.</p>
      <p>The methods are first-principles electronic structure and Wannier-based modelling,
        symmetry-adapted tight-binding Hamiltonians, quantum transport and, increasingly, many-body
        approaches, applied to specific compounds rather than idealised Hamiltonians. The work also
        meets materials chemistry and computational materials science, where bonding, coordination geometry,
        interfaces and molecular design give concrete control over electronic structure. Several projects
        run with experimental groups &mdash; I do not perform experiments myself; the calculations serve
        either to identify the mechanism behind a measurement or to propose a signature worth testing.</p>
    </div>

    <div class="cv-block">
      <h2>Positions</h2>
      <div class="cv-entry">
        <div><span class="what">Postdoctoral Researcher</span><br><span class="where">Computational Quantum Materials, with Prof. Giorgio Sangiovanni and Prof. Ronny Thomale &middot; Julius-Maximilians-Universit&auml;t W&uuml;rzburg, Germany</span></div>
        <div class="when">Oct 2024 &ndash; present</div>
        <p class="detail">Topological and quantum-geometric electronic structure of quantum materials,
          within the DFG Cluster of Excellence <em>ct.qmat</em>: kagome
          and flat-band systems, anomalous and nonlinear transport, and magnetic quantum materials, treated
          with first-principles and Wannier-based models alongside correlated methods. Several projects are
          carried out jointly with theory and experimental groups in W&uuml;rzburg. Independent direction:
          quantum-geometric transport in metal&ndash;organic frameworks, where the choice of linker sets the
          lattice geometry. Mentoring of junior researchers.</p>
      </div>
      <div class="cv-entry">
        <div><span class="what">Visiting Researcher</span><br><span class="where">With Prof. Awadhesh Narayan, Solid State and Structural Chemistry Unit &middot; Indian Institute of Science, Bengaluru</span></div>
        <div class="when">May &ndash; Sep 2024</div>
        <p class="detail">First-principles electronic-structure calculations on magnetic complex-oxide
          interfaces, carried out with the experimental groups measuring them.</p>
      </div>
      <div class="cv-entry">
        <div><span class="what">IISc-IoE Postdoctoral Fellow</span><br><span class="where">With Prof. Awadhesh Narayan, Solid State and Structural Chemistry Unit &middot; Indian Institute of Science, Bengaluru</span></div>
        <div class="when">May 2022 &ndash; May 2024</div>
        <p class="detail">Berry-curvature dipoles and nonlinear Hall response, flat bands in coupled kagome
          lattices, and non-Hermitian topology treated by exact real-space decimation. Started the
          collaborations with oxide-interface and transport experimentalists from which several later papers
          came.</p>
      </div>
      <div class="cv-entry">
        <div><span class="what">Research Associate</span><br><span class="where">With Prof. Awadhesh Narayan, Solid State and Structural Chemistry Unit &middot; Indian Institute of Science, Bengaluru</span></div>
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
          Supervisor: Prof. Debnarayan Jana. Thesis submitted 4 May 2021.</p>
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
    </div>

    <div class="cv-block">
      <h2>Fellowships &amp; funding</h2>
      <div class="cv-entry">
        <div><span class="what">Position funded by the DFG Cluster of Excellence <em>ct.qmat</em></span><br><span class="where">Complexity and Topology in Quantum Matter, Universit&auml;t W&uuml;rzburg &mdash; group funding, not held by me as principal investigator</span></div>
        <div class="when">2024 &ndash; present</div>
      </div>
      <div class="cv-entry">
        <div><span class="what">Institute of Eminence (IoE) Postdoctoral Fellowship</span><br><span class="where">Indian Institute of Science, Bengaluru &mdash; competitive two-year personal fellowship</span></div>
        <div class="when">2022 &ndash; 2024</div>
      </div>
      <div class="cv-entry">
        <div><span class="what">UGC Junior Research Fellowship</span><br><span class="where">through the CSIR-UGC National Eligibility Test, All India Rank 85; held with a University Research Fellowship at the University of Calcutta</span></div>
        <div class="when">2019 &ndash; 2021</div>
      </div>
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
        Calcutta on theoretical and computational projects: problem formulation, numerical implementation,
        analysis, and the preparation of manuscripts and presentations. Several of these
        projects led to co-authored publications.</p>
      <p class="detail" style="margin-top:var(--s2)">Courses I am prepared to teach:</p>
      <div class="tool-grid" style="margin-top:var(--s2)">
        <div class="tool-card"><h3>Core</h3><p>Quantum Mechanics &middot; Condensed Matter and Solid State Physics &middot; Mathematical Physics &middot; Computational Physics.</p></div>
        <div class="tool-card"><h3>Advanced</h3><p>Electronic Structure Theory and DFT &middot; Topological Quantum Matter &middot; Quantum Transport &middot; Low-Dimensional and Semiconductor Physics &middot; Introduction to Many-Body Physics.</p></div>
      </div>
    </div>

    <div class="cv-block">
      <h2>Professional service</h2>
      <p>Referee for <em>Physical Review Letters</em>, <em>Physical Review B</em>, <em>New Journal of
        Physics</em>, <em>Communications Physics</em>, <em>2D Materials</em> and other journals; IOP
        Trusted Reviewer. Session Chair, NAMMA Psi-k Workshop and Conference (2023). Invited lecturer and
        resource person at national workshops.</p>
    </div>

    <div class="cv-block">
      <h2>Technical expertise</h2>
      <div class="tool-grid">
        <div class="tool-card"><h3>Electronic structure</h3><p>Density-functional theory including DFT+<em>U</em>, spin&ndash;orbit coupling and collinear and non-collinear magnetism.<br><span class="codes">Quantum ESPRESSO &middot; VASP &middot; SIESTA &middot; OpenMX; Gaussian and ORCA for molecular and coordination complexes</span></p></div>
        <div class="tool-card"><h3>Wannier &amp; quantum-geometric response</h3><p>Wannier interpolation; Berry curvature, Berry-curvature dipole and quantum metric; anomalous, nonlinear and thermoelectric transport coefficients; topological invariants.<br><span class="codes">Wannier90 &middot; WannierBerri &middot; WannierTools</span></p></div>
        <div class="tool-card"><h3>Model Hamiltonians &amp; transport</h3><p>Symmetry-adapted tight-binding models; real-space decimation and renormalisation; equilibrium and non-equilibrium Green-function (NEGF) quantum transport; non-Hermitian formulations.</p></div>
        <div class="tool-card"><h3>Many-body methods</h3><p>Dynamical mean-field theory (w2dynamics) and the functional renormalisation group (divERGe), applied to flat-band and kagome problems. An expanding part of the work.</p></div>
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
             "working on quantum materials: quantum geometry and unconventional transport, kagome and "
             "flat-band physics, topology and Dirac matter, magnetism and electronic correlations.")

written = [
  page("index.html", "Arka Bandyopadhyay — Quantum Materials Theory", DESC_HOME, HOME,
       "index.html", JSONLD),
  page("research.html", "Research — Arka Bandyopadhyay",
       "Research programme: quantum geometry and unconventional transport; kagome, flat bands and "
       "line-graph physics; topology and Dirac quantum matter; magnetism and correlated quantum matter; "
       "and materials discovery with functional materials.", RESEARCH, "research.html"),
  page("publications.html", "Publications — Arka Bandyopadhyay",
       "Complete publication record of Arka Bandyopadhyay: peer-reviewed papers with DOI and arXiv "
       "links, filterable by research theme, plus manuscripts under review and in preparation.", PUBLICATIONS,
       "publications.html"),
  page("news.html", "News — Arka Bandyopadhyay",
       "Recent papers, awards, invited talks and research visits.", NEWS, "news.html"),
  page("cv.html", "CV — Arka Bandyopadhyay",
       "Curriculum vitae of Arka Bandyopadhyay, theoretical condensed-matter physicist working on "
       "quantum materials: positions, doctorate, awards, invited talks, teaching and expertise.",
       CV, "cv.html"),
]
print("built:", ", ".join(written))
print("collaborators:", COLLAB_N)
