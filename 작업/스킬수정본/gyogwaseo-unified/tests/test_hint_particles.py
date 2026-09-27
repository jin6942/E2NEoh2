"""Authored bilingual grammar links and saved Word style mutation checks."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest
import uuid
from zipfile import ZipFile
from lxml import etree as E

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / '../scripts'))
from structure_hints import (display_pairs, display_lines, aligned_display_segments,
                             bracket_spans, korean_grammar_bracket_spans,
                             omitted_relative_source_text, omitted_conjunction_source_text,
                             VERB_CONSTRUCTION_EMPHASIS)
from book_plan import structure_hint_element
from master_docx import RoleBank, write, NS, tag, set_property
from check_saved_docx import check


def occurrence(text, selected, n=1):
    start = -1
    for _ in range(n):
        start = text.index(selected, start + 1)
    return [start, start + len(selected)]


def linked_hint(en, ko, links, label='구조 연결'):
    pair = {'en': en, 'ko': ko, 'emphasis_links': []}
    for english, korean in links:
        pair['emphasis_links'].append({
            'en_spans': [occurrence(en, *x) if isinstance(x, tuple) else occurrence(en, x) for x in english],
            'ko_spans': [occurrence(ko, *x) if isinstance(x, tuple) else occurrence(ko, x) for x in korean],
        })
    return {'structure_label': label, 'display_pairs': [pair]}


def examples():
    return [
        linked_hint('[using her miniature crime scenes]', '[그녀의 범죄 현장 미니어처를 사용하여]',
                    [(['ing'], ['하여'])], '분사구문'),
        linked_hint('a career [of more than thirty years]', '[30년 이상의] 경력',
                    [(['of'], ['의'])], '전치사구 후치수식'),
        linked_hint('detectives [not only from the US but also from Canada]',
                    '[미국에서뿐만 아니라 캐나다에서도 온] 형사들',
                    # Selected contextual gloss: from — ~에서 온. Share 온 once.
                    [([('from', 1), ('from', 2)], [('에서', 1), ('에서', 2), '온'])], '전치사구 후치수식'),
        linked_hint('[if the scene in the miniature resulted]', '[미니어처 속의 현장이 비롯되었는지]',
                    [(['if'], ['이', '는지'])], '접속사 if'),
        linked_hint('[With the planet becoming warmer]', '[지구가 더 따뜻해지면서]',
                    [(['With', 'ing'], ['가', '면서'])], 'with 구문'),
    ]


def reference_hint(particle='이'):
    hint = linked_hint('the fact [that they can recognize]',
                       '[그것들[문어]' + particle + ' 알아볼 수 있다는] 사실',
                       [(['that'], [particle, '다는'])], '동격의 접속사 that')
    pair = hint['display_pairs'][0]
    pair['pronoun_refs'] = [{
        'en_span': occurrence(pair['en'], 'they'),
        'ko_pronoun_span': occurrence(pair['ko'], '그것들'),
        'ko_reference_span': occurrence(pair['ko'], '[문어]'),
    }]
    return hint


def run_rows(hint):
    element = structure_hint_element(hint)
    paragraph = RoleBank().paragraph('structure_hint', element['runs'])
    return paragraph, [(
        ''.join(run.xpath('./w:t/text()', namespaces=NS)), run.find('w:rPr', NS)
    ) for run in paragraph.findall('w:r', NS)]


class HintParticleTests(unittest.TestCase):
    def test_declared_pronoun_reference_preserves_every_character_and_only_grammar_emphasis(self):
        # Particle choice is authored language-review evidence, not an engine inference.
        for particle in ['이', '가']:
            hint = reference_hint(particle); before = deepcopy(hint)
            pair = display_pairs(hint, require_alignment=True)[0]
            self.assertEqual(korean_grammar_bracket_spans(pair), [(0, 20)])
            self.assertEqual([v for marked, v in aligned_display_segments(pair, 'ko') if marked],
                             [particle, '다는'])
            for language in ('en', 'ko'):
                self.assertEqual(''.join(v for _, v in aligned_display_segments(pair, language)), pair[language])
            paragraph, rows = run_rows(hint)
            marked = []
            for value, props in rows:
                if value == '구조 힌트   ':
                    continue
                underline = props.find('w:u', NS)
                underlined = underline is not None and underline.get(tag('val')) == 'single'
                bold = props.find('w:b', NS)
                bolded = bold is not None and bold.get(tag('val'), '1') != '0'
                self.assertEqual(bolded, underlined, value)
                if underlined:
                    marked.append(value)
                if '문어' in value:
                    self.assertIn('그것들[문어]', value)
                    self.assertFalse(underlined)
            self.assertEqual(marked, ['that', particle, '다는'])
            self.assertEqual(''.join(paragraph.xpath('.//w:t/text()', namespaces=NS)),
                             '구조 힌트   ' + display_lines(hint)[0])
            self.assertEqual(hint, before)

    def test_reference_exception_does_not_relax_undeclared_or_english_brackets(self):
        hint = reference_hint()
        with self.assertRaisesRegex(ValueError, 'nested'):
            bracket_spans(hint['display_pairs'][0]['ko'])
        hint['display_pairs'][0].pop('pronoun_refs')
        with self.assertRaisesRegex(ValueError, 'nested'):
            display_pairs(hint)
        hint = reference_hint(); pair = hint['display_pairs'][0]
        pair['ko'] += ' [다른 [구조]]'
        with self.assertRaisesRegex(ValueError, 'nested'):
            display_pairs(hint)
        hint = reference_hint(); pair = hint['display_pairs'][0]
        pair['en'] += ' [another [structure]]'
        with self.assertRaisesRegex(ValueError, 'nested'):
            display_pairs(hint)
        hint = reference_hint(); pair = hint['display_pairs'][0]
        pair['ko'] += ' [추가 구조]'
        with self.assertRaisesRegex(ValueError, 'counts must match'):
            display_pairs(hint)
        # An ordinary legacy pair remains unchanged without any inferred reference.
        old = linked_hint('the fact [that they can recognize]', '[그것들이 알아볼 수 있다는] 사실',
                          [(['that'], ['이', '다는'])])
        before = deepcopy(old)
        display_pairs(old, require_alignment=True)
        self.assertEqual(old, before)

    def test_pronoun_reference_ranges_require_exact_fields_bounded_integers_and_distinct_order(self):
        baseline = reference_hint()['display_pairs'][0]['pronoun_refs']
        malformed = [None, {}, '', [], [None], [{}], [dict(baseline[0], referent_ko='문어')],
                     baseline * 2]
        for field in ('en_span', 'ko_pronoun_span', 'ko_reference_span'):
            for selected in (None, [1], [True, 4], [1, 2.5], [-1, 4], [4, 4], [1, 1000]):
                row = deepcopy(baseline[0]); row[field] = selected
                malformed.append([row])
        for refs in malformed:
            hint = reference_hint(); hint['display_pairs'][0]['pronoun_refs'] = refs
            with self.subTest(refs=refs), self.assertRaisesRegex(ValueError, 'pronoun_refs'):
                display_pairs(hint)
        hint = linked_hint('[they help them]', '[그들[연구자]이 그것들[문어]을 돕는]',
                           [(['help'], ['는'])])
        pair = hint['display_pairs'][0]
        pair['pronoun_refs'] = [
            {'en_span': occurrence(pair['en'], en), 'ko_pronoun_span': occurrence(pair['ko'], ko),
             'ko_reference_span': occurrence(pair['ko'], ref)}
            for en, ko, ref in [('they', '그들', '[연구자]'), ('them', '그것들', '[문어]')]]
        display_pairs(hint, require_alignment=True)
        self.assertEqual(korean_grammar_bracket_spans(pair), [(0, len(pair['ko']))])
        pair['pronoun_refs'].reverse()
        with self.assertRaisesRegex(ValueError, 'ordered and nonoverlapping'):
            display_pairs(hint)

    def test_reference_english_span_is_a_whole_declared_pronoun_word(self):
        for word in ['they', 'This', 'herself', 'their', 'one', 'ones', 'other', 'others']:
            hint = reference_hint(); pair = hint['display_pairs'][0]
            pair['en'] = pair['en'].replace('they', word)
            pair['pronoun_refs'][0]['en_span'] = occurrence(pair['en'], word)
            display_pairs(hint, require_alignment=True)
        for text, selected in [('thistle', 'this'), ('otherworld', 'other'),
                               ('their-like', 'their'), ("they'reading", 'they'),
                               ('octopus', 'octopus'), ('US', 'US')]:
            hint = reference_hint(); pair = hint['display_pairs'][0]
            pair['en'] = pair['en'].replace('they', text)
            pair['pronoun_refs'][0]['en_span'] = occurrence(pair['en'], selected)
            with self.subTest(text=text), self.assertRaisesRegex(ValueError, 'whole English'):
                display_pairs(hint)

    def test_reference_translation_order_can_reverse_without_reusing_korean_ranges(self):
        english = 'the one [(that) it lost]'
        korean = '[그것[문어]이 잃었던] 것[팔]'
        hint = linked_hint(english, korean, [(['that'], ['이', '던'])], '목적격 관계대명사 that 생략')
        hint.update(display_mode='omitted-relative', omitted_relative='that')
        pair = hint['display_pairs'][0]
        pair['pronoun_refs'] = [
            {'en_span': occurrence(english, 'one'), 'ko_pronoun_span': occurrence(korean, '것', 2),
             'ko_reference_span': occurrence(korean, '[팔]')},
            {'en_span': occurrence(english, 'it'), 'ko_pronoun_span': occurrence(korean, '그것'),
             'ko_reference_span': occurrence(korean, '[문어]')},
        ]
        before = deepcopy(hint)
        display_pairs(hint, require_alignment=True)
        self.assertEqual(omitted_relative_source_text(hint), 'the one it lost')
        self.assertEqual(korean_grammar_bracket_spans(pair), [(0, korean.index('] 것') + 1)])
        paragraph, rows = run_rows(hint)
        self.assertIn(korean, ''.join(paragraph.xpath('.//w:t/text()', namespaces=NS)))
        self.assertEqual([value for value, props in rows if props.find('w:u', NS) is not None
                          and props.find('w:u', NS).get(tag('val')) == 'single'], ['that', '이', '던'])
        self.assertEqual(hint, before)
        for pronoun in ('그것', '것'):
            changed = deepcopy(hint); changed_pair = changed['display_pairs'][0]
            changed_pair['pronoun_refs'][0].update(
                ko_pronoun_span=occurrence(korean, pronoun),
                ko_reference_span=occurrence(korean, '[문어]'))
            with self.subTest(pronoun=pronoun), self.assertRaisesRegex(ValueError, 'must not overlap or be reused'):
                display_pairs(changed, require_alignment=True)

    def test_reference_pronoun_allows_only_complete_observed_contraction_suffixes(self):
        for apostrophe in ("'", '’'):
            for suffix, pronoun in [('s', 'That'), ('re', 'they'), ('ve', 'we'),
                                    ('ll', 'it'), ('d', 'she'), ('m', 'I')]:
                english = pronoun + apostrophe + suffix + ' [why they survive]'
                korean = '그것[문어의 능력]이 [그들이 살아남는 이유다]'
                hint = linked_hint(english, korean, [(['why'], ['이유'])], '관계부사 why')
                pair = hint['display_pairs'][0]
                pair['pronoun_refs'] = [{'en_span': [0, len(pronoun)],
                                        'ko_pronoun_span': occurrence(korean, '그것'),
                                        'ko_reference_span': occurrence(korean, '[문어의 능력]')}]
                with self.subTest(english=english):
                    display_pairs(hint, require_alignment=True)
                    self.assertEqual(''.join(v for _, v in aligned_display_segments(pair, 'en')), english)
                    self.assertEqual([v for marked, v in aligned_display_segments(pair, 'en') if marked], ['why'])
            for tail in ('sword', 'remainder', 'veiled', 'llama', 'dog', 'more', 't', 's-like', "s're"):
                hint = reference_hint(); pair = hint['display_pairs'][0]
                pair['en'] = pair['en'].replace('they', 'they' + apostrophe + tail)
                with self.subTest(apostrophe=apostrophe, tail=tail), self.assertRaisesRegex(ValueError, 'whole English'):
                    display_pairs(hint)

    def test_reference_must_follow_plain_korean_pronoun_and_have_one_nonempty_bracket(self):
        for pronoun, ref in [('그것들 ', '[문어]'), ('그것들,', '[문어]'),
                             ('[그것들]', '[문어]'), ('그것들', '[]'), ('그것들', '[  ]'),
                             ('그것들', '[문[어]]'), ('그것들', '[문어\n]'), ('그것들', '문어')]:
            hint = reference_hint(); pair = hint['display_pairs'][0]
            pair['ko'] = '[' + pronoun + ref + '이 알아볼 수 있다는] 사실'
            pair['pronoun_refs'][0].update(ko_pronoun_span=[1, 1 + len(pronoun)],
                                          ko_reference_span=[1 + len(pronoun), 1 + len(pronoun) + len(ref)])
            with self.subTest(pronoun=pronoun, ref=ref), self.assertRaises(ValueError):
                display_pairs(hint)
        hint = reference_hint(); pair = hint['display_pairs'][0]
        pair['ko'] = pair['ko'].replace('그것들[', '그것들 [')
        pair['pronoun_refs'][0]['ko_reference_span'] = occurrence(pair['ko'], '[문어]')
        with self.assertRaisesRegex(ValueError, 'immediately follow'):
            display_pairs(hint)

    def test_reference_and_pronoun_cannot_be_included_in_korean_grammar_emphasis(self):
        for selected in ('문어', '문', '[문어]', '그것들', '그것들[문어]이'):
            hint = reference_hint(); pair = hint['display_pairs'][0]
            pair['emphasis_links'][0]['ko_spans'] = [occurrence(pair['ko'], selected)]
            with self.subTest(selected=selected), self.assertRaises(ValueError):
                display_pairs(hint, require_alignment=True)
            with self.assertRaises(ValueError):
                aligned_display_segments(pair, 'ko')

    def test_omitted_modes_count_only_grammar_brackets_and_preserve_source_removal(self):
        for mode, english, korean, label, ending, expected in [
                ('relative', 'arms [(that) they lost]', '[그것들[문어]이 잃었던] 팔',
                 '목적격 관계대명사 that 생략', '던', 'arms they lost'),
                ('conjunction', '[(that) they can recognize]', '[그것들[문어]이 알아볼 수 있다는]',
                 '접속사 that 생략', '다는', 'they can recognize')]:
            hint = linked_hint(english, korean, [(['that'], ['이', ending])], label)
            hint.update(display_mode='omitted-' + mode, **{'omitted_' + mode: 'that'})
            pair = hint['display_pairs'][0]
            pair['pronoun_refs'] = [{'en_span': occurrence(english, 'they'),
                                    'ko_pronoun_span': occurrence(korean, '그것들'),
                                    'ko_reference_span': occurrence(korean, '[문어]')}]
            display_pairs(hint, require_alignment=True)
            remove = omitted_relative_source_text if mode == 'relative' else omitted_conjunction_source_text
            self.assertEqual(remove(hint), expected)
            paragraph, rows = run_rows(hint)
            self.assertIn(korean, ''.join(paragraph.xpath('.//w:t/text()', namespaces=NS)))
            marked = [value for value, props in rows if props.find('w:u', NS) is not None
                      and props.find('w:u', NS).get(tag('val')) == 'single']
            self.assertEqual(marked, ['that', '이', ending])
            pair['emphasis_links'][0]['ko_spans'] = [occurrence(korean, '문어')]
            with self.assertRaisesRegex(ValueError, 'referent plain'):
                display_pairs(hint, require_alignment=True)

    def test_pronoun_reference_does_not_add_function_combination_exception(self):
        hint = reference_hint(); hint['category'] = 'function-combination'
        with self.assertRaisesRegex(ValueError, 'Function-combination hints do not use pronoun_refs'):
            display_pairs(hint)

    def test_learning_checker_and_saved_word_keep_declared_reference_plain(self):
        from test_learning_content import fixture
        from check_learning_content import check as check_learning
        original = 'They know the fact that they can recognize.'
        data = fixture([original, 'We save valuable materials.', 'I protect local resources.'])
        hint = reference_hint()
        hint.update(span=[original.index('the fact'), len(original) - 1],
                    meaning_ko='그것들[문어]이 알아볼 수 있다는 사실', explanation='명시적으로 검수할 대명사 참조 시험')
        data['sentences'][0]['hints'] = [hint]
        before = deepcopy(data)
        self.assertEqual(check_learning(data, scope='learning')['status'], 'STRUCTURE_PASS')
        self.assertEqual(data, before)
        plan = {'blocks': [{'id': 'pronoun-reference', 'elements': [structure_hint_element(hint)]}]}
        folder = HERE / ('master-test-' + uuid.uuid4().hex); folder.mkdir()
        saved = folder / 'pronoun-reference.docx'; write(plan, saved)
        self.assertEqual(check(plan, saved)['errors'], [])
        with ZipFile(saved) as archive:
            root = E.fromstring(archive.read('word/document.xml'))
        run = next(r for r in root.findall('.//w:sdtContent/w:p/w:r', NS)
                   if '문어' in ''.join(r.xpath('./w:t/text()', namespaces=NS)))
        props = run.find('w:rPr', NS)
        self.assertEqual(props.find('w:b', NS).get(tag('val')), '0')
        self.assertIn(props.find('w:u', NS).get(tag('val')), ('none', '0'))

    def test_pronoun_reference_changes_keep_conservative_delta_review_scope(self):
        from test_review_packets import two_units
        from review_packets import _diff, _impact
        baseline = two_units()
        baseline['sentences'][0]['hints'] = [reference_hint()]
        for addition in (True, False):
            old, new = deepcopy(baseline), deepcopy(baseline)
            if addition:
                old['sentences'][0]['hints'][0]['display_pairs'][0].pop('pronoun_refs')
            else:
                new['sentences'][0]['hints'][0]['display_pairs'][0]['pronoun_refs'][0]['en_span'][0] += 1
            changes = _diff(old, new)
            self.assertTrue(any('pronoun_refs' in row['path'] for row in changes))
            units, _, report = _impact(new, old, changes)
            self.assertEqual(units, {'u1', 'u2'})
            self.assertTrue(report['full_learning_fallback'])
            self.assertTrue(report['full_questions_fallback'])

    def test_authored_verb_construction_policy_changes_only_english_emphasis(self):
        hint = linked_hint('[is called a detective]', '[형사라고 불린다]',
                           [(['is called'], ['라고 불린다'])], 'be called A 구문')
        default_paragraph, default_rows = run_rows(hint)
        hint['emphasis_policy'] = VERB_CONSTRUCTION_EMPHASIS
        before = deepcopy(hint)
        display_pairs(hint, require_alignment=True)
        paragraph, rows = run_rows(hint)
        marked = []
        for value, props in rows:
            if value == '구조 힌트   ':
                continue
            underline = props.find('w:u', NS)
            underlined = underline is not None and underline.get(tag('val')) == 'single'
            bold = props.find('w:b', NS)
            bolded = bold is not None and bold.get(tag('val'), '1') != '0'
            if props.find('w:color', NS).get(tag('val')) == '7030A0':
                self.assertFalse(bolded, value)
                self.assertFalse(underlined, value)
            elif underlined:
                self.assertTrue(bolded, value)
                marked.append(value)
        self.assertEqual(marked, ['라고 불린다'])
        self.assertEqual(hint, before)
        self.assertEqual(E.tostring(paragraph.find('w:pPr', NS)),
                         E.tostring(default_paragraph.find('w:pPr', NS)))
        self.assertEqual(''.join(paragraph.xpath('.//w:t/text()', namespaces=NS)),
                         ''.join(default_paragraph.xpath('.//w:t/text()', namespaces=NS)))
        self.assertTrue(any(value == 'is called' and props.find('w:u', NS) is not None
                            for value, props in default_rows))

    def test_verb_policy_rejects_unknown_values_and_wrong_hint_modes(self):
        for policy in [None, '', False, 'english-only', 'ko-only']:
            hint = examples()[0]; hint['emphasis_policy'] = policy
            with self.subTest(policy=policy), self.assertRaisesRegex(ValueError, 'emphasis_policy'):
                display_pairs(hint)
        for extra in [{'category': 'function-combination'}, {'category': 'paired-structure'},
                      {'display_mode': 'omitted-relative', 'omitted_relative': 'that'}]:
            hint = examples()[0]; hint.update(extra, emphasis_policy=VERB_CONSTRUCTION_EMPHASIS)
            with self.subTest(extra=extra), self.assertRaisesRegex(ValueError, 'general structure hint'):
                display_pairs(hint)

    def test_verb_policy_cannot_hide_missing_or_invalid_english_alignment(self):
        base = linked_hint('[is called a detective]', '[형사라고 불린다]',
                           [(['is called'], ['라고 불린다'])], 'be called A 구문')
        base['emphasis_policy'] = VERB_CONSTRUCTION_EMPHASIS
        def remove_links(pair):
            pair.pop('emphasis_links')
        def empty_links(pair):
            pair.update(emphasis_links=[], emphasis_note='영어를 인쇄할 때 강조하지 않음')
        def missing_english(pair):
            pair['emphasis_links'][0].pop('en_spans')
        def empty_english(pair):
            pair['emphasis_links'][0]['en_spans'] = []
        def outside_english(pair):
            pair['emphasis_links'][0]['en_spans'] = [[1, 1000]]
        def repeated_english(pair):
            pair['emphasis_links'].append(deepcopy(pair['emphasis_links'][0]))
        for mutate in (remove_links, empty_links, missing_english, empty_english,
                       outside_english, repeated_english):
            hint = deepcopy(base); mutate(hint['display_pairs'][0])
            with self.subTest(mutate=mutate.__name__), self.assertRaises(ValueError):
                structure_hint_element(hint)
        hint = {'emphasis_policy': VERB_CONSTRUCTION_EMPHASIS}
        with self.assertRaisesRegex(ValueError, 'display_pairs'):
            display_pairs(hint, required=False)

    def test_verb_policy_keeps_source_span_validation(self):
        from test_learning_content import fixture
        from check_learning_content import check as check_learning
        data = fixture(['She is called a detective.', 'We save valuable materials.', 'I protect local resources.'])
        hint = linked_hint('[is called a detective]', '[형사라고 불린다]',
                           [(['is called'], ['라고 불린다'])], 'be called A 구문')
        hint.update(span=[4, 25], meaning_ko='형사라고 불린다', explanation='독립 검수용 구문 연결',
                    emphasis_policy=VERB_CONSTRUCTION_EMPHASIS)
        data['sentences'][0]['hints'] = [hint]
        self.assertEqual(check_learning(data, scope='learning')['status'], 'STRUCTURE_PASS')
        hint['span'] = [4, 1000]
        with self.assertRaises(ValueError):
            check_learning(data, scope='learning')

    def test_saved_verb_policy_docx_rejects_english_emphasis_or_missing_korean_emphasis(self):
        hint = linked_hint('[is called a detective]', '[형사라고 불린다]',
                           [(['is called'], ['라고 불린다'])], 'be called A 구문')
        hint['emphasis_policy'] = VERB_CONSTRUCTION_EMPHASIS
        plan = {'blocks': [{'id': 'verb-hint-style', 'elements': [structure_hint_element(hint)]}]}
        folder = HERE / ('master-test-' + uuid.uuid4().hex); folder.mkdir()
        saved = folder / 'verb-hint.docx'; write(plan, saved)
        self.assertEqual(check(plan, saved)['errors'], [])
        with ZipFile(saved) as archive:
            package = [(entry, archive.read(entry.filename)) for entry in archive.infolist()]
        document = {entry.filename: raw for entry, raw in package}['word/document.xml']
        for n, (text, prop, value) in enumerate([
                ('is called', 'b', '1'), ('is called', 'u', 'single'),
                ('라고 불린다', 'b', '0'), ('라고 불린다', 'u', 'none')]):
            root = E.fromstring(document)
            run = next(r for r in root.findall('.//w:sdtContent/w:p/w:r', NS)
                       if ''.join(r.xpath('./w:t/text()', namespaces=NS)) == text)
            set_property(run.find('w:rPr', NS), prop, {'val': value})
            target = folder / f'changed-{n}.docx'
            with ZipFile(target, 'w') as archive:
                for entry, raw in package:
                    archive.writestr(entry, E.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
                                     if entry.filename == 'word/document.xml' else raw)
            with self.subTest(text=text, prop=prop):
                result = check(plan, target)
                self.assertIn('SAVED_FORMAT_MISMATCH', {row['code'] for row in result['errors']})
                self.assertNotIn('SAVED_CONTENT_MISMATCH', {row['code'] for row in result['errors']})

    def test_only_exact_bilingual_grammar_targets_are_bold_and_underlined(self):
        expected = [('ing', '하여'), ('of', '의'), ('fromfrom', '에서에서온'),
                    ('if', '이는지'), ('Withing', '가면서')]
        for hint, selected in zip(examples(), expected):
            with self.subTest(hint=hint):
                before = deepcopy(hint)
                display_pairs(hint, require_alignment=True)
                paragraph, rows = run_rows(hint)
                highlighted = {'7030A0': '', '000000': ''}
                for value, props in rows:
                    if value == '구조 힌트   ':
                        continue
                    underline = props.find('w:u', NS)
                    underlined = underline is not None and underline.get(tag('val')) == 'single'
                    bold = props.find('w:b', NS)
                    bolded = bold is not None and bold.get(tag('val'), '1') != '0'
                    self.assertEqual(bolded, underlined, value)
                    if underlined:
                        self.assertNotIn('[', value); self.assertNotIn(']', value)
                        highlighted[props.find('w:color', NS).get(tag('val'))] += value
                    self.assertEqual(props.find('w:sz', NS).get(tag('val')), '15')
                self.assertEqual(tuple(highlighted.values()), selected)
                self.assertEqual(hint, before)
                self.assertEqual(''.join(paragraph.xpath('.//w:t/text()', namespaces=NS)),
                                 '구조 힌트   ' + display_lines(hint)[0])

    def test_pairing_can_cross_language_order_without_merging_targets(self):
        hint = linked_hint('[if … because]', '[이므로 … 인지]',
                           [(['if'], ['인지']), (['because'], ['이므로'])])
        pair = display_pairs(hint, require_alignment=True)[0]
        self.assertEqual([v for marked, v in aligned_display_segments(pair, 'ko') if marked],
                         ['이므로', '인지'])

    def test_correlative_target_excludes_prepositions_and_content_words(self):
        hint = linked_hint('[not only from the US but also from Canada]',
                           '[미국에서뿐만 아니라 캐나다에서도]',
                           [(['not only', 'but also'], ['뿐만 아니라', '도'])], '상관어구')
        pair = display_pairs(hint, require_alignment=True)[0]
        self.assertEqual([x for yes, x in aligned_display_segments(pair, 'en') if yes],
                         ['not only', 'but also'])
        self.assertEqual([x for yes, x in aligned_display_segments(pair, 'ko') if yes],
                         ['뿐만 아니라', '도'])

    def test_missing_current_alignment_and_old_one_sided_fields_are_rejected(self):
        hint = examples()[0]; pair = hint['display_pairs'][0]
        pair.pop('emphasis_links')
        with self.assertRaisesRegex(ValueError, 'emphasis_links'):
            display_pairs(hint, require_alignment=True)
        self.assertEqual(aligned_display_segments(pair, 'en'), [(False, pair['en'])])
        for field in ['ko_emphasis_spans', 'en_emphasis_spans']:
            old = deepcopy(hint); old['display_pairs'][0][field] = []
            with self.assertRaisesRegex(ValueError, 'legacy'):
                display_pairs(old)

    def test_absent_overt_counterpart_requires_recorded_reason_and_no_guess(self):
        hint = {'structure_label': '최소 형용사 수식', 'display_pairs': [{
            'en': '[useful] tools', 'ko': '[유용한] 도구', 'emphasis_links': []}]}
        with self.assertRaisesRegex(ValueError, 'emphasis_note'):
            display_pairs(hint, require_alignment=True)
        pair = hint['display_pairs'][0]
        pair['emphasis_note'] = '합성 수식 시험에서 한국어 관형형 어미에 대응되는 독립 영어 문법 표면형이 없다.'
        display_pairs(hint, require_alignment=True)
        for language in ('en', 'ko'):
            self.assertEqual(aligned_display_segments(pair, language), [(False, pair[language])])

    def test_omitted_relative_marks_letters_only_and_keeps_editorial_parentheses_plain(self):
        hint = linked_hint('tools [(that) we repair]', '[우리가 고치는] 도구',
                           [(['that'], ['가', '는'])], '목적격 관계대명사 that 생략')
        hint.update(display_mode='omitted-relative', omitted_relative='that')
        display_pairs(hint, require_alignment=True)
        paragraph, rows = run_rows(hint)
        marked = []
        for value, props in rows:
            underline = props.find('w:u', NS)
            if underline is not None and underline.get(tag('val')) == 'single':
                self.assertEqual(props.find('w:b', NS).get(tag('val'), '1'), '1')
                marked.append(value)
        self.assertEqual(marked, ['that', '가', '는'])
        self.assertIn('[(that)', ''.join(paragraph.xpath('.//w:t/text()', namespaces=NS)))

    def test_omitted_relative_supports_authored_subject_particle_and_relative_ending(self):
        hint = linked_hint('tools [(that) we repair]', '[우리가 고치는] 도구',
                           [(['that'], ['가', '는'])], '목적격 관계대명사 that 생략')
        hint.update(display_mode='omitted-relative', omitted_relative='that')
        display_pairs(hint, require_alignment=True)
        paragraph, rows = run_rows(hint)
        marked = [value for value, props in rows if props.find('w:u', NS) is not None
                  and props.find('w:u', NS).get(tag('val')) == 'single']
        self.assertEqual(marked, ['that', '가', '는'])
        self.assertEqual(''.join(paragraph.xpath('.//w:t/text()', namespaces=NS)),
                         '구조 힌트   tools [(that) we repair] → [우리가 고치는] 도구 (목적격 관계대명사 that 생략)')

    def test_omitted_relative_multiple_korean_ranges_still_reject_missing_outside_or_full_constituent(self):
        base = linked_hint('tools [(that) we repair]', '[우리가 고치는] 도구',
                           [(['that'], ['가', '는'])], '목적격 관계대명사 that 생략')
        base.update(display_mode='omitted-relative', omitted_relative='that')
        ko = base['display_pairs'][0]['ko']
        bad = [[], [occurrence(ko, '가'), occurrence(ko, '도구')],
               [occurrence(ko, '우리가'), occurrence(ko, '고치는')],
               [[1, ko.index(']')]]]
        for ranges in bad:
            hint = deepcopy(base)
            hint['display_pairs'][0]['emphasis_links'][0]['ko_spans'] = ranges
            with self.subTest(ranges=ranges), self.assertRaises(ValueError):
                display_pairs(hint, require_alignment=True)

    def test_bad_links_missing_sides_brackets_and_overlaps_are_rejected(self):
        malformed = [None, {}, 'of', [{}], [{'en_spans': [[10, 12]]}],
                     [{'en_spans': [], 'ko_spans': [[7, 8]]}],
                     [{'en_spans': [[10, 12]], 'ko_spans': []}],
                     [{'en_spans': [[True, 12]], 'ko_spans': [[7, 8]]}],
                     [{'en_spans': [[9, 12]], 'ko_spans': [[7, 8]]}],
                     [{'en_spans': [[10, 12]], 'ko_spans': [[8, 9]]}],
                     [{'en_spans': [[10, 12]], 'ko_spans': [[7, 99]]}],
                     [{'en_spans': [[10, 12], [10, 12]], 'ko_spans': [[7, 8]]}]]
        for links in malformed:
            hint = examples()[1]; hint['display_pairs'][0]['emphasis_links'] = links
            with self.subTest(links=links), self.assertRaises(ValueError):
                display_pairs(hint, require_alignment=True)
        hint = examples()[1]
        hint['display_pairs'][0]['emphasis_links'] *= 2
        with self.assertRaisesRegex(ValueError, 'overlap'):
            display_pairs(hint, require_alignment=True)

    def test_current_manuscript_checker_requires_alignment_before_generation(self):
        from test_book_plan import hint_fixture
        from check_learning_content import check as check_learning
        data = hint_fixture()
        pair = data['sentences'][0]['hints'][0]['display_pairs'][0]
        pair.pop('emphasis_links', None); pair.pop('emphasis_note', None)
        with self.assertRaisesRegex(ValueError, 'emphasis_links'):
            check_learning(data, scope='learning')

    def test_paragraph_geometry_and_plain_handoff_text_are_unchanged(self):
        hint = examples()[0]
        paragraph, _ = run_rows(hint)
        original = RoleBank().paragraph('structure_hint', [{'run': 1, 'text': 'geometry'}])
        self.assertEqual(E.tostring(paragraph.find('w:pPr', NS)), E.tostring(original.find('w:pPr', NS)))
        before = display_lines(hint)
        hint['display_pairs'][0].pop('emphasis_links')
        self.assertEqual(display_lines(hint), before)
        with self.assertRaisesRegex(ValueError, 'Unapproved inline underline'):
            RoleBank().paragraph('sv', [{'run': 0, 'text': 'wrong role', 'underline': True}])

    def test_saved_format_checker_rejects_spread_or_missing_emphasis_in_both_languages(self):
        plan = {'blocks': [{'id': 'hint-style', 'elements': [structure_hint_element(examples()[0])]}]}
        folder = HERE / ('master-test-' + uuid.uuid4().hex); folder.mkdir()
        saved = folder / 'hint.docx'; write(plan, saved)
        self.assertEqual(check(plan, saved)['errors'], [])
        with ZipFile(saved) as archive:
            package = [(entry, archive.read(entry.filename)) for entry in archive.infolist()]
        document = {entry.filename: raw for entry, raw in package}['word/document.xml']
        for n, (text, prop, value) in enumerate([
                ('[us', 'b', '1'), ('[us', 'u', 'single'), ('ing', 'b', '0'), ('ing', 'u', 'none'),
                ('[그녀의 범죄 현장 미니어처를 사용', 'b', '1'),
                ('[그녀의 범죄 현장 미니어처를 사용', 'u', 'single'),
                ('하여', 'b', '0'), ('하여', 'u', 'none'), ('하여', 'color', '7030A0')]):
            with self.subTest(text=text, prop=prop, value=value):
                root = E.fromstring(document)
                run = next(r for r in root.findall('.//w:sdtContent/w:p/w:r', NS)
                           if ''.join(r.xpath('./w:t/text()', namespaces=NS)) == text)
                set_property(run.find('w:rPr', NS), prop, {'val': value})
                target = folder / f'changed-{n}.docx'
                with ZipFile(target, 'w') as archive:
                    for entry, raw in package:
                        archive.writestr(entry, E.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
                                         if entry.filename == 'word/document.xml' else raw)
                result = check(plan, target)
                self.assertIn('SAVED_FORMAT_MISMATCH', {row['code'] for row in result['errors']})
                self.assertNotIn('SAVED_CONTENT_MISMATCH', {row['code'] for row in result['errors']})


if __name__ == '__main__':
    unittest.main()
