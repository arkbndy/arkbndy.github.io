/* ==========================================================================
   Arka Bandyopadhyay — site behaviour
   Theme, navigation, and rendering of news / publications from /data.
   Every number shown on the site is derived from data/publications.json.
   ========================================================================== */
(function () {
  'use strict';

  var ME = 'Arka Bandyopadhyay';
  var root = document.documentElement;

  /* ---------- Theme ---------- */
  try {
    var saved = localStorage.getItem('theme');
    if (saved === 'dark' || saved === 'light') root.setAttribute('data-theme', saved);
  } catch (e) { /* storage unavailable */ }

  document.addEventListener('click', function (e) {
    var btn = e.target.closest('.theme-toggle');
    if (!btn) return;
    var dark = root.getAttribute('data-theme')
      ? root.getAttribute('data-theme') === 'dark'
      : window.matchMedia('(prefers-color-scheme: dark)').matches;
    var next = dark ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    btn.setAttribute('aria-label', next === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
    try { localStorage.setItem('theme', next); } catch (err) { /* ignore */ }
  });

  /* ---------- Mobile navigation ---------- */
  var toggle = document.querySelector('.nav-toggle');
  var links = document.getElementById('nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      links.hidden = open;
    });
    var mq = window.matchMedia('(max-width: 860px)');
    var sync = function () { links.hidden = mq.matches && toggle.getAttribute('aria-expanded') !== 'true'; };
    mq.addEventListener ? mq.addEventListener('change', sync) : mq.addListener(sync);
    sync();
  }

  /* ---------- Header shadow ---------- */
  var header = document.querySelector('.site-header');
  if (header) {
    var onScroll = function () { header.classList.toggle('is-scrolled', window.scrollY > 8); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---------- Helpers ---------- */
  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  function boldMe(a) { return esc(a).replace(ME, '<span class="me">' + ME + '</span>'); }

  function venue(p) {
    var s = '<em>' + esc(p.journal) + '</em>';
    if (p.volume) s += ' <strong>' + esc(p.volume) + '</strong>';
    if (p.pages) s += ', ' + esc(p.pages);
    if (p.year) s += ' (' + esc(p.year) + ')';
    return s;
  }
  function links_(p) {
    var out = '';
    if (p.doi) out += '<a class="tag" href="https://doi.org/' + esc(p.doi) + '" target="_blank" rel="noopener">DOI</a>';
    if (p.arxiv) out += '<a class="tag" href="https://arxiv.org/abs/' + esc(p.arxiv) + '" target="_blank" rel="noopener">arXiv:' + esc(p.arxiv) + '</a>';
    if (p.role) out += '<span class="tag tag--role">' + esc(p.role) + '</span>';
    if (p.award) out += '<span class="tag tag--award">' + esc(p.award) + '</span>';
    if (p.note) out += '<span class="tag tag--note">' + esc(p.note) + '</span>';
    return out;
  }

  var MONTHS = ['January','February','March','April','May','June',
                'July','August','September','October','November','December'];
  function prettyDate(d) {
    var b = String(d).split('-'), m = parseInt(b[1], 10);
    return (MONTHS[m - 1] ? MONTHS[m - 1] + ' ' : '') + b[0];
  }
  function toRoman(n) {
    var map = [[10,'X'],[9,'IX'],[5,'V'],[4,'IV'],[1,'I']], out = '';
    map.forEach(function (m) { while (n >= m[0]) { out += m[1]; n -= m[0]; } });
    return out;
  }

  /* ---------- News ---------- */
  var newsEl = document.querySelector('[data-news]');
  if (newsEl) {
    var limit = parseInt(newsEl.getAttribute('data-news') || '0', 10);
    fetch('data/news.json').then(function (r) { return r.json(); }).then(function (items) {
      var list = limit > 0 ? items.slice(0, limit) : items;
      newsEl.innerHTML = list.map(function (n) {
        var body = n.link
          ? n.text + ' <a class="tag" href="' + esc(n.link) + '" target="_blank" rel="noopener">Read</a>'
          : n.text;
        return '<li><time datetime="' + esc(n.date) + '">' + esc(prettyDate(n.date)) + '</time>' +
               '<div class="body">' + body + '</div></li>';
      }).join('');
    }).catch(function () { newsEl.innerHTML = '<li class="empty">News could not be loaded.</li>'; });
  }

  /* ---------- Publications ---------- */
  var selEl = document.getElementById('selected-pubs');
  var pubEl = document.getElementById('pub-list');
  var preEl = document.getElementById('preprint-list');
  var recEl = document.getElementById('record');

  if (selEl || pubEl || preEl || recEl) {
    fetch('data/publications.json').then(function (r) { return r.json(); }).then(function (d) {
      if (recEl) renderRecord(d);
      if (selEl) renderSelected(d.peer_reviewed.filter(function (p) { return p.selected; }), d.pillars);
      if (preEl) renderPreprints(d.preprints);
      if (pubEl) initList(d.peer_reviewed);
    }).catch(function () {
      [selEl, pubEl, preEl].forEach(function (el) {
        if (el) el.innerHTML = '<p class="empty">Publications could not be loaded.</p>';
      });
    });
  }

  /* Numbers computed from the data, so they can never drift out of date. */
  function renderRecord(d) {
    var pr = d.peer_reviewed;
    var lead = pr.filter(function (p) { return /first/i.test(p.role || ''); }).length;
    var corr = pr.filter(function (p) { return /corresponding/i.test(p.role || ''); }).length;
    recEl.innerHTML =
      '<div><b>' + pr.length + '</b><span>peer-reviewed publications</span></div>' +
      '<div><b>' + lead + '</b><span>as first or joint-first author</span></div>' +
      '<div><b>' + corr + '</b><span>as corresponding author</span></div>' +
      '<div><b>' + d.preprints.length + '</b><span>manuscripts under review or in preparation</span></div>';
  }

  function renderSelected(items, pillars) {
    selEl.innerHTML = items.map(function (p) {
      var href = p.doi ? 'https://doi.org/' + p.doi : (p.arxiv ? 'https://arxiv.org/abs/' + p.arxiv : null);
      var title = href ? '<a href="' + esc(href) + '" target="_blank" rel="noopener">' + esc(p.title) + '</a>' : esc(p.title);
      var label = pillars && pillars[p.tags[0]] ? pillars[p.tags[0]].split(/[,&]/)[0].trim() : '';
      return '<article class="selected-item">' +
        '<h3>' + title + '</h3>' +
        (p.summary ? '<p class="why">' + esc(p.summary) + '</p>' : '') +
        '<p class="meta">' + (label ? '<span class="pill">' + esc(label) + '</span>' : '') +
        venue(p) + (p.role ? ' &middot; ' + esc(p.role) : '') + (p.award ? ' &middot; ' + esc(p.award) : '') +
        '</p></article>';
    }).join('');
  }

  function renderPreprints(items) {
    preEl.innerHTML = items.map(function (p, i) {
      return '<article class="pub"><div class="idx">' + toRoman(items.length - i) + '</div><div>' +
        '<div class="title">' + esc(p.title) + '</div>' +
        '<div class="authors">' + boldMe(p.authors) + '</div>' +
        '<div class="venue"><em>' + esc(p.journal) + '</em> (' + esc(p.year) + ')</div>' +
        '<div class="links">' + links_(p) + '</div></div></article>';
    }).join('');
  }

  function initList(all) {
    var search = document.getElementById('pub-search');
    var chips = Array.prototype.slice.call(document.querySelectorAll('.chip[data-tag]'));
    var countEl = document.getElementById('pub-count');
    var active = 'all';

    // descending numbering over the whole record, so a paper keeps its number when filtered
    var numberOf = {};
    all.forEach(function (p, i) { numberOf[p.id] = all.length - i; });

    function draw() {
      var q = ((search && search.value) || '').trim().toLowerCase();
      var items = all.filter(function (p) {
        if (active !== 'all' && p.tags.indexOf(active) === -1) return false;
        if (!q) return true;
        return (p.title + ' ' + p.authors + ' ' + p.journal + ' ' + p.year).toLowerCase().indexOf(q) !== -1;
      });

      countEl.textContent = items.length === all.length
        ? all.length + ' peer-reviewed publications'
        : items.length + ' of ' + all.length + ' peer-reviewed publications';

      if (!items.length) { pubEl.innerHTML = '<p class="empty">No publications match that filter.</p>'; return; }

      var years = [], byYear = {};
      items.forEach(function (p) {
        if (!byYear[p.year]) { byYear[p.year] = []; years.push(p.year); }
        byYear[p.year].push(p);
      });

      pubEl.innerHTML = years.map(function (y) {
        return '<section class="year-group" aria-label="Publications from ' + esc(y) + '">' +
          '<h3 class="year-label">' + esc(y) + '</h3>' +
          byYear[y].map(function (p) {
            return '<article class="pub"><div class="idx">' + numberOf[p.id] + '</div><div>' +
              '<div class="title">' + esc(p.title) + '</div>' +
              '<div class="authors">' + boldMe(p.authors) + '</div>' +
              '<div class="venue">' + venue(p) + '</div>' +
              '<div class="links">' + links_(p) + '</div></div></article>';
          }).join('') + '</section>';
      }).join('');
    }

    if (search) search.addEventListener('input', draw);
    chips.forEach(function (c) {
      c.addEventListener('click', function () {
        active = c.getAttribute('data-tag');
        chips.forEach(function (o) { o.setAttribute('aria-pressed', String(o === c)); });
        draw();
      });
    });
    draw();
  }

  /* ---------- Footer year ---------- */
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();
