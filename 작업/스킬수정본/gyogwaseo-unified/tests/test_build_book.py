from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
import unittest
import uuid
from zipfile import ZipFile

from lxml import etree as E

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'scripts'))
from build_book import build, file_hash, patch_blocks
from book_plan import compile_plan
from master_docx import NS, tag, block_index, write
from test_book_plan import fixture


class BuildBookTests(unittest.TestCase):
    def setUp(self):
        self.folder = HERE / ('build-book-test-' + uuid.uuid4().hex)
        self.folder.mkdir()
        self.docx = self.folder / 'cumulative.docx'
        self.data = fixture()

    def run_build(self, data=None, **kwargs):
        suffix = uuid.uuid4().hex
        return build(data or self.data, self.docx, self.folder / (suffix + '-plan.json'),
                     self.folder / (suffix + '-report.json'), **kwargs)

    def package(self):
        with ZipFile(self.docx) as archive:
            return {x.filename: archive.read(x.filename) for x in archive.infolist()}

    def blocks(self):
        root = E.fromstring(self.package()['word/document.xml'])
        return {key: E.tostring(value) for key, value in block_index(root.find('w:body', NS)).items()}

    def mutate(self, callback):
        parts = self.package()
        root = E.fromstring(parts['word/document.xml'])
        callback(root)
        parts['word/document.xml'] = E.tostring(root, encoding='UTF-8', xml_declaration=True, standalone=True)
        with ZipFile(self.docx, 'w') as archive:
            for name, value in parts.items():
                archive.writestr(name, value)

    def test_learning_to_full_patches_only_changes_and_preserves_others(self):
        learning = deepcopy(self.data)
        del learning['assessment']
        del learning['question_sources']
        first = self.run_build(learning, scope='learning')
        before = self.blocks()
        parts_before = self.package()
        final = self.run_build(scope='full', mode='patch', expected_sha256=first['saved_sha256'])
        after = self.blocks()
        canonical_ids = [x['id'] for x in compile_plan(self.data)['blocks']]
        self.assertEqual(list(after), canonical_ids)
        self.assertEqual(final['preserved_blocks'], ['u1/reading', 'u1/analysis'])
        for key in final['preserved_blocks']:
            self.assertEqual(before[key], after[key])
        for part, value in parts_before.items():
            if part != 'word/document.xml':
                self.assertEqual(self.package()[part], value)
        self.assertEqual(final['status'], 'BUILT_NOT_FINAL')
        self.assertEqual(final['saved_docx_validation']['format_validation'], 'PASS')
        self.assertEqual(final['word_visual_review'], 'NOT_PERFORMED')
        saved_plan = json.loads(Path(final['plan_output']).read_text(encoding='utf-8'))
        self.assertEqual([x['id'] for x in saved_plan['blocks']], canonical_ids)
        self.assertEqual(json.loads(Path(final['report_output']).read_text(encoding='utf-8'))['saved_sha256'], file_hash(self.docx))

    def test_create_refuses_existing_target_without_change(self):
        self.docx.write_bytes(b'user original')
        with self.assertRaisesRegex(ValueError, 'existing DOCX'):
            self.run_build()
        self.assertEqual(self.docx.read_bytes(), b'user original')

    def test_stale_hash_refuses_patch(self):
        self.run_build(scope='learning')
        before = self.docx.read_bytes()
        with self.assertRaisesRegex(ValueError, 'version changed'):
            self.run_build(mode='patch', expected_sha256='0' * 64)
        self.assertEqual(self.docx.read_bytes(), before)

    def test_unchanged_patch_keeps_docx_bytes(self):
        first = self.run_build(scope='learning')
        before = self.docx.read_bytes()
        result = self.run_build(scope='learning', mode='patch', expected_sha256=first['saved_sha256'])
        self.assertEqual(result['changed_blocks'], [])
        self.assertEqual(self.docx.read_bytes(), before)

    def test_format_only_difference_selects_that_block(self):
        self.run_build(scope='learning')
        def change(root):
            blocks = block_index(root.find('w:body', NS))
            rpr = blocks['u1/reading'].find('.//w:r/w:rPr', NS)
            node = rpr.find('w:color', NS)
            if node is None:
                node = E.SubElement(rpr, tag('color'))
            node.set(tag('val'), 'FF0000')
        self.mutate(change)
        before = self.blocks()
        result = self.run_build(scope='learning', mode='patch', expected_sha256=file_hash(self.docx))
        self.assertEqual(result['changed_blocks'], ['u1/reading'])
        self.assertEqual(self.blocks()['u1/analysis'], before['u1/analysis'])
        self.assertEqual(result['saved_docx_validation']['format_validation'], 'PASS')

    def test_unmanaged_content_requires_migration(self):
        self.run_build(scope='learning')
        def change(root):
            body = root.find('w:body', NS)
            p = E.Element(tag('p'))
            E.SubElement(E.SubElement(p, tag('r')), tag('t')).text = 'Unreviewed original'
            body.insert(0, p)
        self.mutate(change)
        before = self.docx.read_bytes()
        with self.assertRaisesRegex(ValueError, 'Unmanaged'):
            self.run_build(scope='learning', mode='patch', expected_sha256=file_hash(self.docx))
        self.assertEqual(self.docx.read_bytes(), before)

    def test_reordering_is_not_automatically_fixed(self):
        self.run_build(scope='learning')
        def change(root):
            body = root.find('w:body', NS)
            first = body[0]
            body.remove(first)
            body.insert(1, first)
        self.mutate(change)
        before = self.docx.read_bytes()
        with self.assertRaisesRegex(ValueError, 'order'):
            self.run_build(scope='learning', mode='patch', expected_sha256=file_hash(self.docx))
        self.assertEqual(self.docx.read_bytes(), before)

    def test_sidecars_are_exclusive_and_paths_must_differ(self):
        plan = self.folder / 'plan.json'
        report = self.folder / 'report.json'
        plan.write_text('user existing plan', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'already exist'):
            build(self.data, self.docx, plan, report)
        self.assertFalse(self.docx.exists())
        self.assertEqual(plan.read_text(encoding='utf-8'), 'user existing plan')
        with self.assertRaisesRegex(ValueError, 'different'):
            build(self.data, self.docx, report, report)

    def test_input_path_collision_is_rejected(self):
        source = self.folder / 'input.json'
        source.write_text(json.dumps(self.data, ensure_ascii=False), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'input manuscript'):
            build(self.data, self.docx, source, self.folder / 'report.json', input_path=source)
        self.assertFalse(self.docx.exists())

    def test_middle_and_tail_insertions_use_canonical_anchors(self):
        def block(key):
            return {'id': key, 'elements': [{'role': 'analysis_prose', 'runs': [{'run': 0, 'text': key}]}]}
        old = {'blocks': [block(x) for x in ('cover', 'u1/reading', 'u2/reading')]}
        keys = ['cover', 'u1/reading', 'u1/workbook', 'u2/reading', 'mock1', 'mock2']
        new = {'blocks': [block(x) for x in keys]}
        initial = write(old, self.docx)
        before = self.blocks()
        updates, preserved = patch_blocks(new, self.docx)
        self.assertEqual(updates[0]['insert_before'], 'u2/reading')
        self.assertEqual(updates[1]['insert_after'], 'u2/reading')
        self.assertEqual(updates[2]['insert_after'], 'mock1')
        write({'blocks': updates}, self.docx, mode='patch', expected_sha256=initial['sha256'])
        after = self.blocks()
        self.assertEqual(list(after), keys)
        self.assertTrue(all(after[key] == before[key] for key in preserved))

    def test_global_margin_change_is_not_silently_rebuilt(self):
        self.run_build(scope='learning')
        self.mutate(lambda root: root.find('.//w:sectPr/w:pgMar', NS).set(tag('top'), '2000'))
        before = self.docx.read_bytes()
        with self.assertRaisesRegex(ValueError, 'global formatting'):
            self.run_build(scope='learning', mode='patch', expected_sha256=file_hash(self.docx))
        self.assertEqual(self.docx.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
