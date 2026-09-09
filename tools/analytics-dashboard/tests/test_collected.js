const {test} = require('node:test');
const assert = require('node:assert/strict');
const {youtubeRetention} = require('../static/collected.js');
test('YouTube curve preserves raw ratios, scales units and excludes missing data', () => {
  const item = {reports:{retention:{status:'ok',response:{
    columnHeaders:[{name:'elapsedVideoTimeRatio'},{name:'audienceWatchRatio'}],
    rows:[[0.01,1.2],[0.5,0.4],[0.6,null]]
  }}}};
  assert.deepEqual(youtubeRetention(item), [
    {seconds:1,percent:120,precision:'exact'},
    {seconds:50,percent:40,precision:'exact'}
  ]);
  assert.deepEqual(youtubeRetention({}), []);
  item.reports.retention.status='error';
  assert.deepEqual(youtubeRetention(item), []);
});
