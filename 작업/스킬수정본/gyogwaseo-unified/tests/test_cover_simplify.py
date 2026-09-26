"""Approved compact cover and conservative body-logo relationship regression.

Fixtures are synthetic layout data. These tests do not evaluate real textbook
content or claim a Word pagination/visual review. The legacy-package fixture is
constructed locally so this module also runs from a standalone skill archive.
"""
from copy import deepcopy
import hashlib
from pathlib import Path
import sys
import unittest
import uuid
from zipfile import ZipFile

from lxml import etree as E

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / '../scripts'))
from book_plan import compile_plan
from check_saved_docx import check
from master_docx import NS, RoleBank, block_index, tag, write
from test_book_plan import fixture
from verify_release import runtime_file

REL_PART = 'word/_rels/document.xml.rels'
LOGO_PART = 'word/media/image1.png'
REL_ID = 'rIdCoverLogo'
REL_NS = 'http://schemas.openxmlformats.org/package/2006/relationships'
DRAW_NS = {
    **NS,
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}
IMAGE_TYPE = DRAW_NS['r'] + '/image'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text(element):
    return ''.join(run['text'] for run in element.get('runs', []))


def cover_fixture(special=False):
    data = fixture()
    data['metadata'].update(course='공통영어2', publisher_author='능률(민병천)',
                            lesson='SL01' if special else 'UNIT04')
    data['cover'].update(lesson_label='SPECIAL LESSON' if special else 'LESSON',
                         lesson_number='01' if special else '04')
    return data


def cover_plan(special=False):
    complete = compile_plan(cover_fixture(special), 'learning')
    return {'blocks': [next(b for b in complete['blocks'] if b['id'] == 'cover')]}


class CompactCoverTests(unittest.TestCase):
    def setUp(self):
        self.bank = RoleBank()
        # Use the package inventory's existing runtime-directory contract.
        # Automatic recursive cleanup can stall on the Windows sandbox ACL.
        self.directory = HERE / ('master-test-' + uuid.uuid4().hex)
        self.assertTrue(runtime_file(Path('tests') / self.directory.name / 'cover.docx'),
                        'Synthetic cover files must never enter the skill package inventory')
        self.directory.mkdir()

    def package(self, path):
        with ZipFile(path) as z:
            return {item.filename: z.read(item.filename) for item in z.infolist()}

    def put_package(self, path, parts):
        with ZipFile(path, 'w') as z:
            for info, original in self.bank.package:
                z.writestr(info, parts.get(info.filename, original))

    def legacy_file(self):
        """Old managed cover, preserved body, existing logo, no body-logo rel."""
        parts = {info.filename: value for info, value in self.bank.package}
        rels = E.fromstring(parts[REL_PART])
        for rel in list(rels):
            if rel.get('Id') == REL_ID:
                rels.remove(rel)
        parts[REL_PART] = E.tostring(rels, xml_declaration=True, encoding='UTF-8', standalone=True)
        root = deepcopy(self.bank.root)
        body = root.find('w:body', NS)
        section = deepcopy(body.find('w:sectPr', NS))
        for node in list(body):
            body.remove(node)
        for identity, value in [('cover', '이전 표지'), ('preserve', '수정하지 않는 본문')]:
            body.append(self.bank.block({'id': identity, 'elements': [
                {'role': 'analysis_prose', 'runs': [{'run': 0, 'text': value}]}]}))
        body.append(section)
        parts['word/document.xml'] = E.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
        target = self.directory / 'legacy.docx'
        self.put_package(target, parts)
        return target

    def patch(self, target):
        return write(cover_plan(), target, 'patch', digest(target))

    def saved_cover(self):
        target = self.directory / 'cover.docx'
        plan = cover_plan()
        write(plan, target)
        return plan, target

    def mutate_saved(self, target, mutate):
        parts = self.package(target)
        mutate(parts)
        changed = self.directory / ('changed-' + uuid.uuid4().hex + '.docx')
        self.put_package(changed, parts)
        return changed

    def assert_saved_rejected(self, plan, target):
        result = check(plan, target)
        self.assertEqual(result['status'], 'FAIL')
        self.assertEqual(result['format_validation'], 'FAIL')
        self.assertTrue(result['format_errors'])

    def test_cover_order_removes_separate_lesson_and_brand_rows(self):
        data = cover_fixture()
        original = deepcopy(data)
        cover = compile_plan(data, 'learning')['blocks'][0]
        roles = [row['role'] for row in cover['elements']]
        self.assertEqual(cover['id'], 'cover')
        self.assertEqual(roles[:4], ['cover_logo', 'cover_series_title',
                                    'cover_course_title', 'cover_publisher_large'])
        self.assertNotIn('runs', cover['elements'][0])
        for removed in ('cover_brand', 'cover_lesson_label', 'cover_lesson_number', 'cover_publisher'):
            self.assertNotIn(removed, roles)
        self.assertEqual(text(cover['elements'][1]), '혼공교재 독해편')
        self.assertEqual(text(cover['elements'][2]), '공통영어2')
        self.assertNotIn('혼공교재', text(cover['elements'][2]))
        self.assertEqual(text(cover['elements'][3]), '능률(민병천)  ·  4과')
        self.assertNotIn('04', text(cover['elements'][3]))
        self.assertNotIn('\n', text(cover['elements'][3]))
        self.assertEqual(data, original)

    def test_special_lesson_identity_is_retained_without_padded_number(self):
        rows = cover_plan(special=True)['blocks'][0]['elements']
        publisher = next(text(row) for row in rows if row['role'] == 'cover_publisher_large')
        self.assertEqual(publisher, '능률(민병천)  ·  Special Lesson 1')
        self.assertNotIn('01', publisher)
        self.assertNotIn('\n', publisher)

    def test_static_logo_has_exact_approved_size_and_relationship(self):
        paragraph = self.bank.paragraph('cover_logo')
        drawing = paragraph.find('.//w:drawing', DRAW_NS)
        self.assertIsNotNone(drawing)
        extents = drawing.findall('.//wp:extent', DRAW_NS)
        self.assertEqual(len(extents), 1)
        self.assertEqual((int(extents[0].get('cx')), int(extents[0].get('cy'))),
                         (108 * 12700, 72 * 12700))
        self.assertEqual(drawing.xpath('.//a:blip/@r:embed', namespaces=DRAW_NS), [REL_ID])
        self.assertEqual(paragraph.xpath('.//w:t/text()', namespaces=NS), [])
        with self.assertRaises(ValueError):
            self.bank.paragraph('cover_logo', [{'run': 0, 'text': '다른 로고'}])

    def test_series_and_publisher_use_approved_readable_sizes(self):
        series = self.bank.paragraph('cover_series_title', [{'run': 0, 'text': '혼공교재 독해편'}])
        props = series.find('w:r/w:rPr', NS)
        self.assertEqual(props.find('w:sz', NS).get(tag('val')), '28')
        self.assertEqual(props.find('w:color', NS).get(tag('val')), '203864')
        bold = props.find('w:b', NS)
        self.assertIsNotNone(bold)
        self.assertNotIn(bold.get(tag('val'), '1').lower(), ('0', 'false', 'off'))
        publisher = self.bank.paragraph('cover_publisher_large', [{'run': 0, 'text': '능률(민병천) · 4과'}])
        self.assertEqual(publisher.find('w:r/w:rPr/w:sz', NS).get(tag('val')), '28')
        spacing = publisher.find('w:pPr/w:spacing', NS)
        self.assertNotEqual(spacing.get(tag('lineRule'), 'auto'), 'auto')
        self.assertGreaterEqual(int(spacing.get(tag('line'))), 364)

    def test_fresh_cover_passes_saved_text_and_format_checks(self):
        plan, target = self.saved_cover()
        result = check(plan, target)
        self.assertEqual(result['status'], 'SAVED_CONTENT_MATCH')
        self.assertEqual(result['format_validation'], 'PASS')
        self.assertEqual(result['errors'], [])

    def test_patch_imports_only_approved_relationship_and_preserves_other_parts(self):
        target = self.legacy_file()
        before = self.package(target)
        asset_hash = digest(self.bank.reference)
        before_root = E.fromstring(before['word/document.xml'])
        kept = E.tostring(block_index(before_root.find('w:body', NS))['preserve'])
        report = self.patch(target)
        after = self.package(target)
        self.assertEqual(report['other_package_parts'], 'PRESERVED_EXCEPT_APPROVED_COVER_IMAGE_RELATIONSHIP')
        self.assertEqual(report['approved_relationship_migrations'], [REL_PART])
        self.assertEqual(set(after), set(before))
        for part in before:
            if part not in {'word/document.xml', REL_PART}:
                self.assertEqual(after[part], before[part], part)
        old_rels = {r.get('Id'): dict(r.attrib) for r in E.fromstring(before[REL_PART])}
        new_rels = {r.get('Id'): dict(r.attrib) for r in E.fromstring(after[REL_PART])}
        self.assertEqual(set(new_rels) - set(old_rels), {REL_ID})
        self.assertEqual({key: new_rels[key] for key in old_rels}, old_rels)
        self.assertEqual(new_rels[REL_ID]['Target'], 'media/image1.png')
        self.assertEqual(new_rels[REL_ID]['Type'], IMAGE_TYPE)
        self.assertEqual(new_rels[REL_ID].get('TargetMode', 'Internal'), 'Internal')
        after_root = E.fromstring(after['word/document.xml'])
        self.assertEqual(E.tostring(block_index(after_root.find('w:body', NS))['preserve']), kept)
        self.assertEqual(digest(self.bank.reference), asset_hash)
        self.assertEqual(check(cover_plan(), target, 'targeted')['status'], 'SAVED_CONTENT_MATCH')

    def test_repeat_patch_keeps_already_approved_relationship_bytes(self):
        target = self.legacy_file()
        self.patch(target)
        before = self.package(target)
        self.patch(target)
        after = self.package(target)
        self.assertEqual(after[REL_PART], before[REL_PART])
        self.assertEqual(after[LOGO_PART], before[LOGO_PART])
        rels = [r for r in E.fromstring(after[REL_PART]) if r.get('Id') == REL_ID]
        self.assertEqual(len(rels), 1)

    def test_conflicting_logo_relationship_refuses_patch_without_saving(self):
        for field, value in [('Target', 'media/wrong-logo.png'), ('Type', IMAGE_TYPE + '-wrong'),
                             ('TargetMode', 'External')]:
            with self.subTest(field=field):
                target = self.legacy_file()
                parts = self.package(target)
                rels = E.fromstring(parts[REL_PART])
                attrs = {'Id': REL_ID, 'Type': IMAGE_TYPE, 'Target': 'media/image1.png'}
                attrs[field] = value
                E.SubElement(rels, '{' + REL_NS + '}Relationship', attrs)
                parts[REL_PART] = E.tostring(rels, xml_declaration=True, encoding='UTF-8', standalone=True)
                self.put_package(target, parts)
                before = target.read_bytes()
                with self.assertRaises(ValueError):
                    self.patch(target)
                self.assertEqual(target.read_bytes(), before)

    def test_wrong_existing_media_refuses_patch_without_replacing_original(self):
        target = self.legacy_file()
        parts = self.package(target)
        parts[LOGO_PART] = b'not-the-approved-logo'
        self.put_package(target, parts)
        before = target.read_bytes()
        with self.assertRaises(ValueError):
            self.patch(target)
        self.assertEqual(target.read_bytes(), before)

    def test_saved_checker_detects_missing_cover_drawing(self):
        plan, target = self.saved_cover()
        def mutate(parts):
            root = E.fromstring(parts['word/document.xml'])
            drawing = root.find('.//w:drawing', NS)
            drawing.getparent().remove(drawing)
            parts['word/document.xml'] = E.tostring(root, encoding='UTF-8')
        self.assert_saved_rejected(plan, self.mutate_saved(target, mutate))

    def test_saved_checker_detects_body_logo_relationship_retarget(self):
        plan, target = self.saved_cover()
        def mutate(parts):
            rels = E.fromstring(parts[REL_PART])
            next(r for r in rels if r.get('Id') == REL_ID).set('Target', 'media/wrong-logo.png')
            parts[REL_PART] = E.tostring(rels, encoding='UTF-8')
        self.assert_saved_rejected(plan, self.mutate_saved(target, mutate))

    def test_saved_checker_detects_missing_body_logo_relationship(self):
        plan, target = self.saved_cover()
        def mutate(parts):
            rels = E.fromstring(parts[REL_PART])
            rels.remove(next(r for r in rels if r.get('Id') == REL_ID))
            parts[REL_PART] = E.tostring(rels, encoding='UTF-8')
        self.assert_saved_rejected(plan, self.mutate_saved(target, mutate))

    def test_saved_checker_detects_logo_media_corruption(self):
        plan, target = self.saved_cover()
        def mutate(parts):
            parts[LOGO_PART] = parts[LOGO_PART] + b'changed'
        self.assert_saved_rejected(plan, self.mutate_saved(target, mutate))


if __name__ == '__main__':
    unittest.main()
