"""Compile a structurally checked common manuscript into MASTER role blocks.

This writes a layout plan, not a FINAL or a new revision of an existing DOCX.
Use master_docx.py create once, then patch only the reviewed changed block IDs.
Saved DOCX comparison and Word visual review remain separate required steps.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

from check_book import check
from check_learning_content import text as required, check as check_learning
from master_docx import RoleBank
from source_contract import (display_lesson, unit_subheadings, normalize_course,
                             display_book_name, display_source_label)
from structure_hints import display_pairs, aligned_display_segments, lexical_step, VERB_CONSTRUCTION_EMPHASIS
from compact_layout import apply_compact_adjustments

CIRCLES = '①②③④⑤'
NBSP = '\u00a0'


def p(role, value='', **kwargs):
    runs = [{'run': 0, 'text': value}] if isinstance(value, str) else value
    return {'role': role, 'runs': runs, **kwargs}


def r(index, value, **kwargs):
    return {'run': index, 'text': value, **kwargs}


def gap(role='analysis_sentence_gap'):
    return {'role': role, 'chain': False}


def gloss_text(g):
    result = g['headword'] + ' — ' + g['meaning_ko']
    if g.get('referent_ko'):
        result += ' (' + g['referent_ko'] + ')'
    return result


def syntax_practices(unit, sentences):
    """Resolve the reviewed analysis-to-workbook links without rewriting content."""
    points = {row['id']: row for row in unit['analysis']['grammar_points'] if 'id' in row}
    for point_id in unit['workbook'].get('syntax_point_ids', []):
        point = points[point_id]
        practice = point['practice']
        sentence = sentences[(unit['source_id'], point['sentence_id'])]
        glosses = {g['id']: g for g in sentence['glosses']}
        overrides = {row['gloss_id']: row for row in practice.get('support_overrides', [])}
        supports = []
        for gid in practice['support_gloss_ids']:
            gloss = dict(glosses[gid])
            if gid in overrides:
                gloss.update(headword=overrides[gid]['form'], meaning_ko=overrides[gid]['meaning_ko'])
            supports.append(gloss)
        yield point, sentence['text'][slice(*practice['span'])], [
            *supports]


def grammar_number(index):
    return chr(0x2460 + index) if index < 20 else f'{index + 1}.'


def structure_hint_element(hint):
    # Brackets delimit meaning; only bilingual grammar links receive emphasis.
    pairs = display_pairs(hint)
    runs = [r(0, '구조 힌트   ')]
    ko_only_verb = hint.get('emphasis_policy') == VERB_CONSTRUCTION_EMPHASIS
    step = lexical_step(hint)
    if step is not None:
        # The lexical starting point stays plain. Only the reviewed grammatical
        # correspondence in the actual source verb phrase is emphasized.
        runs.extend([r(1, step['form'] + '('),
                     r(0, step['meaning_ko'], format_role='structure_hint_ko'),
                     r(1, ') → ')])
    for index, pair in enumerate(pairs):
        if index:
            runs.append(r(1, ' / '))
        # Hidden English emphasis still has validated, reviewable source links.
        runs.extend(r(0, value, underline=True) if emphasized and not ko_only_verb else r(1, value)
                    for emphasized, value in aligned_display_segments(pair, 'en'))
        runs.append(r(1, '(' if step is not None else ' → '))
        runs.extend(r(1 if emphasized else 0, value, format_role='structure_hint_ko')
                    for emphasized, value in aligned_display_segments(pair, 'ko'))
        if step is not None:
            runs.append(r(1, ')'))
    if hint.get('display_mode') == 'verb-function':
        runs.append(r(1, ' (' + hint['formula_label'] + ')'))
    elif hint.get('category') not in {'function-combination', 'paired-structure'}:
        runs.append(r(1, ' (' + hint['structure_label'] + ')'))
    return p('structure_hint', runs)


def passage_runs(view):
    """Keep source characters and add labels by separate verified offsets."""
    value = view['passage']
    inserts, underlines, slot_whitespace = {}, [], []
    for mark in view['annotations']:
        kind = mark['kind']
        if kind in {'underline', 'numbered_word'}:
            start, end = mark['span']
            underlines.append((start, end))
        if kind == 'numbered_word':
            offset = mark['span'][0]
        elif kind in {'insertion_slot', 'sentence_number'}:
            offset = mark['offset']
        elif kind == 'underline':
            continue
        else:
            raise ValueError(f'Unknown question annotation: {kind}')
        symbol = CIRCLES[mark['number'] - 1]
        label = symbol + NBSP
        if kind == 'insertion_slot':
            # Normalize only whitespace touching a generated slot, after source
            # offsets were established. The authoritative passage stays intact.
            left, right = offset, offset
            while left and value[left - 1].isspace():
                left -= 1
            while right < len(value) and value[right].isspace():
                right += 1
            slot_whitespace.append((left, right))
            label = (' ' if left else '') + label
        inserts.setdefault(offset, []).append(label)
    cuts = sorted({0, len(value), *inserts, *(x for pair in underlines + slot_whitespace for x in pair)})
    runs = []
    for i, start in enumerate(cuts):
        for label in inserts.get(start, []):
            runs.append(r(0, label))
        if i + 1 == len(cuts):
            continue
        end = cuts[i + 1]
        if start < end:
            if any(a <= start and end <= b for a, b in slot_whitespace):
                continue
            if any(a <= start and end <= b for a, b in underlines):
                runs.append(r(1, value[start:end], format_role='question_underlined_reference'))
            else:
                runs.append(r(0, value[start:end]))
    if not view.get('preserve_paragraphs', False):
        # Source/annotation offsets remain authoritative. Only the printed runs
        # join paragraph boundaries, after every original offset has been used.
        for run in runs:
            run['text'] = re.sub(r'[\r\n]+[ \t]*', ' ', run['text'])
    return runs


def marked_paragraph(role, runs, **kwargs):
    """Require the intended underline spans in the actual saved Word file."""
    spans, offset = [], 0
    for run in runs:
        end = offset + len(run['text'])
        if run.get('underline') or run.get('format_role') == 'question_underlined_reference':
            spans.append([offset, end])
        offset = end
    return p(role, runs, **({'required_underlines': spans} if spans else {}), **kwargs)


def passage_elements(view, role):
    runs = passage_runs(view)
    if not view.get('preserve_paragraphs', False):
        return [marked_paragraph(role, runs)]
    paragraphs, current = [], []
    for run in runs:
        parts = re.split(r'\r\n|\r|\n', run['text'])
        for index, part in enumerate(parts):
            if index and current:
                paragraphs.append(marked_paragraph(role, current, chain=False))
                current = []
            if part:
                current.append({**run, 'text': part})
    if current:
        paragraphs.append(marked_paragraph(role, current, chain=False))
    return paragraphs


NEGATIVE_PROMPT_WORDS = ('않는', '않은', '없는')  # 2026-09-26 사용자 지시: 발문의 부정어에 밑줄


def negative_runs(text, lead=''):
    """발문 속 부정어(않는·않은·없는)만 밑줄 런으로 나눈다."""
    runs, pos = [], 0
    pattern = re.compile('|'.join(NEGATIVE_PROMPT_WORDS))
    for m in pattern.finditer(text):
        runs.append(r(0, (lead if pos == 0 else '') + text[pos:m.start()]))
        runs.append(r(0, m.group(), underline=True))
        pos = m.end()
    runs.append(r(0, (lead if pos == 0 else '') + text[pos:]))
    return [x for x in runs if x['text']]


def prompt_runs(q):
    prefix = f'{q["number"]}.  '
    value = q['question']
    if q['type'] != '함축 의미':
        return negative_runs(value, prefix)
    target = q['target']
    # An explicit span disambiguates repeated target text in a prompt.
    marks = q.get('prompt_underlines')
    if not isinstance(marks, list) or len(marks) != 1:
        raise ValueError('Meaning prompt requires one prompt_underlines span')
    span = marks[0]
    if (not isinstance(span, list) or len(span) != 2 or any(type(x) is not int for x in span)
            or not 0 <= span[0] < span[1] <= len(value) or value[slice(*span)] != target):
        raise ValueError('Meaning prompt target span differs from the passage expression')
    start, end = span
    return negative_runs(value[:start], prefix) + [r(0, value[start:end], underline=True)] + negative_runs(value[end:])


def question_elements(q, view, source_label, scope='mock', *, include_passage=True, spaced=False):
    prefix = 'workbook' if scope == 'workbook' else 'mock'
    # A16: source ranges remain in manuscript/views, not student-facing paragraphs.
    prompt_role = 'mock_question_prompt_spaced' if prefix == 'mock' and spaced else prefix + '_question_prompt'
    els = [marked_paragraph(prompt_role, prompt_runs(q), anchor='question/' + q['id'])]
    if include_passage and q['type'] in {'삽입', '순서'}:
        els += [p('given_label', '〈주어진 문장〉' if q['type'] == '삽입' else '〈주어진 글〉'),
                p('given_box', re.sub(r'[\r\n]+[ \t]*', ' ', view['given']))]
    if include_passage and q['type'] == '순서':
        els += [p(prefix + '_question_passage', f'({k}) ' + re.sub(r'[\r\n]+[ \t]*', ' ', view['blocks'][k])) for k in 'ABC']
    elif include_passage:
        els += passage_elements(view, prefix + '_question_passage')
    if q['type'] == '요약':
        els.append(p('mock_summary_spaced', '[요약문] ' + q['summary']))
    if q['choice_mode'] != 'in_passage':
        for choice in sorted(q['choices'], key=lambda x: x['number']):
            els.append(p(prefix + '_question_choice', [r(0, CIRCLES[choice['number'] - 1] + '  '), r(1, choice['text'])]))
    els[-1]['chain'] = False
    return els


def explanation_elements(q, e):
    els = [p('question_answer', [r(0, f'{q["number"]}.  '), r(1, CIRCLES[e['answer'] - 1])]),
           p('choice_translation_heading', '정답 근거'),
           p('question_evidence', e['evidence']),
           p('question_explanation', e['explanation'], chain=False)]
    if q['choice_mode'] == 'text':
        korean = {c['number']: c['text'] for c in e['choices_ko']}
        els.append(p('choice_translation_heading', '선지 해석'))
        choices = sorted(e['choices'], key=lambda x: x['number'])
        for i, c in enumerate(choices):
            role = 'correct_choice_translation' if c['number'] == e['answer'] else 'choice_translation'
            els.append(p(role, [r(0, CIRCLES[c['number'] - 1] + '   '),
                                r(1, c['text'] + '   '), r(2, '(' + korean[c['number']] + ')')],
                         chain=i < len(choices) - 1))
    els.append(p('wrong_reasons_heading', '오답 정리'))
    wrongs = sorted(e['wrong_reasons'], key=lambda x: x['number'])
    for i, wrong in enumerate(wrongs):
        els.append(p('wrong_reason', [r(0, CIRCLES[wrong['number'] - 1] + '   '), r(1, wrong['text'])], chain=i < len(wrongs)-1))
    return els


def compile_plan(data,scope='full'):
    if data.get('rule_revision') != 'R2026-09-23':
        raise ValueError('Current generation requires rule_revision R2026-09-23 and a renewed reading review')
    if scope not in {'full','learning'}:
        raise ValueError('Unknown layout scope')
    if scope=='learning':
        learning_check=check_learning(data, scope='learning')
        validation={'status':learning_check['status'],'learning':learning_check,'question_views':{}}
    else:
        validation = check(data)
    if validation['status'] != 'STRUCTURE_PASS':
        raise ValueError('Common manuscript did not pass structural checks: ' + validation['status'])
    bank = RoleBank()
    meta = data['metadata']
    cover = data.get('cover', {})
    for field in ['lesson_label', 'lesson_number', 'topic_first', 'topic_ko']:
        required(cover.get(field), f'cover/{field}')
    topic_en = ' '.join(x.strip() for x in [cover['topic_first'], cover.get('topic_second', '')] if x.strip())
    if any(c in topic_en for c in '\r\n'):
        raise ValueError('Cover English title must be a single line of source text')
    lesson = display_lesson(meta, cover)
    lesson_note = cover.get('lesson_note', '')
    if not isinstance(lesson_note, str) or any(c in lesson_note for c in '\r\n'):
        raise ValueError('cover/lesson_note must be a single-line string')
    lesson_note = lesson_note.strip()
    cover_lesson = lesson + (f' ({lesson_note})' if lesson_note else '')
    labels_fixed = bank.contract['fixed_labels']
    def sentence_ref(positions):
        if not positions or positions != list(range(positions[0], positions[-1] + 1)):
            raise ValueError('Sentence reference must be a nonempty contiguous source range')
        value = str(positions[0]) if len(positions) == 1 else f'{positions[0]}~{positions[-1]}'
        return labels_fixed['sentence_reference'].format(range=value)
    sources = {s['id']: s for s in data['sources']}
    for s in sources.values():
        required(s.get('label'), 'Human-readable source label')
    sentences = {(s['source_id'], s['id']): s for s in data['sentences']}
    numbers = {(source['id'], s['id']): n for source in sources.values()
               for n, s in enumerate(source['sentences'], 1)}
    qlist = data.get('assessment',{}).get('questions',[]) if scope=='full' else []
    questions = {q['id']: q for q in qlist}
    explanations = {e['id']: e for e in data.get('assessment',{}).get('explanations',[])}
    views = validation['question_views']
    quick = data.get('assessment',{}).get('quick_key',[])
    set_ids = list(dict.fromkeys(x['set_id'] for x in data.get('assessment',{}).get('plan',[]))) if scope=='full' else []
    if scope=='full' and (not set_ids or set_ids[0] != 'workbook'):
        raise ValueError('Workbook must precede the mini-exam rounds in the approved plan')
    labels = data.get('set_labels', {})
    for set_id in set_ids:
        if set_id != 'workbook':
            required(labels.get(set_id), f'Human-readable set label {set_id}')
    set_labels = {'workbook': '워크북', **labels}
    blocks = []
    def block(identity, elements):
        if not elements:
            raise ValueError('Empty output block')
        blocks.append({'id': identity, 'elements': elements})

    counts = f'{len(data["units"])}개 문단   /   본문 {len(sentences)}문장   /   전체 {len(qlist)}문항'
    detail_parts = []
    if set_ids:
        detail_parts.append(f'워크북 실전문제 {sum(q["set_id"] == "workbook" for q in qlist)}문항')
        mock_counts = [sum(q['set_id'] == sid for q in qlist) for sid in set_ids[1:]]
        if mock_counts and len(set(mock_counts)) == 1:
            detail_parts.append(bank.contract['presentation_policy']['equal_mock_counts'].format(
                count=mock_counts[0], rounds=len(mock_counts)))
        else:
            detail_parts.extend(f'{set_labels[sid]} {n}문항' for sid,n in zip(set_ids[1:],mock_counts))
    detail = '  +  '.join(detail_parts)
    if scope=='learning':
        counts=f'{len(data["units"])}개 문단   /   본문 {len(sentences)}문장'
        detail='혼공해석지 + 지문분석지'
    steps = list(bank.contract['cover_steps'] if scope=='full' else bank.contract['cover_steps'][:2])
    if scope == 'full' and len(set_ids[1:]) != 3:
        steps[-1] = steps[-1].replace('세 회로', f'{len(set_ids[1:])}회로')
    course_display = '영어2' if normalize_course(meta['course']) == '영어2' else meta['course']
    block('cover', [{'role': 'cover_logo'}, p('cover_series_title', '혼공교재 독해편'),
        p('cover_course_title', course_display),
        p('cover_publisher_large', meta['publisher_author'] + '  ·  ' + cover_lesson),
        {'kind': 'table', 'role': 'cover_topic_box', 'entries': [topic_en, cover['topic_ko']]},
        p('cover_counts', counts), p('cover_assessment_counts', detail),
        p('cover_steps_heading', '이 한 권으로 이어지는 학습'),
        *[p('cover_step', step, chain=i < len(steps)-1) for i, step in enumerate(steps)]])

    for unit_number, unit in enumerate(data['units'], 1):
        uid, src = unit['id'], unit['source_id']
        sid_list = unit['sentence_ids']
        a = unit['analysis']
        un = f'문단 {unit_number}'
        source_range = f'{display_source_label(sources[src])} · 문장 {numbers[(src,sid_list[0])]}~{numbers[(src,sid_list[-1])]}'
        reading = [p('interpretation_header', f'{display_book_name(meta)} · {lesson} 혼공해석지', page_break_before=True),
                   p('unit_source_range', un + ' · ' + source_range),
                   p('unit_topic_english', [r(0, a['title_or_topic_en']),
                       r(0, ' (' + a['title_or_topic_ko'] + ')', format_role='unit_topic_korean')],
                       heading_kind=a['heading_kind'])]
        # Retain any legacy unit.hook in the manuscript, but never print it.
        if unit_number == 1:
            reading.append({'role': 'interpretation_guide_gap', 'chain': True})
            for role in ['guide_reading', 'guide_symbols', 'guide_heading', 'guide_item_one', 'guide_item_two', 'guide_item_three']:
                locator = bank.contract['roles'][role]['locator']['zero_based_index']
                reading.append(p(role, bank.contract['guide_runs'][str(locator)]))
        reading.append(gap('interpretation_rule'))
        analysis = [p('analysis_header', f'{lesson} · {un} | 지문 분석', page_break_before=True)]
        subheadings_at = {}
        for heading in unit_subheadings(data, unit):
            if heading['before_sentence_id'] in sid_list:
                subheadings_at.setdefault(heading['before_sentence_id'], []).append(heading)
        for sid in sid_list:
            for heading in subheadings_at.get(sid, []):
                reading.append(p('source_subheading', heading['text'], source_heading_id=heading['id']))
            sentence = sentences[(src, sid)]
            sn = numbers[(src, sid)]
            english = [sentence['text'][c['start']:c['end']] for c in sentence['chunks']]
            english_role = 'interpretation_key_english' if sentence['key'] else 'interpretation_english'
            en_runs = [r(0, f'{sn}.  ')]
            for i, chunk in enumerate(english):
                if i:
                    en_runs.append(r(2, '  /  '))
                en_runs.append(r(1, chunk))
            if sentence['key']:
                # The contract binds the complete visible marker with Word-compatible
                # zero-width no-break characters; keep the MASTER run unchanged.
                en_runs.append(r(8, labels_fixed['key_marker']))
            reading.append(p(english_role, en_runs))
            sv_line = validation['learning']['sv_lines'][f'{src}/{sid}']
            if sv_line:
                reading.append(p('sv', [r(0, '주어·동사   '), r(1, sv_line)]))
            g_runs = [r(0, '※ ')]
            for i, g in enumerate(sentence['glosses']):
                if i:
                    g_runs.append(r(0, ' / '))
                if g['star']:
                    g_runs.append(r(1, '★'))
                g_runs.append(r(0, (NBSP if g['star'] else '') + gloss_text(g)))
            if sentence['glosses']:
                reading.append(p('gloss', g_runs))
            for h in sentence.get('hints', []):
                reading.append(structure_hint_element(h))
            reading += [p('interpretation_answer_label', '나의 해석'),
                        {'role': 'interpretation_answer_space_one'},
                        {'role': 'interpretation_answer_space_two', 'chain': sid == sid_list[-1]}]
            en_runs, ko_runs = [r(0, f'{sn}.  ')], []
            for i, (eng, chunk) in enumerate(zip(english, sentence['chunks']), 1):
                if i > 1:
                    en_runs.append(r(3, ' / '))
                    ko_runs.append(r(2, ' / '))
                en_runs += [r(1, str(i)), r(2, eng)]
                ko_runs += [r(0, str(i)), r(1, chunk['ko'])]
            if sentence['key']:
                # Keep the final English word with the end marker. Preserve all
                # three visible spaces and the marker's existing internal binders.
                en_runs.append(r(bank.contract['semantic_run_indices']['analysis_key_marker'],
                                 labels_fixed['key_marker'].replace(' ', NBSP)))
            analysis += [p('analysis_key_english_chunks' if sentence['key'] else 'analysis_english_chunks', en_runs),
                         p('analysis_korean_chunks', ko_runs),
                         p('analysis_natural_translation', [r(0, labels_fixed['natural_translation']), r(1, sentence['natural_ko'])], chain=False), gap()]
        review = bank.contract['additional_paragraph_roles']['interpretation_review_line']
        reading.append(p('interpretation_review_line', review['runs'], chain=False))
        block(uid + '/reading', reading)
        analysis += [p('analysis_header', f'{lesson} · {un} | 지문 분석', page_break_before=True),
                     p('analysis_section_heading', labels_fixed['analysis_section_heading']), p('analysis_prose', a['intent_ko'], chain=False), gap(),
                     p('analysis_flow_heading', labels_fixed['analysis_flow_heading'])]
        for row in a['flow']:
            positions = [numbers[(src, x)] for x in row['sentence_ids']]
            analysis.append(p('analysis_flow_item', [r(0, '(' + row.get('label', '흐름') + ')  '),
                              r(1, sentence_ref(positions)), r(2, ' — ' + row['text_ko'])], chain=False))
        analysis += [gap(), p('analysis_easy_explanation_heading', labels_fixed['analysis_easy_explanation_heading'])]
        for row in a['easy_explanations']:
            original = sentences[(src, row['sentence_id'])]['text']
            analysis += [p('analysis_easy_sentence', [r(0, sentence_ref([numbers[(src,row['sentence_id'])]]) + '  '), r(1, original)]),
                         p('analysis_easy_explanation', [r(0, '↳  '), r(1, ' '.join(row['explanatory_sentences']))], chain=False)]
        if a['grammar_points']:
            analysis += [gap(), p('analysis_grammar_heading', labels_fixed['analysis_grammar_heading'])]
            for i, row in enumerate(a['grammar_points']):
                original = sentences[(src, row['sentence_id'])]['text']
                analysis.append(p('analysis_grammar_item', [r(0, grammar_number(i) + ' ' + row['title']),
                    r(1, ' ' + sentence_ref([numbers[(src,row['sentence_id'])]])), r(2, ':  '),
                    r(3, original[slice(*row['span'])]), r(4, ' — ' + row['explanation'])], chain=False))
        if a['relations']:
            analysis += [gap(), p('analysis_relations_heading', labels_fixed['analysis_relations_heading'])]
            for row in a['relations']:
                h, s, ant = row['head'], row['synonym'], row['antonym']
                analysis.append(p('analysis_relations_item', [r(0,h['text']),r(1,' ('+h['meaning_ko']+')'),r(2,'   '+labels_fixed['synonym']+'  '),
                    r(3,s['text']),r(4,' ('+s['meaning_ko']+')'),r(5,'   '+labels_fixed['antonym']+'  '),r(6,ant['text']),r(7,' ('+ant['meaning_ko']+')')],chain=False))
        block(uid + '/analysis', analysis)
        if scope=='learning':
            continue
        terms = {term['id']: term for row in a['relations'] for term in row.values()}
        wb = unit['workbook']
        workbook = [p('workbook_header', f'{lesson} · {un} 워크북', page_break_before=True),
                    p('workbook_subtitle', a['title_or_topic_en']+' ('+a['title_or_topic_ko']+')',heading_kind=a['heading_kind'])]
        for role, heading, entries in [
            ('workbook_word_table', '1. 오늘의 낱말 — 우리말 뜻을 쓰세요', [x['text'] for x in unit['today_words']]),
            ('workbook_relations_table', '2. 유의어·반의어 뜻 쓰기 — 우리말 뜻을 쓰세요', [terms[x]['text'] for x in wb['relation_order']])]:
            if entries:
                workbook += [p('workbook_words_heading' if role == 'workbook_word_table' else 'workbook_relations_heading', heading),
                             {'kind':'table','role':role,'entries':entries}, gap('workbook_table_gap')]
        qid = wb['question_id']
        view = views[qid]
        workbook.append(p('workbook_question_heading','3. 실전문제'))
        workbook += question_elements(questions[qid],view,source_label(sources,view,numbers),'workbook')
        workbook.append(p('workbook_continuation', un+' 워크북 (계속)', page_break_before=True, chain=True))
        syntax_enabled = data['metadata'].get('syntax_training_version') == 1
        if syntax_enabled:
            workbook.append(p('workbook_key_sentences_heading', '4. 구문 결합해서 해석하기', anchor='syntax/heading'))
            for i, (point, expression, supports) in enumerate(syntax_practices(unit, sentences), 1):
                formula = point['practice']['formula_support']
                support_runs = [r(0, '도움말  '), r(1, formula['en']), r(2, ' — '+formula['ko'])]
                for gloss in supports:
                    support_runs += [r(2, ' / '), r(1, gloss['headword']), r(2, ' — '+gloss['meaning_ko'])]
                workbook += [p('workbook_key_sentence', [r(0, f'{i}.   '), r(1, expression+' → ______________________________')], chain=True, anchor='syntax/'+point['id']),
                             p('choice_translation', support_runs, chain=False)]
            workbook.append(gap('workbook_question_gap'))
        key_number = 5 if syntax_enabled else 4
        workbook.append(p('workbook_key_sentences_heading',f'{key_number}. 핵심 문장 {len(wb["key_sentence_ids"])}개 다시 해석하기',anchor='key/heading'))
        for i,sid in enumerate(wb['key_sentence_ids'],1):
            workbook += [p('workbook_key_sentence',[r(0,f'{i}.   '),r(1,sentences[(src,sid)]['text'])],anchor='key/'+sid),
                         p('workbook_key_answer_label','나의 해석  '),
                         # 2026-09-26 사용자 결정: 두 줄 해석을 쓸 수 있도록 답안선 2줄
                         # 같은 테두리 문단이 이어지면 한 줄로 합쳐지므로 두 답안선 사이에 테두리 없는 간격 문단을 둔다.
                         {'role':'workbook_key_answer_space','chain':True},
                         {'role':'workbook_question_gap','chain':True},
                         {'role':'workbook_key_answer_space','chain':i<len(wb['key_sentence_ids'])}]
        block(uid + '/workbook',workbook)
    if scope=='learning':
        answer_blocks = {unit['id'] + '/answers' for unit in data['units']}
        learning_layout = {**data, 'layout_adjustments': [row for row in data.get('layout_adjustments', [])
                           if not (row.get('kind') == 'compact_block' and row.get('block_id') in answer_blocks)]}
        apply_compact_adjustments(learning_layout, blocks, bank.contract, content_hash(data))
        for b in blocks:
            bank.block(b)
        return {'schema_version':1,'purpose':'LEARNING_STAGE_LAYOUT_PLAN_NOT_FINAL',
                'blocks':blocks,'semantic_review':'NOT_PERFORMED','visual_review':'NOT_PERFORMED'}
    for set_id in set_ids[1:]:
        group = sorted([q for q in qlist if q['set_id']==set_id],key=lambda q:q['number'])
        els=[p('mock_round_header',lesson+' '+set_labels[set_id],page_break_before=True),
             p('mock_subtitle',topic_en+' · '+str(len(group))+'문항')]
        printed_groups = set()
        group_records = {g['id']: g for g in data['assessment'].get('passage_groups', [])}
        for index, q in enumerate(group):
            gid = q.get('passage_group_id')
            if gid and gid not in printed_groups:
                shared = group_records[gid]
                child_numbers = [questions[qid]['number'] for qid in shared['question_ids']]
                # 2026-09-26 사용자 지시: 매회 공유 장문(마지막 두 문항) 세트는 항상 새 쪽에서 시작한다.
                els.append(p('mock_question_prompt',
                             f'[{child_numbers[0]}~{child_numbers[-1]}] 다음 글을 읽고 물음에 답하시오.',
                             page_break_before=True, chain=True, anchor='passage_group/' + gid))
                shared_view = validation['passage_group_views'][gid]
                els += passage_elements({**shared_view, 'preserve_paragraphs': True}, 'mock_question_passage')
                printed_groups.add(gid)
            els += question_elements(q,views[q['id']],source_label(sources,views[q['id']],numbers),
                                     include_passage=not gid, spaced=index > 0)
        block(set_id,els)
    answers=[p('answers_header',lesson+' 정답과 해설',page_break_before=True),p('quick_answers_heading','객관식 빠른 정답')]
    for set_id in set_ids:
        answers.append(p('quick_answers_set_heading',set_labels[set_id]))
        rows=sorted([q for q in quick if q['set_id']==set_id],key=lambda q:q['number'])
        for offset in range(0,len(rows),8):
            answers.append(p('quick_answers_row','   '.join(f'{q["number"]}. {CIRCLES[q["answer"]-1]}' for q in rows[offset:offset+8]),chain=False))
    block('answers/quick',answers)
    for un,unit in enumerate(data['units'],1):
        wb=unit['workbook'];src=unit['source_id'];qid=wb['question_id']
        els=[p('workbook_answer_unit_heading',f'문단 {un} 워크북 정답',page_break_before=True)]
        terms={term['id']:term for row in unit['analysis']['relations'] for term in row.values()}
        for title,rows in [('1. 오늘의 낱말',unit['today_words']),('2. 유의어·반의어 뜻 쓰기',[terms[x] for x in wb['relation_order']])]:
            if rows:
                els.append(p('workbook_answer_activity_heading',title))
                els.append({'kind': 'table', 'role': 'workbook_answer_grid',
                            'entries': [{'runs': [r(0, f'{i}.'), r(1, ' '+row['meaning_ko'])]} for i,row in enumerate(rows,1)]})
        els.append(p('workbook_answer_activity_heading','3. 실전문제'))
        els += explanation_elements(questions[qid],explanations[qid])
        syntax_enabled = data['metadata'].get('syntax_training_version') == 1
        if syntax_enabled:
            els.append(p('workbook_key_answers_heading','4. 구문 결합해서 해석하기'))
            practices = list(syntax_practices(unit, sentences))
            els += [p('workbook_key_answer', f'{i}. '+point['practice']['answer_ko'], chain=i<len(practices))
                    for i,(point,expression,supports) in enumerate(practices,1)]
        key_number = 5 if syntax_enabled else 4
        els.append(p('workbook_key_answers_heading',f'{key_number}. 핵심 문장 해석'))
        keys=wb['key_sentence_ids']
        els += [p('workbook_key_answer',f'{i}. '+sentences[(src,sid)]['natural_ko'],chain=i<len(keys)) for i,sid in enumerate(keys,1)]
        block(unit['id']+'/answers',els)
    for set_id in set_ids[1:]:
        els=[p('mock_answers_header',set_labels[set_id]+' 정답과 해설',page_break_before=True)]
        for q in sorted([q for q in qlist if q['set_id']==set_id],key=lambda q:q['number']):
            els += explanation_elements(q,explanations[q['id']])
        block('answers/'+set_id,els)
    apply_compact_adjustments(data, blocks, bank.contract, content_hash(data))
    apply_continuations(data, blocks)
    # Fail before writing a plan if any template role/run combination is invalid.
    for b in blocks:
        bank.block(b)
    return {'schema_version':1,'purpose':'COMMON_TEXTBOOK_LAYOUT_PLAN_NOT_FINAL',
            'blocks':blocks,'semantic_review':'NOT_PERFORMED','visual_review':'NOT_PERFORMED'}


def content_hash(data):
    value={k:v for k,v in data.items() if k!='layout_adjustments'}
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()


def apply_continuations(data, blocks):
    """Word-observed continuation anchors; no page estimates or silent shrinking."""
    lookup={b['id']:b for b in blocks}
    unit_names={u['id']:f'문단 {i}' for i,u in enumerate(data['units'],1)}
    seen=set()
    for adjustment in data.get('layout_adjustments',[]):
        if adjustment.get('kind') == 'compact_block':
            continue  # Validated and applied by the bounded compact-role stage.
        if adjustment.get('content_sha256')!=content_hash(data):
            raise ValueError('Continuation decision belongs to a different manuscript revision')
        if adjustment.get('renderer')!='Microsoft Word' or type(adjustment.get('observed_page')) is not int:
            raise ValueError('Continuation needs an actual Word page observation')
        required(adjustment.get('reason'),'Continuation observation')
        bid=adjustment.get('block_id');anchor=adjustment.get('before_anchor')
        kind = adjustment.get('kind', 'workbook_continuation')
        if bid not in lookup or kind not in {'workbook_continuation', 'question_page_break'}:
            raise ValueError('Unknown continuation block or adjustment kind')
        uid=bid[:-len('/workbook')]
        if (kind == 'workbook_continuation' and (not bid.endswith('/workbook') or uid not in unit_names)) or (bid,anchor) in seen:
            raise ValueError('Invalid or repeated continuation placement')
        seen.add((bid,anchor))
        elements=lookup[bid]['elements']
        positions=[i for i,e in enumerate(elements) if e.get('anchor')==anchor]
        if len(positions)!=1 or positions[0]==0:
            raise ValueError('Continuation requires one existing noninitial content anchor')
        if kind == 'question_page_break':
            target = elements[positions[0]]
            if not anchor.startswith(('question/', 'passage_group/')):
                raise ValueError('Question page break requires a question or shared-passage anchor')
            if anchor.startswith('question/'):
                qid = anchor[len('question/'):]
                question = next((q for q in data.get('assessment', {}).get('questions', []) if q['id'] == qid), {})
                if question.get('passage_group_id'):
                    raise ValueError('Move the shared-passage group, not a child question alone')
            target['page_break_before'] = True
            if target['role'] == 'mock_question_prompt_spaced':
                target['role'] = 'mock_question_prompt'
        else:
            # Keep the whole key-sentence activity together after syntax practice,
            # superseding earlier observations within that activity. Validate the
            # recorded anchor first, then avoid duplicate/mid-activity headers.
            if anchor.startswith('key/'):
                continue
            elements.insert(positions[0],p('workbook_continuation',unit_names[uid]+' 워크북 (계속)',chain=True))


def source_label(sources,view,numbers):
    src=view['source_id'];ids=view['source_sentence_ids']
    return f'[{display_source_label(sources[src])} · 원문 문장 {numbers[(src,ids[0])]}~{numbers[(src,ids[-1])]}]'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path);parser.add_argument('output',type=Path)
    parser.add_argument('--scope',choices=['full','learning'],default='full')
    args=parser.parse_args()
    if args.input.resolve()==args.output.resolve():
        raise ValueError('Plan must not overwrite manuscript')
    raw=args.input.read_bytes()
    plan=compile_plan(json.loads(raw.decode('utf-8-sig')),args.scope)
    plan['input_sha256']=hashlib.sha256(raw).hexdigest()
    args.output.write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'status':'PLAN_COMPILED','blocks':len(plan['blocks']),'output':str(args.output)}))


if __name__=='__main__':
    main()
