const VXUpload = (() => {
  const files = [];
  const ICON = { image: '🖼', video: '🎞', audio: '🎙', text: '📄' };
  const kind = n => { const e = n.split('.').pop().toLowerCase(); return ['jpg', 'jpeg', 'png', 'webp', 'bmp', 'gif'].includes(e) ? 'image' : ['mp4', 'mov', 'avi', 'webm', 'mkv'].includes(e) ? 'video' : ['wav', 'mp3', 'm4a', 'ogg', 'flac'].includes(e) ? 'audio' : ['txt', 'md', 'eml', 'csv', 'log'].includes(e) ? 'text' : null };
  function render() {
    $('#files').innerHTML = files.map((f, i) => `<li><span>${ICON[kind(f.name)]} ${VX.esc(f.name)} <span class="mute small">${(f.size / 1048576).toFixed(2)} MB</span></span><button class="x" data-i="${i}" title="Remove">×</button></li>`).join('');
    $('#files').querySelectorAll('.x').forEach(b => b.onclick = () => { files.splice(+b.dataset.i, 1); render() });
  }
  function add(list) {
    [...list].forEach(f => { if (!kind(f.name)) VX.toast('Unsupported file: ' + f.name); else if (f.size > 50 * 1048576) VX.toast(f.name + ' is over 50 MB'); else files.push(f) }); render();
  }
  function init() {
    const d = $('#drop'), i = $('#file');
    d.onclick = () => i.click(); i.onchange = () => { add(i.files); i.value = '' };
    ['dragover', 'dragenter'].forEach(e => d.addEventListener(e, ev => { ev.preventDefault(); d.classList.add('over') }));
    ['dragleave', 'drop'].forEach(e => d.addEventListener(e, ev => { ev.preventDefault(); d.classList.remove('over') }));
    d.addEventListener('drop', ev => add(ev.dataTransfer.files));
  }
  return { files, init };
})();
