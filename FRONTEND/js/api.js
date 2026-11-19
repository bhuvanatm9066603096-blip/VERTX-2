(async () => {
  const m = $('#view'), id = VX.caseId(); if (!id) return VX.needCase(m);
  let r; try { r = await VXAPI.report(id) } catch (e) { return m.innerHTML = `<div class="card">${VX.esc(e.message)}</div>` }
  const o = r.summary.overall, e = VX.esc;
  m.innerHTML = `<div class="row between"><div><h1>Forensic report</h1><p class="mute mono">Case ${e(r.case.id)} · generated ${e(r.case.generated)}</p></div>
  <div class="row noprint"><button class="btn" onclick="print()">Print / PDF</button><a class="btn ghost" href="${VXAPI.download(id, 'html')}">Download HTML</a><a class="btn ghost" href="${VXAPI.download(id, 'json')}">Download JSON</a></div></div>
  <div class="stack" style="margin-top:20px">
  <div class="card"><h2>Summary ${VX.lvBadge(o.level)}</h2><p>${e(r.summary.text)}</p><p class="small mute">Confidence: ${o.confidence.label} (${o.confidence.score}) · ${e(o.confidence.note)}</p></div>
  <div class="card"><h2>Flagged evidence</h2><div style="overflow-x:auto"><table><tr><th>File</th><th>Location</th><th>Indicator</th><th>Score</th><th>Why flagged</th></tr>${r.flagged.map(f => `<tr><td>${e(f.file)}</td><td>${e(f.location)}</td><td>${e(f.indicator)}</td><td>${f.score}</td><td class="mute">${e(f.why)}</td></tr>`).join('') || '<tr><td colspan="5" class="mute">No flags raised.</td></tr>'}</table></div></div>
  <div class="card"><h2>Cross-modal context</h2>${r.cross_modal.map(f => `<div class="find ${f.severity}"><b>${e(f.title)}</b><div class="small mute">${e(f.detail)} <i>Sources: ${f.sources.map(e).join(', ')}</i></div></div>`).join('') || '<p class="mute">None.</p>'}</div>
  <div class="card"><h2>Source trace</h2>${r.trace.map(t => `<div style="margin-bottom:10px"><b>${e(t.name)}</b> <span class="badge ${t.level}">${t.level}</span><div class="mono mute">${t.sha256}</div><div class="small mute">${t.signals.map(e).join(' · ')}</div></div>`).join('')}</div>
  <div class="card"><h2>Limitations</h2><ul style="padding-left:18px">${r.limitations.map(l => `<li>${e(l)}</li>`).join('')}</ul></div>
  <div class="card"><h2>Recommended human checks</h2><ul style="padding-left:18px">${r.checks.map(l => `<li>${e(l)}</li>`).join('')}</ul></div></div>`;
})();
