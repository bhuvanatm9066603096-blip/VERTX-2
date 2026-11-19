const API = location.port === '5000' ? '' : 'http://localhost:5000';
async function j(p, o) {
  let r; try { r = await fetch(API + p, o) } catch (e) { throw new Error('Cannot reach the backend. Start it with: python app.py') }
  const d = await r.json().catch(() => ({})); if (!r.ok) throw new Error(d.error || r.statusText); return d;
}
const VXAPI = {
  upload: fd => j('/api/upload', { method: 'POST', body: fd }),
  analyze: id => j('/api/analyze/' + id, { method: 'POST' }),
  results: id => j('/api/results/' + id),
  cases: () => j('/api/cases'),
  report: id => j('/api/report/' + id),
  download: (id, f) => `${API}/api/report/${id}/download?format=${f}`,
  orig: (id, n) => `${API}/api/evidence/${id}/original/${encodeURIComponent(n)}`,
  ela: (id, n) => `${API}/api/evidence/${id}/ela/${encodeURIComponent(n)}`
};
