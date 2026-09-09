const {test} = require('node:test');
const assert = require('node:assert/strict');
const {nativeRates, nativeGeometry, nativeMatches, dashboardContentRows} = require('../static/native.js');
test('rates preserve missing and zero values and identify rounded input', () => {
  const record = {metrics: [
    {key:'views', value:1000, precision:'exact'},
    {key:'follows', value:0, precision:'exact'},
    {key:'comments', value:null, precision:'exact'},
    {key:'shares', value:20, precision:'rounded'}
  ]};
  const rates = nativeRates(record);
  assert.equal(rates.length, 2);
  assert.equal(rates[0].value, 0);
  assert.equal(rates[1].approximate, true);
  record.metrics[0].value = 0;
  assert.deepEqual(nativeRates(record), []);
});
test('curve uses video time, allows replay values above 100%, preserves precision', () => {
  const result = nativeGeometry({duration_seconds:20, retention:[
    {seconds:0, percent:120, precision:'exact'},
    {seconds:10, percent:60, precision:'estimated'}
  ]});
  assert.equal(result.ceiling, 120);
  assert.equal(result.points[1].x, 455);
  assert.equal(result.points[1].precision, 'estimated');
});

test('detail capture matching isolates platform/post and handles Instagram URL aliases', () => {
  const record = {platform:'Instagram', content_id:'ABC', content_url:'https://www.instagram.com/reel/ABC/'};
  assert.equal(nativeMatches(record, {platform:'Instagram', id:'numeric-id', url:'https://instagram.com/p/ABC/?source=link'}), true);
  assert.equal(nativeMatches(record, {platform:'YouTube', id:'ABC'}), false);
  assert.equal(nativeMatches(record, {platform:'Instagram', id:'DEF', url:'https://instagram.com/reel/DEF/'}), false);
  assert.equal(nativeMatches(record, {platform:'Instagram'}), false);
});

test('native-only posts remain accessible without duplicate content rows', () => {
  const native = {platform:'Instagram', content_id:'ABC', content_url:'https://instagram.com/reel/ABC/', title:'Native'};
  const data = {platforms:[{platform:'Instagram', content:[]}], native_insights:{records:[native, {...native, id:'older-capture'}]}};
  assert.equal(dashboardContentRows(data).length, 1);
  assert.equal(dashboardContentRows(data)[0].native_only, true);
  data.platforms[0].content.push({id:'numeric', url:'https://instagram.com/p/ABC/', title:'API'});
  assert.equal(dashboardContentRows(data).length, 1);
  assert.equal(dashboardContentRows(data)[0].title, 'API');
});

test('summary hierarchy keeps native detail outside main content', () => {
  const fs = require('node:fs');
  const path = require('node:path');
  const html = fs.readFileSync(path.join(__dirname, '../static/index.html'), 'utf8');
  const main = html.split('<main>')[1].split('</main>')[0];
  assert.ok(main.indexOf('<h2>Audience</h2>') < main.indexOf('<h2>Latest content funnels</h2>'));
  assert.ok(main.indexOf('<h2>Latest content funnels</h2>') < main.indexOf('<h2>Content</h2>'));
  assert.ok(!main.includes('id="native-insights"'));
  assert.ok(html.includes('<dialog id="content-dialog"'));
});
