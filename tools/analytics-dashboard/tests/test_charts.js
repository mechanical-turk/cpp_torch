const {test} = require('node:test');
const assert = require('node:assert/strict');
const {audienceChartModel} = require('../static/charts.js');
const point = (day, followers) => ({captured_at: `2026-09-${String(day).padStart(2, '0')}T12:00:00Z`, followers});
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
