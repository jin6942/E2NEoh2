"""Check source/learning-unit/annotation/workbook links in a common manuscript.

See references/manuscript-data.md. All offsets are Unicode code points. Lexical
level, translation and grammatical judgments are supplied by the content reviewer;
this checker does not infer them or certify them. A structural PASS is never FINAL.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

from analysis_body import build_analysis_bodies
from learning_units import group_units
from question_source import excerpt, span
from sv_line import render_sv
from syntax_training import training_version, check_unit as check_syntax_unit
from source_contract import (lesson_identity, check_source_structure, display_book_name,
                             display_source_label)
from structure_hints import (display_pairs, omitted_relative_source_text, omitted_conjunction_source_text,
                             MODAL_FORM, MODAL_PERFECT_FORM, MODAL_PERFECT_VERB, VERB_FUNCTION_FORMULA)

WORDS = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)*")
PRONOUNS = {'they', 'their', 'them', 'themselves', 'our', 'us', 'his', 'hers', 'its'}
EXEMPTIONS = {'below-middle1-unneeded', 'standalone-and-but', 'standalone-you', 'proper-name-repeat'}
READING_RULE_REVISION = 'R2026-09-23'
DUPLICATE_GLOSS_PAREN = re.compile(
    r"\(\s*(?P<verb>[A-Za-z]+)(?:\s+[A-Za-z]+){0,2}\s+"
    r"(?:A\s+(?:to\s+[VB]|with\s+B|as\s+B|for\s+B|B|V(?:-ing)?)|V(?:-ing)?)"
    r"\s*(?:—|–| - )\s*[^()]*[가-힣][^()]*\)")
# Narrowly catch the reviewed verb-construction duplicate class. This is not a
# ban on English gloss parentheses or an automatic grammar classifier.
DUPLICATE_GLOSS_VERBS = set(('allow allows allowed allowing help helps helped helping '
    'keep keeps kept keeping make makes made making tell tells told telling '
    'finish finishes finished finishing give gives gave given giving '
    'provide provides provided providing send sends sent sending '
    'compare compares compared comparing').split())


def text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{label}: nonempty text required')
    return value


def records(rows, label, key=lambda r: r['id']):
    if not isinstance(rows, list):
        raise ValueError(f'{label}: list required')
    indexed = {}
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError(f'{label}: object required')
        identity = key(row)
        if identity in indexed:
            raise ValueError(f'{label}: duplicate identity {identity}')
        indexed[identity] = row
    return indexed


def reading_rules(sentence, glosses, required=False):
    """Validate declared reading constraints, without inferring grammar from text.

    Legacy annotations may omit these declarations. A declaration is a reviewer's
    claim; passing this check neither finds missing claims nor verifies its grammar.
    """
    original = sentence['text']
    declaration = sentence.get('reading_checks')
    if declaration is None and not required:
        return
    if not isinstance(declaration, dict):
        raise ValueError('reading_checks must be an object')
    if required:
        text(declaration.get('review_record'), 'Reading-rule review record')
        for field in ['required_breaks', 'protected_spans', 'function_gloss_ids']:
            if field not in declaration:
                raise ValueError(f'New reading revision requires explicit {field}')
    if 'function_gloss_ids' in declaration:
        expected = [gid for gid, g in glosses.items() if g.get('kind') == 'function']
        if declaration['function_gloss_ids'] != expected:
            raise ValueError('Reviewed function_gloss_ids must match all declared function glosses in order')
    breaks = {c['start'] for c in sentence['chunks'][1:]}
    for field in ['required_breaks', 'protected_spans']:
        if not isinstance(declaration.get(field, []), list):
            raise ValueError(f'reading_checks/{field} must be a list')
    for row in declaration.get('required_breaks', []):
        if row.get('kind') not in {'postpositive-adjective', 'postnominal-preposition', 'passive-agent-by'}:
            raise ValueError('Unknown required reading-boundary kind')
        at = row.get('at')
        if type(at) is not int or not 0 < at < len(original) or original[at].isspace():
            raise ValueError('Required reading boundary must start an actual source phrase')
        text(row.get('reason'), 'Reviewer-supplied boundary reason')
        if row['kind'] == 'passive-agent-by':
            by_starts = {m.start() for m in re.finditer(r'\bby\b', original, flags=re.IGNORECASE)}
            if at not in by_starts:
                raise ValueError('Passive-agent reading boundary must start source by')
        if at not in breaks:
            if row['kind'] == 'passive-agent-by':
                raise ValueError('Missing declared passive-agent by reading boundary')
            raise ValueError('Missing declared postmodifier reading boundary')
    for row in declaration.get('protected_spans', []):
        kind = row.get('kind')
        if kind not in {'dummy-it-prefix', 'fixed-expression', 'adjective-complement', 'quantity-kind-of'}:
            raise ValueError('Unknown protected reading-span kind')
        a, b = span(row.get('span'), original)
        text(row.get('reason'), 'Reviewer-supplied protected-span reason')
        if any(a < cut < b for cut in breaks):
            raise ValueError('Reading boundary splits a declared protected span')
        if kind == 'quantity-kind-of':
            # The reviewer declares a same-order quantity/kind expression; the
            # checker only binds that claim to one unsplit source/gloss span.
            # It does not infer this category for arbitrary noun + of phrases.
            gid = row.get('gloss_id')
            g = glosses.get(gid) if isinstance(gid, str) else None
            if g is None:
                raise ValueError('Quantity/kind-of span needs its combined gloss')
            if g.get('spans') != [[a, b]]:
                raise ValueError('Quantity/kind-of gloss must have exactly its single protected source span')
            normalize = lambda value: re.sub(r'\s+', ' ', value).strip().casefold()
            phrase = normalize(original[a:b])
            head = g.get('headword')
            if (not isinstance(head, str) or normalize(head) != phrase or
                    len(WORDS.findall(phrase)) < 2 or not re.search(r'\bof$', phrase)):
                raise ValueError('Quantity/kind-of headword must match its source expression ending in of')
            for other_id, other in glosses.items():
                if other_id == gid:
                    continue
                if any(max(a, x) < min(b, y) and original[max(a, x):min(b, y)].strip()
                       for x, y in other['spans']):
                    raise ValueError('Quantity/kind-of expression cannot duplicate its component glosses')
        if kind == 'dummy-it-prefix':
            gid = row.get('gloss_id')
            g = glosses.get(gid)
            if g is None:
                raise ValueError('Dummy-It prefix needs its combined gloss')
            head = re.sub(r'\s+', ' ', g['headword'].replace("'", '\u2032').strip()).lower()
            if not re.fullmatch(r'it .+ that s\u2032 v\u2032', head):
                raise ValueError('Dummy-It gloss must retain a full It ... that S\u2032 V\u2032 template')
            if not re.fullmatch(r'it\b.+\bthat', original[a:b], flags=re.IGNORECASE | re.DOTALL):
                raise ValueError('Declared dummy-It prefix must run from source It through that')
            if not any(x <= a and b <= y for x, y in g['spans']):
                raise ValueError('Combined dummy-It gloss must cover its declared prefix')
            for other_id, other in glosses.items():
                if other_id == gid:
                    continue
                if not any(a <= x < b for x, _ in other['spans']):
                    continue
                other_head = other['headword'].strip().lower()
                if other_head == 'it' or re.match(r'^that(?:\s|$)', other_head):
                    raise ValueError('Separate It/that gloss duplicates the combined dummy-It template')


def split_phrasal_display_ranges(hint, original):
    """Check authored omitted-object fragments, without identifying verb grammar."""
    pairs = display_pairs(hint)
    a, b = span(hint['span'], original)
    selected = [span(s, original) for s in hint['display_spans']]
    if any(not a <= x < y <= b for x, y in selected):
        raise ValueError('Split-phrasal-verb display_spans must lie inside the hint span')
    fragments = [original[x:y] for x, y in selected]
    if any(not fragment.strip() or fragment != fragment.strip() for fragment in fragments):
        raise ValueError('Split-phrasal-verb fragments must be nonempty source text without edge whitespace')
    if not original[selected[0][1]:selected[1][0]].strip():
        raise ValueError('Split-phrasal-verb omitted gap must contain actual source text')
    if any(word.start() < edge < word.end() for word in WORDS.finditer(original)
           for selected_span in selected for edge in selected_span):
        raise ValueError('Split-phrasal-verb fragments must not cut through source words')
    english = pairs[0]['en'].replace('[', '').replace(']', '')
    if english != ' … '.join(fragments):
        raise ValueError('Split-phrasal-verb English must match its exact original fragments joined by spaced ellipses')
    return selected


def omitted_relative_display_range(hint, original):
    """Match the hint excerpt after removing its one certified editorial marker.

    No transcription, sentence, chunk or S/V data is changed or normalized.
    Ordinary parenthetical additions never enter this narrowly scoped path.
    """
    english = omitted_relative_source_text(hint)
    start, end = span(hint['span'], original)
    matches = list(re.finditer(re.escape(english), original[start:end]))
    if len(matches) != 1:
        raise ValueError('Omitted-relative display must match one exact original excerpt after its certified supplement is removed')
    selected = (start + matches[0].start(), start + matches[0].end())
    if any(word.start() < edge < word.end() for word in WORDS.finditer(original) for edge in selected):
        raise ValueError('Omitted-relative source excerpt must not cut through source words')
    return selected


def omitted_conjunction_display_range(hint, original):
    """Match source after removing only the reviewed omitted-that marker."""
    english = omitted_conjunction_source_text(hint)
    start, end = span(hint['span'], original)
    matches = list(re.finditer(re.escape(english), original[start:end]))
    if len(matches) != 1:
        raise ValueError('Omitted-conjunction display must match one exact original excerpt after its certified supplement is removed')
    selected = (start + matches[0].start(), start + matches[0].end())
    if any(word.start() < edge < word.end() for word in WORDS.finditer(original) for edge in selected):
        raise ValueError('Omitted-conjunction source excerpt must not cut through source words')
    return selected


def verb_form_review(gloss, original):
    """Validate an authored form decision, not an automatic suffix/POS guess."""
    review = gloss.get('verb_form')
    if review is None:
        return
    if gloss.get('kind') == 'function' or not isinstance(review, dict):
        raise ValueError('verb_form requires a lexical gloss and an explicit review object')
    usage = review.get('usage')
    if usage not in {'past-participle', 'passive-participle', 'perfect-participle',
                     'regular-past', 'irregular-past', 'ing', 'third-person-singular'}:
        raise ValueError('Unknown reviewed verb_form usage')
    a, b = span(review.get('source_span'), original)
    if not any(x <= a < b <= y for x, y in gloss['spans']):
        raise ValueError('verb_form source_span must belong to its lexical gloss')
    source_form = original[a:b]
    if not any(m.span() == (a, b) for m in WORDS.finditer(original)):
        raise ValueError('verb_form source_span must select one complete original verb token')
    lemma = review.get('lemma')
    if not isinstance(lemma, str) or not WORDS.fullmatch(lemma):
        raise ValueError('verb_form needs the reviewed one-word lemma')
    if usage == 'regular-past' and not source_form.casefold().endswith('ed'):
        raise ValueError('Reviewed regular-past exception applies only to the source -ed form')
    if usage == 'ing' and not source_form.casefold().endswith('ing'):
        raise ValueError('Reviewed ing form must retain its actual source -ing position')
    if usage == 'third-person-singular':
        text(review.get('review_record'), 'Third-person-singular lexical-verb review record')
        base = lemma.casefold()
        forms = {base + 's'}
        if base.endswith(('s', 'x', 'z', 'ch', 'sh')):
            forms = {base + 'es'}
        if base.endswith('o'):
            forms.add(base + 'es')
        if len(base) > 1 and base.endswith('y') and base[-2] not in 'aeiou':
            forms = {base[:-1] + 'ies'}
        if base.endswith('z') and not base.endswith('zz'):
            forms.add(base + 'zes')
        if base == 'have':
            forms = {'has'}
        if base in {'do', 'go'}:
            forms = {base + 'es'}
        if base == 'be' or source_form.casefold() not in forms:
            raise ValueError('Reviewed third-person-singular source must match its lexical lemma; do not strip a final s or normalize a be/function formula')
    head = WORDS.match(gloss['headword'])
    expected = source_form if usage in {'past-participle', 'passive-participle', 'irregular-past'} else lemma
    if head is None or head.group().casefold() != expected.casefold():
        raise ValueError('Reviewed verb_form headword must preserve passive/independent p.p./irregular past, and use the lemma for active perfect, regular past, ing or third-person singular')
    if usage in {'passive-participle', 'perfect-participle'}:
        text(review.get('function_gloss_id'), 'Reviewed participle function_gloss_id')
    particle_spans = review.get('particle_spans', [])
    if not isinstance(particle_spans, list):
        raise ValueError('Reviewed participle particle_spans must be a list of source words')
    if particle_spans:
        if usage != 'passive-participle' or 'verb_construction' in gloss:
            raise ValueError('Reviewed passive particle_spans cannot be an object frame or another verb form')
        text(review.get('review_record'), 'Passive phrasal-verb review record')
        selected = [span(p, original) for p in particle_spans]
        if (selected != sorted(selected) or len(set(selected)) != len(selected) or
                any(x < b or not any(m.span() == (x, y) for m in WORDS.finditer(original)) for x, y in selected)):
            raise ValueError('Reviewed participle particles must select complete following source words')
        if gloss['spans'] != [[a, b]] + [list(p) for p in selected]:
            raise ValueError('Reviewed participle lexical spans must contain only its verb and particles')
        source_form = ' '.join([source_form] + [original[x:y] for x, y in selected])
    # Local copy only (공통영어2 YBM(박준언) 2과 Further Reading, 2026-09-29 사용자 결정
    # “p.p.에 to V 결합”): a passive p.p. completed by a reviewed to-complement keeps
    # the actual p.p. and adds only the `to V` frame (`believed to V`).
    passive_to = (usage == 'passive-participle' and not particle_spans
                  and isinstance(gloss.get('verb_construction'), dict)
                  and gloss['verb_construction'].get('kind') == 'to-complement')
    if passive_to and gloss['headword'].strip() == source_form + ' to V':
        pass
    elif usage == 'passive-participle' and gloss['headword'].strip() != source_form:
        raise ValueError('Reviewed passive participle headword must preserve only its actual source p.p.')
    if usage == 'perfect-participle':
        # This must be in a field actually printed by the glossary renderer,
        # not merely in metadata invisible to the learner.
        annotations = (f'({source_form}{particle} {lemma}의 p.p.형)' for particle in ('은', '는'))
        if not any(annotation in gloss.get('meaning_ko', '') for annotation in annotations):
            raise ValueError('Active perfect gloss must print its source p.p.-to-lemma annotation in meaning_ko')
        if gloss['headword'].strip().casefold() != lemma.casefold() and 'verb_construction' not in gloss:
            raise ValueError('Active perfect construction headword needs reviewed source-bound verb_construction')


def verb_construction_review(gloss, original):
    """Bind an authored lexical frame to source words, without guessing grammar."""
    review = gloss.get('verb_construction')
    if review is None:
        return
    if not isinstance(review, dict) or gloss.get('kind') != 'lexical':
        raise ValueError('verb_construction requires a lexical gloss and an explicit review')
    if review.get('kind') not in {'verb-frame', 'to-complement'}:
        raise ValueError('Reviewed verb_construction kind must distinguish a frame or to-complement')
    text(review.get('review_record'), 'Verb-construction review record')
    a, b = span(review.get('verb_span'), original)
    if not any(m.span() == (a, b) for m in WORDS.finditer(original)):
        raise ValueError('verb_construction verb_span must select one complete source verb')
    lemma = review.get('lemma')
    if not isinstance(lemma, str) or not WORDS.fullmatch(lemma):
        raise ValueError('verb_construction needs a reviewed lemma')
    form = gloss.get('verb_form')
    if form is not None and (form['source_span'] != [a, b] or form['lemma'] != lemma):
        raise ValueError('verb_construction and verb_form must identify the same source verb and lemma')
    links = review.get('link_spans')
    if not isinstance(links, list):
        raise ValueError('verb_construction requires source-bound link_spans')
    selected = [span(p, original) for p in links]
    if selected != sorted(selected) or any(x < b for x, y in selected):
        raise ValueError('verb_construction linking words must follow its verb in source order')
    if any(not any(m.span() == (x, y) for m in WORDS.finditer(original)) for x, y in selected):
        raise ValueError('verb_construction link_spans must select complete source words')
    if len(set(selected)) != len(selected):
        raise ValueError('verb_construction cannot repeat a linking-word position')
    if any(not any(x <= p < q <= y for x, y in gloss['spans']) for p, q in [(a, b)] + selected):
        raise ValueError('verb_construction words must belong to its lexical gloss')
    if gloss['spans'] != [[a, b]] + [list(p) for p in selected]:
        raise ValueError('verb_construction lexical spans must contain only its source verb and linking words, not objects')
    head = gloss['headword'].split()
    # Local copy only (2과 Further Reading, 2026-09-29): a passive p.p. + to V keeps
    # its actual p.p. headword; parallel `to V … and to V` may link each actual to.
    passive_to = (review['kind'] == 'to-complement' and isinstance(form, dict)
                  and form.get('usage') == 'passive-participle')
    expected_head = original[a:b] if passive_to else lemma
    if not head or head[0].casefold() != expected_head.casefold():
        raise ValueError('verb_construction must use its reviewed lemma as the headword')
    if passive_to:
        if (head[1:] != ['to', 'V'] or not selected
                or any(original[x:y].casefold() != 'to' for x, y in selected)):
            raise ValueError('Reviewed passive to-complement must be one actual p.p. + to V frame')
        return
    suffix = head[1:]
    if not any(w in {'A', 'B', 'V', 'V-ing'} for w in suffix):
        raise ValueError('verb_construction must retain its A/B/V frame')
    if [w.casefold() for w in suffix if w not in {'A', 'B', 'V', 'V-ing'}] != [original[x:y].casefold() for x, y in selected]:
        raise ValueError('verb_construction must preserve its source-bound linking words')
    if review['kind'] == 'to-complement' and (suffix != ['to', 'V'] or len(selected) != 1):
        raise ValueError('Reviewed to-complement must be one verb + to V frame')


def verb_phrase_review(gloss, original, required=False):
    """Check the source binding of a reviewed, combined passive/perfect gloss."""
    review = gloss.get('verb_phrase')
    if review is None:
        return
    if gloss.get('kind') != 'lexical' or not isinstance(review, dict) or 'verb_form' in gloss:
        raise ValueError('verb_phrase requires one lexical phrase, separate from verb_form')
    idiom = review.get('usage') == 'idiom'
    if review.get('usage') not in {None, 'idiom'}:
        raise ValueError('Unknown reviewed verb_phrase usage')
    formula = text(review.get('formula_label'), 'Reviewed verb-phrase formula')
    perfect_progressive = re.search(r'\b(?:have|has|had)\b.*\bbeen V-ing$', formula, re.IGNORECASE)
    if required and not idiom and not perfect_progressive:
        raise ValueError('Current passive/perfect training separates formula and lexical gloss; a combined verb_phrase requires an explicitly reviewed idiom')
    if (not VERB_FUNCTION_FORMULA.fullmatch(formula) or not
            (re.search(r'\s+p\.?p\.?$', formula, re.IGNORECASE) or perfect_progressive)):
        raise ValueError('Combined verb_phrase declares a passive or perfect formula')
    ranges = review.get('source_spans')
    if not isinstance(ranges, list) or not ranges:
        raise ValueError('verb_phrase needs actual source_spans')
    selected = [span(s, original) for s in ranges]
    if selected != sorted(selected) or any(a[1] > b[0] for a, b in zip(selected, selected[1:])):
        raise ValueError('verb_phrase source_spans must be ordered and nonoverlapping')
    for a, b in selected:
        if not any(x <= a < b <= y for x, y in gloss['spans']):
            raise ValueError('verb_phrase source spans must be covered by its gloss')
        if any(m.start() < edge < m.end() for m in WORDS.finditer(original) for edge in (a, b)):
            raise ValueError('verb_phrase source spans must not cut a word')
        if not re.fullmatch(r"[A-Za-z]+(?:['’-][A-Za-z]+)*(?: [A-Za-z]+(?:['’-][A-Za-z]+)*)*", original[a:b]):
            raise ValueError('verb_phrase source spans require lexical words without punctuation or edge spaces')
    phrase = ' '.join(original[a:b] for a, b in selected)
    head = gloss['headword']
    if idiom:
        text(review.get('review_record'), 'Idiom review record')
        text(review.get('reason'), 'Idiom contextual meaning reason')
        dictionary = text(review.get('dictionary_headword'), 'Idiom dictionary headword')
        if head != dictionary:
            raise ValueError('Reviewed idiom must print its dictionary headword')
        source_words = phrase.split()
        dictionary_words = [w for w in dictionary.split() if w not in {'A', 'B', 'V', 'V-ing'}]
        # Only the explicitly reviewed initial auxiliary is normalized. The
        # lexical verb and preposition must remain source-bound; this does not
        # certify that an arbitrary expression is semantically an idiom.
        if (not dictionary_words or dictionary_words[0] != 'be' or
                not source_words or source_words[0].casefold() not in
                {'be', 'am', 'is', 'are', 'was', 'were', 'been', 'being'} or
                [w.casefold() for w in dictionary_words[1:]] != [w.casefold() for w in source_words[1:]]):
            raise ValueError('Idiom dictionary/source correspondence must preserve its lexical words and normalize only reviewed be')
    elif head != phrase and not head.startswith(phrase + ' '):
        raise ValueError('Combined passive/perfect headword must preserve the actual source verb phrase')
    if not idiom and head != phrase:
        suffix = head[len(phrase) + 1:].split(' ')
        if not any(token in {'A', 'B'} for token in suffix) or any(not WORDS.fullmatch(token) for token in suffix):
            raise ValueError('Combined headword suffix must be an A/B construction frame with source-bound words')
        source_tail = [original[m.start():m.end()] for x, y in gloss['spans']
                       for m in WORDS.finditer(original, x, y) if m.start() >= selected[-1][1]]
        if [token for token in suffix if token not in {'A', 'B'}] != source_tail:
            raise ValueError('Combined construction frame must preserve its actual source-bound linking words')
    a, b = span(review.get('verb_span'), original)
    if not any(x <= a < b <= y for x, y in selected) or (not idiom and b != selected[-1][1]):
        raise ValueError('verb_phrase must end at its reviewed lexical verb, before objects')
    if any(m.start() < edge < m.end() for m in WORDS.finditer(original) for edge in (a, b)):
        raise ValueError('verb_phrase verb_span must preserve complete lexical words')
    if not re.fullmatch(r"[A-Za-z]+(?:['’-][A-Za-z]+)*(?: [A-Za-z]+(?:['’-][A-Za-z]+)*)*", original[a:b]):
        raise ValueError('verb_phrase verb_span must select actual lexical words')


def participle_function_review(glosses, original):
    """Check declared voice and formula links; never infer undeclared POS."""
    for gid, gloss in glosses.items():
        review = gloss.get('verb_form', {})
        usage = review.get('usage')
        if usage not in {'passive-participle', 'perfect-participle'}:
            continue
        function_id = review['function_gloss_id']
        function = glosses.get(function_id)
        links = [g for g in glosses.values() if gid in g.get('combines_with', [])]
        if (function is None or function.get('kind') != 'function' or
                not any(g['id'] == function_id for g in links)):
            raise ValueError('Reviewed participle must link exactly one composite function gloss')
        for other in links:
            if other['id'] == function_id:
                continue
            if not outer_function(other, function, original, passive=usage == 'passive-participle'):
                raise ValueError('Reviewed participle must link exactly one composite function gloss; only a source-bound earlier outer to V or simple-passive modal function may also link it')
        formula = function['headword'].strip()
        prefix = re.sub(r'\s+p\.?p\.?$', '', formula, flags=re.IGNORECASE).split()
        auxiliaries = [word for word in prefix if word.casefold() != 'not']
        supported = bool(VERB_FUNCTION_FORMULA.fullmatch(formula) and
                         re.search(r'\s+p\.?p\.?$', formula, flags=re.IGNORECASE))
        # This classifies only an authored formula, never sentence text. The
        # final auxiliary distinguishes active perfect from every passive
        # composite, including modal/perfect/progressive combinations.
        passive = bool(supported and auxiliaries and auxiliaries[-1].casefold() in
                       {'be', 'am', 'is', 'are', 'was', 'were', 'been', 'being'})
        perfect = bool(supported and auxiliaries and auxiliaries[-1].casefold() in {'have', 'has', 'had'})
        if ((usage == 'passive-participle' and not passive) or
                (usage == 'perfect-participle' and not perfect)):
            raise ValueError('Reviewed passive/active-perfect participle must match its composite formula; passive takes precedence in have been p.p.')
        a, b = review['source_span']
        if (not any(x < a for x, y in function['spans']) or
                any(y > b for x, y in function['spans'])):
            raise ValueError('Participle function gloss must bind its earlier source auxiliary and stop before objects')


def outer_function(outer, composite, original, passive=False):
    """Recognize an authored outer infinitive frame with separate source words.

    A lexical target can be shared by had to V + be p.p. or would V + be p.p.,
    but this must not license splitting modal-perfect composites. No sentence
    POS or infinitive interpretation is inferred here; only the authored frame
    and exact earlier source words are checked.
    """
    head = outer['headword'].strip().split()
    if outer.get('kind') != 'function' or len(head) < 2 or head[-1] != 'V':
        return False
    to_frame = head[-2:] == ['to', 'V']
    composite_auxiliaries = re.sub(r'\s+p\.?p\.?$', '', composite['headword'], flags=re.IGNORECASE).split()
    simple_passive = bool(passive and composite_auxiliaries and all(
        word.casefold() in {'be', 'am', 'is', 'are', 'was', 'were', 'been', 'being'}
        for word in composite_auxiliaries))
    modal_frame = simple_passive and bool(MODAL_FORM.fullmatch(' '.join(head[:-1])))
    if not to_frame and not modal_frame:
        return False
    boundary = min(a for a, b in composite['spans'])
    if not outer['spans'] or any(b > boundary for a, b in outer['spans']):
        return False
    parts = []
    for a, b in outer['spans']:
        if any(m.start() < edge < m.end() for m in WORDS.finditer(original) for edge in (a, b)):
            return False
        selected = original[a:b]
        if not re.fullmatch(r"[A-Za-z]+(?:['’-][A-Za-z]+)*(?: [A-Za-z]+(?:['’-][A-Za-z]+)*)*", selected):
            return False
        parts.extend(selected.split())
    expected = [word.casefold() for word in head[:-1]]
    actual = [word.casefold() for word in parts]
    # Preserve existing dictionary have/be infinitive frames while retaining
    # their actual had/has/was/is source positions in lexical coverage.
    if expected and actual:
        if expected[0] == 'have' and actual[0] in {'have', 'has', 'had'}:
            actual[0] = 'have'
        if expected[0] == 'be' and actual[0] in {'be', 'am', 'is', 'are', 'was', 'were'}:
            actual[0] = 'be'
    return actual == expected


def contextual_gloss_meanings(meaning):
    """Read complete printed main senses, excluding parenthetical side notes."""
    contextual = re.sub(r'\([^()]*\)', '', meaning)
    return {part.strip() for part in contextual.split(',') if part.strip()}


def lexical_step_review(hint, lexical, functions, original):
    reviewed = [g for g in lexical if g.get('verb_form', {}).get('usage') in
                {'passive-participle', 'perfect-participle'}]
    step = hint.get('lexical_step')
    if reviewed and step is None:
        raise ValueError('Reviewed passive/perfect verb-function hint needs its lexical_step')
    if step is None:
        return
    target = next((g for g in lexical if g['id'] == step.get('gloss_id')), None)
    if target is None:
        raise ValueError('lexical_step must reference a linked lexical gloss')
    review = target.get('verb_form', {})
    if review.get('usage') not in {'passive-participle', 'perfect-participle'}:
        raise ValueError('lexical_step needs a reviewed passive or active-perfect participle')
    a, b = review['source_span']
    expected = original[a:b] if review['usage'] == 'passive-participle' else review['lemma']
    if step['form'] != expected:
        raise ValueError('lexical_step form must match the reviewed passive p.p. or active-perfect lemma')
    if hint['display_span'][1] != b:
        raise ValueError('Reviewed verb-function display must end at its exact lexical participle, before objects')
    function = next((f for f in functions if f['id'] == review['function_gloss_id']), None)
    if function is None or hint['formula_label'] != function['headword']:
        raise ValueError('lexical_step formula must match its reviewed composite function gloss')
    # For a simple lexical gloss its local meaning is already printed. A full
    # A/B/V frame needs a separately reviewed short local meaning in the hint.
    if 'verb_construction' not in target:
        if step['meaning_ko'] not in contextual_gloss_meanings(target['meaning_ko']):
            raise ValueError('Simple lexical_step meaning must match its printed lexical gloss meaning')


def participle_focus_review(hint, pairs, glosses, original):
    """Verify explicit independent-p.p. focus, not incidental participles."""
    if 'participle_focus_gloss_id' not in hint:
        return
    if hint.get('category') in {'function-combination', 'paired-structure'} or hint.get('display_mode') in {
            'verb-function', 'modal-perfect-verb', 'omitted-relative', 'omitted-conjunction'}:
        raise ValueError('Independent participle focus requires its own general structural hint')
    gid = hint['participle_focus_gloss_id']
    gloss = glosses.get(gid) if isinstance(gid, str) else None
    if gloss is None or gloss.get('verb_form', {}).get('usage') != 'past-participle':
        raise ValueError('participle_focus_gloss_id must identify a reviewed independent past-participle gloss')
    a, b = gloss['verb_form']['source_span']
    hstart, hend = hint['span']
    if not hstart <= a < b <= hend:
        raise ValueError('Independent participle focus must belong to its source hint span')
    english = original[a:b]
    # Ignore parenthetical usage/common-meaning notes, then select one complete
    # authored contextual sense. This never chooses a translation or treats a
    # Korean suffix as the whole lexical meaning (개최된 cannot become just 된).
    meanings = contextual_gloss_meanings(gloss['meaning_ko'])
    for pair in pairs:
        for link in pair.get('emphasis_links', []):
            if (len(link['en_spans']) == len(link['ko_spans']) == 1 and
                    pair['en'][slice(*link['en_spans'][0])] == english and
                    pair['ko'][slice(*link['ko_spans'][0])] in meanings):
                return
    raise ValueError('Independent participle focus must align the whole source p.p. with its entire contextual Korean meaning')


def relative_hint_coverage(sentence, glosses):
    """Check declared relative locations against actual general-hint English.

    This uses authored gloss IDs and already reviewed subject_relative clauses,
    never marker spelling or Korean gloss prose to infer grammar. Undeclared
    legacy sentences remain readable; missing semantic declarations are not found.
    """
    declaration = sentence.get('reading_checks')
    if not isinstance(declaration, dict) or 'relative_gloss_ids' not in declaration:
        return
    ids = declaration['relative_gloss_ids']
    if (not isinstance(ids, list) or
            any(not isinstance(gid, str) or not gid.strip() or gid != gid.strip() for gid in ids)):
        raise ValueError('relative_gloss_ids must be a list of nonempty gloss IDs; [] is allowed')
    if len(set(ids)) != len(ids):
        raise ValueError('relative_gloss_ids must not contain duplicate IDs')
    if any(gid not in glosses for gid in ids):
        raise ValueError('relative_gloss_ids points to an unknown gloss in this sentence')
    original = sentence['text']
    targets = {span(selected, original) for gid in ids for selected in glosses[gid]['spans']}
    for clause in sentence.get('clauses', []):
        if clause.get('kind') != 'subject_relative':
            continue
        start, marker = clause.get('start'), clause.get('marker')
        if (type(start) is not int or not isinstance(marker, str) or not marker or start < 0 or
                original[start:start + len(marker)] != marker):
            raise ValueError('Reviewed subject_relative marker must match its exact source start')
        targets.add((start, start + len(marker)))
    if not targets:
        return
    displayed_ranges = []
    for hint in sentence.get('hints', []):
        if hint.get('category') in {'function-combination', 'paired-structure'}:
            continue
        if hint.get('display_mode') == 'split-phrasal-verb':
            # The omitted gap cannot stand in for a relative marker that the
            # student never sees; only the two verified printed pieces count.
            displayed_ranges.extend(split_phrasal_display_ranges(hint, original))
            continue
        if hint.get('display_mode') == 'omitted-relative':
            displayed_ranges.append(omitted_relative_display_range(hint, original))
            continue
        if hint.get('display_mode') == 'omitted-conjunction':
            displayed_ranges.append(omitted_conjunction_display_range(hint, original))
            continue
        start, end = span(hint['span'], original)
        for pair in display_pairs(hint):
            english = pair['en'].replace('[', '').replace(']', '')
            # Source matching is constrained by the reviewed hint span; merely
            # widening that span cannot cover an absent marker in printed text.
            for match in re.finditer(re.escape(english), original[start:end]):
                displayed_ranges.append((start + match.start(), start + match.end()))
    for start, end in sorted(targets):
        if not any(left <= start < end <= right for left, right in displayed_ranges):
            raise ValueError(f'Relative marker [{start}, {end}] needs a source-matching general structure hint display')


def us_country_gloss_ids(original, glosses):
    """Use an explicit country gloss, not capitalization alone, to identify US.

    This narrow compatibility rule uses existing reviewed fields. It does not
    classify other names or infer the meaning of an unglossed occurrence.
    """
    return {gid for gid, g in glosses.items()
            if g.get('kind') != 'function'
            and g['headword'].strip() in {'US', 'the US', 'The US'}
            and g['meaning_ko'].strip() in {'미국', '미합중국'}
            and any(word.group() == 'US' for start, end in g['spans']
                    for word in WORDS.finditer(original[start:end]))}


def proper_name_identity(word):
    """Normalize only a terminal possessive for a declared name-repeat link."""
    return re.sub(r"['’]s$", '', word.lower())


def glossary(sentence, today_ids, require_reading_checks=False,
             earlier_us_country_gloss_ids=()):
    original = sentence['text']
    glosses = records(sentence.get('glosses'), 'glosses')
    intervals = {}
    previous = -1
    for gid, g in glosses.items():
        text(gid, 'gloss id')
        text(g.get('headword'), f'{gid}/headword')
        text(g.get('meaning_ko'), f'{gid}/meaning_ko')
        if require_reading_checks and any(match.group('verb').casefold() in DUPLICATE_GLOSS_VERBS
                for match in DUPLICATE_GLOSS_PAREN.finditer(g['meaning_ko'])):
            raise ValueError('Gloss meaning cannot duplicate an English expression and its meaning inside parentheses; use its verb-construction headword once')
        if require_reading_checks and g['headword'].strip().casefold() == 'you':
            raise ValueError('Standalone you gloss is excluded; retain source you and declare standalone-you coverage')
        if not isinstance(g.get('spans'), list) or not g['spans']:
            raise ValueError(f'{gid}: source spans required')
        ranges = [span(x, original) for x in g['spans']]
        if ranges != sorted(ranges) or any(a[1] > b[0] for a, b in zip(ranges, ranges[1:])):
            raise ValueError(f'{gid}: overlapping/unordered internal spans')
        if ranges[0][0] < previous:
            raise ValueError('Glosses must follow first source occurrence order')
        previous = ranges[0][0]
        signature = tuple(ranges)
        intervals.setdefault(signature, []).append(gid)
        kind = g.get('kind')
        if kind is not None and kind not in {'function', 'lexical'}:
            raise ValueError('Gloss kind must be function or lexical when supplied')
        if kind != 'function' and 'combines_with' in g:
            raise ValueError('Only function glosses can declare combines_with')
        normalized = re.sub(r'[\s.+]', '', g['headword']).lower()
        if (require_reading_checks and normalized == 'tov' and
                re.fullmatch(r'[~∼]?\s*(?:하기로|하려고|하는\s*데)', g['meaning_ko'].strip())):
            raise ValueError('Do not split to V as ~하기로/~하려고/~하는 데; use the reviewed verb + to V expression once')
        if kind == 'function':
            links = g.get('combines_with')
            if (not isinstance(links, list) or not links or
                    any(not isinstance(x, str) for x in links) or len(set(links)) != len(links)):
                raise ValueError('Function gloss needs unique lexical combines_with IDs')
            if normalized == 'hadpp' and g['meaning_ko'] != '~했다':
                raise ValueError('had p.p. function gloss meaning must be exactly ~했다')
        verb_form_review(g, original)
        verb_construction_review(g, original)
        verb_phrase_review(g, original, required=require_reading_checks)
        gstar = g.get('star')
        if type(gstar) is not bool:
            raise ValueError('Each gloss needs an explicit star boolean')
        learned = g.get('today_word_id')
        if gstar != (learned in today_ids):
            raise ValueError('Gloss star and confirmed today-word identity disagree')
        if learned is not None and learned not in today_ids:
            raise ValueError('Unknown today-word link')

    for gid, g in glosses.items():
        for target_id in g.get('combines_with', []):
            if target_id not in glosses or glosses[target_id].get('kind') != 'lexical':
                raise ValueError('Function combines_with must point to a lexical gloss in this sentence')
        if 'verb_phrase' in g:
            selected = g['verb_phrase']['source_spans']
            for other in glosses.values():
                if other['id'] != gid and any(max(a, x) < min(b, y)
                        for a, b in selected for x, y in other['spans']):
                    raise ValueError('Combined passive/perfect gloss must not duplicate its function or lexical components')
        if g.get('verb_form', {}).get('usage') == 'past-participle':
            if any(gid in f.get('combines_with', []) and
                    re.fullmatch(r'p\.?p\.?', f['headword'].strip(), re.IGNORECASE) for f in glosses.values()):
                raise ValueError('Reviewed standalone participle keeps its contextual meaning without a duplicate p.p. function gloss')
    participle_function_review(glosses, original)
    for ids in intervals.values():
        if len(ids) == 1:
            continue
        # Only one explicitly linked function/lexical pair may share an identical
        # source range. This is not blanket permission for duplicate glosses.
        if len(ids) != 2:
            raise ValueError('Duplicate gloss of exactly the same source positions')
        pair = [glosses[gid] for gid in ids]
        function = next((g for g in pair if g.get('kind') == 'function'), None)
        lexical = next((g for g in pair if g.get('kind') == 'lexical'), None)
        if function is None or lexical is None or lexical['id'] not in function['combines_with']:
            raise ValueError('Duplicate source positions need an explicitly linked function/lexical pair')
        if pair[0].get('kind') != 'function':
            raise ValueError('At the same source position, function gloss must precede lexical gloss')

    reading_rules(sentence, glosses, required=require_reading_checks)

    country_ids = us_country_gloss_ids(original, glosses)
    repeat_country_ids = country_ids | set(earlier_us_country_gloss_ids)
    expected = [(m.start(), m.end()) for m in WORDS.finditer(original)]
    coverage = sentence.get('lexical_coverage')
    if not isinstance(coverage, list) or [tuple(x['span']) for x in coverage] != expected:
        raise ValueError('Lexical coverage must account for each English word occurrence in order')
    for item in coverage:
        a, b = span(item['span'], original)
        surface = original[a:b]
        token = surface.lower()
        gid = item.get('gloss_id')
        lexical_targets = {target_id for g in glosses.values() for target_id in g.get('combines_with', [])
                           if any(x <= a and b <= y for x, y in glosses[target_id]['spans'])}
        if len(lexical_targets) > 1:
            raise ValueError('Word occurrence has ambiguous linked lexical glosses')
        if lexical_targets and gid not in lexical_targets:
            raise ValueError('Combined word lexical coverage must point to its lexical gloss, not its function')
        if gid is not None:
            if gid not in glosses:
                raise ValueError('Lexical coverage points to an unknown gloss')
            g = glosses[gid]
            if not any(x <= a and b <= y for x, y in g['spans']):
                raise ValueError('Gloss does not cover the claimed word occurrence')
            if token in PRONOUNS and not (surface == 'US' and gid in country_ids):
                text(g.get('referent_ko'), 'Mandatory pronoun referent')
            if item.get('exemption') is not None:
                raise ValueError('Covered words cannot also be exempted')
        else:
            exemption = item.get('exemption')
            country_repeat = (surface == 'US' and exemption == 'proper-name-repeat'
                              and item.get('first_gloss_id') in repeat_country_ids)
            if exemption not in EXEMPTIONS or (token in PRONOUNS and not country_repeat):
                raise ValueError('Missing required gloss or unsupported exemption')
            text(item.get('reason'), 'Lexical exemption reason')
            if exemption == 'standalone-you' and token != 'you':
                raise ValueError('you exception applied to another word')
            if require_reading_checks and token == 'you' and exemption != 'standalone-you':
                raise ValueError('Uncovered you requires the explicit standalone-you exemption, not a word-level claim')
            if exemption == 'standalone-and-but' and token not in {'and', 'but'}:
                raise ValueError('and/but exception applied to another word')
            if exemption == 'below-middle1-unneeded' and item.get('level') != 'below-middle1':
                raise ValueError('Middle1-and-above words cannot use a basic-word exemption')
            if exemption == 'proper-name-repeat':
                text(item.get('first_gloss_id'), 'Proper name first occurrence link')
    hints = sentence.get('hints', [])
    if not isinstance(hints, list) or len(hints) > 2:
        raise ValueError('At most two structure hints per sentence')
    seen = []
    combination_seen = False
    for h in hints:
        pairs = display_pairs(h, required=require_reading_checks,
                              require_alignment=require_reading_checks)
        a, b = span(h.get('span'), original)
        text(h.get('meaning_ko'), 'Hint meaning')
        text(h.get('explanation'), 'Hint structural explanation')
        participle_focus_review(h, pairs, glosses, original)
        if h.get('display_mode') == 'split-phrasal-verb':
            split_phrasal_display_ranges(h, original)
        if h.get('display_mode') == 'omitted-relative':
            omitted_relative_display_range(h, original)
        if h.get('display_mode') == 'omitted-conjunction':
            omitted_conjunction_display_range(h, original)
        if h.get('category') == 'paired-structure':
            selected = [span(s, original) for s in h['display_spans']]
            if any(not a <= x < y <= b for x, y in selected):
                raise ValueError('Paired-structure display_spans must lie inside the hint span')
            expected = ' … '.join(original[x:y] for x, y in selected)
            if pairs[0]['en'] not in {expected, expected + ' …'}:
                raise ValueError('Paired-structure English must match its original fragments joined by spaced ellipses')
        if h.get('category') == 'function-combination':
            combination_seen = True
            ids = h.get('gloss_ids')
            minimum = 1 if h.get('display_mode') == 'verb-function' else 2
            if (not isinstance(ids, list) or len(ids) < minimum or
                    any(not isinstance(gid, str) for gid in ids) or len(set(ids)) != len(ids)):
                raise ValueError('Combination hint needs distinct function and lexical gloss IDs')
            linked = [glosses.get(gid) for gid in ids]
            if any(g is None for g in linked):
                raise ValueError('Combination hint points to an unknown gloss')
            functions = [g for g in linked if g.get('kind') == 'function']
            lexical = [g for g in linked if g.get('kind') == 'lexical']
            combined = [g for g in lexical if 'verb_phrase' in g]
            if h.get('display_mode') == 'verb-function' and combined:
                if len(linked) != 1 or len(combined) != 1:
                    raise ValueError('Combined passive/perfect hint must reference its one expression gloss without duplicate function/lexical entries')
            elif not functions or not lexical or any(g.get('kind') not in {'function', 'lexical'} for g in linked):
                raise ValueError('Combination hint must connect function and lexical glosses')
            if any(not any(l['id'] in f['combines_with'] for l in lexical) for f in functions):
                raise ValueError('Combination hint glosses lack an explicit combination link')
            if not combined and any(not any(l['id'] in f['combines_with'] for f in functions) for l in lexical):
                raise ValueError('Combination hint contains an unrelated lexical gloss')
            if any(not (a <= x < y <= b) for g in linked for x, y in g['spans']):
                raise ValueError('Combination hint must cover its linked original gloss spans')
            if h.get('display_mode') == 'modal-perfect-verb':
                start, end = span(h.get('display_span'), original)
                if not a <= start < end <= b:
                    raise ValueError('Modal-perfect display_span must lie inside the hint span')
                if pairs[0]['en'] != original[start:end]:
                    raise ValueError('Modal-perfect display must match its exact original verb phrase')
                if not any(MODAL_PERFECT_FORM.fullmatch(g['headword'].strip()) for g in functions):
                    raise ValueError('Modal-perfect display needs a linked modal-perfect function gloss')
                verb = MODAL_PERFECT_VERB.fullmatch(pairs[0]['en'])
                verb_start = start + verb.start('participle')
                if not any(x <= verb_start < end <= y for g in lexical for x, y in g['spans']):
                    raise ValueError('Modal-perfect display participle must come from a linked lexical gloss')
            elif h.get('display_mode') == 'verb-function':
                start, end = span(h.get('display_span'), original)
                if not a <= start < end <= b or pairs[0]['en'] != original[start:end]:
                    raise ValueError('Verb-function display must match its exact original verb phrase within the hint span')
                if combined:
                    review = combined[0]['verb_phrase']
                    if (h['formula_label'] != review['formula_label'] or
                            start != review['source_spans'][0][0] or end != review['verb_span'][1]):
                        raise ValueError('Verb-function display/formula must match its reviewed expression and end before objects')
                else:
                    if start != min(x for g in linked for x, y in g['spans']):
                        raise ValueError('Verb-function display must start at its linked function')
                    if not any(start <= x < end == y for g in lexical for x, y in g['spans']):
                        raise ValueError('Verb-function display must end at a linked lexical verb, before objects')
                    lexical_step_review(h, lexical, functions, original)
        elif combination_seen:
            raise ValueError('Function-combination hints must follow higher-priority hints')
        if any((x <= a and b <= y) or (a <= x and y <= b) for x, y in seen):
            raise ValueError('Contained structure hints must be combined')
        seen.append((a, b))
    relative_hint_coverage(sentence, glosses)
    return glosses


def check(data, scope='full'):
    if scope not in {'learning', 'full'}:
        raise ValueError('Unknown learning-content check scope')
    if data.get('schema_version') != 1:
        raise ValueError('Unsupported manuscript schema version')
    revision = data.get('rule_revision')
    if revision is not None and revision != READING_RULE_REVISION:
        raise ValueError('Unsupported rule revision')
    require_reading_checks = revision == READING_RULE_REVISION
    meta = data.get('metadata', {})
    syntax_version = training_version(data)
    for name in ['book_name', 'course', 'publisher_author', 'lesson']:
        text(meta.get(name), f'metadata/{name}')
    display_book_name(meta)
    identity = lesson_identity(meta, data.get('cover'))
    sources = records(data.get('sources'), 'sources')
    if not sources:
        raise ValueError('No authoritative source transcription')
    source_sentences, source_order, preceding_sentence = {}, [], {}
    for source_id, source in sources.items():
        text(source_id, 'source ID')
        display_source_label(source)
        prov = source.get('provenance', {})
        for name in ['filename', 'location', 'verification_record']:
            text(prov.get(name), f'provenance/{name}')
        if not re.fullmatch('[0-9a-f]{64}', prov.get('sha256', '')):
            raise ValueError('Source artifact SHA-256 required')
        bounds = source.get('sentences')
        if not isinstance(bounds, list) or not bounds:
            raise ValueError('No verified source sentence boundaries')
        excerpt(source, {'source_id': source_id, 'first_sentence': bounds[0]['id'],
                         'last_sentence': bounds[-1]['id']})
        previous = None
        for s in bounds:
            key = (source_id, s['id'])
            source_sentences[key] = source['text'][s['start']:s['end']]
            source_order.append(key)
            preceding_sentence[key] = previous
            previous = key
    paragraphs = data.get('paragraphs')
    grouping = group_units(paragraphs, data.get('grouping_resolutions'))
    source_checks = [check_source_structure(source, paragraphs) for source in sources.values()]
    source_issues = [issue for report in source_checks for issue in report['issues']]
    if source_issues:
        return {'status': 'NEEDS_SOURCE_REVIEW', 'scope': scope, 'source_issues': source_issues,
                'grouping': grouping, 'lesson_identity': identity}
    if grouping['status'] != 'READY':
        return {'status': 'NEEDS_SOURCE_REVIEW', 'grouping': grouping}
    paragraph_order = [(p['source_id'], sid) for p in paragraphs for sid in p['sentence_ids']]
    if paragraph_order != source_order:
        raise ValueError('Paragraphs omit, duplicate, or reorder original sentences')
    units = data.get('units')
    unit_map = records(units, 'units')
    if len(units) != len(grouping['units']):
        raise ValueError('Common learning-unit count differs from the grouping decision')
    for actual, expected in zip(units, grouping['units']):
        text(actual.get('id'), 'unit ID')
        for key in ['source_id', 'paragraph_ids', 'sentence_ids']:
            if actual.get(key) != expected[key]:
                raise ValueError(f'{actual["id"]}: common grouping differs at {key}')
    annotations = records(data.get('sentences'), 'sentences', lambda r: (r['source_id'], r['id']))
    if list(annotations) != source_order:
        raise ValueError('Annotation sentence coverage/order differs from source')
    for key, s in annotations.items():
        if s.get('text') != source_sentences[key]:
            raise ValueError(f'{key}: annotated text differs from authoritative transcription')
        if type(s.get('key')) is not bool:
            raise ValueError('Explicit key-sentence boolean required')
        if 'sv_review' in s:
            review = s['sv_review']
            # Rendering validates the explicit empty clauses, review record and
            # self hash. The source order, not an annotation ID lookup alone,
            # establishes the immediately preceding same-source context.
            if review is None:
                raise ValueError('sv_review must be an explicit review record')
            render_sv(s['text'], s.get('clauses'), review)
            previous = preceding_sentence[key]
            if previous is None or previous != (key[0], review['context_sentence_id']):
                raise ValueError(f'{key}: sv_review context must be the immediately preceding same-source sentence')
            context_hash = hashlib.sha256(source_sentences[previous].encode('utf-8')).hexdigest()
            if review['context_text_sha256'] != context_hash:
                raise ValueError(f'{key}: sv_review context_text_sha256 differs from authoritative context')
    analysis = build_analysis_bodies({'sentences': list(annotations.values()), 'units': units})
    rendered_sv, all_glosses, proper_repeat_links, shortages = {}, {}, [], []
    syntax_reports = []
    earlier_us_country_ids = set()
    for uid, unit in unit_map.items():
        sid = unit['source_id']
        today = records(unit.get('today_words'), f'{uid}/today_words')
        if len(today) > 8:
            raise ValueError('At most eight confirmed today words per common unit')
        for row in today.values():
            text(row.get('text'), 'Today-word source form')
            text(row.get('meaning_ko'), 'Today-word meaning')
        unit_glosses = {}
        for sent_id in unit['sentence_ids']:
            s = annotations[(sid, sent_id)]
            rendered_sv[f'{sid}/{sent_id}'] = render_sv(s['text'], s.get('clauses'), s.get('sv_review'))
            gs = glossary(s, today, require_reading_checks=require_reading_checks,
                          earlier_us_country_gloss_ids=earlier_us_country_ids)
            for gid, gloss in gs.items():
                if gid in all_glosses:
                    raise ValueError('Gloss IDs must be globally unique')
                all_glosses[gid] = (sid, sent_id, gloss)
                unit_glosses[gid] = gloss
            earlier_us_country_ids.update(us_country_gloss_ids(s['text'], gs))
            for c in s['lexical_coverage']:
                if c.get('exemption') == 'proper-name-repeat':
                    first = all_glosses.get(c['first_gloss_id'])
                    if first is None or first[0] != sid:
                        raise ValueError('Proper-name repeat needs an earlier gloss in the same independent source')
                    earlier_text = annotations[(first[0], first[1])]['text']
                    earlier_index = source_order.index((first[0], first[1]))
                    current_index = source_order.index((sid, sent_id))
                    if earlier_index > current_index or (earlier_index == current_index and
                            first[2]['spans'][0][0] >= c['span'][0]):
                        raise ValueError('Proper-name first occurrence must precede this occurrence')
                    earlier_words = {proper_name_identity(w.group()) for x, y in first[2]['spans']
                                     for w in WORDS.finditer(earlier_text[x:y])}
                    if proper_name_identity(s['text'][c['span'][0]:c['span'][1]]) not in earlier_words:
                        raise ValueError('Proper-name repetition link refers to a different original name')
                    proper_repeat_links.append(c['first_gloss_id'])
        for tid, row in today.items():
            linked = [g for g in unit_glosses.values() if g.get('today_word_id') == tid]
            if not linked:
                raise ValueError('Today word has no starred gloss in its common unit')
            origin = row.get('source_gloss_id')
            if origin not in unit_glosses or unit_glosses[origin].get('today_word_id') != tid:
                raise ValueError('Today-word source gloss missing or linked to a different word')
        a = unit.get('analysis', {})
        for field in ['title_or_topic_en', 'title_or_topic_ko', 'intent_ko']:
            text(a.get(field), f'{uid}/{field}')
        if a.get('heading_kind') not in {'제목', '주제'}:
            raise ValueError('Select exactly one title or topic')
        flow = a.get('flow')
        if not isinstance(flow, list) or not flow:
            raise ValueError('Analysis flow is required')
        if [x for row in flow for x in row['sentence_ids']] != unit['sentence_ids']:
            raise ValueError('Analysis flow does not cover every unit sentence exactly once in order')
        for row in flow:
            text(row.get('text_ko'), 'Flow description')
            if 'label' in row:
                text(row['label'], 'Flow stage label')
        easy = a.get('easy_explanations', [])
        if len({r['sentence_id'] for r in easy}) != len(easy):
            raise ValueError('Duplicate easy-explanation sentence')
        for row in easy:
            if row['sentence_id'] not in unit['sentence_ids']:
                raise ValueError('Easy explanation borrows a sentence from another unit')
            lines = row.get('explanatory_sentences')
            if not isinstance(lines, list) or not lines:
                raise ValueError('Each easy explanation needs a nonempty explanatory-sentence list')
            for line in lines:
                text(line, 'Easy explanation')
        selected_ids = [row['sentence_id'] for row in easy]
        if selected_ids != [sent_id for sent_id in unit['sentence_ids'] if sent_id in selected_ids]:
            raise ValueError('Easy explanations must follow original sentence order')
        grammar = a.get('grammar_points', [])
        for row in grammar:
            if row.get('sentence_id') not in unit['sentence_ids']:
                raise ValueError('Grammar evidence is outside its unit')
            original = annotations[(sid, row['sentence_id'])]['text']
            span(row.get('span'), original)
            text(row.get('title'), 'Grammar title')
            text(row.get('explanation'), 'Grammar explanation')
        syntax_report = check_syntax_unit(
            unit, [annotations[(sid, sent_id)] for sent_id in unit['sentence_ids']],
            syntax_version, scope)
        syntax_reports.append(syntax_report)
        relations = a.get('relations', [])
        terms = {}
        for row in relations:
            for field in ['head', 'synonym', 'antonym']:
                term = row.get(field, {})
                tid = text(term.get('id'), 'Relation term ID')
                text(term.get('text'), 'Relation term text')
                text(term.get('meaning_ko'), 'Relation term meaning')
                if tid in terms:
                    raise ValueError('Relation term IDs must be unique within a unit')
                terms[tid] = term
        keys = [x for x in unit['sentence_ids'] if annotations[(sid, x)]['key']]
        if scope == 'full':
            wb = unit.get('workbook', {})
            shuffled = wb.get('relation_order')
            if not isinstance(shuffled, list) or Counter(shuffled) != Counter(terms.keys()):
                raise ValueError('Workbook relation activity differs from confirmed analysis terms')
            if len(terms) > 1 and shuffled == list(terms):
                raise ValueError('Workbook relation terms remain in the grouped analysis order')
            if wb.get('key_sentence_ids') != keys:
                raise ValueError('Workbook key sentences differ from the reading/analysis selection')
            text(wb.get('question_id'), 'Workbook practical question link')
        actual_counts = {'key_sentences': len(keys), 'easy_explanations': len(easy),
                         'grammar_points': syntax_report['base_grammar_point_count'], 'relations': len(relations)}
        if len(keys) != min(2, len(unit['sentence_ids'])) or len(easy) != min(3, len(unit['sentence_ids'])):
            raise ValueError('Existing distinct source sentences cannot be omitted as a quantity shortage')
        expected_counts = {'key_sentences': 2, 'easy_explanations': 3, 'grammar_points': 3, 'relations': 3}
        exceptions = records(unit.get('quantity_exceptions', []), 'quantity exceptions', lambda r: r['field'])
        for field, actual in actual_counts.items():
            expected = expected_counts[field]
            if actual > expected:
                raise ValueError(f'{uid}/{field}: exceeds the confirmed default')
            if actual < expected:
                exc = exceptions.pop(field, None)
                if not exc or exc.get('actual') != actual or exc.get('expected') != expected:
                    raise ValueError(f'{uid}/{field}: record actual source shortage and counts')
                text(exc.get('reason'), 'Source-shortage reason')
                text(exc.get('reported_to_user'), 'Actual shortage report reference')
                shortages.append({'unit_id': uid, **exc})
        if exceptions:
            raise ValueError('Unused or unknown quantity exception')
    undeclared_relatives = [f'{sid}/{sent_id}' for (sid, sent_id), s in annotations.items()
                           if 'relative_gloss_ids' not in (s.get('reading_checks') or {})]
    relative_declarations = {
        'status': ('DECLARED_LOCATIONS_CHECKED' if not undeclared_relatives else
                   'UNDECLARED_LEGACY_INPUT' if len(undeclared_relatives) == len(annotations) else
                   'PARTIALLY_DECLARED'),
        'declared_sentence_count': len(annotations) - len(undeclared_relatives),
        'undeclared_sentences': undeclared_relatives,
        'scope': 'REVIEWER_DECLARED_LOCATIONS_ONLY_NOT_GRAMMAR_INFERENCE',
    }
    form_reviews = [g for s in annotations.values() for g in s['glosses'] if 'verb_form' in g]
    phrase_reviews = [g for s in annotations.values() for g in s['glosses'] if 'verb_phrase' in g]
    return {'status': 'STRUCTURE_PASS', 'scope': scope, 'lesson_identity': identity,
            'source_checks': source_checks, 'source_count': len(sources), 'unit_count': len(units),
            'sentence_count': len(annotations), 'gloss_count': len(all_glosses),
            'shortages': shortages, 'sv_lines': rendered_sv, 'analysis_bodies': analysis,
            'source_artifact_bytes': 'NOT_CHECKED_BY_THIS_TOOL',
            'lexical_level_and_exemptions': 'REVIEWER_SUPPLIED_NOT_AUTOMATICALLY_VERIFIED',
            'all_repeated_today_word_occurrences': 'REQUIRES_SEMANTIC_REVIEW',
            'verb_form_declarations': {'form_count': len(form_reviews), 'phrase_count': len(phrase_reviews),
                'status': 'DECLARED_LOCATIONS_CHECKED' if form_reviews or phrase_reviews else 'UNDECLARED_LEGACY_INPUT',
                'scope': 'REVIEWER_DECLARED_LOCATIONS_ONLY_NOT_GRAMMAR_OR_MEANING_INFERENCE'},
            'reading_rule_declarations': 'SUPPLIED_CONSTRAINTS_ONLY_NOT_GRAMMAR_INFERENCE',
            'reading_revision_audit': 'DECLARATIONS_REQUIRED' if require_reading_checks else 'NOT_REQUESTED_LEGACY_INPUT',
            'relative_hint_declarations': relative_declarations,
            'syntax_training': {'version': syntax_version,
                'status': 'DECLARED_LINKS_CHECKED' if syntax_version == 1 else 'UNDECLARED_LEGACY_INPUT',
                'units': syntax_reports, 'semantic_review': 'NOT_PERFORMED'},
            'semantic_review': 'NOT_PERFORMED', 'visual_review': 'NOT_PERFORMED'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('input', type=Path)
    p.add_argument('report', type=Path)
    p.add_argument('--scope', choices=['learning', 'full'], default='full')
    args = p.parse_args()
    if args.input.resolve() == args.report.resolve():
        raise ValueError('Report cannot overwrite manuscript')
    raw = args.input.read_bytes()
    try:
        result = check(json.loads(raw.decode('utf-8-sig')), scope=args.scope)
    except (ValueError, TypeError, KeyError, AttributeError) as exc:
        result = {'status': 'FAIL', 'error': str(exc)}
    result['input_sha256'] = hashlib.sha256(raw).hexdigest()
    args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k not in {'sv_lines', 'analysis_bodies'}}, ensure_ascii=False))
    return 0 if result['status'] == 'STRUCTURE_PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
