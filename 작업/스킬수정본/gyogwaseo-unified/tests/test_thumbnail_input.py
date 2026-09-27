"""Exercise the original input consumers without requiring Pillow or fonts."""
import ast
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from contextlib import contextmanager
from uuid import uuid4
import unittest

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / '../scripts'))
from test_promotion import sample
from convert_thumbnail_input import convert, legacy_title


@contextmanager
def working_directory():
    # Keep generated test artifacts under tests, as the package runner does.
    directory = ROOT / "thumbnail-input-test" / uuid4().hex
    directory.mkdir(parents=True)
    yield directory


def original_consumers():
    path = ROOT / '../scripts/build_thumbnail.py'
    tree = ast.parse(path.read_text(encoding='utf-8'))
    names = {'parse_meta', 'clean', 'pick_sentence', 'stats'}
    constants = {'MIN_CHUNKS', 'MIN_GLOSS', 'SENT_MIN', 'SENT_MAX'}
    nodes = [n for n in tree.body if
             (isinstance(n, ast.FunctionDef) and n.name in names) or
             (isinstance(n, ast.Assign) and any(isinstance(x, ast.Name) and x.id in constants
                                               for x in ast.walk(n.targets[0])))]
    namespace = {'re': re}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), namespace)
    return namespace


class ThumbnailInputTests(unittest.TestCase):
    def test_original_title_counts_and_preview(self):
        data = sample()
        data['metadata'].update(course='공통영어2', publisher_author='YBM(박준언)', lesson='UNIT04')
        converted = convert(data)
        original = original_consumers()
        self.assertEqual(original['parse_meta'](converted), ('공통영어2', 'YBM(박준언)', '4과'))
        self.assertEqual(original['stats'](converted),
                         (3, sum(len(s['glosses']) for s in data['sentences'])))
        self.assertEqual(original['pick_sentence'](converted)['chunks'],
                         ['They repair useful tools', 'to protect local resources.'])

    def test_all_glosses_stars_referents_and_source_order_preserved(self):
        data = sample()
        before = deepcopy(data)
        converted = convert(data)
        rows = converted['sections'][0]['sentences']
        for sentence, row in zip(data['sentences'], rows):
            expected = [[g['headword'], g['meaning_ko'] +
                         (' (' + g['referent_ko'] + ')' if g.get('referent_ko') else ''), g['star']]
                        for g in sentence['glosses']]
            self.assertEqual(row['gloss'], expected)
        self.assertEqual(data, before)

    def test_only_approved_copy_changed_and_logo_unchanged(self):
        code = (ROOT.parent / 'scripts/build_thumbnail.py').read_bytes()
        self.assertEqual(code.count('분석지 해석 수록'.encode('utf-8')), 1)
        self.assertNotIn('모범 해석 수록'.encode('utf-8'), code)
        restored = code.replace('분석지 해석 수록'.encode('utf-8'), '모범 해석 수록'.encode('utf-8'))
        self.assertEqual(hashlib.sha256(restored).hexdigest(),
                         'c7c2436ee53bd725913193a0ad07fcb7421e51c0892ba31074f36472c695ca40')
        for name, digest in {
            'assets/logo-horizontal.png': '3ef55a70160bf49a178b984cb1813a01af4581dd07c72618034d63e303d61360'
        }.items():
            self.assertEqual(hashlib.sha256((ROOT.parent / name).read_bytes()).hexdigest(), digest)

    def test_invalid_and_missing_source_content_rejected(self):
        for field in ('sources', 'sentences'):
            data = sample()
            data[field] = []
            with self.subTest(field=field), self.assertRaises(ValueError):
                convert(data)
        data = sample()
        data['sentences'][0]['text'] = 'Changed original.'
        with self.assertRaises(ValueError):
            convert(data)

    def test_unrepresentable_title_rejected(self):
        for field, value in [('course', '공통 영어2'), ('publisher_author', 'YBM · 박준언'),
                             ('lesson', 'Special Reading')]:
            metadata = sample()['metadata']
            metadata[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                legacy_title(metadata)

    def test_numbered_lesson_labels(self):
        for label in ('UNIT04', 'LESSON04', '4과', '제 4과'):
            metadata = sample()['metadata']
            metadata['lesson'] = label
            self.assertTrue(legacy_title(metadata).endswith(' 4과'))

    def test_cli_writes_readable_json_and_refuses_overwrite(self):
        with working_directory() as temp:
            source, output = Path(temp) / 'input.json', Path(temp) / 'legacy.json'
            source.write_text(json.dumps(sample(), ensure_ascii=False), encoding='utf-8-sig')
            command = [sys.executable, str(ROOT / '../scripts/convert_thumbnail_input.py'),
                       str(source), str(output)]
            first = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(first.returncode, 0, first.stderr)
            saved = output.read_bytes()
            self.assertEqual(json.loads(saved), convert(sample()))
            second = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
            self.assertNotEqual(second.returncode, 0)
            self.assertEqual(output.read_bytes(), saved)

    def test_cli_invalid_input_leaves_no_output(self):
        with working_directory() as temp:
            source, output = Path(temp) / 'input.json', Path(temp) / 'legacy.json'
            source.write_text('{}', encoding='utf-8')
            result = subprocess.run([sys.executable, str(ROOT / '../scripts/convert_thumbnail_input.py'),
                                     str(source), str(output)], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
