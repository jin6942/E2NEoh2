"""Join common learning content with independently authored question/key records.

Required: learning manuscript fields plus assessment (check_answer_links contract)
and question_sources [{id, ...question_source.build_view input}]. This is a full
book STRUCTURE check, not a claim of semantic, saved-DOCX, or independent review.
"""
import argparse
import hashlib
import json
from pathlib import Path

from check_learning_content import check as check_learning, records, text
from check_answer_links import check as check_answers
from question_source import build_view, span
from source_contract import course_policy, normalize_course


def reference_grade(course, scope):
    known_grade = course_policy(course)['reference_grade']
    grade = known_grade if known_grade is not None else scope.get('reference_grade')
    if type(grade) is not int or grade not in (1, 2):
        raise ValueError('An unmapped course requires an explicitly verified reference_grade of 1 or 2')
    if scope.get('reference_grade') is not None and scope['reference_grade'] != grade:
        raise ValueError('Explicit reference_grade conflicts with the verified textbook course')
    return grade


def check_learned_relation_uses(question, unit):
    """Check actual links; whether the word meaning decides a choice needs review."""
    terms = {term['id']: term for relation in unit['analysis']['relations']
             for term in [relation['head'], relation['synonym'], relation['antonym']]}
    uses = question.get('learned_relation_uses')
    # The full learning check already validates the reported zero-set source
    # shortage. Such a unit receives an ordinary practical question and does
    # not need an invented synonym/antonym or a forced today-word substitute.
    if not terms and (uses is None or uses == []):
        return
    if not isinstance(uses, list) or not uses:
        raise ValueError('Workbook question requires actual learned_relation_uses from its own unit')
    choices = {row['number']: row['text'] for row in question['choices']}
    seen = set()
    for use in uses:
        if not isinstance(use, dict) or use.get('term_id') not in terms:
            raise ValueError('Workbook learned relation must come from the assigned common unit')
        number = use.get('choice_number')
        if type(number) is not int or number not in choices:
            raise ValueError('Learned relation use points to an absent choice')
        a, b = span(use.get('choice_span'), choices[number])
        if choices[number][a:b] != text(use.get('surface'), 'Actual learned-word choice surface'):
            raise ValueError('Learned relation surface differs from the actual choice span')
        text(use.get('reason_ko'), 'Actual word-meaning judgment rationale')
        identity = (use['term_id'], number, a, b)
        if identity in seen:
            raise ValueError('Duplicate learned relation use')
        seen.add(identity)


def check(data):
    learning = check_learning(data, scope='full')
    if learning['status'] != 'STRUCTURE_PASS':
        return {'status': learning['status'], 'learning': learning}
    assessment = data.get('assessment')
    if not isinstance(assessment, dict):
        raise ValueError('A complete book needs assessment records')
    answers = check_answers(assessment)
    if answers['status'] != 'PASS':
        return {'status': 'FAIL', 'learning': learning, 'assessment': answers}
    scope = assessment['scope']
    if scope.get('kind') == 'full':
        if normalize_course(scope.get('course')) != normalize_course(data['metadata']['course']):
            raise ValueError('Assessment course differs from verified book metadata')
        if scope.get('unit_ids') != [u['id'] for u in data['units']]:
            raise ValueError('Assessment unit list differs from the common learning units')
    elif scope.get('kind') == 'partial':
        raise ValueError('Partial assessment cannot pass the complete-book checker')
    grade = reference_grade(data['metadata']['course'], scope)
    sources = records(data['sources'], 'sources')
    questions = records(assessment['questions'], 'questions')
    planned = records(assessment['plan'], 'plan')
    source_requests = records(data.get('question_sources'), 'question_sources')
    if set(questions) != set(source_requests):
        raise ValueError('Every question requires its own source-reconstruction input')
    workbook_ids = []
    for unit in data['units']:
        qid = unit['workbook']['question_id']
        if qid not in planned or planned[qid].get('set_id') != 'workbook' or planned[qid].get('unit_id') != unit['id']:
            raise ValueError('Workbook question ID is not assigned to that same learning unit')
        workbook_ids.append(qid)
    if set(workbook_ids) != {qid for qid, p in planned.items() if p['set_id'] == 'workbook'}:
        raise ValueError('Extra or missing workbook questions')
    groups = records(assessment.get('passage_groups', []), 'passage_groups')
    views = {}
    for qid, q in questions.items():
        request = source_requests[qid]
        if request.get('type') != q['type'] or request.get('source_id') not in sources:
            raise ValueError(f'{qid}: question type or authoritative source is inconsistent')
        view = build_view(sources[request['source_id']], request, expected_grade=grade,
                          benchmark_type='long41_42' if q.get('passage_group_id') else q['type'])
        for field in ['passage', 'given', 'blocks', 'target']:
            # Compare fields actually supplied by the source reconstruction
            # helper; summaries and choices are authored content, not source.
            if field in view and q.get(field) != view[field]:
                raise ValueError(f'{qid}: printed {field} differs from source reconstruction')
        if 'answer' in view and q['answer'] != view['answer']:
            raise ValueError(f'{qid}: answer differs from the source transformation')
        if 'correct_order' in view and q['permutations'][q['answer'] - 1] != view['correct_order']:
            raise ValueError(f'{qid}: ordering answer does not reconstruct the source')
        if q['set_id'] == 'workbook':
            unit = next(u for u in data['units'] if u['id'] == planned[qid]['unit_id'])
            # The source belongs to this verified lesson, but need not overlap
            # the workbook's reading unit. Keep its studied-word goal instead.
            check_learned_relation_uses(q, unit)
        views[qid] = view
    group_views = {}
    for gid, group in groups.items():
        owner = views[group['passage_question_id']]
        for qid in group['question_ids']:
            member = views[qid]
            if (member['source_id'], member['source_span'], member['original']) != \
                    (owner['source_id'], owner['source_span'], owner['original']):
                raise ValueError('Shared long-reading questions must reconstruct the exact same source extent')
        group_views[gid] = dict(owner, question_ids=list(group['question_ids']),
                               group_id=gid, preserve_paragraphs=True)
    return {'status': 'STRUCTURE_PASS', 'learning': learning, 'assessment': answers,
            'question_views': views, 'checked_question_count': len(questions),
            'passage_group_views': group_views,
            'independent_length_review_required': [qid for qid, view in views.items()
                if view['length_comparison']['independent_review_required']],
            'semantic_review': 'NOT_PERFORMED', 'independent_reviews': 'NOT_PERFORMED',
            'docx_presence': 'NOT_CHECKED_BY_THIS_TOOL', 'visual_review': 'NOT_PERFORMED'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('input', type=Path)
    p.add_argument('report', type=Path)
    a = p.parse_args()
    if a.input.resolve() == a.report.resolve():
        raise ValueError('Report cannot overwrite manuscript')
    raw = a.input.read_bytes()
    try:
        result = check(json.loads(raw.decode('utf-8-sig')))
    except (ValueError, TypeError, KeyError, AttributeError) as exc:
        result = {'status': 'FAIL', 'error': str(exc)}
    result['input_sha256'] = hashlib.sha256(raw).hexdigest()
    a.report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k not in {'learning', 'assessment', 'question_views', 'passage_group_views'}}, ensure_ascii=False))
    return 0 if result['status'] == 'STRUCTURE_PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
