(async () => {
  const m = $('#view'), id = VX.caseId(); if (!id) return VX.needCase(m);
  let d; try { d = await VXAPI.results(id) } catch (e) { return m.innerHTML = `<div class="card">${VX.esc(e.message)}</div>` }
  const o = d.correlation.overall, G = d.correlation.graph;
  const graph = G.nodes.length > 1 ? (() => {
    const n = G.nodes.length, P = G.nodes.map((_, i) => [200 + 130 * Math.cos(i / n * 6.283 - 1.57), 150 + 100 * Math.sin(i / n * 6.283 - 1.57)]);
    const C = { agree: '#ff4d5e', conflict: '#22e4d4', weak: '#456' };
    return `<svg viewBox="0 0 400 300" style="max-width:420px;width:100%">${G.edges.map(e => `<line x1="${P[e.a][0]}" y1="${P[e.a][1]}" x2="${P[e.b][0]}" y2="${P[e.b][1]}" stroke="${C[e.relation]}" stroke-width="2"/>`).join('')}
    ${G.nodes.map((v, i) => { const l = v.risk >= 65 ? 'high' : v.risk >= 35 ? 'medium' : 'low'; return `<circle cx="${P[i][0]}" cy="${P[i][1]}" r="16" fill="#06112a" stroke="var(--${l})" stroke-width="3"/><text x="${P[i][0]}" y="${P[i][1] + 4}" fill="#fff" font-size="11" text-anchor="middle">${v.risk}</text><text x="${P[i][0]}" y="${P[i][1] + 32}" fill="#8aa3c4" font-size="10" text-anchor="middle">${VX.esc(v.label.slice(0, 18))}</text>` }).join('')}</svg>
    <p class="small mute">Lines: <span class="high">red = signals agree</span>, <span class="low">teal = conflict</span>, grey = weak link.</p>`
  })() : '<p class="mute">Add a second item to see cross-modal links.</p>';
  m.innerHTML = `<h1>Analysis results</h1><p class="mute mono">Case ${id}</p>
  <div class="card row" style="margin-top:20px;gap:28px"><div class="gauge" style="--p:${o.risk};--c:var(--${o.level})"><b>${o.risk}</b></div>
   <div style="flex:1;min-width:240px"><h2>Overall indicator: ${VX.lvBadge(o.level)}</h2><p>${VX.esc(d.report.summary.text)}</p>
   <p class="small mute">Consistency confidence: <b>${o.confidence.label}</b> (${o.confidence.score}). ${VX.esc(o.confidence.note)}</p>
   <div class="row noprint" style="margin-top:12px"><a class="btn" href="evidence.html?case=${id}">Inspect evidence</a><a class="btn ghost" href="report.html?case=${id}">Forensic report</a></div></div></div>
  <h2 style="margin-top:30px">Per-file analysis</h2><div class="grid">${d.results.map(r => `<div class="card rc"><div class="row between"><h3>${VX.esc(r.name)}</h3>${VX.lvBadge(r.level)}</div>
   <p class="small mute">${r.kind.toUpperCase()} · risk ${r.risk}/100 · confidence ${r.confidence.label} · ${r.flags.length} flag(s)</p>${VX.bar(r.risk, r.level)}
   <div style="margin-top:10px">${r.signals.map(s => `<div class="sig" style="grid-template-columns:150px 1fr 30px"><span>${VX.esc(s.label)}</span>${VX.bar(s.value)}<b>${s.value}</b></div>`).join('') || '<p class="small mute">No indicators matched.</p>'}</div>
   <details class="small mute" style="margin-top:8px"><summary>Limitations</summary><ul style="padding-left:18px">${r.limitations.map(l => `<li>${VX.esc(l)}</li>`).join('')}</ul></details></div>`).join('')}</div>
  <h2 style="margin-top:30px">Cross-modal correlation</h2><div class="grid"><div class="card">${graph}</div><div class="card">${d.correlation.findings.map(f => `<div class="find ${f.severity}"><b>${VX.esc(f.title)}</b> <span class="badge mute">${f.severity}</span><div class="small mute">${VX.esc(f.detail)}</div></div>`).join('') || '<p class="mute">No cross-modal observations.</p>'}</div></div>`;
})();
