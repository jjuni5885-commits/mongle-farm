// ===== 몽글 포털판 다국어 층: 한국어 원문을 화면에 나가는 순간 영어로 (사전 MG_DICT, 한국어 사용자는 그대로) =====
(function () {
  var HAN = /[ᄀ-ᇿㄱ-ㆎ가-힣]/;
  function pick() {
    try { var q = /[?&#]lang=([a-z]{2})/.exec(location.search + location.hash); if (q) return q[1] === 'ko' ? 'ko' : 'en'; } catch (e) { }
    var L = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language || 'en'];
    for (var i = 0; i < L.length; i++) if (String(L[i] || '').toLowerCase().indexOf('ko') === 0) return 'ko';
    return 'en';
  }
  var LANG = pick(); window.MG_LANG = LANG; window.__mgMissing = []; window.mgT = function (s) { return s; };
  document.documentElement.lang = LANG;
  if (LANG === 'ko') { document.title = '몽글 목장 대탈출'; return; }
  var EX = new Map(), TP = [];
  function tpl(k, v) {
    var names = [], lit = 0;
    var re = k.replace(/\{(\d|s)\}|[^{]+|\{/g, function (m, p) { if (p != null) { names.push(p); return p === 's' ? '(.+?)' : '([+-]?\\d+(?:\\.\\d+)?)'; } lit += m.length; return m.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); });
    return { re: new RegExp('^' + re + '$'), names: names, v: v, lit: lit };
  }
  MG_DICT.forEach(function (r) { if (/\{(\d|s)\}/.test(r[0])) TP.push(tpl(r[0], r[1])); else EX.set(r[0], r[1]); });
  TP.sort(function (a, b) { return b.lit - a.lit; });
  var cache = new Map(), miss = {};
  function tr0(core, d) {
    var v = EX.get(core); if (v != null) return v;
    for (var i = 0; i < TP.length; i++) {
      var t = TP[i], m = t.re.exec(core); if (!m) continue;
      var vals = {}, ok = true;
      for (var j = 0; j < t.names.length && ok; j++) { var n = t.names[j], g = m[j + 1]; if (n === 's') { var sub = d < 3 ? tr0(g.trim(), d + 1) : null; if (sub == null) ok = false; else vals.s = sub; } else vals[n] = g; }
      if (ok) return t.v.replace(/\{(\d|s)\}/g, function (q, n) { return vals[n] != null ? vals[n] : q; });
    }
    return null;
  }
  function tr(s) {
    if (typeof s !== 'string' || !HAN.test(s)) return s;
    var c = cache.get(s); if (c !== undefined) return c;
    var m = /^(\s*)([\s\S]*?)(\s*)$/.exec(s), v = tr0(m[2], 0), out;
    if (v == null) { if (!miss[m[2]]) { miss[m[2]] = 1; window.__mgMissing.push(m[2]); } out = s; } else out = m[1] + v + m[3];
    if (cache.size > 3000) cache.clear(); cache.set(s, out); return out;
  }
  window.mgT = tr;
  document.title = 'Mongle Farm Escape';
  function txt(n) { var p = n.parentNode; if (!p || p.nodeName === 'SCRIPT' || p.nodeName === 'STYLE') return; var s = n.data; if (!HAN.test(s)) return; var v = tr(s); if (v !== s) n.data = v; }
  var AT = ['aria-label', 'placeholder', 'title'];
  function attrs(el) { if (!el.getAttribute) return; for (var i = 0; i < AT.length; i++) { var s = el.getAttribute(AT[i]); if (s && HAN.test(s)) { var v = tr(s); if (v !== s) el.setAttribute(AT[i], v); } } }
  function walk(root) {
    if (root.nodeType === 3) { txt(root); return; }
    if (root.nodeType !== 1 && root.nodeType !== 11) return;
    if (root.nodeName === 'SCRIPT' || root.nodeName === 'STYLE') return;
    if (root.nodeType === 1) attrs(root);
    var w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT), t; while ((t = w.nextNode())) txt(t);
    if (root.querySelectorAll) root.querySelectorAll('[aria-label],[placeholder],[title]').forEach(attrs);
  }
  walk(document.body);
  new MutationObserver(function (list) { list.forEach(function (m) { if (m.type === 'characterData') txt(m.target); else if (m.type === 'attributes') attrs(m.target); else m.addedNodes.forEach(walk); }); })
    .observe(document.body, { childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: AT });
  // 캔버스 글자(간판, 효과 글자): 번역문이 길어지면 캔버스 폭 안에 들어가게 maxWidth를 줌
  var P = CanvasRenderingContext2D.prototype, f = P.fillText, sk = P.strokeText, ms = P.measureText;
  function draw(fn, ctx, a) {
    var t = a[0];
    if (typeof t === 'string' && HAN.test(t)) { var v = tr(t); if (v !== t) return fn.call(ctx, v, a[1], a[2], a.length > 3 && a[3] != null ? a[3] : ctx.canvas.width * 0.8); }
    return fn.apply(ctx, a);
  }
  P.fillText = function () { return draw(f, this, arguments); };
  P.strokeText = function () { return draw(sk, this, arguments); };
  P.measureText = function (t) { return ms.call(this, typeof t === 'string' && HAN.test(t) ? tr(t) : t); };
})();
