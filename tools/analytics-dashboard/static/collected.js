/* Full API reports retain native definitions, missing values and source dates. */
function youtubeRetention(item) {
  const report = item.reports?.retention;
  const headers = report?.response?.columnHeaders?.map(h => h.name) || [];
  const x = headers.indexOf('elapsedVideoTimeRatio');
  const y = headers.indexOf('audienceWatchRatio');
  if (report?.status !== 'ok' || x < 0 || y < 0) return [];
  return (report.response.rows || []).filter(row => Number.isFinite(row[x]) && Number.isFinite(row[y]))
    .map(row => ({seconds: row[x] * 100, percent: row[y] * 100, precision: 'exact'}));
}

function renderCollectedInsights(item) {
  const esc = v => escapeHtml(String(v ?? 'Unknown'));
  const nice = v => v.replace(/_/g, ' ').replace(/([a-z])([A-Z])/g, '$1 $2');
  const value = v => v == null ? 'Unknown' : typeof v === 'object' ? JSON.stringify(v) : v;
  const cells = (values, tag='td') => values.map(v => `<${tag}>${esc(value(v))}</${tag}>`).join('');
  const keyValues = (name, object) => !object || !Object.keys(object).length ? '' : `<details><summary>${esc(name)}</summary><div class="report-table"><table><thead><tr><th>Native metric</th><th>Value</th></tr></thead><tbody>${Object.entries(object).map(([key,v]) => `<tr>${cells([key,value(v)])}</tr>`).join('')}</tbody></table></div></details>`;
  if (item.native_only) return '';
  let html = '<h2>Collected platform insights</h2><p class="chart-note">API/provider data. Unknown is not zero. Processed reports may lag public counts.</p>';
  const retention = youtubeRetention(item);
  if (retention.length) {
    const geometry = nativeGeometry({retention, duration_seconds:100});
    html += `<h3>Audience retention</h3><svg class="api-retention" viewBox="0 0 900 285" role="img" aria-label="YouTube API audience watch ratio across video progress">
      ${[0,geometry.ceiling/2,geometry.ceiling].map(v => `<line x1="55" x2="855" y1="${245-v/geometry.ceiling*210}" y2="${245-v/geometry.ceiling*210}" class="chart-gridline"/><text x="0" y="${250-v/geometry.ceiling*210}">${v.toFixed(0)}%</text>`).join('')}
      <polyline class="chart-line" points="${geometry.points.map(p => `${p.x},${p.y}`).join(' ')}"/>
      ${geometry.points.map(p => `<circle class="chart-dot" r="2" cx="${p.x}" cy="${p.y}"><title>${p.seconds.toFixed(0)}% through video: ${p.percent.toFixed(1)}% audience watch ratio</title></circle>`).join('')}
      <text x="55" y="275">Start</text><text x="775" y="275">End (100%)</text></svg>
      <p class="chart-note">${retention.length} API samples. Horizontal axis: percentage through the video. Vertical axis: audienceWatchRatio × 100; replays can exceed 100%. Not the Shorts stayed-to-watch metric. Analytics end date: ${esc(item.analytics_end_date)}.</p>`;
  }
  for (const [name, report] of Object.entries(item.reports || {})) {
    const headers = report.response?.columnHeaders || [];
    const rows = report.response?.rows || [];
    html += `<details><summary>${esc(nice(name))} · ${rows.length} rows · ${esc(report.status)}</summary>`;
    if (!rows.length) html += '<p>No processed rows returned. This does not establish zero activity.</p>';
    else html += `<div class="report-table"><table><thead><tr>${cells(headers.map(h=>h.name),'th')}</tr></thead><tbody>${rows.map(row=>`<tr>${cells(row)}</tr>`).join('')}</tbody></table></div>`;
    html += '</details>';
  }
  html += keyValues('Content metrics', item.metrics);
  html += keyValues('Public engagement', item.public_metrics);
  if (item.platform === 'Instagram') html += keyValues('Public engagement', {likes:item.likes, comments:item.comments});
  for (const type of ['public_metrics','non_public_metrics','organic_metrics','promoted_metrics']) html += keyValues(`Video ${nice(type)}`, item.media?.[type]);
  return html;
}

if (typeof module !== 'undefined') module.exports = {youtubeRetention};
