(async () => {
  const m = $('#view'), id = VX.caseId(); if (!id) return VX.needCase(m);
  let d; try { d = await VXAPI.results(id) } catch (e) { return m.innerHTML = `<div class="card">${VX.esc(e.message)}</div>` }
  m.innerHTML = `<h1>Evidence review</h1><p class="mute mono">Case ${id} · originals are preserved unmodified</p><div class="grid" style="grid-template-columns:260px 1fr;margin-top:20px"><div class="list" id="list"></div><div class="card" id="viewer"></div></div>`;
  $('#list').innerHTML = d.results.map((r, i) => `<button data-i="${i}">${r.kind.toUpperCase()} · ${VX.esc(r.name)}<br><span class="small ${r.level}">${r.level} · ${r.flags.length} flag(s)</span></button>`).join('');
  const meta = r => `<p class="small mute mono" style="margin-top:12px">SHA-256 ${r.sha256}</p>`;
  const flagList = (r, seek) => r.flags.map((f, i) => `<div class="find strengthens"><b>${VX.esc(f.indicator)}</b> <span class="badge high">${f.score}</span><div class="small mute">${VX.esc(f.why)}</div>${seek && (f.timestamp != null || f.start != null) ? `<button class="btn ghost chip" data-t="${f.timestamp ?? f.start}">Jump to ${f.timestamp ?? f.start}s</button>` : ''}</div>`).join('') || '<p class="mute">Nothing flagged for this item.</p>';
  function show(i) {
    const r = d.results[i], v = $('#viewer'), url = VXAPI.orig(id, r.file);
    document.querySelectorAll('#list button').forEach((b, k) => b.classList.toggle('on', k === i));
    let h = `<h2>${VX.esc(r.name)}</h2>`;
    if (r.kind === 'image') h += `<div class="row noprint"><button class="btn ghost" id="tg">Show ELA map</button></div><div class="stage" style="margin-top:10px"><img id="im" src="${url}" alt="evidence">${r.flags.filter(f => f.where).map(f => `<div class="box" title="${VX.esc(f.indicator)}" style="left:${f.where.x * 100}%;top:${f.where.y * 100}%;width:${f.where.w * 100}%;height:${f.where.h * 100}%"></div>`).join('')}</div>`;
    else if (r.kind === 'video') h += `<video id="md" src="${url}" controls style="max-width:100%;border-radius:10px"></video>`;
    else if (r.kind === 'audio') h += `<audio id="md" src="${url}" controls style="width:100%"></audio>`;
    else { let t = r.text || '', out = '', p = 0; r.flags.filter(f => f.span).sort((a, b) => a.span[0] - b.span[0]).forEach(f => { if (f.span[0] >= p) { out += VX.esc(t.slice(p, f.span[0])) + `<mark title="${VX.esc(f.indicator)}">${VX.esc(t.slice(f.span[0], f.span[1]))}</mark>`; p = f.span[1] } }); h += `<pre class="txt">${out + VX.esc(t.slice(p))}</pre>` }
    v.innerHTML = h + '<h3 style="margin-top:18px">Flagged evidence</h3>' + flagList(r, true) + meta(r);
    const tg = $('#tg'); if (tg) tg.onclick = () => { const ela = tg.textContent.startsWith('Show'); $('#im').src = ela ? VXAPI.ela(id, r.ela_file) : url; tg.textContent = ela ? 'Show original' : 'Show ELA map' };
    v.querySelectorAll('[data-t]').forEach(b => b.onclick = () => { const md = $('#md'); if (md) { md.currentTime = +b.dataset.t; md.play() } });
  }
  document.querySelectorAll('#list button').forEach(b => b.onclick = () => show(+b.dataset.i)); show(0);
})();
