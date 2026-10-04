/* Pure chart geometry and projection math also run under node:test. */
const DAY_MS = 86400000;

function validAudiencePoints(history) {
  return history.filter(p => Number.isFinite(p.followers) && Number.isFinite(Date.parse(p.captured_at)))
    .map(p => ({...p, time: Date.parse(p.captured_at)})).sort((a, b) => a.time - b.time);
}

function audienceChartModel(history, days = 0) {
  const valid = validAudiencePoints(history);
  const end = valid.at(-1)?.time;
  const points = valid.filter(p => !days || p.time >= end - days * DAY_MS);
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

function interpolatedCount(points, time) {
  if (!points.length || time < points[0].time || time > points.at(-1).time) return null;
  const exact = points.find(point => point.time === time);
  if (exact) return exact.followers;
  const rightIndex = points.findIndex(point => point.time > time);
  if (rightIndex <= 0) return null;
  const left = points[rightIndex - 1], right = points[rightIndex];
  const fraction = (time - left.time) / (right.time - left.time);
  return left.followers + (right.followers - left.followers) * fraction;
}

function audienceProjectionModel(history) {
  const points = validAudiencePoints(history);
  if (!points.length) return {scenarios: [], horizons: []};
  const latest = points.at(-1);
  const horizons = [
    {key: 'week', label: '1 week', days: 7},
    {key: 'month', label: '1 month', days: 30},
    {key: 'quarter', label: '3 months', days: 90}
  ];
  const windowRate = days => {
    if (points.length < 2) return {rate: null, observedDays: 0};
    const startTime = Math.max(points[0].time, latest.time - days * DAY_MS);
    const observedDays = (latest.time - startTime) / DAY_MS;
    const count = interpolatedCount(points, startTime);
    return {
      observedDays,
      rate: count == null || observedDays <= 0 ? null : (latest.followers - count) / observedDays
    };
  };
  const elapsedDays = points.length < 2 ? 0 : (latest.time - points[0].time) / DAY_MS;
  const trailing7 = windowRate(7), trailing14 = windowRate(14), trailing30 = windowRate(30);
  const definitions = [
    {key: '7d', label: '1-week pace', ...trailing7},
    {key: '14d', label: '2-week pace', ...trailing14},
    {key: '30d', label: '1-month pace', ...trailing30},
    {
      key: 'all', label: 'All-time pace', observedDays: elapsedDays,
      rate: elapsedDays > 0 ? (latest.followers - points[0].followers) / elapsedDays : null
    }
  ];
  return {
    current: latest.followers,
    asOf: latest.time,
    horizons,
    scenarios: definitions.map(definition => ({
      ...definition,
      projections: horizons.map(horizon => {
        if (!Number.isFinite(definition.rate)) return {...horizon, count: null, gain: null};
        const count = Math.max(0, Math.round(latest.followers + definition.rate * horizon.days));
        return {...horizon, count, gain: count - latest.followers};
      })
    }))
  };
}

function audienceProjectionChartModel(projection) {
  const available = (projection.scenarios || []).filter(scenario =>
    scenario.projections.some(point => Number.isFinite(point.count))
  );
  if (!Number.isFinite(projection.current) || !available.length) return {series: []};
  const values = [projection.current, ...available.flatMap(scenario =>
    scenario.projections.filter(point => Number.isFinite(point.count)).map(point => point.count)
  )];
  const low = Math.min(...values), high = Math.max(...values);
  const padding = Math.max(1, Math.ceil((high - low) * .08));
  const min = Math.max(0, low - padding), max = high + padding;
  const x = days => 80 + days / 90 * 860;
  const y = count => 300 - (count - min) / (max - min) * 265;
  return {
    min, max,
    series: available.map(scenario => ({
      key: scenario.key,
      label: scenario.label,
      rate: scenario.rate,
      points: [
        {days: 0, count: projection.current, x: x(0), y: y(projection.current)},
        ...scenario.projections.filter(point => Number.isFinite(point.count))
          .map(point => ({...point, x: x(point.days), y: y(point.count)}))
      ]
    }))
  };
}

function setupChartDialog(data) {
  const dialog = document.querySelector('#chart-dialog');
  const range = document.querySelector('#chart-range');
  const slider = document.querySelector('#chart-point');
  const plot = document.querySelector('#chart-plot');
  const readout = document.querySelector('#chart-readout');
  const projections = document.querySelector('#chart-projections');
  const projectionPlot = document.querySelector('#projection-plot');
  const projectionNote = document.querySelector('#projection-note');
  let platform, model;
  let requestSerial = 0;
  const time = value => new Date(value).toLocaleString([], {dateStyle: 'medium', timeStyle: 'medium'});
  const signed = value => `${value >= 0 ? '+' : ''}${number.format(value)}`;
  const dailyRate = value => `${value >= 0 ? '+' : ''}${value.toFixed(2)}/day`;
  function renderProjections() {
    const projection = audienceProjectionModel(data.audience_history[platform.platform] || []);
    if (!projection.scenarios.length) {
      projectionPlot.textContent = '';
      projections.innerHTML = '<p class="chart-note">No saved audience history is available for projections.</p>';
      projectionNote.textContent = '';
      return;
    }
    const chart = audienceProjectionChartModel(projection);
    if (!chart.series.length) {
      projectionPlot.innerHTML = '<p class="chart-note">At least two saved snapshots are needed to draw a projection.</p>';
    } else {
      const ticks = Array.from({length: 4}, (_, index) =>
        Math.round(chart.min + (chart.max - chart.min) * index / 3)
      ).filter((value, index, all) => all.indexOf(value) === index);
      const xTicks = [{days: 0, label: 'Now'}, ...projection.horizons];
      projectionPlot.innerHTML = `<div class="projection-legend">${chart.series.map(series =>
        `<span><i class="projection-swatch projection-${series.key}"></i>${series.label}</span>`
      ).join('')}</div>
      <svg viewBox="0 0 1000 350" role="img" aria-label="${escapeHtml(platform.platform)} projected audience counts for the next three months">
        ${ticks.map(value => { const y = 300 - (value - chart.min) / (chart.max - chart.min) * 265;
          return `<line class="chart-gridline" x1="80" x2="940" y1="${y}" y2="${y}"/><text x="68" y="${y + 5}" text-anchor="end">${number.format(value)}</text>`;
        }).join('')}
        ${xTicks.map(tick => { const x = 80 + tick.days / 90 * 860;
          return `<line class="projection-x-tick" x1="${x}" x2="${x}" y1="35" y2="300"/><text x="${x}" y="332" text-anchor="${tick.days === 0 ? 'start' : tick.days === 90 ? 'end' : 'middle'}">${tick.label}</text>`;
        }).join('')}
        ${chart.series.map(series => `<polyline class="projection-line projection-${series.key}" points="${series.points.map(point => `${point.x},${point.y}`).join(' ')}"/>
          ${series.points.slice(1).map(point => `<circle class="projection-point projection-${series.key}" cx="${point.x}" cy="${point.y}" r="4"><title>${series.label}, ${point.label}: ${number.format(point.count)}</title></circle>`).join('')}`
        ).join('')}
        <circle class="projection-origin" cx="80" cy="${chart.series[0].points[0].y}" r="5"><title>Current: ${number.format(projection.current)}</title></circle>
      </svg>`;
    }
    projections.innerHTML = `<div class="projection-table-wrap"><table class="projection-table">
      <thead><tr><th>Growth pace</th><th>Average daily</th>${projection.horizons.map(horizon => `<th>${horizon.label}</th>`).join('')}</tr></thead>
      <tbody>${projection.scenarios.map(scenario => `<tr>
        <th scope="row">${scenario.label}${scenario.observedDays > 0 ? `<small>${scenario.observedDays.toFixed(1)} recorded days</small>` : ''}</th>
        <td>${Number.isFinite(scenario.rate) ? dailyRate(scenario.rate) : '<span class="projection-missing">Not enough history</span>'}</td>
        ${scenario.projections.map(value => value.count == null
          ? '<td><span class="projection-missing">Unavailable</span></td>'
          : `<td><strong>${number.format(value.count)}</strong><small>${signed(value.gain)}</small></td>`).join('')}
      </tr>`).join('')}</tbody>
    </table></div>`;
    projectionNote.textContent = `Starting from ${number.format(projection.current)} on ${time(projection.asOf)}. Straight-line projections preserve each observed average; they are scenarios, not predicted outcomes.`;
  }
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
  document.querySelector('#platform-grid').addEventListener('click', async event => {
    const button = event.target.closest('[data-chart]');
    if (!button) return;
    const requestedPlatform = button.dataset.chart;
    const serial = ++requestSerial;
    try {
      const response = await fetch('/api/dashboard', {cache: 'no-store'});
      if (response.ok) data = await response.json();
    } catch {
      // Keep the already loaded snapshot available if a live refresh fails.
    }
    if (serial !== requestSerial) return;
    platform = data.platforms.find(p => p.platform === requestedPlatform);
    document.querySelector('#chart-title').textContent = `${platform.platform} · ${platform.metric_label || 'Followers'}`;
    range.value = '0';
    dialog.querySelector('details').open = false;
    render();
    renderProjections();
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

if (typeof module !== 'undefined') module.exports = {
  audienceChartModel, audienceProjectionModel, audienceProjectionChartModel
};
