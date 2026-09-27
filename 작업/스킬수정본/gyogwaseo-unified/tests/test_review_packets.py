"""Packet isolation and conservative scope regressions; no review certification."""
from copy import deepcopy
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest
import uuid

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / '../scripts'))
from review_packets import make_packet, save_packet, canonical_sha256, _diff, _impact
from test_book import fixture
from test_learning_content import fixture as learning_fixture
from revision_fixtures import upgrade_assessment_fixture, length_review
from check_answer_links import ORDER_PERMUTATIONS
from question_source import build_view
from export_handoff import render


def two_units():
    data = fixture()
    second = learning_fixture()
    second['sources'][0]['id'] = 'src2'
    second['paragraphs'][0].update(id='p2', source_id='src2')
    second['units'][0].update(id='u2', source_id='src2', paragraph_ids=['p2'])
    second['units'][0]['workbook']['question_id'] = 'q2'
    renamed = {g['id']: 'second-' + g['id'] for s in second['sentences'] for g in s['glosses']}
    renamed.update({t['id']: 'second-' + t['id'] for r in second['units'][0]['analysis']['relations'] for t in r.values()})
    renamed['w1'] = 'second-w1'
    def rename(value):
        if isinstance(value, dict):
            return {k: rename(v) for k, v in value.items()}
        if isinstance(value, list):
            return [rename(v) for v in value]
        return renamed.get(value, value) if isinstance(value, str) else value
    second = rename(second)
    for sentence in second['sentences']:
        sentence['source_id'] = 'src2'
    for name in ('sources', 'paragraphs', 'units', 'sentences'):
        data[name].extend(second[name])
    assessment = data['assessment']
    assessment['scope']['unit_ids'].append('u2')
    for name in ('plan', 'questions', 'quick_key', 'explanations'):
        row = deepcopy(assessment[name][0])
        row.update(id='q2', number=2)
        if name == 'plan':
            row['unit_id'] = 'u2'
        if name == 'questions':
            row['passage'] = second['sources'][0]['text']
            row['learned_relation_uses'][0]['term_id'] = renamed[row['learned_relation_uses'][0]['term_id']]
        assessment[name].insert(1, row)
    request = deepcopy(data['question_sources'][0])
    request.update(id='q2', source_id='src2')
    data['question_sources'].insert(1, request)
    return data


def order_book():
    data = fixture()
    learning = learning_fixture([s['text'] for s in data['sentences']] + ['Finally everyone tests it.'])
    learning['paragraphs'][0]['sentence_ids'].append('s4')
    learning['units'][0]['sentence_ids'].append('s4')
    learning['units'][0]['analysis']['flow'][0]['sentence_ids'].append('s4')
    for key in ('sources', 'paragraphs', 'units', 'sentences'):
        data[key] = learning[key]
    for request in data['question_sources']:
        request['last_sentence'] = 's4'
    for q in data['assessment']['questions']:
        q['passage'] = data['sources'][0]['text']
    upgrade_assessment_fixture(data)
    q = next(q for q in data['assessment']['questions'] if q['id'] == 'mock1-1')
    req = next(r for r in data['question_sources'] if r['id'] == q['id'])
    source = data['sources'][0]
    b = source['sentences']
    req.update(type='순서', length_review=length_review('순서'), block_spans={
        'given': [0, b[1]['start']], 'A': [b[3]['start'], len(source['text'])],
        'B': [b[2]['start'], b[3]['start']], 'C': [b[1]['start'], b[2]['start']]})
    view = build_view(source, req, expected_grade=1)
    choices = [{'number': i + 1, 'text': ' → '.join(order)} for i, order in enumerate(ORDER_PERMUTATIONS)]
    q.update(type='순서', choice_mode='order', passage=None, given=view['given'], blocks=view['blocks'],
             choices=choices, answer=5, permutations=deepcopy(ORDER_PERMUTATIONS))
    for name in ('quick_key', 'explanations'):
        row = next(r for r in data['assessment'][name] if r['id'] == q['id'])
        row['answer'] = 5
        if name == 'explanations':
            row.update(choices=deepcopy(choices), choices_ko=[],
                       wrong_reasons=[{'number': i, 'text': 'Synthetic wrong order'} for i in range(1, 5)])
    return data


def keys(value):
    found = set()
    if isinstance(value, dict):
        found.update(value)
        for item in value.values():
            found.update(keys(item))
    elif isinstance(value, list):
        for item in value:
            found.update(keys(item))
    return found


@contextmanager
def packet_folder():
    # Normal directory creation inherits the workspace ACL on Windows; Python's
    # private temporary-directory mode is not writable in this runner.
    path = HERE / ('review-packet-test-' + uuid.uuid4().hex)
    path.mkdir()
    try:
        yield path
    finally:
        for child in path.iterdir():
            child.unlink()
        path.rmdir()


class ReviewPacketTests(unittest.TestCase):
    def test_blind_strict_whitelist_and_immutable_detached_input(self):
        data = fixture()
        data['assessment']['questions'][0]['private_teacher_note'] = 'LEAK_SENTINEL'
        data['assessment']['questions'][0]['choices'][0]['answer_hint'] = 'LEAK_SENTINEL'
        data['assessment']['explanations'][0]['evidence'] = 'LEAK_SENTINEL'
        before = deepcopy(data)
        packet = make_packet(data, 'questions-blind')
        self.assertEqual(data, before)
        forbidden = {'answer', 'evidence', 'explanation', 'wrong_reasons', 'choices_ko',
                     'original', 'source_id', 'source_span', 'source_sentence_ids',
                     'replacement', 'correct_order', 'permutations', 'length_review',
                     'learned_relation_uses', 'question_sources', 'metadata', 'source_reconstruction'}
        self.assertFalse(forbidden & keys(packet))
        self.assertNotIn('LEAK_SENTINEL', json.dumps(packet))
        packet['selected_data']['questions'][0]['student_blocks'][0]['text'] = 'mutated packet'
        self.assertEqual(data, before)

    def test_shared_passage_is_real_printed_view_and_closes_all_members(self):
        data = fixture()
        packet = make_packet(data, 'questions-blind', question_ids=['mock1-4'])
        self.assertEqual(packet['scope']['assigned']['question_ids'], ['mock1-4', 'mock1-5'])
        groups = packet['selected_data']['passage_groups']
        self.assertEqual(len(groups), 1)
        passage = ''.join(x['text'] for x in groups[0]['student_blocks'])
        self.assertIn('Changed', passage)
        self.assertIn('①', passage)
        self.assertEqual(sum(len(b['underlines']) for b in groups[0]['student_blocks']), 5)
        for q in packet['selected_data']['questions']:
            self.assertNotIn('Changed', ''.join(b['text'] for b in q['student_blocks']))

    def test_ordering_has_only_given_abc_student_blocks(self):
        data = order_book()
        packet = make_packet(data, 'questions-blind', question_ids=['mock1-1'])
        blocks = packet['selected_data']['questions'][0]['student_blocks']
        text = '\n'.join(b['text'] for b in blocks)
        self.assertIn('(A) Finally everyone tests it.', text)
        self.assertIn('(C) We save', text)
        self.assertNotIn(data['sources'][0]['text'], text)
        self.assertFalse({'block_spans', 'correct_order', 'original', 'permutations', 'answer'} & keys(packet))

    def test_answer_change_and_baseline_never_leak_to_blind(self):
        baseline = fixture()
        current = deepcopy(baseline)
        qid = 'mock1-1'
        for name in ('questions', 'quick_key', 'explanations'):
            q = next(r for r in current['assessment'][name] if r['id'] == qid)
            q['answer'] = 3
            if name == 'explanations':
                q['wrong_reasons'] = [{'number': n, 'text': 'ANSWER_DIFF_SENTINEL'} for n in (1, 2, 4, 5)]
        packet = make_packet(current, 'questions-blind', baseline=baseline, changed_only=True)
        self.assertEqual(packet['scope']['assigned']['question_ids'], [qid])
        self.assertFalse({'baseline_digest', 'changes', 'change_scope', 'before', 'after', 'reasons'} & keys(packet))
        self.assertNotIn('ANSWER_DIFF_SENTINEL', json.dumps(packet))
        compare = make_packet(current, 'questions-compare', baseline=baseline, changed_only=True)
        answer_changes = [c for c in compare['changes'] if c['path'].endswith('/answer')]
        self.assertTrue(answer_changes)
        self.assertTrue(all(c['after'] == 3 for c in answer_changes))

    def test_sentence_change_closes_full_unit_and_linked_questions(self):
        baseline = two_units()
        current = deepcopy(baseline)
        current['sentences'][-1]['natural_ko'] = 'Changed translation'
        learning = make_packet(current, 'learning', baseline=baseline, changed_only=True)
        self.assertEqual(learning['scope']['assigned']['unit_ids'], ['u2'])
        self.assertEqual(len(learning['selected_data']['sentences']), 3)
        self.assertEqual(learning['selected_data']['units'][0], current['units'][1])
        questions = make_packet(current, 'questions-blind', baseline=baseline, changed_only=True)
        self.assertEqual(questions['scope']['assigned']['question_ids'], ['q2'])

    def test_current_hint_leaf_changes_retain_unit_and_linked_question_scope(self):
        # Scope tests deliberately do not certify the grammatical correspondence.
        baseline = two_units()
        baseline['sentences'][3]['hints'] = [{
            'omitted_relative': 'that', 'emphasis_policy': 'reviewed-declaration',
            'display_pairs': [{'en': 'tools [(that) we repair]', 'ko': '[우리가 고치는] 도구',
                'emphasis_note': 'reviewed absence reason',
                'emphasis_links': [{'en_spans': [[8, 12]], 'ko_spans': [[3, 4], [7, 8]]}]}]}]
        paths = [
            ('omitted_relative',), ('emphasis_policy',),
            ('display_pairs', 0, 'emphasis_note'),
            ('display_pairs', 0, 'emphasis_links', 0, 'en_spans', 0, 0),
            ('display_pairs', 0, 'emphasis_links', 0, 'ko_spans', 1, 1),
        ]
        for path in paths:
            current = deepcopy(baseline)
            parent = current['sentences'][3]['hints'][0]
            for key in path[:-1]:
                parent = parent[key]
            value = parent[path[-1]]
            parent[path[-1]] = value + 1 if isinstance(value, int) else value + '-changed'
            units, questions, scope = _impact(current, baseline, _diff(baseline, current))
            with self.subTest(path=path):
                self.assertEqual(units, {'u2'})
                self.assertEqual(questions, {'q2'})
                self.assertFalse(scope['full_learning_fallback'])
                self.assertFalse(scope['full_questions_fallback'])

    def test_subject_display_leaf_changes_include_unit_and_linked_questions(self):
        # This tests impact classification, not the grammatical validity of a
        # declared shorter span. The S/V validator handles its source bounds.
        baseline = two_units()
        clause = baseline['sentences'][3]['clauses'][0]
        clause.update(subject_display_spans=deepcopy(clause['subject_spans']),
                      subject_display_review='Keep this reviewed subject complete.')
        for field in ['subject_display_spans', 'subject_display_review']:
            current = deepcopy(baseline)
            changed = current['sentences'][3]['clauses'][0]
            if field == 'subject_display_spans':
                changed[field][0][1] -= 1
            else:
                changed[field] = 'Reviewed trailing postmodifier omitted only in display.'
            units, questions, scope = _impact(current, baseline, _diff(baseline, current))
            with self.subTest(field=field):
                self.assertEqual(units, {'u2'})
                self.assertEqual(questions, {'q2'})
                self.assertFalse(scope['full_learning_fallback'])
                self.assertFalse(scope['full_questions_fallback'])

    def test_subject_display_field_addition_and_removal_keep_conservative_fallback(self):
        baseline = two_units()
        current = deepcopy(baseline)
        clause = current['sentences'][3]['clauses'][0]
        clause.update(subject_display_spans=deepcopy(clause['subject_spans']),
                      subject_display_review='Keep this reviewed subject complete.')
        for before, after in [(baseline, current), (current, baseline)]:
            units, questions, scope = _impact(after, before, _diff(before, after))
            self.assertEqual(units, {'u1', 'u2'})
            self.assertEqual(questions, {q['id'] for q in after['assessment']['questions']})
            self.assertTrue(scope['full_learning_fallback'])
            self.assertTrue(scope['full_questions_fallback'])

    def test_hint_alignment_additions_and_source_changes_keep_conservative_fallback(self):
        baseline = two_units()
        baseline['sentences'][3]['hints'] = [{'display_pairs': [{
            'en': '[repair]', 'ko': '[고치다]',
            'emphasis_links': [{'en_spans': [[1, 7]], 'ko_spans': [[1, 4]]}]}]}]
        mutations = [
            lambda d: d['sentences'][3]['hints'][0].update(emphasis_policy='ko-only-verb-construction'),
            lambda d: d['sentences'][3]['hints'][0]['display_pairs'][0]['emphasis_links'].append(
                {'en_spans': [[1, 7]], 'ko_spans': [[1, 4]]}),
            lambda d: d['sources'][1].update(text=d['sources'][1]['text'] + ' Added source.'),
            lambda d: d['sources'][1]['sentences'][0].update(end=1),
        ]
        for mutate in mutations:
            current = deepcopy(baseline); mutate(current)
            units, questions, scope = _impact(current, baseline, _diff(baseline, current))
            with self.subTest(mutate=mutate):
                self.assertEqual(units, {'u1', 'u2'})
                self.assertEqual(questions, {q['id'] for q in current['assessment']['questions']})
                self.assertTrue(scope['full_learning_fallback'])
                self.assertTrue(scope['full_questions_fallback'])

    def test_syntax_training_leaf_changes_keep_unit_and_linked_question_scope(self):
        # A scope test never certifies the declared grammar or translation.
        baseline = two_units()
        unit = baseline['units'][1]
        point = unit['analysis']['grammar_points'][0]
        point.update(id='point-1', formula_key='be p.p.',
                     supplemental={'function_gloss_id': 'f1', 'reason': 'Reviewed absent hint'},
                     practice={'span': [0, 3], 'formula_support': {'en': 'be p.p.', 'ko': '~되다'},
                               'support_gloss_ids': ['g1'], 'answer_ko': '고쳐진다',
                               'support_overrides': [{'gloss_id': 'g1', 'form': 'repair',
                                   'source_span': [0, 3], 'meaning_ko': '고치다', 'review_record': 'Authored support'}]})
        unit['analysis']['formula_routes'] = [{'sentence_id': 's1', 'function_gloss_id': 'f1',
            'formula_key': 'be not p.p.', 'route': 'approved-exception', 'grammar_point_id': 'point-1',
            'review_record': 'Authored route', 'exception_kind': 'partial-negation',
            'replacement_grammar_point_id': 'point-2', 'approval_reference': 'User selection',
            'partial_negation_span': [0, 3]}]
        unit['workbook']['syntax_point_ids'] = ['point-1']
        paths = [
            ('analysis', 'grammar_points', 0, 'id'),
            ('analysis', 'grammar_points', 0, 'formula_key'),
            ('analysis', 'grammar_points', 0, 'practice', 'span', 1),
            ('analysis', 'grammar_points', 0, 'practice', 'formula_support', 'ko'),
            ('analysis', 'grammar_points', 0, 'practice', 'support_gloss_ids', 0),
            ('analysis', 'grammar_points', 0, 'practice', 'answer_ko'),
            ('analysis', 'grammar_points', 0, 'practice', 'support_overrides', 0, 'meaning_ko'),
            ('analysis', 'grammar_points', 0, 'practice', 'support_overrides', 0, 'source_span', 1),
            ('analysis', 'grammar_points', 0, 'supplemental', 'reason'),
            ('analysis', 'formula_routes', 0, 'review_record'),
            ('analysis', 'formula_routes', 0, 'exception_kind'),
            ('analysis', 'formula_routes', 0, 'replacement_grammar_point_id'),
            ('analysis', 'formula_routes', 0, 'approval_reference'),
            ('analysis', 'formula_routes', 0, 'partial_negation_span', 1),
            ('workbook', 'syntax_point_ids', 0),
        ]
        for path in paths:
            current = deepcopy(baseline); parent = current['units'][1]
            for key in path[:-1]: parent = parent[key]
            value = parent[path[-1]]
            parent[path[-1]] = value + 1 if isinstance(value, int) else value + '-changed'
            units, questions, scope = _impact(current, baseline, _diff(baseline, current))
            with self.subTest(path=path):
                self.assertEqual(units, {'u2'})
                self.assertEqual(questions, {'q2'})
                self.assertFalse(scope['full_learning_fallback'])
                self.assertFalse(scope['full_questions_fallback'])

    def test_unit_analysis_change_retains_full_analysis_and_glosses(self):
        baseline = two_units()
        current = deepcopy(baseline)
        current['units'][1]['analysis']['intent_ko'] = 'Changed unit intent'
        packet = make_packet(current, 'learning', baseline=baseline, changed_only=True)
        self.assertEqual(packet['scope']['assigned']['unit_ids'], ['u2'])
        self.assertEqual(packet['selected_data']['units'][0]['analysis'], current['units'][1]['analysis'])
        self.assertTrue(packet['selected_data']['sentences'][0]['glosses'])
        self.assertEqual(packet['context']['sources'][0]['text'], current['sources'][1]['text'])
        self.assertEqual(packet['scope']['context_only']['source_ids'], ['src2'])

    def test_explicit_unit_selection_links_workbook_and_never_narrows_impact(self):
        baseline = two_units()
        current = deepcopy(baseline)
        current['sentences'][-1]['natural_ko'] = 'Changed translation'
        packet = make_packet(current, 'questions-blind', unit_ids=['u1'],
                             question_ids=['mock1-1'], baseline=baseline, changed_only=True)
        self.assertEqual(set(packet['scope']['assigned']['question_ids']),
                         {q['id'] for q in current['assessment']['questions']})

    def test_source_metadata_and_unknown_changes_fall_back(self):
        baseline = two_units()
        for mutate in (lambda d: d['sources'][0]['provenance'].update(verification_record='Changed source review'),
                       lambda d: d['metadata'].update(edition='Changed edition'),
                       lambda d: d.update(author_claimed_change_scope=['q2']),
                       lambda d: d['units'][1]['analysis'].update(unknown_dependency='new')):
            with self.subTest(mutate=mutate):
                current = deepcopy(baseline)
                mutate(current)
                packet = make_packet(current, 'questions-compare', baseline=baseline, changed_only=True)
                self.assertTrue(packet['scope']['whole_stage_assigned'])
                self.assertTrue(packet['change_scope']['full_questions_fallback'])

    def test_unclassified_question_field_falls_back_to_whole_question_stage(self):
        baseline = two_units()
        current = deepcopy(baseline)
        current['assessment']['questions'][0]['new_dependency'] = 'q2'
        packet = make_packet(current, 'questions-compare', baseline=baseline, changed_only=True)
        self.assertTrue(packet['scope']['whole_stage_assigned'])
        self.assertFalse(packet['change_scope']['full_learning_fallback'])

    def test_changed_group_member_expands_shared_pair(self):
        baseline = fixture()
        current = deepcopy(baseline)
        current['assessment']['questions'][4]['question'] += ' Updated'
        packet = make_packet(current, 'questions-blind', baseline=baseline, changed_only=True)
        self.assertEqual(packet['scope']['assigned']['question_ids'], ['mock1-4', 'mock1-5'])

    def test_equal_baseline_empty_and_still_not_final_or_certified(self):
        data = fixture()
        for role in ('learning', 'questions-blind', 'questions-compare'):
            packet = make_packet(data, role, baseline=deepcopy(data), changed_only=True)
            self.assertEqual(packet['status'], 'NOT_FINAL')
            self.assertEqual(packet['certification'], 'NOT_CERTIFIED')
            self.assertFalse(packet['scope']['whole_stage_assigned'])
            self.assertTrue(all(not rows for rows in packet['scope']['assigned'].values()))
            self.assertEqual(packet['review_contract']['approval_reuse'], 'NOT_IMPLEMENTED')

    def test_unknown_ids_and_missing_baseline_raise(self):
        for kwargs in ({'unit_ids': ['missing']}, {'question_ids': ['missing']},
                       {'unit_ids': 'u1'}, {'changed_only': True}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                make_packet(fixture(), 'questions-blind', **kwargs)

    def test_current_structural_failure_is_not_exported(self):
        data = fixture()
        data['assessment']['questions'][0]['passage'] += ' Invented'
        with self.assertRaises(ValueError):
            make_packet(data, 'questions-blind')

    def test_content_and_full_json_digest_distinguish_layout_data(self):
        data = fixture()
        one = make_packet(data, 'learning')
        data['layout_adjustments'] = {'unresolved': 'Observed page edge'}
        two = make_packet(data, 'learning')
        self.assertEqual(one['input_digest']['content_sha256'], two['input_digest']['content_sha256'])
        self.assertNotEqual(one['input_digest']['canonical_full_json_sha256'],
                            two['input_digest']['canonical_full_json_sha256'])
        self.assertEqual(two['input_digest']['canonical_full_json_sha256'], canonical_sha256(data))
        self.assertIsNone(two['input_digest']['file_sha256'])
        self.assertIn('references/editorial-core.md', [r['path'] for r in two['current_rules']])

    def test_cli_new_output_exact_file_hash_and_no_overwrite(self):
        with packet_folder() as folder:
            root = Path(folder)
            source = root / 'manuscript.json'
            output = root / 'review.json'
            source.write_text(json.dumps(fixture(), ensure_ascii=False, indent=1), encoding='utf-8-sig')
            command = [sys.executable, '-X', 'utf8', '-B', str(HERE / '../scripts/review_packets.py'),
                       str(source), str(output), '--role', 'questions-blind', '--question-id', 'mock1-4']
            first = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(first.returncode, 0, first.stderr)
            raw = output.read_bytes()
            packet = json.loads(raw)
            self.assertEqual(packet['input_digest']['file_sha256'], hashlib.sha256(source.read_bytes()).hexdigest())
            self.assertEqual(packet['scope']['assigned']['question_ids'], ['mock1-4', 'mock1-5'])
            again = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
            self.assertNotEqual(again.returncode, 0)
            self.assertEqual(output.read_bytes(), raw)
            with self.assertRaises(FileExistsError):
                save_packet(output, packet)

    def test_cli_equal_baseline_and_changed_only(self):
        with packet_folder() as folder:
            root = Path(folder)
            source, output = root / 'manuscript.json', root / 'review.json'
            source.write_text(json.dumps(fixture()), encoding='utf-8')
            run = subprocess.run([sys.executable, '-X', 'utf8', '-B', str(HERE / '../scripts/review_packets.py'),
                                  str(source), str(output), '--role', 'learning', '--baseline', str(source),
                                  '--changed-only'], capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(run.returncode, 0, run.stderr)
            packet = json.loads(output.read_bytes())
            self.assertEqual(packet['scope']['assigned']['unit_ids'], [])
            self.assertEqual(packet['baseline_digest']['file_sha256'], packet['input_digest']['file_sha256'])

    def test_handoff_wrapper_full_exports_match_complete_render_bytes(self):
        with packet_folder() as root:
            source = root / 'manuscript.json'
            learning, assessment = root / 'learning.txt', root / 'assessment.txt'
            data = fixture()
            source.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
            run = subprocess.run([sys.executable, '-X', 'utf8', '-B', str(HERE / '../scripts/export_handoff.py'),
                                  str(source), '--learning', str(learning), '--assessment', str(assessment)],
                                 capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(run.returncode, 0, run.stderr)
            expected = render(data)
            self.assertEqual(learning.read_bytes(), expected['learning'].encode('utf-8'))
            self.assertEqual(assessment.read_bytes(), expected['assessment'].encode('utf-8'))

    def test_handoff_wrapper_packet_uses_exact_input_bytes_and_shared_scope(self):
        with packet_folder() as root:
            source, output = root / 'manuscript.json', root / 'packet.json'
            source.write_text(json.dumps(fixture(), ensure_ascii=False, indent=3), encoding='utf-8-sig')
            raw = source.read_bytes()
            run = subprocess.run([sys.executable, '-X', 'utf8', '-B', str(HERE / '../scripts/export_handoff.py'),
                                  str(source), '--review-packet', str(output), '--review-role', 'questions-blind',
                                  '--question-id', 'mock1-4'], capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(run.returncode, 0, run.stderr)
            packet = json.loads(output.read_bytes())
            self.assertEqual(packet['input_digest']['file_sha256'], hashlib.sha256(raw).hexdigest())
            self.assertEqual(packet['scope']['assigned']['question_ids'], ['mock1-4', 'mock1-5'])
            self.assertEqual(source.read_bytes(), raw)
            self.assertEqual(packet['status'], 'NOT_FINAL')

    def test_handoff_wrapper_rejects_partial_flags_without_packet_before_writing(self):
        with packet_folder() as root:
            source, output = root / 'manuscript.json', root / 'learning_FINAL.txt'
            source.write_text(json.dumps(fixture()), encoding='utf-8')
            for flags in (['--changed-only'], ['--unit-id', 'u1'],
                          ['--question-id', 'q1'], ['--baseline', str(source)],
                          ['--review-role', 'learning']):
                with self.subTest(flags=flags):
                    run = subprocess.run([sys.executable, '-X', 'utf8', '-B',
                                          str(HERE / '../scripts/export_handoff.py'), str(source),
                                          '--learning', str(output), *flags],
                                         capture_output=True, text=True, encoding='utf-8')
                    self.assertNotEqual(run.returncode, 0)
                    self.assertFalse(output.exists())

    def test_handoff_wrapper_rejects_packet_and_final_mixing(self):
        with packet_folder() as root:
            source, packet, final = root / 'manuscript.json', root / 'packet.json', root / 'learning_FINAL.txt'
            source.write_text(json.dumps(fixture()), encoding='utf-8')
            run = subprocess.run([sys.executable, '-X', 'utf8', '-B', str(HERE / '../scripts/export_handoff.py'),
                                  str(source), '--review-packet', str(packet), '--review-role', 'learning',
                                  '--learning', str(final)], capture_output=True, text=True, encoding='utf-8')
            self.assertNotEqual(run.returncode, 0)
            self.assertFalse(packet.exists())
            self.assertFalse(final.exists())

    def test_handoff_wrapper_never_overwrites_existing_final_or_source(self):
        with packet_folder() as root:
            source, final = root / 'manuscript.json', root / 'learning_FINAL.txt'
            source.write_text(json.dumps(fixture()), encoding='utf-8')
            final.write_bytes(b'EXISTING_FINAL_MUST_STAY_IDENTICAL\r\n')
            for target in (source, final):
                before = target.read_bytes()
                run = subprocess.run([sys.executable, '-X', 'utf8', '-B', str(HERE / '../scripts/export_handoff.py'),
                                      str(source), '--review-packet', str(target), '--review-role', 'learning'],
                                     capture_output=True, text=True, encoding='utf-8')
                self.assertNotEqual(run.returncode, 0)
                self.assertEqual(target.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
