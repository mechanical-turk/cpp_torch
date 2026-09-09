/* Native snapshots stay separate from API totals and from other capture dates. */
function nativeRates(record) {
  const metrics = Object.fromEntries(record.metrics.map(m => [m.key, m]));
  const pairs = [
    ['Follows per 1,000 views', 'follows', 'views'],
    ['Follows per 1,000 viewers', 'follows', 'viewers'],
    ['Profile visits per 1,000 views', 'profile_visits', 'views'],
    ['Comments per 1,000 views', 'comments', 'views'],
    ['Shares per 1,000 views', 'shares', 'views'],
    ['Saves per 1,000 views', 'saves', 'views']
  ];
  return pairs.flatMap(([label, a, b]) => {
    const top = metrics[a], bottom = metrics[b];
    if (top?.value == null || !(bottom?.value > 0)) return [];
    return [{label, value: top.value / bottom.value * 1000,
      approximate: top.precision !== 'exact' || bottom.precision !== 'exact'}];
  });
}

function nativeGeometry(record) {
  const ceiling = Math.max(100, ...record.retention.map(p => p.percent));
  return {ceiling, points: record.retention.map(p => ({...p,
    x: 55 + p.seconds / record.duration_seconds * 800,
    y: 245 - p.percent / ceiling * 210}))};
}

function nativeContentKey(value) {
  try {
    const url = new URL(value);
    // Instagram API and native UI can use /p/ and /reel/ for the same post.
    const path = url.pathname.replace(/^\/(p|reel|reels)\//, '/post/').replace(/\/$/, '');
    return url.hostname.replace(/^www\./, '') + path;
  } catch { return null; }
}

function nativeMatches(record, item) {
  if (record.platform !== item.platform) return false;
  if (item.id != null && String(item.id) === String(record.content_id)) return true;
  const key = nativeContentKey(item.url);
  return key !== null && key === nativeContentKey(record.content_url);
}

function dashboardContentRows(data) {
  const rows = data.platforms.flatMap(platform => platform.content.map(item => ({
    ...item, platform: platform.platform, source_captured_at: item.source_captured_at || platform.captured_at
  })));
  for (const record of data.native_insights?.records || []) {
    if (!rows.some(item => nativeMatches(record, item))) rows.push({
      id: record.content_id, url: record.content_url, platform: record.platform,
      title: record.title, published_at: record.published_at, native_only: true
    });
  }
  return rows;
}

function setupNativeInsights(data) {
  const container = document.querySelector('#native-insights');
  const select = document.querySelector('#native-select');
  const dialog = document.querySelector('#content-dialog');
  let records = [];
  let opener;
  const esc = v => escapeHtml(String(v ?? ''));
  const safeURL = value => /^https?:\/\//.test(value || '') ? esc(value) : '#';
  const render = () => {
    const r = records[Number(select.value)];
    if (!r) {
      container.textContent = 'No native insights captured for this post yet. Retention, screenshots and creative analysis will appear here after capture.';
      if (data.errors.length) container.textContent += ` Capture loading errors: ${data.errors.join('; ')}`;
      return;
    }
    const geometry = nativeGeometry(r);
    const points = geometry.points;
    const source = id => r.screenshots.find(s => s.id === id);
    const sourceLink = id => {
      const s = source(id);
      return s ? `<a href="${esc(s.url)}" target="_blank" rel="noreferrer">${esc(s.label)}</a>` : 'Source unavailable';
    };
    const curve = points.length ? `<svg viewBox="0 0 900 285" role="img" aria-label="Retention percentage by video time; dashed segments include estimated points">
      ${[0, geometry.ceiling / 2, geometry.ceiling].map(v => `<line x1="55" x2="855" y1="${245-v/geometry.ceiling*210}" y2="${245-v/geometry.ceiling*210}" class="chart-gridline"/><text x="2" y="${250-v/geometry.ceiling*210}">${v.toFixed(0)}%</text>`).join('')}
      ${(r.events || []).map(e => `<line x1="${55+e.seconds/r.duration_seconds*800}" x2="${55+e.seconds/r.duration_seconds*800}" y1="35" y2="245" class="native-event"><title>${esc(e.label)} at ${e.seconds}s</title></line>`).join('')}
      ${points.slice(1).map((p,i) => `<line x1="${points[i].x}" y1="${points[i].y}" x2="${p.x}" y2="${p.y}" class="chart-line" ${p.precision === 'estimated' || points[i].precision === 'estimated' ? 'stroke-dasharray="6 5"' : ''}/>`).join('')}
      ${points.map(p => `<circle cx="${p.x}" cy="${p.y}" r="4" class="chart-dot"><title>${p.seconds}s: ${p.percent}% (${esc(p.precision)})</title></circle>`).join('')}
      <text x="55" y="277">0s</text><text x="800" y="277">${r.duration_seconds}s</text></svg>` : '<p>Retention curve unavailable. No curve inferred from average watch time.</p>';
    const rates = nativeRates(r);
    container.innerHTML = `
      ${data.errors.length ? `<p role="alert">Some captures could not load: ${esc(data.errors.join('; '))}</p>` : ''}
      <p><a href="${safeURL(r.content_url)}" target="_blank" rel="noreferrer">${esc(r.title)}</a> · ${esc(r.platform)} / ${esc(r.format)} · ${esc(r.source_surface)}</p>
      <p class="chart-note">Captured ${esc(displayTime(r.captured_at))} · ${esc(r.period)}. This is a saved observation, not a live feed.</p>
      <div class="native-layout"><div>
        <h3>Retention and video moments</h3>${curve}
        <p class="chart-note">${esc(r.retention_definition || 'Use the source platform’s retention definition.')} Dashed segments include estimates. Lines connect observations; they do not add measurements.</p>
        <details><summary>Retention values and sources</summary><table class="native-table"><thead><tr><th>Time</th><th>Retained</th><th>Precision</th><th>Source</th></tr></thead><tbody>${points.map(p => `<tr><td>${p.seconds}s</td><td>${p.percent}%</td><td>${esc(p.precision)}</td><td>${sourceLink(p.source)}</td></tr>`).join('')}</tbody></table></details>
        <ul>${(r.events || []).map(e => `<li><strong>${e.seconds}s:</strong> ${esc(e.label)}</li>`).join('')}</ul>
        <p class="chart-note">Media evidence: ${esc(r.media_source || 'Not inspected yet')}</p>
      </div><div>
        <h3>Engagement and conversion</h3>
        <div class="native-metrics">${r.metrics.map(m => `<div><span>${esc(m.label)}</span><strong>${m.value == null ? 'Unknown' : `${m.precision === 'exact' ? '' : '≈ '}${number.format(m.value)}${m.unit === 'percent' ? '%' : m.unit === 'seconds' ? 's' : ''}`}</strong><small>${esc(m.precision)} · ${sourceLink(m.source)}</small></div>`).join('')}</div>
        <ul>${rates.map(m => `<li>${esc(m.label)}: <strong>${m.approximate ? '≈ ' : ''}${m.value.toFixed(2)}</strong></li>`).join('')}</ul>
        <p class="chart-note">Rates use this capture only. Views can repeat. Follows can happen directly from a Reel; profile visits are not a required intermediate step.</p>
      </div></div>
      <details><summary>Native screenshots (${r.screenshots.length})</summary><div class="native-screens">${r.screenshots.map(s => `<a href="${esc(s.url)}" target="_blank" rel="noreferrer"><img src="${esc(s.url)}" alt="${esc(s.label)}" loading="lazy"><span>${esc(s.label)}</span></a>`).join('')}</div></details>
      <div class="native-analysis">${['observed', 'hypotheses', 'next_test', 'limitations'].map(key => `<div><h3>${({observed:'Observed', hypotheses:'Possible explanations', next_test:'Next test', limitations:'Limits'})[key]}</h3><p>${esc(r.analysis?.[key] || 'Not assessed yet.')}</p></div>`).join('')}</div>
      <p class="chart-note">Compare captures within the same platform and format at similar publication ages. A retention bump or higher follow rate does not prove a creative choice caused it.</p>`;
  };
  select.addEventListener('change', render);
  document.querySelector('#content-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
  });
  dialog.addEventListener('close', () => opener?.focus());
  return (item, summary, trigger) => {
    opener = trigger;
    document.querySelector('#content-title').textContent = item.title;
    document.querySelector('#content-platform').textContent = item.platform;
    const link = document.querySelector('#content-link');
    link.href = /^https?:\/\//.test(item.url || '') ? item.url : '#';
    link.hidden = !/^https?:\/\//.test(item.url || '');
    document.querySelector('#content-summary-source').textContent = item.native_only ? 'Native evidence below; no matching API content snapshot.' : `Dashboard summary snapshot: ${displayTime(item.source_captured_at)}. Native captures below retain their own dates and definitions.`;
    document.querySelector('#content-summary').innerHTML = Object.entries(summary).map(([key, value]) => `<div><span>${esc(key)}</span><strong>${esc(value)}</strong></div>`).join('');
    document.querySelector('#content-summary').hidden = !!item.native_only;
    document.querySelector('#content-reports').innerHTML = renderCollectedInsights(item);
    records = data.records.filter(record => nativeMatches(record, item))
      .sort((a,b) => new Date(b.captured_at) - new Date(a.captured_at));
    select.disabled = !records.length;
    select.innerHTML = records.length ? records.map((r,i) => `<option value="${i}">${esc(displayTime(r.captured_at))} · ${esc(r.period)}</option>`).join('') : '<option>No captures</option>';
    render();
    dialog.showModal();
    dialog.scrollTop = 0;
  };
}

if (typeof module !== 'undefined') module.exports = {nativeRates, nativeGeometry, nativeMatches, dashboardContentRows};
