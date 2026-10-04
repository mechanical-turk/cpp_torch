const {test} = require('node:test');
const assert = require('node:assert/strict');
const {
  audienceChartModel, audienceProjectionModel, audienceProjectionChartModel
} = require('../static/charts.js');
const point = (day, followers) => ({captured_at: `2026-09-${String(day).padStart(2, '0')}T12:00:00Z`, followers});
const datedPoint = (date, followers) => ({captured_at: `${date}T12:00:00Z`, followers});
test('filters invalid values, sorts timestamps and spaces by time', () => {
  const model = audienceChartModel([point(5, 20), point(1, 10), point(2, 11), point(3, null), {captured_at: 'bad', followers: 1}]);
  assert.equal(model.points.length, 3);
  assert.equal(model.points[1].x, 295);
  assert.equal(model.points[2].x, 940);
});
test('ranges anchor to latest saved observation', () => {
  const model = audienceChartModel([point(1, 1), point(4, 4), point(5, 5)], 1);
  assert.deepEqual(model.points.map(p => p.followers), [4, 5]);
});
test('empty, single, zero and flat histories have safe coordinates', () => {
  assert.deepEqual(audienceChartModel([]), {points: []});
  for (const history of [[point(1, 0)], [point(1, 5), point(2, 5)]]) {
    const model = audienceChartModel(history);
    assert.ok(model.max > model.min);
    assert.ok(model.points.every(p => Number.isFinite(p.x) && Number.isFinite(p.y)));
  }
});
test('projects 1-week, 2-week, 1-month and all-time daily growth into three horizons', () => {
  const history = [];
  for (let day = 1; day <= 31; ++day) history.push(point(day, 100 + (day - 1) * 2));
  const model = audienceProjectionModel(history);
  assert.equal(model.current, 160);
  assert.deepEqual(model.horizons.map(h => h.days), [7, 30, 90]);
  assert.deepEqual(model.scenarios.map(s => s.key), ['7d', '14d', '30d', 'all']);
  for (const scenario of model.scenarios) {
    assert.equal(scenario.rate, 2);
    assert.deepEqual(scenario.projections.map(p => p.count), [174, 220, 340]);
    assert.deepEqual(scenario.projections.map(p => p.gain), [14, 60, 180]);
  }
});
test('uses the available span and reports it when trailing history is short', () => {
  const model = audienceProjectionModel([point(1, 10), point(6, 20)]);
  assert.equal(model.scenarios.find(s => s.key === '7d').rate, 2);
  assert.equal(model.scenarios.find(s => s.key === '7d').observedDays, 5);
  assert.equal(model.scenarios.find(s => s.key === '14d').rate, 2);
  assert.equal(model.scenarios.find(s => s.key === '14d').observedDays, 5);
  assert.equal(model.scenarios.find(s => s.key === '30d').rate, 2);
  assert.equal(model.scenarios.find(s => s.key === '30d').observedDays, 5);
  assert.equal(model.scenarios.find(s => s.key === 'all').rate, 2);
});
test('interpolates the count at a trailing-window boundary', () => {
  const model = audienceProjectionModel([
    datedPoint('2026-08-01', 100),
    datedPoint('2026-09-05', 170),
    datedPoint('2026-09-12', 191)
  ]);
  assert.equal(model.scenarios.find(s => s.key === '7d').rate, 3);
  assert.ok(Math.abs(model.scenarios.find(s => s.key === '30d').rate - 2.2333333333) < 1e-9);
});
test('projection model safely handles invalid and single-point histories', () => {
  assert.deepEqual(audienceProjectionModel([]), {scenarios: [], horizons: []});
  const model = audienceProjectionModel([point(1, 12), {captured_at: 'bad', followers: 99}]);
  assert.ok(model.scenarios.every(s => s.rate === null));
  assert.ok(model.scenarios.every(s => s.projections.every(p => p.count === null)));
});
test('projection chart maps all scenarios from now through three months', () => {
  const projection = audienceProjectionModel([point(1, 10), point(8, 24)]);
  const chart = audienceProjectionChartModel(projection);
  assert.equal(chart.series.length, 4);
  for (const series of chart.series) {
    assert.equal(series.points[0].x, 80);
    assert.equal(series.points.at(-1).x, 940);
    assert.ok(series.points.every(point => Number.isFinite(point.y)));
  }
  assert.ok(chart.max > chart.min);
});
test('projection chart stays empty without a measurable growth interval', () => {
  const projection = audienceProjectionModel([point(1, 10)]);
  assert.deepEqual(audienceProjectionChartModel(projection), {series: []});
});
