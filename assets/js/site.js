/* ============================================================
   Arka Bandyopadhyay — site behaviour
   Theme toggle, mobile nav, and rendering of news + publications
   from the JSON files in /data.
   ============================================================ */
(function () {
  'use strict';

  /* ---------- Theme ---------- */
  var root = document.documentElement;
  try {
    var saved = localStorage.getItem('theme');
    if (saved === 'dark' || saved === 'light') root.setAttribute('data-theme', saved);
  } catch (e) { /* storage unavailable */ }

  document.addEventListener('click', function (e) {
    var btn = e.target.closest('.theme-toggle');
    if (!btn) return;
    var isDark = root.getAttribute('data-theme')
      ? root.getAttribute('data-theme') === 'dark'
      : window.matchMedia('(prefers-color-scheme: dark)').matches;
    var next = isDark ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('theme', next); } catch (err) { /* ignore */ }
  });

  /* ---------- Mobile nav ---------- */
  var navToggle = document.querySelector('.nav-toggle');
  var navLinks = document.getElementById('nav-links');
  if (navToggle && navLinks) {
    navToggle.addEventListener('click', function () {
      var open = navToggle.getAttribute('aria-expanded') === 'true';
      navToggle.setAttribute('aria-expanded', String(!open));
      navLinks.hidden = open;
    });
    var mq = window.matchMedia('(max-width: 820px)');
    var sync = function () {
      navLinks.hidden = mq.matches && navToggle.getAttribute('aria-expanded') !== 'true';
    };
    mq.addEventListener ? mq.addEventListener('change', sync) : mq.addListener(sync);
    sync();
  }

  /* ---------- Header shadow on scroll ---------- */
  var header = document.querySelector('.site-header');
  if (header) {
    var onScroll = function () { header.classList.toggle('scrolled', window.scrollY > 8); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---------- Helpers ---------- */
  var ME = 'Arka Bandyopadhyay';

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function boldMe(authors) {
    return esc(authors).replace(ME, '<span class="me">' + ME + '</span>');
  }

  function venue(p) {
    var s = '<em>' + esc(p.journal) + '</em>';
    if (p.volume) s += ' <strong>' + esc(p.volume) + '</strong>';
    if (p.pages) s += ', ' + esc(p.pages);
    if (p.year) s += ' (' + esc(p.year) + ')';
    return s;
  }

  function links(p) {
    var out = '';
    if (p.doi) {
      out += '<a class="taglink" href="https://doi.org/' + esc(p.doi) + '" target="_blank" rel="noopener">DOI</a>';
    }
    if (p.arxiv) {
      out += '<a class="taglink" href="https://arxiv.org/abs/' + esc(p.arxiv) + '" target="_blank" rel="noopener">arXiv:' + esc(p.arxiv) + '</a>';
    }
    if (p.role) out += '<span class="badge badge-role">' + esc(p.role) + '</span>';
    if (p.award) out += '<span class="badge badge-award">' + esc(p.award) + '</span>';
    if (p.note) out += '<span class="badge badge-note">' + esc(p.note) + '</span>';
    return out;
  }

  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'];

  function prettyDate(d) {
    var parts = String(d).split('-');
    var y = parts[0], m = parseInt(parts[1], 10);
    return (m && MONTHS[m - 1] ? MONTHS[m - 1] + ' ' : '') + y;
  }

  /* ---------- News ---------- */
  var newsEl = document.getElementById('news-list');
  if (newsEl) {
    var limit = parseInt(newsEl.dataset.limit || '0', 10);
    fetch('data/news.json')
      .then(function (r) { return r.json(); })
      .then(function (items) {
        var list = limit > 0 ? items.slice(0, limit) : items;
        newsEl.innerHTML = list.map(function (n) {
          var body = n.link
            ? n.text + ' <a class="taglink" href="' + esc(n.link) + '" target="_blank" rel="noopener">Read</a>'
            : n.text;
          return '<li class="news-item"><time datetime="' + esc(n.date) + '">' +
            esc(prettyDate(n.date)) + '</time><div class="body">' + body + '</div></li>';
        }).join('');
      })
      .catch(function () { newsEl.innerHTML = '<li class="empty">News could not be loaded.</li>'; });
  }

  /* ---------- Publications ---------- */
  var selEl = document.getElementById('selected-pubs');
  var pubEl = document.getElementById('pub-list');
  var preEl = document.getElementById('preprint-list');

  if (selEl || pubEl || preEl) {
    fetch('data/publications.json')
      .then(function (r) { return r.json(); })
      .then(function (data) {
        if (selEl) renderSelected(data.peer_reviewed.filter(function (p) { return p.selected; }));
        if (preEl) renderPreprints(data.preprints);
        if (pubEl) initFullList(data.peer_reviewed);
      })
      .catch(function () {
        [selEl, pubEl, preEl].forEach(function (el) {
          if (el) el.innerHTML = '<p class="empty">Publications could not be loaded.</p>';
        });
      });
  }

  function renderSelected(items) {
    selEl.innerHTML = items.map(function (p) {
      var href = p.doi ? 'https://doi.org/' + p.doi : (p.arxiv ? 'https://arxiv.org/abs/' + p.arxiv : null);
      var title = href
        ? '<a href="' + esc(href) + '" target="_blank" rel="noopener">' + esc(p.title) + '</a>'
        : esc(p.title);
      return '<article class="selected-item">' +
        '<h3>' + title + '</h3>' +
        (p.summary ? '<p class="why">' + esc(p.summary) + '</p>' : '') +
        '<p class="meta">' + venue(p) + (p.role ? ' &middot; ' + esc(p.role) : '') +
        (p.award ? ' &middot; ' + esc(p.award) : '') + '</p>' +
        '</article>';
    }).join('');
  }

  function renderPreprints(items) {
    preEl.innerHTML = items.map(function (p, i) {
      return '<article class="pub">' +
        '<div class="idx">' + toRoman(items.length - i) + '</div>' +
        '<div><div class="title">' + esc(p.title) + '</div>' +
        '<div class="authors">' + boldMe(p.authors) + '</div>' +
        '<div class="venue"><em>' + esc(p.journal) + '</em> (' + esc(p.year) + ')</div>' +
        '<div class="links">' + links(p) + '</div></div></article>';
    }).join('');
  }

  function toRoman(n) {
    var map = [[10, 'X'], [9, 'IX'], [5, 'V'], [4, 'IV'], [1, 'I']], out = '';
    map.forEach(function (m) { while (n >= m[0]) { out += m[1]; n -= m[0]; } });
    return out;
  }

  function initFullList(all) {
    var search = document.getElementById('pub-search');
    var chips = Array.prototype.slice.call(document.querySelectorAll('.chip[data-tag]'));
    var countEl = document.getElementById('pub-count');
    var active = 'all';

    function draw() {
      var q = (search && search.value || '').trim().toLowerCase();
      var items = all.filter(function (p) {
        if (active !== 'all' && (!p.tags || p.tags.indexOf(active) === -1)) return false;
        if (!q) return true;
        return (p.title + ' ' + p.authors + ' ' + p.journal + ' ' + p.year).toLowerCase().indexOf(q) !== -1;
      });

      countEl.textContent = items.length + ' of ' + all.length +
        ' peer-reviewed publication' + (all.length === 1 ? '' : 's');

      if (!items.length) {
        pubEl.innerHTML = '<p class="empty">No publications match that filter.</p>';
        return;
      }

      // Descending numbering across the *whole* record, so a paper keeps its number when filtered.
      var numberOf = {};
      all.forEach(function (p, i) { numberOf[p.id] = all.length - i; });

      var years = [], byYear = {};
      items.forEach(function (p) {
        if (!byYear[p.year]) { byYear[p.year] = []; years.push(p.year); }
        byYear[p.year].push(p);
      });

      pubEl.innerHTML = years.map(function (y) {
        return '<div class="year-group"><div class="year-label">' + esc(y) + '</div>' +
          byYear[y].map(function (p) {
            return '<article class="pub">' +
              '<div class="idx">' + numberOf[p.id] + '</div>' +
              '<div><div class="title">' + esc(p.title) + '</div>' +
              '<div class="authors">' + boldMe(p.authors) + '</div>' +
              '<div class="venue">' + venue(p) + '</div>' +
              '<div class="links">' + links(p) + '</div></div></article>';
          }).join('') + '</div>';
      }).join('');
    }

    if (search) search.addEventListener('input', draw);
    chips.forEach(function (c) {
      c.addEventListener('click', function () {
        active = c.dataset.tag;
        chips.forEach(function (o) { o.setAttribute('aria-pressed', String(o === c)); });
        draw();
      });
    });
    draw();
  }
})();
