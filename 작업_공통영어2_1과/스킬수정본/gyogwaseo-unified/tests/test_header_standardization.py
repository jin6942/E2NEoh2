"""Cross-book header consistency and retirement of the yellow introduction."""
from copy import deepcopy
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from zipfile import ZipFile

from lxml import etree as E

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / '../scripts'))
from book_plan import compile_plan
from check_learning_content import check as check_learning
from check_saved_docx import check as check_saved
from export_handoff import render
from master_docx import write, NS
from test_book_plan import fixture
from test_learning_content import fixture as learning_fixture


def content(row):
    return ''.join(run['text'] for run in row.get('runs', []))


def two_unit_fixture():
    data = learning_fixture(['They repair useful tools.'] * 14)
    data['cover'] = fixture()['cover']
    base = deepcopy(data['units'][0])
    data['paragraphs'], data['units'] = [], []
    for i in range(2):
        ids = [f's{j}' for j in range(i * 7 + 1, i * 7 + 8)]
        pid = f'p{i + 1}'
        data['paragraphs'].append({'id': pid, 'source_id': 'src',
                                  'subheading_id': 'h1', 'sentence_ids': ids})
        unit = deepcopy(base)
        unit.update(id=f'u{i + 1}', paragraph_ids=[pid], sentence_ids=ids,
                    hook=f'출력되면 안 되는 예전 질문 {i + 1}')
        unit['analysis']['flow'] = [{'sentence_ids': ids, 'text_ko': '시험용 흐름'}]
        for field in ['easy_explanations', 'grammar_points']:
            for row, sid in zip(unit['analysis'][field], ids):
                row['sentence_id'] = sid
        unit.pop('workbook')
        if i:
            unit['today_words'] = []
        data['units'].append(unit)
    for sentence in data['sentences']:
        sentence['key'] = sentence['id'] in {'s1', 's2', 's8', 's9'}
    return data


class HeaderStandardizationTests(unittest.TestCase):
    def test_lesson_headers_ignore_legacy_book_filename_and_normalize_known_aliases(self):
        for number, old_book, publisher, label in [
                (1, '공통영어2_NE능률(민병천)', 'NE능률(민병천)', '교과서 본문'),
                (2, '공통영어2_NE능률(민병천)', 'NE능률(민병천)', '본문'),
                (3, '공통영어2_NE능률(민병천)', '능률(민병천)', '교과서 본문'),
                (4, '공통영어2 능률(민병천)', ' NE 능률 (민병천) ', '본문')]:
            with self.subTest(lesson=number):
                data = fixture()
                data['metadata'].update(book_name=old_book, course='공통영어2',
                                        publisher_author=publisher, lesson=f'UNIT{number:02d}')
                data['assessment']['scope']['course'] = '공통영어2'
                data['cover']['lesson_number'] = f'{number:02d}'
                data['sources'][0]['label'] = label
                before = deepcopy(data)
                rows = next(b['elements'] for b in compile_plan(data)['blocks'] if b['id'] == 'u1/reading')
                self.assertEqual(content(rows[0]), f'공통영어2 NE능률(민병천) · {number}과 혼공해석지')
                self.assertEqual(content(rows[1]), '문단 1 · 본문 · 문장 1~3')
                out = render(data)
                for key in ['learning', 'assessment']:
                    self.assertIn('[교재명] 공통영어2 NE능률(민병천)\n', out[key])
                    self.assertNotIn('교과서 본문 · 원문 문장', out[key])
                self.assertEqual(data, before)

    def test_special_lesson_and_english_two_display_preserve_identity(self):
        data = fixture()
        data['metadata'].update(course='영어Ⅱ', publisher_author='YBM(박준언)', lesson='SL01')
        data['cover'].update(lesson_label='SPECIAL LESSON', lesson_number='01')
        rows = next(b['elements'] for b in compile_plan(data, 'learning')['blocks'] if b['id'] == 'u1/reading')
        self.assertEqual(content(rows[0]), '영어2 YBM(박준언) · Special Lesson 1 혼공해석지')
        self.assertIn('[UNIT] SL01', render(data, 'learning')['learning'])

    def test_distinct_source_and_other_publisher_names_are_not_replaced(self):
        data = fixture()
        data['metadata'].update(course='공통영어2', publisher_author='YBM(박준언)')
        data['assessment']['scope']['course'] = '공통영어2'
        data['sources'][0]['label'] = 'Further Reading'
        before = deepcopy(data)
        rows = next(b['elements'] for b in compile_plan(data)['blocks'] if b['id'] == 'u1/reading')
        self.assertEqual(content(rows[0]), '공통영어2 YBM(박준언) · 0과 혼공해석지')
        self.assertIn('Further Reading · 문장', content(rows[1]))
        self.assertEqual(data, before)

    def test_legacy_hook_cannot_reappear_in_docx_plan_or_either_handoff(self):
        data = fixture()
        baseline_plan, baseline_handoff = compile_plan(data), render(data)
        for hook in ['옛 도입 질문은 나타나면 안 됩니다.', '', None]:
            with self.subTest(hook=hook):
                data['units'][0]['hook'] = hook
                before = deepcopy(data)
                # Full output equality also rules out an orphan empty hook paragraph.
                self.assertEqual(compile_plan(data), baseline_plan)
                self.assertEqual(render(data), baseline_handoff)
                self.assertEqual(data, before)

    def test_hook_is_not_required_in_learning_or_full_scope(self):
        data = fixture()
        data['units'][0].pop('hook', None)
        for scope in ['learning', 'full']:
            with self.subTest(scope=scope):
                self.assertEqual(check_learning(data, scope)['status'], 'STRUCTURE_PASS')
                self.assertFalse(any(e['role'] == 'unit_hook' for b in compile_plan(data, scope)['blocks']
                                     for e in b['elements']))

    def test_every_unit_has_same_header_order_and_only_first_has_common_guide(self):
        data = two_unit_fixture()
        plan = compile_plan(data, 'learning')
        rows = [b['elements'] for b in plan['blocks'] if b['id'].endswith('/reading')]
        base_roles = ['interpretation_header', 'unit_source_range', 'unit_topic_english']
        guides = ['guide_reading', 'guide_symbols', 'guide_heading',
                  'guide_item_one', 'guide_item_two', 'guide_item_three']
        self.assertEqual([e['role'] for e in rows[0][:11]],
                         base_roles + ['interpretation_guide_gap'] + guides + ['interpretation_rule'])
        self.assertEqual([e['role'] for e in rows[1][:4]], base_roles + ['interpretation_rule'])
        handoff = render(data, 'learning')['learning']
        self.assertNotIn('[흥미 훅]', handoff)
        self.assertNotIn('출력되면 안 되는 예전 질문', handoff)

    def test_saved_docx_omits_hook_and_keeps_existing_heading_typography(self):
        data = fixture()
        data['units'][0]['hook'] = '이전 원고의 노란 질문'
        plan = compile_plan(data)
        with TemporaryDirectory(prefix='textbook-header-') as folder:
            path = Path(folder) / 'probe.docx'
            write(plan, path)
            self.assertEqual(check_saved(plan, path)['status'], 'SAVED_CONTENT_MATCH')
            with ZipFile(path) as z:
                root = E.fromstring(z.read('word/document.xml'))
        text = ''.join(root.xpath('//w:t/text()', namespaces=NS))
        self.assertNotIn('이전 원고의 노란 질문', text)
        self.assertNotIn('잠깐, 이 글은', text)
        paragraphs = root.findall('.//w:p', NS)
        guide_at = next(i for i, p in enumerate(paragraphs)
                        if ''.join(p.xpath('.//w:t/text()', namespaces=NS)).startswith('읽는 법'))
        self.assertEqual(''.join(paragraphs[guide_at - 1].xpath('.//w:t/text()', namespaces=NS)), '')
        self.assertIn(data['units'][0]['analysis']['title_or_topic_en'],
                      ''.join(paragraphs[guide_at - 2].xpath('.//w:t/text()', namespaces=NS)))
        gap = paragraphs[guide_at - 1]
        self.assertEqual(gap.find('w:pPr/w:spacing', NS).get('{' + NS['w'] + '}line'), '236')
        self.assertEqual(gap.find('w:pPr/w:keepNext', NS).get('{' + NS['w'] + '}val'), '1')
        self.assertIsNone(gap.find('w:pPr/w:pBdr', NS))
        heading = next(p for p in root.findall('.//w:p', NS)
                       if ''.join(p.xpath('.//w:t/text()', namespaces=NS)).endswith('혼공해석지'))
        val = '{' + NS['w'] + '}val'
        self.assertEqual(heading.find('w:r/w:rPr/w:sz', NS).get(val), '26')
        self.assertEqual(heading.find('w:r/w:rPr/w:color', NS).get(val), '1F4E79')
        self.assertEqual(heading.find('w:pPr/w:jc', NS).get(val), 'center')

    def test_missing_or_multiline_identity_cannot_silently_break_header(self):
        for field in ['course', 'publisher_author']:
            for value in ['', None, 'first\nsecond']:
                with self.subTest(field=field, value=value):
                    data = fixture()
                    data['metadata'][field] = value
                    with self.assertRaisesRegex(ValueError, 'metadata/' + field):
                        compile_plan(data)
        data = fixture()
        data['sources'][0].pop('label')
        with self.assertRaisesRegex(ValueError, 'source/label'):
            compile_plan(data)


if __name__ == '__main__':
    unittest.main()
