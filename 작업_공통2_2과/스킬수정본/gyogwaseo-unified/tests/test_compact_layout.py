"""Compact layout permissions and content preservation, using synthetic blocks."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / '../scripts'))
from compact_layout import apply_compact_adjustments, content_hash


def fixture():
    data = {'metadata': {'book_name': '합성 시험'}, 'units': [{'id': 'u1'}, {'id': 'u2'}]}
    paragraph = lambda role, text, **extra: {'role': role, 'runs': [{'run': 0, 'text': text}], **extra}
    blocks = [
        {'id': 'u1/analysis', 'elements': [
            paragraph('analysis_header', '끊어읽기', page_break_before=True),
            paragraph('analysis_prose', '앞쪽은 같은 역할도 보존', chain=False),
            {'role': 'analysis_sentence_gap', 'chain': False},
            paragraph('analysis_header', '글의 의도', page_break_before=True),
            paragraph('analysis_prose', '그대로 남을 설명', chain=False, anchor='intent'),
            {'role': 'analysis_sentence_gap', 'chain': False},
            paragraph('analysis_grammar_item', '① 구문 설명', chain=True),
        ]},
        {'id': 'u1/answers', 'elements': [
            paragraph('workbook_answer_unit_heading', '문단 1 워크북 정답', page_break_before=True),
            {'kind': 'table', 'role': 'workbook_key_answer', 'entries': ['1. 표 내용']},
            paragraph('workbook_key_answer', '1. 해석 그대로', chain=True),
            paragraph('workbook_key_answer', '2. 해석 그대로', chain=False),
        ]},
        {'id': 'u1/reading', 'elements': [paragraph('analysis_prose', '읽기 보존')]},
        {'id': 'u2/analysis', 'elements': [paragraph('analysis_header', '다른 단원'),
                                         paragraph('analysis_prose', '다른 단원 보존')]},
    ]
    sources = ['analysis_prose', 'analysis_sentence_gap', 'analysis_grammar_item', 'workbook_key_answer']
    contract = {'roles': {role: {} for role in sources}, 'derived_roles': {}, 'compact_profiles': {}}
    for profile in ['spacing', 'spacing_and_type']:
        role_map = {role: role + '_' + profile for role in sources}
        contract['compact_profiles'][profile] = {'role_map': role_map}
        contract['derived_roles'].update({target: {'base_role': source} for source, target in role_map.items()})
    return data, blocks, contract


def request(data, block_id='u1/analysis', profile='spacing', **changes):
    row = {'kind': 'compact_block', 'block_id': block_id, 'profile': profile,
           'content_sha256': content_hash(data), 'renderer': 'Microsoft Word',
           'observed_page': 2, 'evidence_pdf_sha256': 'a' * 64,
           'reason': 'Word에서 한 줄이 다음 쪽으로 넘어감',
           'approval_reference': '사용자 승인 2026-09-25'}
    row.update(changes)
    return row


class CompactLayoutTests(unittest.TestCase):
    def test_real_profiles_preserve_fonts_until_second_stage_and_enforce_floor(self):
        from master_docx import RoleBank, NS, tag
        bank = RoleBank()
        mapping = bank.contract['compact_profiles']
        def paragraph(profile,role):
            return bank.paragraph(mapping[profile]['role_map'][role], [{'run': 0, 'text': '보존'}])
        spacing = paragraph('spacing','analysis_prose')
        smaller = paragraph('spacing_and_type','analysis_prose')
        self.assertEqual(spacing.find('w:r/w:rPr/w:sz',NS).get(tag('val')), '20')
        self.assertEqual(smaller.find('w:r/w:rPr/w:sz',NS).get(tag('val')), '19')
        self.assertEqual(spacing.find('w:pPr/w:spacing',NS).get(tag('line')), '270')
        self.assertEqual(paragraph('spacing_and_type','choice_translation').find('w:r/w:rPr/w:sz',NS).get(tag('val')), '17')
        self.assertEqual(paragraph('spacing_and_type','analysis_grammar_heading').find('w:r/w:rPr/w:sz',NS).get(tag('val')), '20')

    def test_full_manuscript_learning_projection_ignores_only_known_answer_adjustments(self):
        from book_plan import compile_plan
        from test_book_plan import fixture as real_fixture
        data = real_fixture()
        data['layout_adjustments'] = [request(data,'u1/analysis'),request(data,'u1/answers')]
        full = compile_plan(data)
        learning = compile_plan(data,'learning')
        a = next(b for b in full['blocks'] if b['id']=='u1/analysis')
        b = next(b for b in learning['blocks'] if b['id']=='u1/analysis')
        self.assertEqual(a,b)
        self.assertFalse(any(b['id'].endswith('/answers') for b in learning['blocks']))

    def test_saved_compact_font_mutation_is_detected(self):
        from master_docx import RoleBank, NS, tag
        from saved_format import paragraph_record, Styles
        bank=RoleBank()
        styles=Styles({i.filename:raw for i,raw in bank.package})
        role=bank.contract['compact_profiles']['spacing_and_type']['role_map']['analysis_prose']
        expected=bank.paragraph(role,[{'run':0,'text':'원고 내용 보존'}])
        changed=deepcopy(expected)
        changed.find('w:r/w:rPr/w:sz',NS).set(tag('val'),'18')
        self.assertNotEqual(paragraph_record(expected,styles),paragraph_record(changed,styles))

    def test_legacy_and_other_adjustment_kinds_are_untouched(self):
        data, blocks, _ = fixture()
        data.pop('metadata')
        original = deepcopy(blocks)
        apply_compact_adjustments(data, blocks, {})
        data['layout_adjustments'] = [{'kind': 'question_page_break'}]
        apply_compact_adjustments(data, blocks, {})
        self.assertEqual(blocks, original)

    def test_hash_matches_canonical_manuscript_and_ignores_adjustments(self):
        data, blocks, contract = fixture()
        expected = hashlib.sha256(json.dumps(data, ensure_ascii=False, sort_keys=True,
                                             separators=(',', ':')).encode('utf-8')).hexdigest()
        data['layout_adjustments'] = [{'reason': '무관한 관찰'}]
        self.assertEqual(content_hash(data), expected)
        data['layout_adjustments'] = [request(data)]
        apply_compact_adjustments(data, blocks, contract, current_content_hash=expected)
        self.assertEqual(blocks[0]['elements'][4]['role'], 'analysis_prose_spacing')

    def test_analysis_changes_only_roles_after_last_header(self):
        data, blocks, contract = fixture()
        before_data, before_blocks, before_contract = deepcopy(data), deepcopy(blocks), deepcopy(contract)
        data['layout_adjustments'] = [request(data)]
        apply_compact_adjustments(data, blocks, contract)
        expected = deepcopy(before_blocks)
        for row in expected[0]['elements'][4:]:
            row['role'] += '_spacing'
        self.assertEqual(blocks, expected)
        self.assertEqual({k: v for k, v in data.items() if k != 'layout_adjustments'}, before_data)
        self.assertEqual(contract, before_contract)

    def test_answers_preserve_table_runs_chain_order_and_unselected_blocks(self):
        data, blocks, contract = fixture()
        expected = deepcopy(blocks)
        data['layout_adjustments'] = [request(data, 'u1/answers', 'spacing_and_type')]
        apply_compact_adjustments(data, blocks, contract)
        for row in expected[1]['elements'][2:]:
            row['role'] += '_spacing_and_type'
        self.assertEqual(blocks, expected)

    def test_all_required_observation_and_approval_fields_are_enforced(self):
        invalid = {'content_sha256': ['', '0' * 64, None],
                   'renderer': ['LibreOffice', '', None],
                   'observed_page': [0, -1, True, 1.5, '2', None],
                   'evidence_pdf_sha256': ['', 'f' * 63, 'g' * 64, None],
                   'reason': ['', '  ', None], 'approval_reference': ['', '\t', None]}
        for field, values in invalid.items():
            for value in values:
                with self.subTest(field=field, value=value):
                    data, blocks, contract = fixture()
                    data['layout_adjustments'] = [request(data, **{field: value})]
                    original = deepcopy(blocks)
                    with self.assertRaises(ValueError):
                        apply_compact_adjustments(data, blocks, contract)
                    self.assertEqual(blocks, original)
        for field in invalid:
            with self.subTest(missing=field):
                data, blocks, contract = fixture()
                row = request(data)
                row.pop(field)
                data['layout_adjustments'] = [row]
                with self.assertRaises(ValueError):
                    apply_compact_adjustments(data, blocks, contract)

    def test_unknown_unapproved_missing_and_invalid_profiles_are_rejected(self):
        for profile in [None, '', 'aggressive', 'spacing']:
            with self.subTest(profile=profile):
                data, blocks, contract = fixture()
                if profile == 'spacing':
                    contract.pop('compact_profiles')
                data['layout_adjustments'] = [request(data, profile=profile)]
                with self.assertRaises(ValueError):
                    apply_compact_adjustments(data, blocks, contract)
        for role_map in [{}, None, {'analysis_prose': 'arbitrary'}, {'analysis_prose': 'analysis_prose'}]:
            with self.subTest(role_map=role_map):
                data, blocks, contract = fixture()
                contract['compact_profiles']['spacing']['role_map'] = role_map
                data['layout_adjustments'] = [request(data)]
                with self.assertRaises(ValueError):
                    apply_compact_adjustments(data, blocks, contract)

    def test_unknown_duplicate_and_out_of_scope_block_ids_are_rejected(self):
        for bid in ['u1/reading', 'u1/workbook', 'answers/quick', 'answers/mock1', 'unknown/analysis', 'u2/answers', None]:
            with self.subTest(block_id=bid):
                data, blocks, contract = fixture()
                data['layout_adjustments'] = [request(data, block_id=bid)]
                with self.assertRaises(ValueError):
                    apply_compact_adjustments(data, blocks, contract)
        data, blocks, contract = fixture()
        blocks.append(deepcopy(blocks[0]))
        data['layout_adjustments'] = [request(data)]
        with self.assertRaises(ValueError):
            apply_compact_adjustments(data, blocks, contract)

    def test_duplicate_requests_and_later_invalid_requests_are_atomic(self):
        for second in ['duplicate', 'invalid']:
            with self.subTest(second=second):
                data, blocks, contract = fixture()
                data['layout_adjustments'] = [request(data), request(data)]
                if second == 'invalid':
                    data['layout_adjustments'][1] = request(data, 'u1/answers', approval_reference='')
                original = deepcopy(blocks)
                with self.assertRaises(ValueError):
                    apply_compact_adjustments(data, blocks, contract)
                self.assertEqual(blocks, original)

    def test_missing_analysis_boundary_and_no_eligible_role_are_rejected(self):
        for mode in ['no_header', 'no_mapping', 'table_only']:
            with self.subTest(mode=mode):
                data, blocks, contract = fixture()
                if mode == 'no_header':
                    blocks[0]['elements'] = blocks[0]['elements'][4:]
                elif mode == 'no_mapping':
                    blocks[0]['elements'] = blocks[0]['elements'][:4]
                else:
                    blocks[0]['elements'] = blocks[0]['elements'][:4] + [deepcopy(blocks[1]['elements'][1])]
                data['layout_adjustments'] = [request(data)]
                with self.assertRaises(ValueError):
                    apply_compact_adjustments(data, blocks, contract)

    def test_derived_role_cannot_change_the_base_semantics(self):
        data, blocks, contract = fixture()
        contract['derived_roles']['analysis_prose_spacing']['base_role'] = 'workbook_key_answer'
        data['layout_adjustments'] = [request(data)]
        with self.assertRaises(ValueError):
            apply_compact_adjustments(data, blocks, contract)


if __name__ == '__main__':
    unittest.main()
