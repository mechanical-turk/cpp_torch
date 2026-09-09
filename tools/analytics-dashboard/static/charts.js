/* Pure chart geometry also runs under node:test. */
function audienceChartModel(history, days = 0) {
  const valid = history.filter(p => Number.isFinite(p.followers) && Number.isFinite(Date.parse(p.captured_at)))
    .map(p => ({...p, time: Date.parse(p.captured_at)})).sort((a, b) => a.time - b.time);
  const end = valid.at(-1)?.time;
  const points = valid.filter(p => !days || p.time >= end - days * 86400000);
  if (!points.length) return {points: []};
  const start = points[0].time;
  const values = points.map(p => p.followers);
  const low = Math.min(...values), high = Math.max(...values);
  const padding = Math.max(1, Math.ceil((high - low) * .1));
  const min = Math.max(0, low - padding), max = high + padding;
  return {min, max, start, end, points: points.map(p => ({...p,
    x: end === start ? 510 : 80 + (p.time - start) / (end - start) * 860,
    y: 340 - (p.followers - min) / (max - min) * 310
  }))};
}

function setupChartDialog(data) {
  const dialog = document.querySelector('#chart-dialog');
  const range = document.querySelector('#chart-range');
  const slider = document.querySelector('#chart-point');
  const plot = document.querySelector('#chart-plot');
  const readout = document.querySelector('#chart-readout');
  let platform, model;
  const time = value => new Date(value).toLocaleString([], {dateStyle: 'medium', timeStyle: 'medium'});
  function selectPoint(index) {
    const point = model.points[index];
    if (!point) return;
    slider.value = index;
    slider.setAttribute('aria-valuetext', `${point.followers}, ${time(point.time)}`);
    readout.textContent = `${time(point.time)} · ${number.format(point.followers)} ${(platform.metric_label || 'followers').toLowerCase()}`;
    const marker = plot.querySelector('.chart-marker');
    marker.setAttribute('cx', point.x);
    marker.setAttribute('cy', point.y);
  }
  function render() {
    model = audienceChartModel(data.audience_history[platform.platform] || [], Number(range.value));
    const points = model.points;
    slider.disabled = !points.length;
    slider.max = Math.max(0, points.length - 1);
    document.querySelector('#chart-values').innerHTML = points.map(p => `<tr><td>${time(p.time)}</td><td>${number.format(p.followers)}</td></tr>`).join('');
    document.querySelector('#chart-summary').textContent = `${points.length} snapshots`;
    if (!points.length) {
      plot.textContent = 'No saved snapshots available.';
      readout.textContent = '';
      return;
    }
    const ticks = Array.from({length: 5}, (_, i) => Math.round(model.min + (model.max - model.min) * i / 4))
      .filter((value, index, all) => all.indexOf(value) === index);
    const dateLabel = t => new Date(t).toLocaleString([], {month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'});
    plot.innerHTML = `<svg viewBox="0 0 1000 395" role="img" aria-label="${escapeHtml(platform.platform)} audience history, time on horizontal axis and count on vertical axis">
      ${ticks.map(value => { const y = 340 - (value - model.min) / (model.max - model.min) * 310;
        return `<line class="chart-gridline" x1="80" x2="940" y1="${y}" y2="${y}"/><text x="68" y="${y + 5}" text-anchor="end">${number.format(value)}</text>`;
      }).join('')}
      <polyline class="chart-line" points="${points.map(p => `${p.x},${p.y}`).join(' ')}"/>
      ${points.map(p => `<circle class="chart-dot" cx="${p.x}" cy="${p.y}" r="3"><title>${time(p.time)}: ${p.followers}</title></circle>`).join('')}
      <circle class="chart-marker" r="6"/>
      <text x="80" y="375">${dateLabel(model.start)}</text>
      ${model.start !== model.end ? `<text x="940" y="375" text-anchor="end">${dateLabel(model.end)}</text>` : ''}
    </svg>`;
    selectPoint(points.length - 1);
  }
  document.querySelector('#platform-grid').addEventListener('click', event => {
    const button = event.target.closest('[data-chart]');
    if (!button) return;
    platform = data.platforms.find(p => p.platform === button.dataset.chart);
    document.querySelector('#chart-title').textContent = `${platform.platform} · ${platform.metric_label || 'Followers'}`;
    range.value = '0';
    dialog.querySelector('details').open = false;
    render();
    dialog.showModal();
  });
  range.addEventListener('change', render);
  slider.addEventListener('input', () => selectPoint(Number(slider.value)));
  plot.addEventListener('pointermove', event => {
    const svg = plot.querySelector('svg');
    if (!svg || !model.points.length) return;
    const position = new DOMPoint(event.clientX, event.clientY).matrixTransform(svg.getScreenCTM().inverse());
    let nearest = 0;
    model.points.forEach((p, index) => {
      if (Math.abs(p.x - position.x) < Math.abs(model.points[nearest].x - position.x)) nearest = index;
    });
    selectPoint(nearest);
  });
  document.querySelector('#chart-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    const rect = dialog.getBoundingClientRect();
    if (event.target === dialog && (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom)) dialog.close();
  });
}

if (typeof module !== 'undefined') module.exports = {audienceChartModel};
