from copy import deepcopy
import json
from pathlib import Path
import sys
import shutil
import unittest
import uuid
from zipfile import ZipFile
from lxml import etree as E

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from split_book import export, verify_split, partition, sha, VOLUME_KINDS, MANIFEST_NAME
from check_saved_docx import extract, NS, q


BASE = '혼공독해교재_공통영어2_능률(민)_4과'


def fixture(directory):
    specs = [('cover', 'cover_course_title'), ('u1/reading', 'interpretation_header'),
             ('u1/analysis', 'analysis_header'), ('u1/workbook', 'workbook_header'),
             ('u2/reading', 'interpretation_header'), ('u2/analysis', 'analysis_header'),
             ('u2/workbook', 'workbook_header'), ('mock1', 'mock_round_header'),
             ('answers/quick', 'answers_header'), ('u1/answers', 'workbook_answer_unit_heading'),
             ('u2/answers', 'workbook_answer_unit_heading'), ('answers/mock1', 'mock_answers_header')]
    plan = {'schema_version': 1, 'blocks': [{'id': bid, 'elements': [
        {'role': role, 'runs': [{'run': 0, 'text': bid + ' 원문'}]}]} for bid, role in specs]}
    root = E.Element(q('document'), nsmap={'w': NS['w']})
    body = E.SubElement(root, q('body'))
    for block in plan['blocks']:
        sdt = E.SubElement(body, q('sdt'))
        pr = E.SubElement(sdt, q('sdtPr'))
        E.SubElement(pr, q('tag')).set(q('val'), 'gyogwaseo:' + block['id'])
        p = E.SubElement(E.SubElement(sdt, q('sdtContent')), q('p'))
        ppr = E.SubElement(p, q('pPr'))
        E.SubElement(ppr, q('spacing')).set(q('after'), '120')
        run = E.SubElement(p, q('r'))
        rpr = E.SubElement(run, q('rPr'))
        E.SubElement(rpr, q('sz')).set(q('val'), '17')
        E.SubElement(run, q('t')).text = block['elements'][0]['runs'][0]['text']
    section = E.SubElement(body, q('sectPr'))
    E.SubElement(section, q('pgSz')).set(q('w'), '11906')
    source = directory / 'book.docx'
    with ZipFile(source, 'w') as z:
        z.writestr('word/document.xml', E.tostring(root))
        z.writestr('word/styles.xml', b'<styles/>')
        z.writestr('word/footer1.xml', b'<footer>PAGE</footer>')
        z.writestr('word/media/image1.png', b'preserved image bytes')
    plan_path = directory / 'plan.json'
    plan_path.write_text(json.dumps(plan, ensure_ascii=False), encoding='utf-8')
    return source, plan_path, plan


def rewrite_part(path, part, data):
    with ZipFile(path) as z:
        parts = [(i, z.read(i.filename)) for i in z.infolist()]
    with ZipFile(path, 'w') as z:
        for i, old in parts:
            z.writestr(i, data if i.filename == part else old)


class SplitBookTests(unittest.TestCase):
    def setUp(self):
        # Default Windows temp can carry incompatible inherited ACLs. Use an
        # exclusive test-owned directory next to this test and remove only it.
        self.root = Path(__file__).resolve().parent / ('_split_test_' + uuid.uuid4().hex)
        self.root.mkdir()
        def cleanup():
            if self.root.parent == Path(__file__).resolve().parent and self.root.name.startswith('_split_test_'):
                shutil.rmtree(self.root)
        self.addCleanup(cleanup)
        self.source, self.plan_path, self.plan = fixture(self.root)
        self.output = self.root / '출고'

    def create(self):
        return export(self.source, self.plan_path, self.output, BASE)

    def test_exact_five_partition_retains_cover_once_and_no_pdf(self):
        before = self.source.read_bytes()
        result = self.create()
        self.assertEqual([v['kind'] for v in result['volumes']], list(VOLUME_KINDS))
        self.assertEqual(len(list(self.output.glob('*.docx'))), 6)
        self.assertFalse(list(self.output.glob('*.pdf')))
        self.assertEqual(result['volumes'][0]['block_ids'], ['cover', 'u1/reading', 'u2/reading'])
        all_ids = [bid for v in result['volumes'] for bid in v['block_ids']]
        self.assertCountEqual(all_ids, [b['id'] for b in self.plan['blocks']])
        self.assertEqual(len(all_ids), len(set(all_ids)))
        self.assertEqual(self.source.read_bytes(), before)
        self.assertEqual(Path(result['integrated_docx']['path']).read_bytes(), before)
        self.assertEqual(len(list(self.output.glob('*.zip'))), 1)
        self.assertEqual(verify_split(result)['status'], 'SPLIT_CONTENT_MATCH')
        for v in result['volumes'][:4]:
            self.assertFalse(any('answers' in b['id'] for b in extract(v['path'])['blocks']))
        self.assertEqual(result['visual_review'], 'NOT_PERFORMED')

    def test_other_package_parts_and_actual_saved_typography_are_preserved(self):
        result = self.create()
        with ZipFile(self.source) as source:
            for v in result['volumes']:
                with ZipFile(v['path']) as saved:
                    for name in source.namelist():
                        if name != 'word/document.xml':
                            self.assertEqual(source.read(name), saved.read(name))
                    self.assertIn(b'w:val="17"', saved.read('word/document.xml'))

    def test_no_overwrite_any_existing_volume_or_manifest(self):
        result = self.create()
        snapshots = {p: p.read_bytes() for p in self.output.iterdir()}
        with self.assertRaisesRegex(ValueError, 'new-only'):
            self.create()
        self.assertEqual(snapshots, {p: p.read_bytes() for p in self.output.iterdir()})

    def test_source_plan_difference_stops_before_output(self):
        self.plan['blocks'][1]['elements'][0]['runs'][0]['text'] = 'Changed text'
        self.plan_path.write_text(json.dumps(self.plan), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'differs'):
            self.create()
        self.assertFalse(self.output.exists())

    def test_unknown_or_missing_or_duplicate_block_fails_closed(self):
        for mutation in ('unknown', 'missing', 'duplicate'):
            plan = deepcopy(self.plan)
            if mutation == 'unknown':
                plan['blocks'][1]['id'] = 'unmapped'
            elif mutation == 'missing':
                plan['blocks'] = [b for b in plan['blocks'] if not b['id'].endswith('/workbook')]
            else:
                plan['blocks'].append(deepcopy(plan['blocks'][1]))
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                partition(plan)

    def test_answer_role_in_student_block_is_rejected(self):
        self.plan['blocks'][3]['elements'].append({'role': 'question_answer', 'runs': []})
        with self.assertRaisesRegex(ValueError, 'Answer role'):
            partition(self.plan)

    def test_filename_base_validation_and_special_lesson(self):
        for invalid in ('../book', '혼공독해교재_공통영어2_능률(민)_04과', BASE + '.docx', BASE + '*'):
            with self.subTest(base=invalid), self.assertRaises(ValueError):
                export(self.source, self.plan_path, self.output, invalid)
        result = export(self.source, self.plan_path, self.output,
                        '혼공독해교재_공통영어2_능률(민)_SpecialLesson1')
        self.assertIn('SpecialLesson1_03_워크북+변형문제.docx', result['volumes'][2]['filename'])

    def test_saved_body_change_is_detected_even_with_updated_file_hash(self):
        result = self.create()
        volume = result['volumes'][0]
        with ZipFile(volume['path']) as z:
            xml = z.read('word/document.xml').replace('원문'.encode(), '오염'.encode(), 1)
        rewrite_part(volume['path'], 'word/document.xml', xml)
        volume['sha256'] = sha(Path(volume['path']).read_bytes())
        self.assertEqual(verify_split(result)['status'], 'FAIL')

    def test_saved_style_change_is_detected_even_with_updated_file_hash(self):
        result = self.create()
        volume = result['volumes'][3]
        rewrite_part(volume['path'], 'word/styles.xml', b'<changed/>')
        volume['sha256'] = sha(Path(volume['path']).read_bytes())
        self.assertEqual(verify_split(result)['status'], 'FAIL')

    def test_integrated_delivery_tampering_is_detected(self):
        result = self.create()
        Path(result['integrated_docx']['path']).write_bytes(b'different integrated book')
        self.assertEqual(verify_split(result)['status'], 'FAIL')

    def test_corrupt_volume_is_reported_as_failure_without_verifier_crash(self):
        result = self.create()
        volume = result['volumes'][2]
        Path(volume['path']).write_bytes(b'not a ZIP')
        volume['sha256'] = sha(b'not a ZIP')
        self.assertEqual(verify_split(result)['status'], 'FAIL')

    def test_manifest_tampering_or_path_reuse_is_detected(self):
        result = self.create()
        for field in ('coverage', 'roles', 'path', 'blocks'):
            tampered = deepcopy(result)
            if field == 'coverage':
                tampered['source_coverage'].pop()
            elif field == 'roles':
                tampered['volumes'][0]['kind'] = 'answers'
            elif field == 'path':
                tampered['volumes'][0]['path'] = tampered['volumes'][4]['path']
            else:
                tampered['volumes'][0]['block_ids'].append('answers/quick')
            with self.subTest(field=field):
                self.assertEqual(verify_split(tampered)['status'], 'FAIL')

    def test_source_or_plan_hash_change_invalidates_split(self):
        result = self.create()
        self.plan_path.write_text(self.plan_path.read_text(encoding='utf-8') + ' ', encoding='utf-8')
        self.assertEqual(verify_split(result)['status'], 'FAIL')

    def test_custom_xml_or_unmanaged_content_is_not_silently_copied(self):
        with ZipFile(self.source, 'a') as z:
            z.writestr('customXml/item1.xml', '<answers>hidden answers</answers>')
        with self.assertRaisesRegex(ValueError, 'hidden/embedded'):
            self.create()
        self.assertFalse(self.output.exists())

    def test_manifest_is_saved_internal_record_not_release_approval(self):
        result = self.create()
        saved = json.loads((self.output / MANIFEST_NAME).read_text(encoding='utf-8'))
        self.assertEqual(saved, result)
        self.assertEqual(saved['release_authorization'], 'NOT_PERFORMED')
        self.assertEqual(saved['saved_validation']['status'], 'SPLIT_CONTENT_MATCH')

    def test_delivery_zip_contains_exactly_six_docx_and_round_trips_bytes(self):
        result = self.create()
        entries = [result['integrated_docx']] + result['volumes']
        with ZipFile(result['delivery_zip']['path']) as archive:
            self.assertEqual(archive.namelist(), [entry['filename'] for entry in entries])
            self.assertTrue(all(name.endswith('.docx') for name in archive.namelist()))
            self.assertIsNone(archive.testzip())
            for entry in entries:
                self.assertEqual(archive.read(entry['filename']), Path(entry['path']).read_bytes())

    def test_zip_entry_tamper_is_detected_even_after_zip_hash_refresh(self):
        result = self.create()
        archive = result['delivery_zip']
        rewrite_part(archive['path'], result['volumes'][0]['filename'], b'different DOCX')
        archive['sha256'] = sha(Path(archive['path']).read_bytes())
        self.assertEqual(verify_split(result)['status'], 'FAIL')

    def test_zip_extra_pdf_or_unsafe_entry_is_rejected(self):
        for extra in ('internal.pdf', '../outside.docx'):
            result = export(self.source, self.plan_path, self.output / str(len(extra)), BASE)
            archive = result['delivery_zip']
            with ZipFile(archive['path'], 'a') as z:
                z.writestr(extra, b'not an authorized delivery')
            archive['sha256'] = sha(Path(archive['path']).read_bytes())
            with self.subTest(extra=extra):
                self.assertEqual(verify_split(result)['status'], 'FAIL')


if __name__ == '__main__':
    unittest.main()
