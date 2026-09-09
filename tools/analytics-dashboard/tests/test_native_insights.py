import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('native', Path(__file__).resolve().parents[1] / 'native_insights.py')
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)


def fixture():
    return dict(id='test-1', platform='Instagram', content_id='reel', title='Test',
                format='short', captured_at='2026-09-07T14:00:00Z', period='Lifetime',
                source_surface='Instagram iOS', duration_seconds=20,
                screenshots=[dict(id='retention', path='screen.png', label='Retention')],
                metrics=[dict(key='follows', label='Follows', unit='count', value=None,
                              precision='exact', source='retention')],
                retention=[dict(seconds=0, percent=100, precision='estimated', source='retention')])


class NativeTest(unittest.TestCase):
    def test_provenance_and_curve_validation(self):
        for change in [dict(source='missing'), dict(precision='assumed'), dict(seconds=21), dict(percent=float('nan'))]:
            record = fixture()
            record['retention'][0].update(change)
            with self.assertRaises(ValueError):
                native.validate(record)
        record = fixture()
        record['retention'].append(copy.copy(record['retention'][0]))
        with self.assertRaises(ValueError):
            native.validate(record)

    def test_import_preserves_unknown_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)
            (path / 'screen.png').write_bytes(b'\x89PNG\r\n\x1a\nfixture')
            (path / 'input.json').write_text(json.dumps(fixture()))
            root = path / 'private'
            native.import_record(path / 'input.json', root)
            with self.assertRaises(ValueError):
                native.import_record(path / 'input.json', root)
            data = native.load_records(root)
            self.assertFalse(data['errors'])
            self.assertIsNone(data['records'][0]['metrics'][0]['value'])
            self.assertTrue(native.evidence_file('test-1/screen-0.png', root))
            for relative in ('../screen.png', 'test-1/record.json', 'test-1/missing.png', '/etc/passwd'):
                self.assertIsNone(native.evidence_file(relative, root))
            (root / 'test-1/screen-0.png').unlink()
            (root / 'test-1/screen-0.png').symlink_to(path / 'screen.png')
            self.assertIsNone(native.evidence_file('test-1/screen-0.png', root))

    def test_bad_record_does_not_break_dashboard(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'bad').mkdir()
            (root / 'bad/record.json').write_text('{}')
            data = native.load_records(root)
            self.assertEqual(data['records'], [])
            self.assertEqual(len(data['errors']), 1)

    def test_actual_raster_type_not_filename(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'screenshot.png'
            path.write_bytes(b'\xff\xd8\xfftest')
            self.assertEqual(native.image_type(path), ('image/jpeg', '.jpg'))
            path.write_text('<html>not a screenshot</html>')
            with self.assertRaises(ValueError):
                native.image_type(path)


if __name__ == '__main__':
    unittest.main()
