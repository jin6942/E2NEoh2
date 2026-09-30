"""Check declared analysis/practice routes without parsing English grammar.

Version 1 keeps the three base grammar points and links each actual declared
passive/perfect formula to a selected hint or a representative analysis point.
Meaning, formula selection and the educational adequacy of support are reviewed
by people; these checks prove source positions, IDs, coverage and counts only.
"""
import re

from question_source import span
from structure_hints import VERB_FUNCTION_FORMULA


def _text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'Syntax training {label}: nonempty text required')
    return value


def canonical_formula_key(value):
    """Normalize writing, never merge tense, voice, modal or negative forms."""
    value = ' '.join(_text(value, 'formula key').casefold().split())
    return re.sub(r'(?<!\w)p\.?p\.?(?!\w)', 'p.p.', value)


def authored_formula_kind(headword):
    """Classify only the already-authored formula, never original sentences."""
    if not isinstance(headword, str) or not VERB_FUNCTION_FORMULA.fullmatch(headword.strip()):
        return None
    if not re.search(r'\s+p\.?p\.?$', headword.strip(), re.IGNORECASE):
        return None
    prefix = re.sub(r'\s+p\.?p\.?$', '', headword.strip(), flags=re.IGNORECASE)
    auxiliaries = [part.casefold() for part in prefix.split() if part.casefold() != 'not']
    if auxiliaries and auxiliaries[-1] in {'be', 'am', 'is', 'are', 'was', 'were', 'been', 'being'}:
        return 'passive'
    if auxiliaries and auxiliaries[-1] in {'have', 'has', 'had'}:
        return 'active-perfect'
    return None


def training_version(data):
    value = data.get('metadata', {}).get('syntax_training_version')
    declared = False
    for unit in data.get('units', []):
        analysis = unit.get('analysis', {})
        declared |= 'formula_routes' in analysis or 'syntax_point_ids' in unit.get('workbook', {})
        declared |= any(any(field in point for field in ('formula_key', 'practice', 'supplemental'))
                        for point in analysis.get('grammar_points', []))
    if value is None:
        if declared:
            raise ValueError('Syntax training partial contract: metadata.syntax_training_version=1 is required')
        return None
    if type(value) is not int or value != 1:
        raise ValueError('Unsupported syntax_training_version; expected integer 1')
    return value


def _source_span(value, original, label):
    a, b = span(value, original)
    selected = original[a:b]
    if selected != selected.strip():
        raise ValueError(f'Syntax training {label}: edge whitespace is not part of the selected span')
    for edge in (a, b):
        if (0 < edge < len(original)
                and re.fullmatch(r"[\w'’\-]", original[edge - 1])
                and re.fullmatch(r"[\w'’\-]", original[edge])):
            raise ValueError(f'Syntax training {label}: preserve source word boundaries')
    return a, b


def _glosses(sentence):
    rows = sentence.get('glosses', [])
    result = {}
    for gloss in rows:
        gid = _text(gloss.get('id'), 'gloss ID')
        if gid in result:
            raise ValueError('Syntax training duplicate gloss ID')
        result[gid] = gloss
    return result


def function_candidates(sentences):
    """Expose linked passive/perfect formula declarations for authoring tools."""
    result = {}
    for sentence in sentences:
        glosses = _glosses(sentence)
        for gid, gloss in glosses.items():
            kind = authored_formula_kind(gloss.get('headword'))
            if gloss.get('kind') != 'function' or kind is None:
                continue
            links = gloss.get('combines_with', [])
            if (not isinstance(links, list) or not links
                    or any(not isinstance(link, str) or link not in glosses
                           or glosses[link].get('kind', 'lexical') == 'function' for link in links)):
                raise ValueError('Syntax training formula requires actual linked lexical glosses')
            key = (sentence['id'], gid)
            if key in result:
                raise ValueError('Syntax training duplicate formula occurrence')
            result[key] = {'sentence': sentence, 'function': gloss, 'kind': kind,
                           'formula_key': canonical_formula_key(gloss['headword'])}
    return result


def _matching_hints(candidate):
    return [index for index, hint in enumerate(candidate['sentence'].get('hints', []))
            if hint.get('category') == 'function-combination'
            and candidate['function']['id'] in hint.get('gloss_ids', [])]


def _point_evidence(point, candidates):
    """Find the representative's own declared formula and lexical support."""
    a, b = point['practice']['span']
    supports = point['practice']['support_gloss_ids']
    key = canonical_formula_key(point['formula_key'])
    return [candidate for (sid, _), candidate in candidates.items()
            if sid == point['sentence_id'] and candidate['formula_key'] == key
            and all(a <= x < y <= b for x, y in candidate['function']['spans'])
            and any(gid in supports for gid in candidate['function']['combines_with'])]


def check_unit(unit, sentences, version, scope='full'):
    """Return a unit summary; never mutate the manuscript or certify meaning."""
    if scope not in {'learning', 'full'}:
        raise ValueError('Unknown syntax training check scope')
    points = unit.get('analysis', {}).get('grammar_points', [])
    if version is None:
        return {'unit_id': unit['id'], 'status': 'UNDECLARED_LEGACY_INPUT',
                'base_grammar_point_count': len(points), 'supplemental_count': 0}
    if type(version) is not int or version != 1:
        raise ValueError('Unsupported syntax training version')
    by_sentence = {sentence['id']: sentence for sentence in sentences}
    if set(by_sentence) != set(unit['sentence_ids']) or len(by_sentence) != len(sentences):
        raise ValueError('Syntax training sentence membership differs from the common unit')
    by_id, supplements = {}, []
    for point in points:
        pid = _text(point.get('id'), 'grammar point ID')
        if pid in by_id:
            raise ValueError('Syntax training grammar point IDs must be unique within the unit')
        by_id[pid] = point
        key = canonical_formula_key(point.get('formula_key'))
        if point.get('sentence_id') not in by_sentence:
            raise ValueError('Syntax training grammar point is outside its unit')
        sentence = by_sentence[point['sentence_id']]
        original = sentence['text']
        outer_a, outer_b = span(point.get('span'), original)
        practice = point.get('practice')
        if not isinstance(practice, dict):
            raise ValueError('Syntax training every grammar point requires practice')
        a, b = _source_span(practice.get('span'), original, 'practice')
        if not outer_a <= a < b <= outer_b:
            raise ValueError('Syntax training practice must lie inside the grammar evidence span')
        formula = practice.get('formula_support')
        if not isinstance(formula, dict):
            raise ValueError('Syntax training practice needs explicit formula_support en/ko')
        if canonical_formula_key(formula.get('en')) != key:
            raise ValueError('Syntax training formula_support must use the grammar point formula_key')
        _text(formula.get('ko'), 'formula-support meaning')
        _text(practice.get('answer_ko'), 'practice answer')
        support_ids = practice.get('support_gloss_ids')
        if (not isinstance(support_ids, list) or not support_ids
                or any(not isinstance(gid, str) or not gid for gid in support_ids)
                or len(set(support_ids)) != len(support_ids)):
            raise ValueError('Syntax training practice needs unique support_gloss_ids including lexical support')
        glosses = _glosses(sentence)
        overrides = practice.get('support_overrides', [])
        if not isinstance(overrides, list):
            raise ValueError('Syntax training support_overrides must be a list')
        by_override = {}
        for override in overrides:
            if not isinstance(override, dict):
                raise ValueError('Syntax training invalid support override')
            gid = override.get('gloss_id')
            if not isinstance(gid, str) or gid not in support_ids or gid in by_override:
                raise ValueError('Syntax training override must name one unique selected support gloss')
            gloss = glosses.get(gid)
            if gloss is None or gloss.get('kind', 'lexical') == 'function':
                raise ValueError('Syntax training override must reference an actual lexical support')
            if 'source_span' in override:
                oa, ob = _source_span(override['source_span'], original, 'support override')
                if (not a <= oa < ob <= b
                        or not any(x <= oa < ob <= y for x, y in gloss.get('spans', []))):
                    raise ValueError('Syntax training override source span must lie inside practice and its original gloss')
                if override.get('form') != original[oa:ob]:
                    raise ValueError('Syntax training source override must preserve the exact actual form')
            else:
                construction = gloss.get('verb_construction')
                if not isinstance(construction, dict):
                    raise ValueError('Syntax training override needs a reviewed verb_construction or explicit source_span')
                lemma = gloss.get('verb_form', {}).get('lemma') or construction.get('lemma')
                if override.get('form') != lemma or not isinstance(lemma, str) or not lemma.strip():
                    raise ValueError('Syntax training override form must preserve the reviewed verb lemma')
            _text(override.get('meaning_ko'), 'override basic lexical meaning')
            _text(override.get('review_record'), 'override review_record')
            by_override[gid] = override
        lexical_count = 0
        for gid in support_ids:
            gloss = glosses.get(gid)
            if gloss is None:
                raise ValueError('Syntax training support must be an actual gloss from the same sentence')
            if gloss.get('kind', 'lexical') != 'function':
                lexical_count += 1
            support_head = by_override[gid]['form'] if gid in by_override else gloss.get('headword')
            if canonical_formula_key(support_head) == key:
                raise ValueError('Syntax training support must not repeat the main formula_support')
            _text(gloss.get('meaning_ko'), 'support meaning')
            support_spans = ([by_override[gid]['source_span']]
                             if gid in by_override and 'source_span' in by_override[gid]
                             else gloss.get('spans', []))
            if not any(a <= x < y <= b for x, y in support_spans):
                raise ValueError('Syntax training support is outside the actual practice span')
        if not lexical_count:
            raise ValueError('Syntax training needs at least one lexical support in addition to any ancillary functions')
        if 'supplemental' in point:
            supplemental = point['supplemental']
            if not isinstance(supplemental, dict):
                raise ValueError('Syntax training supplemental must link its source function')
            _text(supplemental.get('function_gloss_id'), 'supplemental function gloss ID')
            _text(supplemental.get('reason'), 'supplemental reason')
            supplements.append(point)
    candidates = function_candidates(sentences)
    for point in supplements:
        key = canonical_formula_key(point['formula_key'])
        if sum(canonical_formula_key(row['formula_key']) == key for row in points) != 1:
            raise ValueError('Syntax training do not repeat a formula in supplemental analysis')
        own = (point['sentence_id'], point['supplemental']['function_gloss_id'])
        if own not in candidates or candidates[own] not in _point_evidence(point, candidates):
            raise ValueError('Syntax training supplemental must use its own actual function and linked lexical support')
    routes = unit.get('analysis', {}).get('formula_routes')
    if not isinstance(routes, list):
        raise ValueError('Syntax training requires explicit analysis.formula_routes, including an empty list')
    seen, used_supplements = set(), set()
    for route in routes:
        if not isinstance(route, dict):
            raise ValueError('Syntax training invalid formula route')
        occurrence = (route.get('sentence_id'), route.get('function_gloss_id'))
        if occurrence not in candidates or occurrence in seen:
            raise ValueError('Syntax training formula route is duplicate or not an actual unit occurrence')
        seen.add(occurrence)
        candidate = candidates[occurrence]
        if canonical_formula_key(route.get('formula_key')) != candidate['formula_key']:
            raise ValueError('Syntax training route formula differs from its actual function gloss')
        _text(route.get('review_record'), 'route review_record')
        common_fields = {'sentence_id', 'function_gloss_id', 'formula_key', 'route', 'review_record'}
        fields_by_route = {
            'hint': {'hint_index'},
            'analysis': {'grammar_point_id'},
            'approved-exception': {'exception_kind', 'grammar_point_id', 'replacement_grammar_point_id',
                                   'approval_reference', 'partial_negation_span'},
        }
        if (route.get('route') not in fields_by_route
                or set(route) - common_fields - fields_by_route[route['route']]):
            raise ValueError('Syntax training formula route contains unknown or inapplicable fields')
        hint_indices = _matching_hints(candidate)
        if route.get('route') == 'hint':
            index = route.get('hint_index')
            if type(index) is not int or index not in hint_indices or 'grammar_point_id' in route:
                raise ValueError('Syntax training hint route must select the same sentence function-combination hint')
        elif route.get('route') == 'analysis':
            if hint_indices:
                raise ValueError('Syntax training selected function hint must be routed as hint')
            point = by_id.get(route.get('grammar_point_id'))
            if ('hint_index' in route or point is None
                    or canonical_formula_key(point['formula_key']) != candidate['formula_key']
                    or not _point_evidence(point, candidates)):
                raise ValueError('Syntax training analysis route needs a same-unit representative of the same actual formula')
            if 'supplemental' in point and occurrence == (
                    point['sentence_id'], point['supplemental']['function_gloss_id']):
                used_supplements.add(point['id'])
        elif route['route'] == 'approved-exception':
            if route.get('exception_kind') != 'partial-negation':
                raise ValueError('Syntax training only the approved partial-negation exception is supported')
            _text(route.get('approval_reference'), 'actual user approval_reference')
            if (candidate['kind'] != 'passive'
                    or 'not' not in candidate['formula_key'].split() or hint_indices):
                raise ValueError('Syntax training partial-negation exception requires an unselected negative passive formula')
            own = by_id.get(route.get('grammar_point_id'))
            replacement = by_id.get(route.get('replacement_grammar_point_id'))
            if (own is None or own['sentence_id'] != occurrence[0]
                    or replacement is None or replacement['sentence_id'] == occurrence[0]):
                raise ValueError('Syntax training exception needs its own point and a different-sentence replacement in this unit')
            original = candidate['sentence']['text']
            pa, pb = _source_span(route.get('partial_negation_span'), original, 'partial-negation evidence')
            a, b = own['practice']['span']
            if (not a <= pa < pb <= b
                    or not all(pa <= x < y <= pb for x, y in candidate['function']['spans'])):
                raise ValueError('Syntax training partial-negation evidence must cover the source function within its own practice')
            # The record declares the partial-negation reading. Position and
            # formula checks do not prove that this semantic judgment is true.
            replacements = _point_evidence(replacement, candidates)
            if not any(row['kind'] == 'passive' and re.fullmatch(
                    r'(?:be|am|is|are|was|were) p\.p\.', row['formula_key'])
                    for row in replacements):
                raise ValueError('Syntax training replacement must practice an actual positive simple passive formula')
            if 'supplemental' in replacement:
                used_supplements.add(replacement['id'])
        else:
            raise ValueError('Syntax training unsupported formula route')
    if seen != set(candidates):
        raise ValueError('Syntax training every declared supported function needs exactly one route')
    if used_supplements != {point['id'] for point in supplements}:
        raise ValueError('Syntax training supplemental point must be used by its own analysis route or an approved replacement exception')
    if scope == 'full' and unit.get('workbook', {}).get('syntax_point_ids') != list(by_id):
        raise ValueError('Syntax training workbook must practice every grammar point exactly once in analysis order')
    return {'unit_id': unit['id'], 'status': 'DECLARED_LINKS_CHECKED',
            'base_grammar_point_count': len(points) - len(supplements),
            'supplemental_count': len(supplements), 'formula_occurrence_count': len(candidates),
            'practice_count': len(points), 'workbook_links': 'CHECKED' if scope == 'full' else 'NOT_CHECKED_LEARNING_SCOPE',
            'semantic_review': 'NOT_PERFORMED'}
