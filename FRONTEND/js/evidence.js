const $ = (s, r = document) => r.querySelector(s);
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const mem = {};
const store = { get(k) { try { return localStorage.getItem(k) } catch (e) { return mem[k] || null } }, set(k, v) { try { localStorage.setItem(k, v) } catch (e) { mem[k] = v } } };
const VX = {
  esc, $,
  caseId: () => new URLSearchParams(location.search).get('case') || store.get('vertx_case'),
  setCase: id => store.set('vertx_case', id),
  toast(m) { const t = $('#toast'); t.textContent = m; t.classList.add('on'); clearTimeout(VX._t); VX._t = setTimeout(() => t.classList.remove('on'), 3200) },
  col: l => `var(--${l})`,
  lvBadge: l => `<span class="badge ${l}">${l}</span>`,
  bar: (v, l) => `<div class="bar" style="--c:var(--${l || (v >= 65 ? 'high' : v >= 35 ? 'medium' : 'low')})"><i style="width:${v}%"></i></div>`,
  needCase(el) { el.innerHTML = `<div class="card">No case selected yet. <a href="analyze.html">Analyze some evidence</a> first.</div>`; }
};
(function nav() {
  const id = VX.caseId(), q = id ? `?case=${id}` : '', cur = location.pathname.split('/').pop();
  const L = [['home', 'Home'], ['analyze', 'Analyze'], ['results', 'Results'], ['evidence', 'Evidence'], ['report', 'Report']];
  document.body.insertAdjacentHTML('afterbegin', `<header class="nav"><a class="brand" href="home.html"><img src="../assets/icons/logo.svg" alt="">TRUTHLENS</a><nav>${L.map(([f, t]) => `<a href="${f}.html${f === 'home' || f === 'analyze' ? '' : q}" class="${cur === f + '.html' ? 'on' : ''}">${t}</a>`).join('')}</nav></header>`);
  document.body.insertAdjacentHTML('beforeend', `<div id="toast"></div><canvas id="bg"></canvas><footer>A detection score is an indicator, not a final verdict. Keep originals and have a human review the findings.</footer>`);
  const c = $('#bg'), x = c.getContext('2d'); let W, H; const P = Array.from({ length: 45 }, () => ({ x: Math.random(), y: Math.random(), vx: (Math.random() - .5) * 2e-4, vy: (Math.random() - .5) * 2e-4 }));
  const fit = () => { W = c.width = innerWidth; H = c.height = innerHeight }; fit(); addEventListener('resize', fit);
  (function f() { x.clearRect(0, 0, W, H); P.forEach(p => { p.x = (p.x + p.vx + 1) % 1; p.y = (p.y + p.vy + 1) % 1 }); x.strokeStyle = 'rgba(34,230,255,.12)'; x.fillStyle = 'rgba(34,230,255,.5)';
    P.forEach((a, i) => { x.fillRect(a.x * W, a.y * H, 2, 2); for (let j = i + 1; j < P.length; j++) { const b = P[j], d = Math.hypot((a.x - b.x) * W, (a.y - b.y) * H); if (d < 150) { x.beginPath(); x.moveTo(a.x * W, a.y * H); x.lineTo(b.x * W, b.y * H); x.stroke() } } }); requestAnimationFrame(f) })();
})();
