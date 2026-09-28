from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / '../scripts'))
import check_learning_content as m
from source_contract import display_lesson, lesson_identity, transcription_sha256, unit_subheadings
from structure_hints import display_pairs, display_lines


def aligned_pair(en, ko, *links):
    """Build explicitly selected test markers; this helper never infers grammar."""
    def selected(value, parts):
        result = []
        for part in parts:
            text, occurrence = part if isinstance(part, tuple) else (part, 0)
            start = -1
            for _ in range(occurrence + 1):
                start = value.index(text, start + 1)
            result.append([start, start + len(text)])
        return result
    return {'en': en, 'ko': ko, 'emphasis_links': [
        {'en_spans': selected(en, english), 'ko_spans': selected(ko, korean)}
        for english, korean in links]}


def absent_marker_pair(en, ko, reason):
    return {'en': en, 'ko': ko, 'emphasis_links': [], 'emphasis_note': reason}


def fixture(texts=None):
    # Synthetic structural test data; not language-reviewed student content.
    texts = texts or ['They repair useful tools.', 'We save valuable materials.', 'I protect local resources.']
    sentences, bounds, offset = [], [], 0
    for n, original in enumerate(texts, 1):
        words = list(m.WORDS.finditer(original))
        glosses, coverage = [], []
        for j, word in enumerate(words):
            gid = f'g{n}-{j}'
            gloss = {'id': gid, 'spans': [[word.start(), word.end()]],
                     'headword': word.group(), 'meaning_ko': '시험용 뜻', 'star': n == 1 and j == 1}
            if gloss['star']:
                gloss['today_word_id'] = 'w1'
            if word.group().lower() in m.PRONOUNS:
                gloss['referent_ko'] = '앞 문맥의 사람들'
            glosses.append(gloss)
            coverage.append({'span': [word.start(), word.end()], 'gloss_id': gid})
        sentences.append({'source_id': 'src', 'id': f's{n}', 'text': original, 'key': n < 3,
                          'chunks': [{'start': 0, 'end': len(original), 'ko': '시험용 대응 청크'}],
                          'natural_ko': '시험용 자연 해석', 'glosses': glosses, 'lexical_coverage': coverage,
                          'reading_checks': {'required_breaks': [], 'protected_spans': [], 'function_gloss_ids': [],
                                             'review_record': 'Synthetic structural test; no language review claimed.'},
                          'clauses': [{'kind': 'main', 'start': 0,
                                       'subject_spans': [[words[0].start(), words[0].end()]],
                                       'verb_spans': [[words[1].start(), words[1].end()]]}]})
        bounds.append({'id': f's{n}', 'start': offset, 'end': offset + len(original)})
        offset += len(original) + 1
    relations = []
    for i in range(3):
        relations.append({k: {'id': f't{i}{k}', 'text': f'term{i}{k}', 'meaning_ko': '시험용 뜻'}
                          for k in ['head', 'synonym', 'antonym']})
    terms = [x['id'] for r in relations for x in r.values()]
    unit = {'id': 'u1', 'source_id': 'src', 'paragraph_ids': ['p1'], 'sentence_ids': ['s1', 's2', 's3'],
            'today_words': [{'id': 'w1', 'text': 'repair', 'meaning_ko': '고치다', 'source_gloss_id': 'g1-1'}],
            'analysis': {'heading_kind': '주제', 'title_or_topic_en': 'Resource Care',
                         'title_or_topic_ko': '자원 관리', 'intent_ko': '자원을 아끼자는 내용',
                         'flow': [{'sentence_ids': ['s1', 's2', 's3'], 'text_ko': '시험용 흐름'}],
                         'easy_explanations': [{'sentence_id': f's{i}', 'explanatory_sentences': ['설명 하나.', '설명 둘.']} for i in range(1, 4)],
                         'grammar_points': [{'sentence_id': f's{i}', 'span': [0, 1], 'title': '시험', 'explanation': '시험용 설명'} for i in range(1, 4)],
                         'relations': relations},
            'workbook': {'relation_order': terms[1:] + terms[:1], 'key_sentence_ids': ['s1', 's2'], 'question_id': 'q1'}}
    return {'schema_version': 1, 'rule_revision': 'R2026-09-23', 'metadata': {'book_name': '시험', 'course': '공통영어1', 'publisher_author': '시험', 'lesson': 'UNIT00'},
            'sources': [{'id': 'src', 'label': '본문', 'text': ' '.join(texts), 'sentences': bounds,
                         'subheadings': [{'id': 'h1', 'text': 'Synthetic Source Heading',
                                          'location': 'fixture heading before s1', 'before_sentence_id': 's1',
                                          'artifact_sha256': '0' * 64}],
                         'provenance': {'filename': 'fixture.txt', 'location': 'test', 'sha256': '0' * 64,
                                        'verification_record': 'Synthetic fixture, not a real source verification'}}],
            'paragraphs': [{'id': 'p1', 'source_id': 'src', 'subheading_id': 'h1', 'sentence_ids': ['s1', 's2', 's3']}],
            'units': [unit], 'sentences': sentences}


def noun_phrase_fixture():
    # Actual question/answer text, synthetic supporting annotations for plumbing
    # tests only; these annotations are not a completed lesson manuscript.
    data = fixture(['What eventually emerged from these parties?',
                    'A vibrant youth movement called hip-hop culture, based on DJing, breakdancing, MCing, and graffiti.',
                    'I protect local resources.'])
    question, answer = data['sentences'][:2]
    question['clauses'] = [{'kind': 'main', 'start': 0, 'subject_spans': [[0, 4]],
                           'verb_spans': [[16, 23]]}]
    data['units'][0]['today_words'][0]['text'] = 'eventually'
    answer['clauses'] = []
    answer['sv_review'] = {'kind': 'noun-phrase-answer', 'reviewed': True,
        'reason': 'Reviewed answer to preceding question; called/based modify the noun phrase and do not supply a finite verb.',
        'source_text_sha256': hashlib.sha256(answer['text'].encode('utf-8')).hexdigest(),
        'context_sentence_id': question['id'],
        'context_text_sha256': hashlib.sha256(question['text'].encode('utf-8')).hexdigest()}
    return data


def modal_hint_fixture(modal='may'):
    original = f'They {modal} have provided people with tools.'
    meaning = {'may': '제공했을지도 모른다', 'may not': '제공하지 않았을지도 모른다',
               "couldn't": '제공했을 리가 없다', 'cannot': '제공했을 리가 없다',
               'ought to': '제공했어야 한다'}[modal]
    data = fixture([original, 'We save valuable materials.', 'I protect local resources.'])
    s = data['sentences'][0]
    start, lexical_start = original.index(modal), original.index('provided')
    end, with_start = lexical_start + len('provided'), original.index('with')
    function = s['glosses'][1]
    lexical = next(g for g in s['glosses'] if g['headword'] == 'provided')
    function.update(kind='function', headword=modal+' have p.p.', meaning_ko='~'+meaning[2:],
                    spans=[[start, lexical_start-1]], combines_with=[lexical['id']])
    lexical.update(kind='lexical', headword='provided A with B', meaning_ko='A에게 B를 제공하다',
                   spans=[[lexical_start, end], [with_start, with_start+4]])
    s['glosses'] = [g for g in s['glosses'] if g in (function, lexical) or
                   not (start <= g['spans'][0][0] < lexical_start or g['headword'] == 'with')]
    for row in s['lexical_coverage']:
        if start <= row['span'][0] < lexical_start:
            row['gloss_id'] = function['id']
        elif row['span'][0] in {lexical_start, with_start}:
            row['gloss_id'] = lexical['id']
    s['reading_checks']['function_gloss_ids'] = [function['id']]
    s['hints'] = [{'category':'function-combination', 'span':[start,with_start+4],
        'gloss_ids':[function['id'],lexical['id']], 'meaning_ko':'검수 전용 뜻',
        'explanation':'검수 전용 근거', 'display_mode':'verb-function', 'display_span':[start,end],
        'formula_label':modal+' have p.p.',
        'display_pairs':[aligned_pair(original[start:end], meaning,
                                      ([modal+' have'], [meaning[2:]]))]}]
    return data


class LearningContentTests(unittest.TestCase):
    def test_noun_phrase_review_binds_authoritative_question_and_keeps_source_unchanged(self):
        data = noun_phrase_fixture(); before = deepcopy(data)
        result = m.check(data, scope='learning')
        self.assertEqual(result['status'], 'STRUCTURE_PASS')
        self.assertEqual(result['sv_lines'], {'src/s1': 'S: What, V: emerged',
                                           'src/s2': '', 'src/s3': 'S: I, V: protect'})
        self.assertEqual(data, before)
        self.assertEqual(result['semantic_review'], 'NOT_PERFORMED')

    def test_noun_phrase_review_rejects_missing_review_and_clauses(self):
        for field in ['sv_review', 'clauses']:
            data = noun_phrase_fixture(); data['sentences'][1].pop(field)
            with self.subTest(field=field), self.assertRaises(ValueError):
                m.check(data, scope='learning')

    def test_noun_phrase_review_rejects_context_and_self_hash_mismatch(self):
        for field, value in [('context_sentence_id', 's3'), ('context_sentence_id', 'missing'),
                             ('context_text_sha256', '0' * 64), ('source_text_sha256', '0' * 64)]:
            data = noun_phrase_fixture(); data['sentences'][1]['sv_review'][field] = value
            with self.subTest(field=field, value=value), self.assertRaisesRegex(ValueError, 'sv_review'):
                m.check(data, scope='learning')

    def test_noun_phrase_review_cannot_use_a_context_from_another_source(self):
        data = noun_phrase_fixture()
        other = deepcopy(data['sources'][0]); other['id'] = 'other'
        other['subheadings'][0]['id'] = 'other-heading'
        other_paragraph = deepcopy(data['paragraphs'][0])
        other_paragraph.update(id='other-p1', source_id='other', subheading_id='other-heading')
        other_unit = deepcopy(data['units'][0])
        other_unit.update(id='other-u1', source_id='other', paragraph_ids=['other-p1'])
        other_sentences = deepcopy(data['sentences'])
        for sentence in other_sentences:
            sentence['source_id'] = 'other'
        # The first sentence of the next source must not use the last sentence
        # of the previous source as its answer context, even with matching IDs.
        first = data['sentences'][0]
        first['clauses'] = []
        first['sv_review'] = dict(data['sentences'][1]['sv_review'],
            source_text_sha256=hashlib.sha256(first['text'].encode('utf-8')).hexdigest(),
            context_sentence_id='s3',
            context_text_sha256=hashlib.sha256(other_sentences[-1]['text'].encode('utf-8')).hexdigest())
        data['sources'].insert(0, other)
        data['paragraphs'].insert(0, other_paragraph)
        data['units'].insert(0, other_unit)
        data['sentences'] = other_sentences + data['sentences']
        with self.assertRaisesRegex(ValueError, 'immediately preceding same-source'):
            m.check(data, scope='learning')

    def split_phrasal_sentence(self):
        original = 'They repair tools after you throw them away.'
        s = fixture([original, 'We save valuable materials.', 'I protect local resources.'])['sentences'][0]
        # Keep the current standalone-you exclusion in this synthetic fixture.
        you = next(g for g in s['glosses'] if g['headword'] == 'you')
        s['glosses'].remove(you)
        for row in s['lexical_coverage']:
            if row.get('gloss_id') == you['id']:
                row.pop('gloss_id')
                row.update(exemption='standalone-you', reason='시험용 you 제외')
        fragments = ['after you throw', 'away']
        ranges = [[original.index(part), original.index(part) + len(part)] for part in fragments]
        s['hints'] = [{'span': [ranges[0][0], ranges[1][1]], 'meaning_ko': '여러분이 버린 후에',
            'explanation': '목적어 them을 생략하고 검토한 구동사 throw away의 두 부분만 보인다.',
            'display_mode': 'split-phrasal-verb', 'display_spans': ranges,
            'structure_label': '시간 접속사 after',
            'display_pairs': [aligned_pair('[after you throw … away]', '[여러분이 버린 후에]',
                                           (['after'], ['후에']))]}]
        return s

    def test_split_phrasal_hint_omits_object_preserves_source_and_one_line_label(self):
        s = self.split_phrasal_sentence(); before = deepcopy(s)
        m.glossary(s, {'w1': {}}, require_reading_checks=True)
        self.assertEqual(display_lines(s['hints'][0]),
                         ['[after you throw … away] → [여러분이 버린 후에] (시간 접속사 after)'])
        self.assertEqual(s, before)

    def test_split_phrasal_hint_matches_in_book_plan_and_final_handoff(self):
        from book_plan import compile_plan
        from export_handoff import render
        sentence = self.split_phrasal_sentence()
        data = fixture([sentence['text'], 'We save valuable materials.', 'I protect local resources.'])
        data['sentences'][0] = sentence
        data['cover'] = {'lesson_label': 'LESSON', 'lesson_number': '00',
                         'topic_first': 'Shared Layout Test', 'topic_second': 'Synthetic Data Only',
                         'topic_ko': '시험용 자료'}
        data['sources'][0]['label'] = '시험용 본문'
        plan = compile_plan(data, 'learning'); output = render(data, 'learning')['learning']
        row = next(e for b in plan['blocks'] for e in b['elements'] if e['role'] == 'structure_hint')
        printed = ''.join(r['text'] for r in row['runs']).removeprefix('구조 힌트   ')
        self.assertEqual(printed, display_lines(sentence['hints'][0])[0])
        self.assertIn('[구조 힌트] ' + printed + '\n', output)
        self.assertNotIn('them', printed)

    def test_split_phrasal_hint_rejects_altered_fragments_and_unmarked_omissions(self):
        for en in ['[after you threw … away]', '[After you throw … away]',
                   '[after you throw away]', '[after you throw ... away]',
                   '[away … after you throw]', '[after you throw … away …]',
                   '[after you throw them away]']:
            with self.subTest(en=en):
                s = self.split_phrasal_sentence()
                marker = 'After' if 'After' in en else 'after'
                s['hints'][0]['display_pairs'][0] = aligned_pair(en, '[여러분이 버린 후에]',
                                                                ([marker], ['후에']))
                with self.assertRaisesRegex(ValueError, 'exact original fragments'):
                    m.glossary(s, {'w1': {}}, require_reading_checks=True)

    def test_split_phrasal_hint_requires_exactly_two_ordered_ranges_inside_hint(self):
        original = self.split_phrasal_sentence(); first, second = original['hints'][0]['display_spans']
        for ranges in [None, [], [first], [first, second, second], [[True, first[1]], second],
                       [second, first], [first, first], [first, [first[1], second[1]]],
                       [[0, 4], second], [first, [second[0], len(original['text']) + 1]]]:
            with self.subTest(ranges=ranges):
                s = deepcopy(original); s['hints'][0]['display_spans'] = ranges
                with self.assertRaises(ValueError):
                    m.glossary(s, {'w1': {}}, require_reading_checks=True)

    def test_split_phrasal_hint_rejects_whitespace_only_gap_and_cut_source_words(self):
        original = self.split_phrasal_sentence(); full = original['text']
        cases = [
            [[full.index('after'), full.index('throw') - 1],
             [full.index('throw'), full.index('away') + 4]],  # only a space omitted
            [[full.index('after'), full.index('throw') + 2],
             [full.index('away'), full.index('away') + 4]],  # verb cut midword
            [[full.index('after'), full.index('throw') + 6],
             [full.index('away'), full.index('away') + 4]],  # trailing edge space
        ]
        for ranges in cases:
            with self.subTest(ranges=ranges):
                s = deepcopy(original); hint = s['hints'][0]
                hint['display_spans'] = ranges
                hint['display_pairs'][0]['en'] = '[' + ' … '.join(full[a:b] for a, b in ranges) + ']'
                with self.assertRaisesRegex(ValueError, 'actual source text|source words|edge whitespace'):
                    m.glossary(s, {'w1': {}}, require_reading_checks=True)

    def test_split_phrasal_hint_keeps_general_pair_brackets_and_korean_label_contract(self):
        original = self.split_phrasal_sentence()['hints'][0]
        for edit in [{'category': 'paired-structure'}, {'category': 'function-combination'},
                     {'display_mode': None}, {'display_mode': 'arbitrary-omission'},
                     {'display_span': [0, 1]}, {'display_pairs': original['display_pairs'] * 2},
                     {'structure_label': None}, {'structure_label': 'English only'},
                     {'display_pairs': [{'en': 'after you throw … away', 'ko': '여러분이 버린 후에'}]},
                     {'display_pairs': [{'en': '[after you throw … away]', 'ko': '여러분이 버린 후에'}]}]:
            with self.subTest(edit=edit), self.assertRaises(ValueError):
                display_pairs({**original, **edit})
        hint = deepcopy(original); hint.pop('display_mode')
        with self.assertRaisesRegex(ValueError, 'display_spans requires'):
            display_pairs(hint)

    def test_split_phrasal_hint_covers_only_printed_relative_marker(self):
        original = 'They repair tools that can drive the insects away.'
        s = fixture([original, 'We save valuable materials.', 'I protect local resources.'])['sentences'][0]
        relative = next(g for g in s['glosses'] if g['headword'] == 'that')
        s['reading_checks']['relative_gloss_ids'] = [relative['id']]
        first = [original.index('that'), original.index('drive') + len('drive')]
        second = [original.index('away'), original.index('away') + len('away')]
        hint = deepcopy(self.split_phrasal_sentence()['hints'][0])
        hint.update(span=[original.index('tools'), second[1]], display_spans=[first, second],
                    structure_label='주격 관계대명사 that')
        hint['display_pairs'] = [aligned_pair('[that can drive … away]', '[쫓아낼 수 있는]',
                                            (['that'], ['는']))]
        s['hints'] = [hint]
        m.glossary(s, {'w1': {}}, require_reading_checks=True)
        # A broad hint span cannot make an omitted relative marker count as seen.
        hint['display_spans'][0] = [original.index('tools'), original.index('tools') + len('tools')]
        hint['display_pairs'][0] = absent_marker_pair('[tools … away]', '[쫓아낼 수 있는]',
            '변조 시험: 관계사가 빠져 대응되는 영어 표면형이 없다.')
        with self.assertRaisesRegex(ValueError, 'Relative marker'):
            m.glossary(s, {'w1': {}}, require_reading_checks=True)
        # Direct relative coverage also verifies fragments before trusting spans.
        hint['display_pairs'][0]['en'] = '[that can drive … away]'
        with self.assertRaisesRegex(ValueError, 'exact original fragments'):
            m.relative_hint_coverage(s, {g['id']: g for g in s['glosses']})

    def paired_sentence(self):
        original = 'They use both to hide in the dark and to secretly crawl through tunnels.'
        s = fixture([original, 'We save valuable materials.', 'I protect local resources.'])['sentences'][0]
        fragments = ['both to hide', 'and to secretly crawl']
        spans = [[original.index(part), original.index(part) + len(part)] for part in fragments]
        s['hints'] = [{'category': 'paired-structure', 'span': [spans[0][0], spans[-1][1]],
            'meaning_ko': '검수 전용 뜻', 'explanation': '검수 전용 구조 근거',
            'display_spans': spans, 'display_pairs': [aligned_pair(
                ' … '.join(fragments) + ' …', '숨기 위해서도 … 몰래 기어가기 위해서도 …',
                (['both'], [('도', 0)]), (['and'], [('도', 1)]))]}]
        return s

    def test_paired_hint_exact_original_fragments_and_optional_trailing_ellipsis(self):
        for trailing in [True, False]:
            s = self.paired_sentence()
            if not trailing:
                s['hints'][0]['display_pairs'][0]['en'] = s['hints'][0]['display_pairs'][0]['en'].removesuffix(' …')
            before = deepcopy(s)
            m.glossary(s, {'w1': {}}, require_reading_checks=True)
            self.assertEqual(s, before)

    def test_paired_hint_rejects_changed_or_reordered_english_fragments(self):
        for en in ['both to hide … and secretly crawl …',
                   'and to secretly crawl … both to hide …',
                   'Both to hide … and to secretly crawl …',
                   'both to hide...and to secretly crawl...',
                   'both to hide … and to secretly crawl … extra']:
            with self.subTest(en=en):
                s = self.paired_sentence()
                first_marker = 'Both' if 'Both' in en else 'both'
                s['hints'][0]['display_pairs'][0] = aligned_pair(
                    en, '숨기 위해서도 … 몰래 기어가기 위해서도 …',
                    ([first_marker], [('도', 0)]), (['and'], [('도', 1)]))
                with self.assertRaisesRegex(ValueError, 'original fragments'):
                    m.glossary(s, {'w1': {}}, require_reading_checks=True)

    def test_paired_hint_spans_reject_invalid_order_overlap_or_outside_grounding(self):
        original = self.paired_sentence()
        first, second = original['hints'][0]['display_spans']
        for ranges in [[], None, [[True, 3]], [[-1, 3]], [[3, 3]],
                       [second, first], [first, first], [first, [first[1]-1, second[1]]],
                       [[0, 4], second], [first, [second[0], len(original['text'])+1]]]:
            with self.subTest(ranges=ranges):
                s = deepcopy(original); s['hints'][0]['display_spans'] = ranges
                with self.assertRaises(ValueError):
                    m.glossary(s, {'w1': {}}, require_reading_checks=True)

    def test_paired_hint_requires_one_bilingual_pair_without_general_label(self):
        hint = self.paired_sentence()['hints'][0]
        for update in [{'display_pairs': []}, {'display_pairs': hint['display_pairs']*2},
                       {'display_pairs': [{'en': hint['display_pairs'][0]['en'], 'ko': 'English only'}]},
                       {'structure_label': '상관구문'}, {'structure_label': None},
                       {'display_en': hint['display_pairs'][0]['en']}]:
            with self.subTest(update=update), self.assertRaises(ValueError):
                display_pairs({**hint, **update})
        hint.pop('display_pairs')
        with self.assertRaisesRegex(ValueError, 'display_pairs'):
            display_pairs(hint, required=False)

    def test_paired_hints_keep_existing_containment_and_two_hint_limit(self):
        s = self.paired_sentence(); outer = s['hints'][0]
        s['hints'].append({'span': outer['display_spans'][0], 'meaning_ko': '검수용 뜻',
            'explanation': '검수용 근거', 'structure_label': '시험용 구조',
            'display_pairs': [aligned_pair('[both to hide]', '[숨기 위해서도]',
                                           (['both'], ['도']))]})
        with self.assertRaisesRegex(ValueError, 'Contained structure hints'):
            m.glossary(s, {'w1': {}}, require_reading_checks=True)
        s['hints'] = [outer]*3
        with self.assertRaisesRegex(ValueError, 'At most two'):
            m.glossary(s, {'w1': {}}, require_reading_checks=True)

    def test_parenthesized_expression_and_meaning_duplicate_is_rejected(self):
        for meaning in ['허용하다 (allow A to V — A가 ~하도록 허용하다)',
                        '끝내다 (finishes V-ing – ~하는 것을 끝내다)',
                        '돕다 (help V — ~하는 것을 돕다)',
                        '유지하다 (keep A B — A를 B한 상태로 유지하다)',
                        '허용하다 (allow A to V - A가 ~하도록 허용하다)']:
            with self.subTest(meaning=meaning):
                d=fixture();d['sentences'][0]['glosses'][1]['meaning_ko']=meaning
                with self.assertRaisesRegex(ValueError,'duplicate an English expression'):
                    m.check(d)

    def test_legitimate_parentheses_in_gloss_meanings_remain_allowed(self):
        for meaning in ['측면 (흔한 뜻: 존경)','쓰다 (write의 변화형)',
                        '~하는 (관계대명사)','비교하다 (compare with)',
                        '뜻 (흔한 뜻: respect — 존경)',
                        '30에서 40 (A to B — A에서 B까지)',
                        '갈고리 같은 (hook — 갈고리 + -like — ~ 같은)',
                        '물 (water pollution — 수질 오염)',
                        '매우 큰 (such a large — 그렇게 큰)',
                        '그러한 (such A as B — B와 같은 A)',
                        '동등한 비교 (as A as B — B만큼 A한)',
                        '가장 큰 (the largest — 가장 큰)']:
            with self.subTest(meaning=meaning):
                d=fixture();d['sentences'][0]['glosses'][1]['meaning_ko']=meaning
                self.assertEqual(m.check(d)['status'],'STRUCTURE_PASS')

    def test_expression_headword_is_allowed_without_duplicate_parenthesis(self):
        s=fixture(['They allow us to leave.','We save valuable materials.','I protect local resources.'])['sentences'][0]
        s['glosses'][1].update(headword='allow A to V',meaning_ko='A가 ~하도록 허용하다')
        result=m.glossary(s,{'w1':{}},require_reading_checks=True)
        self.assertEqual(result[s['glosses'][1]['id']]['headword'],'allow A to V')

    def test_current_standalone_you_gloss_is_excluded_case_insensitively(self):
        for word in ['you','You','YOU']:
            with self.subTest(word=word):
                d=fixture([word+' repair useful tools.','We save valuable materials.','I protect local resources.'])
                with self.assertRaisesRegex(ValueError,'Standalone you gloss'):
                    m.check(d)

    def test_explicit_you_exemption_preserves_source_sv_and_other_glosses(self):
        d=fixture(['You repair useful tools.','We save valuable materials.','I protect local resources.'])
        s=d['sentences'][0];s['glosses'].pop(0)
        s['lexical_coverage'][0].update(gloss_id=None,exemption='standalone-you',
            reason='사용자 확정: 단독 you 각주는 제공하지 않음')
        before=deepcopy(d);result=m.check(d)
        self.assertEqual(result['status'],'STRUCTURE_PASS')
        self.assertEqual(result['sv_lines']['src/s1'],'S: You, V: repair')
        self.assertEqual(d,before)
        self.assertEqual(s['text'],'You repair useful tools.')
        self.assertEqual([g['headword'] for g in s['glosses']],['repair','useful','tools'])

    def test_you_exclusion_cannot_be_disguised_as_low_word_level(self):
        d=fixture(['You repair useful tools.','We save valuable materials.','I protect local resources.'])
        s=d['sentences'][0];s['glosses'].pop(0)
        s['lexical_coverage'][0].update(gloss_id=None,exemption='below-middle1-unneeded',
            level='below-middle1',reason='기초 단어라는 임의 근거')
        with self.assertRaisesRegex(ValueError,'explicit standalone-you'):
            m.check(d)

    def test_you_exemption_does_not_spread_to_other_pronouns(self):
        for word in ['They','Your','Yours','Yourself']:
            with self.subTest(word=word):
                d=fixture([word+' repair useful tools.','We save valuable materials.','I protect local resources.'])
                s=d['sentences'][0];s['glosses'].pop(0)
                s['lexical_coverage'][0].update(gloss_id=None,exemption='standalone-you',reason='잘못 확대한 제외')
                with self.assertRaises(ValueError):m.check(d)

    def test_you_inside_expression_gloss_is_not_deleted_or_banned(self):
        s=fixture(['You know useful tools.','We save valuable materials.','I protect local resources.'])['sentences'][0]
        s['glosses'].pop(1)
        s['glosses'][0].update(headword='you know',meaning_ko='있잖아요',spans=[[0,8]])
        s['lexical_coverage'][1]['gloss_id']=s['glosses'][0]['id']
        before=deepcopy(s)
        self.assertEqual(m.glossary(s,{},require_reading_checks=True)[s['glosses'][0]['id']]['headword'],'you know')
        self.assertEqual(s,before)

    def test_legacy_you_gloss_remains_readable_without_new_rule_claim(self):
        d=fixture(['You repair useful tools.','We save valuable materials.','I protect local resources.'])
        d.pop('rule_revision');before=deepcopy(d)
        self.assertEqual(m.check(d)['status'],'STRUCTURE_PASS')
        self.assertEqual(d,before)

    def test_current_hint_requires_display_pairs_but_legacy_remains_readable(self):
        d=fixture();d['sentences'][0]['hints']=[{'span':[12,24],
            'meaning_ko':'유용한 도구','explanation':'검수용 구조 근거'}]
        with self.assertRaisesRegex(ValueError,'display_pairs'):
            m.check(d)
        d.pop('rule_revision')
        self.assertEqual(m.check(d)['status'],'STRUCTURE_PASS')
        self.assertNotIn('display_pairs',d['sentences'][0]['hints'][0])

    def test_explicit_hint_pair_schema_rejects_missing_or_wrong_language(self):
        invalid=[None,{},[],[None],[{}],[{'en':1,'ko':'뜻'}],
            [{'en':'[useful]','ko':'English only'}],[{'en':'[유용한]','ko':'[유용한]'}],
            [{'en':'[useful]\n tools','ko':'[유용한] 도구'}],
            [{'en':' [useful] tools','ko':'[유용한] 도구'}],
            [{'en':'[useful]','ko':'[유용한]'}]*4]
        for value in invalid:
            with self.subTest(value=value),self.assertRaises(ValueError):
                display_pairs({'display_pairs':value})

    def test_hint_brackets_must_be_balanced_nonnested_and_matched(self):
        invalid=[('[useful tools','[유용한] 도구'),('useful] tools','[유용한] 도구'),
            ('[useful] tools','유용한 도구'),('[[useful]] tools','[유용한] 도구'),
            ('[] useful tools','[유용한] 도구'),('[useful] tools','[유용한] [도구]')]
        for en,ko in invalid:
            with self.subTest(en=en,ko=ko),self.assertRaisesRegex(ValueError,'bracket'):
                display_pairs({'display_pairs':[{'en':en,'ko':ko}]})

    def test_unbracketed_stages_are_only_for_function_combination_hints(self):
        h={'display_pairs':[{'en':'be p.p. + dug up','ko':'파내어지다'}]}
        with self.assertRaisesRegex(ValueError,'corresponding brackets'):
            display_pairs(h)
        h['category']='function-combination'
        self.assertEqual(display_pairs(h),h['display_pairs'])

    def test_general_hint_requires_one_short_structure_label(self):
        h={'display_pairs':[{'en':'tools [we repair]','ko':'[우리가 고치는] 도구'}]}
        for label in [None,'',1,'   ','(목적격 관계대명사 생략)','문법\n설명','문법'*31,'English only']:
            with self.subTest(label=label),self.assertRaisesRegex(ValueError,'structure_label'):
                display_pairs({**h,'structure_label':label})
        h['structure_label']='목적격 관계대명사 that 생략'
        self.assertEqual(display_pairs(h),h['display_pairs'])

    def test_compact_function_pair_requires_formula_plus_lexical_form(self):
        for en in ['had predicted','had p.p.+predicted','had p.p. + ',
                   ' + predicted','had p.p. + + predicted']:
            with self.subTest(en=en),self.assertRaises(ValueError):
                display_pairs({'category':'function-combination',
                    'display_pairs':[{'en':en,'ko':'예측했다'}]})
        for en in ['had p.p + predicted','what to V + do']:
            h={'category':'function-combination','display_pairs':[{'en':en,'ko':'대응 뜻'}]}
            self.assertEqual(display_pairs(h),h['display_pairs'])

    def test_compact_function_pair_cannot_have_multiple_stages_or_general_label(self):
        pair={'en':'had p.p. + predicted','ko':'예측했다'}
        with self.assertRaisesRegex(ValueError,'exactly one compact pair'):
            display_pairs({'category':'function-combination','display_pairs':[pair,pair]})
        with self.assertRaisesRegex(ValueError,'must not append a structure_label'):
            display_pairs({'category':'function-combination','display_pairs':[pair],
                'structure_label':'과거완료'})

    def test_compact_function_pair_accepts_multiple_functions_on_one_line(self):
        from structure_hints import display_lines
        for en,ko in [('be V-ing + be p.p. + produced','생산되고 있다'),
                      ('can + be p.p. + dug up','파내어질 수 있다')]:
            with self.subTest(en=en):
                h={'category':'function-combination','display_pairs':[{'en':en,'ko':ko}]}
                self.assertEqual(display_lines(h),[en+' → '+ko])

    def test_compact_hint_rejects_explicitly_split_modal_perfect_formulas(self):
        for modal in ['may', 'might', 'must', 'should', 'could', 'would', 'can',
                      'will', 'shall', 'may not', 'cannot', "can't", "couldn’t",
                      'should not', "shouldn't", "won't", 'need not', "needn't", 'ought to']:
            for formula in [f'{modal} + have p.p.', f'{modal} + have p.p',
                            f'{modal} + have + p.p.', f'{modal} have + p.p.']:
                with self.subTest(formula=formula), self.assertRaisesRegex(ValueError, 'Modal-perfect'):
                    display_pairs({'category':'function-combination', 'display_pairs':[
                        {'en':formula+' + provided A with B', 'ko':'대응 뜻'}]})

    def test_compact_hint_rejects_modal_perfect_formula_and_preserves_other_combinations(self):
        for en in ['may have p.p. + provided A with B', 'Might have p.p + predicted',
                   'should not have p.p. + left', "can't have p.p. + arrived", 'ought to have p.p. + helped']:
            with self.subTest(en=en), self.assertRaisesRegex(ValueError, 'Modal-perfect'):
                display_pairs({'category':'function-combination', 'display_pairs':[{'en':en,'ko':'대응 뜻'}]})
        for en in ['have p.p. + predicted', 'had p.p. + predicted', 'can + be p.p. + dug up', 'what to V + do']:
            with self.subTest(en=en):
                hint={'category':'function-combination', 'display_pairs':[{'en':en,'ko':'대응 뜻'}]}
                before=deepcopy(hint)
                self.assertEqual(display_pairs(hint), hint['display_pairs'])
                self.assertEqual(hint,before)

    def test_modal_perfect_hint_preserves_original_verb_only_and_linked_complement_gloss(self):
        for modal in ['may', 'may not', "couldn't", 'cannot', 'ought to']:
            with self.subTest(modal=modal):
                data=modal_hint_fixture(modal); before=deepcopy(data)
                self.assertEqual(m.check(data,scope='learning')['status'],'STRUCTURE_PASS')
                self.assertEqual(data,before)
                hint=data['sentences'][0]['hints'][0]
                self.assertEqual(hint['display_pairs'][0]['en'],modal+' have provided')
                self.assertLess(hint['display_span'][1],hint['span'][1])

    def test_modal_perfect_hint_rejects_formula_slots_complements_and_invalid_mode_span(self):
        original=modal_hint_fixture()['sentences'][0]['hints'][0]
        for en in ['may + have + provided', 'may have p.p.', 'may have A', 'may have provided A with B']:
            with self.subTest(en=en), self.assertRaisesRegex(ValueError,'Verb-function'):
                display_pairs({**original,'display_pairs':[{'en':en,'ko':'제공했을지도 모른다'}]})
        for edit in [{'display_mode':None},{'display_mode':'unknown'},{'display_span':None},
                     {'display_span':[True,10]},{'display_span':[10,10]},{'category':'paired-structure'}]:
            with self.subTest(edit=edit), self.assertRaises(ValueError):
                display_pairs({**original,**edit})

    def test_modal_perfect_hint_requires_exact_source_range_and_linked_function_and_lexical_gloss(self):
        edits = [lambda s: s['hints'][0]['display_pairs'][0].update(en='might have provided'),
                 lambda s: s['hints'][0].update(display_span=[0,22]),
                 lambda s: s['hints'][0].update(display_span=[5,23]),
                 lambda s: s['hints'][0]['display_pairs'][0].update(en='may have Provided')]
        for edit in edits:
            data=modal_hint_fixture(); edit(data['sentences'][0])
            pair=data['sentences'][0]['hints'][0]['display_pairs'][0]
            pair.update(aligned_pair(pair['en'],pair['ko'],
                                     ([pair['en'].rsplit(' ',1)[0]],['했을지도 모른다'])))
            with self.assertRaisesRegex(ValueError,'Verb-function'):
                m.check(data,scope='learning')
        data=modal_hint_fixture('may not')
        data['sentences'][0]['hints'][0]['display_pairs'][0]=aligned_pair(
            'may have provided','제공했을지도 모른다',(['may have'],['했을지도 모른다']))
        with self.assertRaisesRegex(ValueError,'exact original'):
            m.check(data,scope='learning')
        data=modal_hint_fixture(); s=data['sentences'][0]; hint=s['hints'][0]
        unrelated=s['glosses'][-1]; unrelated['kind']='lexical'
        s['glosses'][1]['combines_with']=[unrelated['id']]
        hint['gloss_ids']=[s['glosses'][1]['id'],unrelated['id']]
        hint['span'][1]=unrelated['spans'][0][1]
        with self.assertRaisesRegex(ValueError,'end at a linked lexical verb'):
            m.check(data,scope='learning')

    def test_malformed_explicit_hint_pairs_are_rejected_in_legacy_too(self):
        d=fixture();d.pop('rule_revision')
        d['sentences'][0]['hints']=[{'span':[12,24], 'meaning_ko':'뜻',
            'explanation':'검수 근거','display_pairs':'not a list'}]
        with self.assertRaisesRegex(ValueError,'display_pairs'):
            m.check(d)

    def test_integrated_source_annotation_workbook_connection(self):
        result = m.check(fixture())
        self.assertEqual(result['status'], 'STRUCTURE_PASS')
        self.assertEqual(result['sv_lines']['src/s1'], 'S: They, V: repair')
        self.assertEqual(result['gloss_count'], 12)
        self.assertEqual(result['semantic_review'], 'NOT_PERFORMED')

    def rejected(self, edit, pattern=None):
        data = fixture()
        edit(data)
        with self.assertRaisesRegex(ValueError, pattern or '.'):
            m.check(data)

    def test_changed_original_not_normalized_away(self):
        self.rejected(lambda d: d['sentences'][0].update(text='they repair useful tools.'))

    def test_missing_lexical_word_cannot_pass(self):
        self.rejected(lambda d: d['sentences'][0]['lexical_coverage'].pop())

    def test_middle1_word_cannot_be_basic_exempt(self):
        self.rejected(lambda d: d['sentences'][0]['lexical_coverage'][2].update(
            gloss_id=None, exemption='below-middle1-unneeded', level='middle1', reason='기초라고 주장'))

    def test_mandatory_pronoun_cannot_be_basic_exempt(self):
        self.rejected(lambda d: d['sentences'][0]['lexical_coverage'][0].update(
            gloss_id=None, exemption='below-middle1-unneeded', level='below-middle1', reason='쉽다는 이유'))

    def test_mandatory_pronoun_needs_referent(self):
        self.rejected(lambda d: d['sentences'][0]['glosses'][0].pop('referent_ko'))

    def test_star_cannot_be_unlinked(self):
        self.rejected(lambda d: d['sentences'][0]['glosses'][2].update(star=True))

    def test_removed_star_on_today_word_fails(self):
        self.rejected(lambda d: d['sentences'][0]['glosses'][1].update(star=False))

    def test_omitted_flow_sentence_fails(self):
        self.rejected(lambda d: d['units'][0]['analysis']['flow'][0]['sentence_ids'].pop())

    def test_optional_flow_stage_label_is_accepted_without_rewriting_input(self):
        d=fixture();d['units'][0]['analysis']['flow'][0]['label']='도입'
        before=deepcopy(d)
        self.assertEqual(m.check(d,scope='learning')['status'],'STRUCTURE_PASS')
        self.assertEqual(d,before)

    def test_provided_flow_stage_label_must_be_nonempty_text(self):
        for value in [None,1,True,[],{},'', '  ']:
            with self.subTest(label=value):
                d=fixture();d['units'][0]['analysis']['flow'][0]['label']=value
                with self.assertRaisesRegex(ValueError,'Flow stage label'):
                    m.check(d,scope='learning')

    def test_wrong_workbook_key_mapping_fails(self):
        self.rejected(lambda d: d['units'][0]['workbook'].update(key_sentence_ids=['s1', 's3']))

    def test_easy_explanation_accepts_one_or_many_sentences_without_mutating_input(self):
        for count in [1, 4, 8]:
            with self.subTest(count=count):
                data = fixture()
                data['units'][0]['analysis']['easy_explanations'][0]['explanatory_sentences'] = [
                    f'이는 {index}번째 설명이다.' for index in range(count)]
                before = deepcopy(data)
                for scope in ['learning', 'full']:
                    self.assertEqual(m.check(data, scope=scope)['status'], 'STRUCTURE_PASS')
                self.assertEqual(data, before)

    def test_easy_explanation_still_requires_nonempty_text_items(self):
        for value in [None, '', [], [''], ['   '], [None], [1]]:
            with self.subTest(value=value):
                data = fixture()
                data['units'][0]['analysis']['easy_explanations'][0]['explanatory_sentences'] = value
                with self.assertRaisesRegex(ValueError, '[Ee]asy explanation'):
                    m.check(data, scope='learning')

    def test_easy_explanation_source_selection_count_and_order_are_preserved(self):
        data = fixture()
        data['units'][0]['analysis']['easy_explanations'].pop()
        with self.assertRaisesRegex(ValueError, 'Existing distinct source sentences'):
            m.check(data, scope='learning')
        data = fixture()
        data['units'][0]['analysis']['easy_explanations'].reverse()
        with self.assertRaisesRegex(ValueError, 'original sentence order'):
            m.check(data, scope='learning')

    def test_wrong_synonym_workbook_term_fails(self):
        self.rejected(lambda d: d['units'][0]['workbook']['relation_order'].append('invented'))

    def test_unreported_shortage_fails(self):
        self.rejected(lambda d: d['units'][0]['analysis']['grammar_points'].pop())

    def test_reported_shortage_accepted_without_final_claim(self):
        d = fixture()
        d['units'][0]['analysis']['grammar_points'].pop()
        d['units'][0]['quantity_exceptions'] = [{'field': 'grammar_points', 'actual': 2, 'expected': 3,
            'reason': '시험용 원문 근거 부족', 'reported_to_user': '테스트 보고 기록'}]
        result = m.check(d)
        self.assertEqual(result['status'], 'STRUCTURE_PASS')
        self.assertEqual(len(result['shortages']), 1)

    def test_contained_hints_must_merge(self):
        self.rejected(lambda d: d['sentences'][0].update(hints=[
            {'span': [0, 11], 'meaning_ko': '뜻', 'explanation': '설명'},
            {'span': [5, 11], 'meaning_ko': '뜻', 'explanation': '설명'}]))

    def test_proper_name_reference_to_missing_gloss_fails(self):
        self.rejected(lambda d: d['sentences'][0]['lexical_coverage'][2].update(
            gloss_id=None, exemption='proper-name-repeat', first_gloss_id='missing', reason='첫 등장 주장'))

    def test_unheaded_source_review_keeps_task_pending(self):
        d = fixture()
        d['paragraphs'][0]['subheading_id'] = None
        d['sources'][0]['subheadings'] = []
        self.assertEqual(m.check(d)['status'], 'NEEDS_SOURCE_REVIEW')

    def test_actual_source_review_decision_completes_grouping(self):
        d = fixture()
        d['paragraphs'][0]['subheading_id'] = None
        d['sources'][0]['subheadings'] = []
        d['grouping_resolutions'] = [{'source_id': 'src', 'paragraph_ids': ['p1'],
                                     'instruction': '이 세 문장을 하나의 단위로 유지한다는 시험 결정'}]
        self.assertEqual(m.check(d)['status'], 'STRUCTURE_PASS')

    def test_learning_scope_does_not_require_future_workbook_records(self):
        d = fixture()
        del d['units'][0]['workbook']
        self.assertEqual(m.check(d, scope='learning')['status'], 'STRUCTURE_PASS')
        with self.assertRaisesRegex(ValueError, 'Workbook'):
            m.check(d, scope='full')

    def test_legacy_heading_id_is_pending_not_replaced_by_analysis_title(self):
        d = fixture()
        del d['sources'][0]['subheadings']
        result = m.check(d)
        self.assertEqual(result['status'], 'NEEDS_SOURCE_REVIEW')
        self.assertEqual(result['source_issues'][0]['code'], 'MISSING_SOURCE_SUBHEADING')
        self.assertNotIn('subheadings', d['sources'][0])

    def test_original_heading_identity_and_anchor_are_verified(self):
        d = fixture()
        heading = unit_subheadings(d,d['units'][0])[0]
        self.assertEqual(heading['text'],'Synthetic Source Heading')
        self.assertNotEqual(heading['text'],d['units'][0]['analysis']['title_or_topic_en'])
        d['sources'][0]['subheadings'][0]['before_sentence_id']='s2'
        with self.assertRaisesRegex(ValueError,'anchor'):
            m.check(d)

    def test_heading_source_hash_cannot_be_from_another_artifact(self):
        d = fixture()
        d['sources'][0]['subheadings'][0]['artifact_sha256']='1'*64
        with self.assertRaisesRegex(ValueError,'artifact hash'):
            m.check(d)

    def test_lesson_identity_preserves_internal_id_and_formats_display(self):
        for value in ['UNIT03','LESSON 3','제3과','3과','03']:
            self.assertEqual(display_lesson({'lesson':value},{'lesson_number':'03'}),'3과')
            self.assertEqual(lesson_identity({'lesson':value})['internal_id'],'UNIT03')
        d = fixture();d['cover']={'lesson_number':'4'}
        with self.assertRaisesRegex(ValueError,'Lesson identity conflict'):
            m.check(d)

    def _joined_fixture(self):
        d=fixture();source=d['sources'][0];parts=[s['text'] for s in d['sentences']]
        source['text']=''.join(parts);offset=0
        for bound,part in zip(source['sentences'],parts):
            bound['start']=offset;bound['end']=offset+len(part);offset+=len(part)
        return d

    def test_joined_sentence_boundary_needs_review_and_is_not_auto_corrected(self):
        d=self._joined_fixture();before=d['sources'][0]['text']
        result=m.check(d)
        self.assertEqual(result['status'],'NEEDS_SOURCE_REVIEW')
        self.assertEqual([x['code'] for x in result['source_issues']],['JOINED_SENTENCE_BOUNDARY']*2)
        self.assertIn('tools.We',before)
        self.assertEqual(d['sources'][0]['text'],before)

    def test_confirmed_no_space_boundary_exception_is_source_and_text_bound(self):
        d=self._joined_fixture();source=d['sources'][0]
        source['boundary_reviews']=[{
            'left_sentence_id':f's{i}', 'right_sentence_id':f's{i+1}',
            'resolution':'source-confirmed-no-space','reason':'Synthetic no-space source for test only',
            'verification_record':'Synthetic original reviewed for fixture',
            'artifact_sha256':source['provenance']['sha256'],
            'transcription_sha256':transcription_sha256(source)} for i in (1,2)]
        self.assertEqual(m.check(d)['status'],'STRUCTURE_PASS')
        source['boundary_reviews'][0]['transcription_sha256']='1'*64
        with self.assertRaisesRegex(ValueError,'stale'):
            m.check(d)

    def test_newline_source_boundary_is_normal_without_exception(self):
        d=fixture();source=d['sources'][0]
        source['text']='\n'.join(s['text'] for s in d['sentences'])
        self.assertEqual(m.check(d)['status'],'STRUCTURE_PASS')


if __name__ == '__main__':
    unittest.main()
