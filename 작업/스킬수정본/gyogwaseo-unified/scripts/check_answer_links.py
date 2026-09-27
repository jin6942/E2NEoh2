"""Check question/quick-key/explanation correspondence, never semantic correctness.

Input lists must be independently read from the manuscript or saved artifact.
Passing projections made from one JSON does not prove that a DOCX contains them.
Each record has id, set_id, number. Questions have type, question, answer,
choice_mode (text, in_passage, order), choices. Choices are [{number,text}].
Explanations additionally have choices_ko [{number,text}], evidence, explanation,
wrong_reasons [{number,text}]. In-passage choices are internal ①..⑤ mappings:
they are checked but not printed again as a separate student choice list.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
from source_contract import course_policy

TYPES = {'제목', '주제', '요지', '주장', '목적', '심경·분위기', '내용',
         '함축 의미', '빈칸', '요약', '무관한 문장', '삽입', '순서', '어휘'}
SYMBOL_TYPES = {'무관한 문장', '삽입', '어휘'}
ORDER_PERMUTATIONS = [['A', 'C', 'B'], ['B', 'A', 'C'], ['B', 'C', 'A'],
                      ['C', 'A', 'B'], ['C', 'B', 'A']]
CONTENT_PROMPTS = {'다음 글의 내용과 일치하는 것은?', '다음 글의 내용과 일치하지 않는 것은?'}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def check(data):
    errors = []

    def issue(code, location, message):
        errors.append({'code': code, 'location': location, 'message': message})

    def index_records(value, location):
        result = {}
        if not isinstance(value, list):
            issue('LIST_REQUIRED', location, 'Expected a record list')
            return result
        for i, row in enumerate(value):
            loc = f'{location}[{i}]'
            if not isinstance(row, dict) or not nonempty(row.get('id')):
                issue('ID_REQUIRED', loc, 'Missing record ID')
                continue
            key = row['id']
            if key in result:
                issue('DUPLICATE_ID', loc, key)
                continue
            result[key] = row
        return result

    def choice_map(value, expected, location):
        result = {}
        if not isinstance(value, list):
            issue('CHOICES_REQUIRED', location, 'Expected numbered entries')
            return result
        for row in value:
            if not isinstance(row, dict):
                issue('CHOICE_SHAPE', location, 'Entry must be an object')
                continue
            n = row.get('number')
            if type(n) is not int or n not in expected:
                issue('CHOICE_NUMBER', location, str(n))
                continue
            if n in result:
                issue('CHOICE_DUPLICATE', location, str(n))
            if not nonempty(row.get('text')):
                issue('CHOICE_TEXT', location, str(n))
            result[n] = row.get('text')
        if set(result) != set(expected) or len(value) != len(expected):
            issue('CHOICE_COVERAGE', location, f'Expected {sorted(expected)} exactly once')
        return result

    plan = index_records(data.get('plan'), 'plan')
    questions = index_records(data.get('questions'), 'questions')
    quick = index_records(data.get('quick_key'), 'quick_key')
    explanations = index_records(data.get('explanations'), 'explanations')
    if not plan:
        issue('EMPTY_PLAN', 'plan', 'An empty question task cannot pass')
    if not questions:
        issue('EMPTY_QUESTIONS', 'questions', 'No questions were checked')
    for name, records in [('questions', questions), ('quick_key', quick), ('explanations', explanations)]:
        if set(records) != set(plan):
            issue('ID_COVERAGE', name,
                  f'missing={sorted(set(plan) - set(records))}; extra={sorted(set(records) - set(plan))}')

    # Standard complete production checks; partial/custom requests need an explicit
    # approved plan and rationale, never an inferred relaxed default.
    scope = data.get('scope', {})
    if not isinstance(scope, dict):
        scope = {}
    if scope.get('kind') == 'full':
        course = scope.get('course')
        unit_ids = scope.get('unit_ids')
        if not isinstance(unit_ids, list) or not unit_ids or any(not nonempty(x) for x in unit_ids):
            issue('UNIT_PLAN', 'scope', 'Confirmed common unit IDs are required')
            unit_ids = []
        if len(set(unit_ids)) != len(unit_ids):
            issue('UNIT_PLAN', 'scope', 'Duplicate common unit IDs')
        if not nonempty(course):
            issue('COURSE_REQUIRED', 'scope', 'Verified course name is required')
        # The source rule also covers other verified high-school textbook
        # courses with the existing 5x3 default. Identification is reviewed
        # from the authoritative source, not guessed from this string.
        n = course_policy(course)['mock_questions_per_round']
        expected_counts = {'workbook': len(unit_ids), 'mock1': n, 'mock2': n, 'mock3': n}
        counts = Counter(row.get('set_id') for row in plan.values())
        if dict(counts) != expected_counts:
            issue('SET_COUNTS', 'plan', f'Expected {expected_counts}; got {dict(counts)}')
        wb_units = [row.get('unit_id') for row in plan.values() if row.get('set_id') == 'workbook']
        if Counter(wb_units) != Counter(unit_ids):
            issue('WORKBOOK_UNIT_COVERAGE', 'plan', 'Exactly one question per common unit required')
    elif scope.get('kind') not in {'partial', 'custom'} or not nonempty(scope.get('instruction')):
        issue('SCOPE_REQUIRED', 'scope', 'Use full production or record the explicit partial/custom request')

    seen_positions, set_numbers = set(), {}
    for qid, row in plan.items():
        set_id, number = row.get('set_id'), row.get('number')
        if not nonempty(set_id) or type(number) is not int or number < 1:
            issue('DISPLAY_NUMBER', qid, 'A set ID and positive integer number are required')
            continue
        key = (set_id, number)
        if key in seen_positions:
            issue('DISPLAY_DUPLICATE', qid, str(key))
        seen_positions.add(key)
        set_numbers.setdefault(set_id, []).append(number)
        for name, records in [('questions', questions), ('quick_key', quick), ('explanations', explanations)]:
            candidate = records.get(qid)
            if candidate is not None and (candidate.get('set_id'), candidate.get('number')) != key:
                issue('DISPLAY_MISMATCH', f'{name}/{qid}', str(key))
    if scope.get('kind') == 'full':
        for set_id, numbers in set_numbers.items():
            if sorted(numbers) != list(range(1, len(numbers) + 1)):
                issue('DISPLAY_SEQUENCE', set_id, 'Numbers must restart at 1 in each set')

    groups = index_records(data.get('passage_groups', []), 'passage_groups')
    group_members = {}
    group_sets = Counter()
    for gid, group in groups.items():
        loc = f'passage_groups/{gid}'
        qids = group.get('question_ids')
        if group.get('kind') != 'long_reading':
            issue('PASSAGE_GROUP_KIND', loc, 'Shared group must identify long_reading')
        if not isinstance(qids, list) or len(qids) != 2 or \
                any(not nonempty(x) for x in qids) or len(set(qids)) != 2:
            issue('PASSAGE_GROUP_MEMBERS', loc, 'A long passage set requires two distinct question IDs')
            continue
        if any(x not in questions for x in qids):
            issue('PASSAGE_GROUP_MEMBERS', loc, 'A shared question is missing')
            continue
        members = [questions[x] for x in qids]
        set_id = group.get('set_id')
        if not nonempty(set_id) or set_id == 'workbook' or any(q.get('set_id') != set_id for q in members):
            issue('PASSAGE_GROUP_SET', loc, 'Both long-reading questions must belong to the same mini-test')
        if nonempty(set_id):
            group_sets[set_id] += 1
        # This is the common implementation default, modeled on real 41~42
        # sets; it is not described as a subtype the user explicitly chose.
        if [q.get('type') for q in members] != ['제목', '어휘'] or \
                group.get('passage_question_id') != qids[1]:
            issue('PASSAGE_GROUP_DEFAULT', loc, 'Default shared set is title then vocabulary, owned by vocabulary')
        if members[0].get('choice_mode') != 'text' or members[1].get('choice_mode') != 'in_passage':
            issue('PASSAGE_GROUP_CHOICE_MODE', loc, 'Long set requires title choices and five in-passage vocabulary targets')
        numbers = [q.get('number') for q in members]
        available = set_numbers.get(set_id, []) if nonempty(set_id) else []
        if any(type(x) is not int for x in numbers) or not available or \
                numbers != [max(available) - 1, max(available)]:
            issue('PASSAGE_GROUP_POSITION', loc, 'The shared questions must be the last two consecutive questions')
        for qid in qids:
            if qid in group_members:
                issue('PASSAGE_GROUP_DUPLICATE', loc, f'{qid} belongs to more than one group')
            group_members[qid] = gid
            if questions[qid].get('passage_group_id') != gid:
                issue('PASSAGE_GROUP_LINK', qid, 'Question and shared-group links disagree')
    for qid, q in questions.items():
        if q.get('passage_group_id') is not None and group_members.get(qid) != q.get('passage_group_id'):
            issue('PASSAGE_GROUP_LINK', qid, 'Question links to an absent or different shared group')
    if scope.get('kind') == 'full' and dict(group_sets) != {'mock1': 1, 'mock2': 1, 'mock3': 1}:
        issue('LONG_READING_COVERAGE', 'passage_groups', 'Each of the three mini-tests requires one final two-question long set')

    fingerprints = {}
    for qid, q in questions.items():
        loc = f'questions/{qid}'
        kind, mode = q.get('type'), q.get('choice_mode')
        if kind not in TYPES:
            issue('QUESTION_TYPE', loc, 'Unknown type or prohibited grammar question')
        if not nonempty(q.get('question')):
            issue('QUESTION_REQUIRED', loc, 'Question prompt is missing')
        if kind == '내용' and q.get('question') not in CONTENT_PROMPTS:
            issue('CONTENT_PROMPT', loc, 'Use the standard agreement/disagreement prompt, not a specific-fact question')
        # Required content checks precede any symbolic-choice branch.
        if kind == '삽입' and not nonempty(q.get('given')):
            issue('GIVEN_REQUIRED', loc, 'Insertion question has no given sentence')
        if kind == '순서':
            if not nonempty(q.get('given')):
                issue('GIVEN_REQUIRED', loc, 'Ordering question has no given passage')
            blocks = q.get('blocks')
            if not isinstance(blocks, dict) or set(blocks) != {'A', 'B', 'C'} or any(not nonempty(x) for x in blocks.values()):
                issue('BLOCKS_REQUIRED', loc, 'Ordering requires nonempty A/B/C blocks')
        elif not nonempty(q.get('passage')):
            issue('PASSAGE_REQUIRED', loc, 'Question passage is missing')
        if kind == '함축 의미' and not nonempty(q.get('target')):
            issue('TARGET_REQUIRED', loc, 'Target expression is missing')
        prompt_marks = q.get('prompt_underlines', [])
        prompt = q.get('question')
        valid_marks = isinstance(prompt_marks, list) and isinstance(prompt, str)
        if valid_marks:
            valid_marks = all(isinstance(pair, list) and len(pair) == 2 and
                              all(type(x) is int for x in pair) and
                              0 <= pair[0] < pair[1] <= len(prompt) for pair in prompt_marks)
        if valid_marks:
            valid_marks = prompt_marks == sorted(prompt_marks) and \
                all(prompt_marks[i][1] <= prompt_marks[i + 1][0] for i in range(len(prompt_marks) - 1))
        if not valid_marks:
            issue('PROMPT_UNDERLINE_SPAN', loc, 'Prompt underlines need ordered, non-overlapping Unicode spans')
        if kind == '함축 의미' and (not valid_marks or len(prompt_marks) != 1 or
                                 prompt[slice(*prompt_marks[0])] != q.get('target')):
            issue('PROMPT_TARGET_UNDERLINE', loc, 'Underline the exact cited target expression in the prompt')
        if kind == '요약' and not nonempty(q.get('summary')):
            issue('SUMMARY_REQUIRED', loc, 'Summary text is missing')
        if mode not in {'text', 'in_passage', 'order'}:
            issue('CHOICE_MODE', loc, 'Unknown choice mode')
        elif mode == 'in_passage' and kind not in SYMBOL_TYPES:
            issue('CHOICE_MODE', loc, 'This type requires separate choices')
        elif (kind == '순서') != (mode == 'order'):
            issue('CHOICE_MODE', loc, 'Ordering type and choice mode must agree')
        if q.get('set_id') == 'workbook' and (kind in SYMBOL_TYPES | {'순서'} or mode != 'text'):
            issue('WORKBOOK_TYPE', loc, 'Workbook requires learned-word meaning choices')
        choices = choice_map(q.get('choices'), range(1, 6), f'{loc}/choices')
        answer = q.get('answer')
        if type(answer) is not int or answer not in range(1, 6):
            issue('ANSWER_RANGE', loc, 'Answer must be integer 1..5')
        if mode == 'in_passage':
            expected_symbols = {i: chr(0x2460 + i - 1) for i in range(1, 6)}
            if choices != expected_symbols:
                issue('SYMBOL_MAP', loc, 'Internal options must be ① through ⑤')
        if mode == 'order':
            permutations = q.get('permutations')
            if not isinstance(permutations, list) or len(permutations) != 5:
                issue('ORDER_CHOICES', loc, 'Five ordering choices required')
            else:
                valid = all(isinstance(x, list) and sorted(x) == ['A', 'B', 'C'] for x in permutations)
                if not valid or len({tuple(x) for x in permutations if isinstance(x, list) and all(isinstance(y, str) for y in x)}) != 5:
                    issue('ORDER_CHOICES', loc, 'Five distinct permutations of A/B/C required')
                elif permutations != ORDER_PERMUTATIONS:
                    issue('ORDER_CANONICAL_CHOICES', loc, 'Choices must be ACB, BAC, BCA, CAB, CBA in that order')
                elif choices != {i + 1: ' → '.join(x) for i, x in enumerate(permutations)}:
                    issue('ORDER_CHOICE_TEXT', loc, 'Choice text disagrees with permutations')
        # Exact duplication only. Near-clones still need independent review.
        fp = json.dumps([kind, q.get('question'), q.get('passage'), q.get('given'),
                         q.get('blocks'), q.get('target'), q.get('summary'), choices],
                        ensure_ascii=False, sort_keys=True)
        if fp in fingerprints:
            issue('EXACT_DUPLICATE', loc, f'Duplicates {fingerprints[fp]}')
        fingerprints[fp] = qid
        key, exp = quick.get(qid), explanations.get(qid)
        if key is not None and (type(key.get('answer')) is not int or key.get('answer') != answer):
            issue('QUICK_ANSWER_MISMATCH', f'quick_key/{qid}', 'Quick key differs from question answer')
        if exp is None:
            continue
        if type(exp.get('answer')) is not int or exp.get('answer') != answer:
            issue('EXPLANATION_ANSWER_MISMATCH', f'explanations/{qid}', 'Explanation answer differs')
        exp_choices = choice_map(exp.get('choices'), range(1, 6), f'explanations/{qid}/choices')
        if choices != exp_choices:
            issue('EXPLANATION_CHOICES_MISMATCH', qid, 'Student and explanation choices differ')
        if mode == 'text':
            choice_map(exp.get('choices_ko'), range(1, 6), f'explanations/{qid}/choices_ko')
        elif exp.get('choices_ko') not in (None, []):
            issue('SYMBOL_TRANSLATION', qid, 'Do not fabricate sentence translations for symbolic options')
        if type(answer) is int and answer in range(1, 6):
            choice_map(exp.get('wrong_reasons'), set(range(1, 6)) - {answer},
                       f'explanations/{qid}/wrong_reasons')
        for field in ('evidence', 'explanation'):
            if not nonempty(exp.get(field)):
                issue('EXPLANATION_REQUIRED', f'explanations/{qid}/{field}', 'Missing explanation content')

    if scope.get('kind') == 'full' and questions:
        distribution = Counter(q.get('answer') for q in questions.values() if type(q.get('answer')) is int)
        if distribution and max(distribution.values()) / len(questions) >= 0.7:
            issue('ANSWER_DISTRIBUTION', 'questions', 'One answer number accounts for at least 70% of the complete book')
    return {'status': 'FAIL' if errors else 'PASS', 'errors': errors,
            'checked_question_count': len(questions),
            'scope': 'record correspondence and required fields only',
            'source_reconstruction': 'NOT_CHECKED_BY_THIS_TOOL',
            'semantic_review': 'NOT_PERFORMED', 'independent_reviews': 'NOT_PERFORMED',
            'docx_presence': 'NOT_CHECKED_BY_THIS_TOOL', 'visual_review': 'NOT_PERFORMED'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding='utf-8-sig'))
        if not isinstance(data, dict):
            raise ValueError('Input must be an object')
        result = check(data)
    except (ValueError, TypeError, KeyError) as exc:
        result = {'status': 'FAIL', 'errors': [{'code': 'INPUT_INVALID', 'message': str(exc)}]}
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.report:
        args.report.write_text(text + '\n', encoding='utf-8')
    print(text)
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
