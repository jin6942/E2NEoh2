"""Validate and expose student-facing bilingual structure-hint pairs.

The hint's span, meaning_ko and explanation remain review evidence. They are not
a fallback display: current output requires deliberately authored display_pairs.
This checks shape and matching brackets, not translation or grammatical truth.
"""
import re


MODAL_FORM = re.compile(
    r"(?:(?:may|might|must|should|could|would|can|will|shall|need)(?:\s+not)?"
    r"|cannot|(?:ca|could|must|should|would|wo|need)n['’]t|ought(?:\s+not)?\s+to)",
    re.IGNORECASE,
)
PERFECT_FORM = re.compile(r'have\s+p\.?p\.?', re.IGNORECASE)
MODAL_PERFECT_FORM = re.compile(MODAL_FORM.pattern + r'\s+have\s+p\.?p\.?', re.IGNORECASE)
MODAL_PERFECT_VERB = re.compile(
    MODAL_FORM.pattern + r'\s+have\s+(?P<participle>[A-Za-z][A-Za-z’-]*)', re.IGNORECASE)
OMITTED_RELATIVES = {'that', 'which', 'who', 'whom', 'when', 'where', 'why'}
PARENTHETICAL_RELATIVE = re.compile(r'\(\s*(?:that|which|who|whom|when|where|why)\s*\)', re.IGNORECASE)
VERB_CONSTRUCTION_EMPHASIS = 'ko-only-verb-construction'
VERB_FUNCTION_FORMULA = re.compile(
    r'(?:(?:' + MODAL_FORM.pattern + r')\s+)?'
    r'(?:(?:be|am|is|are|was|were|being|been|have|has|had|do|does|did|not)\s+)*'
    r'(?:p\.?p\.?|V-ing|V-ed|V-s|V)', re.IGNORECASE)
OMITTED_MODES = {'omitted-relative', 'omitted-conjunction'}
REFERENCE_PRONOUNS_EN = {
    'i', 'me', 'my', 'mine', 'myself', 'you', 'your', 'yours', 'yourself', 'yourselves',
    'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself',
    'it', 'its', 'itself', 'we', 'us', 'our', 'ours', 'ourselves',
    'they', 'them', 'their', 'theirs', 'themselves', 'themself',
    'this', 'that', 'these', 'those', 'one', 'ones', 'other', 'others', 'oneself',
}
REFERENCE_PRONOUN_CONTRACTION = re.compile(
    r"['’](?:s|re|ve|ll|d|m)(?![A-Za-z0-9_'’-])", re.IGNORECASE)


def lexical_step(hint):
    """Return an authored lexical starting point, without deriving its meaning.

    This validates only the compact display shape. The learning-content checker
    proves the gloss ID, source form/lemma and meaning against the manuscript.
    Legacy verb-function displays remain readable when this field is absent.
    """
    if 'lexical_step' not in hint:
        return None
    if hint.get('display_mode') != 'verb-function' or hint.get('category') != 'function-combination':
        raise ValueError('lexical_step requires function-combination verb-function mode')
    step = hint['lexical_step']
    if not isinstance(step, dict) or set(step) != {'gloss_id', 'form', 'meaning_ko'}:
        raise ValueError('lexical_step requires gloss_id, form and meaning_ko only')
    gloss_id = step['gloss_id']
    if (not isinstance(gloss_id, str) or not gloss_id or gloss_id != gloss_id.strip() or
            len(gloss_id) > 160 or any(c.isspace() or ord(c) < 32 for c in gloss_id)):
        raise ValueError('lexical_step gloss_id requires one compact manuscript ID')
    form = step['form']
    if (not isinstance(form, str) or len(form) > 80 or
            not re.fullmatch(r"[A-Za-z]+(?:['’-][A-Za-z]+)*", form) or form in {'A', 'B', 'V'}):
        raise ValueError('lexical_step form requires one English lexical headword, not a phrase or formula')
    meaning = step['meaning_ko']
    if (not isinstance(meaning, str) or len(meaning) > 60 or
            not re.fullmatch(r'[가-힣]+(?: [가-힣]+)*', meaning)):
        raise ValueError('lexical_step meaning_ko requires a short Korean lexical meaning without commentary or punctuation')
    return step


def validate_verb_function(hint, pair):
    """Validate an authored literal verb display, not infer its tense or voice."""
    selected = hint.get('display_span')
    if (not isinstance(selected, list) or len(selected) != 2 or
            any(type(x) is not int for x in selected) or not 0 <= selected[0] < selected[1]):
        raise ValueError('Verb-function display_span requires one integer source range')
    formula = hint.get('formula_label')
    if (not isinstance(formula, str) or formula != formula.strip() or len(formula) > 60 or
            any(ord(c) < 32 for c in formula) or not VERB_FUNCTION_FORMULA.fullmatch(formula) or
            formula.casefold() in {'v', 'pp', 'p.p', 'p.p.'}):
        raise ValueError('Verb-function formula_label requires one reviewed English tense/voice formula')
    if formula in pair['ko']:
        raise ValueError('Verb-function formula belongs in formula_label, not inside the Korean meaning')
    if (not re.fullmatch(r"[A-Za-z][A-Za-z’'-]*(?: [A-Za-z][A-Za-z’'-]*)*", pair['en']) or
            any(token in {'A', 'B', 'V'} for token in pair['en'].split())):
        raise ValueError('Verb-function English must be the literal source verb phrase without formula slots or complements')
    emphasis_spans(pair, required=True)
    if not pair['emphasis_links']:
        raise ValueError('Verb-function display requires reviewed bilingual grammatical emphasis links')
    # The author links actual grammatical surfaces; irregular forms can fuse
    # lexical and grammatical information. Do not invent a morphology splitter.


def reject_split_modal_perfect(parts):
    """Keep an explicitly written modal-perfect formula together, without parsing source grammar."""
    for index, part in enumerate(parts):
        if MODAL_FORM.fullmatch(part.strip()):
            rest = parts[index + 1:]
            if rest and (PERFECT_FORM.fullmatch(rest[0].strip()) or
                         (len(rest) > 1 and PERFECT_FORM.fullmatch(' '.join(rest[:2]).strip()))):
                raise ValueError('Modal-perfect hints require the literal source verb phrase in modal-perfect-verb mode')
        match = re.fullmatch(r'(.+)\s+have', part.strip(), re.IGNORECASE)
        if (match and MODAL_FORM.fullmatch(match[1]) and index + 1 < len(parts) and
                re.fullmatch(r'p\.?p\.?', parts[index + 1].strip(), re.IGNORECASE)):
            raise ValueError('Modal-perfect hints require the literal source verb phrase in modal-perfect-verb mode')
        if MODAL_PERFECT_FORM.fullmatch(part.strip()):
            raise ValueError('Modal-perfect hints require the literal source verb phrase in modal-perfect-verb mode')


def bracket_spans(value):
    """Return nonnested, nonempty square-bracket spans, including delimiters."""
    spans, start = [], None
    for index, char in enumerate(value):
        if char == '[':
            if start is not None:
                raise ValueError('Hint display brackets must not be nested')
            start = index
        elif char == ']':
            if start is None:
                raise ValueError('Hint display brackets must be balanced')
            if not value[start + 1:index].strip():
                raise ValueError('Hint display brackets must contain a constituent')
            spans.append((start, index + 1))
            start = None
    if start is not None:
        raise ValueError('Hint display brackets must be balanced')
    return spans


def pronoun_references(pair):
    """Validate authored display references without inferring an antecedent.

    Offsets are end-exclusive in the complete display strings, including all
    brackets. A reference bracket is annotation, never a grammatical bracket.
    The actual pronoun translation and referent still need language review.
    """
    if 'pronoun_refs' not in pair:
        return []
    refs = pair['pronoun_refs']
    if not isinstance(refs, list) or not refs:
        raise ValueError('pronoun_refs requires a nonempty list of explicit pronoun references')
    fields = {'en_span': 'en', 'ko_pronoun_span': 'ko', 'ko_reference_span': 'ko'}
    previous_en, korean_ranges = 0, []
    for ref in refs:
        if not isinstance(ref, dict) or set(ref) != set(fields):
            raise ValueError('Each pronoun_refs entry requires en_span, ko_pronoun_span and ko_reference_span only')
        for field, language in fields.items():
            selected = ref[field]
            if (not isinstance(selected, list) or len(selected) != 2 or
                    any(type(x) is not int for x in selected) or
                    not isinstance(pair.get(language), str) or
                    not 0 <= selected[0] < selected[1] <= len(pair[language])):
                raise ValueError('pronoun_refs requires bounded integer start/end pairs in the display text')
        en_start, en_end = ref['en_span']
        ko_start, ko_end = ref['ko_pronoun_span']
        ref_start, ref_end = ref['ko_reference_span']
        english, korean = pair['en'], pair['ko']
        if en_start < previous_en:
            raise ValueError('pronoun_refs English spans must be ordered and nonoverlapping')
        pronoun = english[en_start:en_end]
        if (pronoun.casefold() not in REFERENCE_PRONOUNS_EN or pronoun == 'US' or
                (en_start and re.match(r"[A-Za-z0-9_'’-]", english[en_start - 1])) or
                (en_end < len(english) and re.match(r"[A-Za-z0-9_'’-]", english[en_end]) and
                 not REFERENCE_PRONOUN_CONTRACTION.match(english, en_end))):
            raise ValueError('pronoun_refs en_span must select one whole English personal, demonstrative, reflexive or possessive pronoun')
        if not re.fullmatch(r'[가-힣]+(?: [가-힣]+)*', korean[ko_start:ko_end]):
            raise ValueError('pronoun_refs ko_pronoun_span must select the Korean pronoun without its particle or brackets')
        if ko_end != ref_start:
            raise ValueError('pronoun_refs reference must immediately follow the Korean pronoun')
        reference = korean[ref_start:ref_end]
        if (not reference.startswith('[') or not reference.endswith(']') or
                not reference[1:-1].strip() or any(c in '[]' or ord(c) < 32 for c in reference[1:-1])):
            raise ValueError('pronoun_refs ko_reference_span requires one nonempty bracketed referent without nested brackets or newlines')
        previous_en = en_end
        korean_ranges.append((ko_start, ref_end))
    # Translation order may differ. Each Korean pronoun plus its immediate
    # reference still occupies a distinct, nonoverlapping display range.
    korean_ranges.sort()
    if any(left[1] > right[0] for left, right in zip(korean_ranges, korean_ranges[1:])):
        raise ValueError('pronoun_refs Korean pronoun and reference ranges must not overlap or be reused')
    return refs


def korean_grammar_bracket_spans(pair):
    """Ignore only declared reference brackets while preserving display offsets."""
    value = list(pair['ko'])
    for ref in pronoun_references(pair):
        start, end = ref['ko_reference_span']
        value[start:end] = ' ' * (end - start)
    return bracket_spans(''.join(value))


def emphasis_spans(pair, *, required=False):
    """Validate explicit bilingual links, never infer a morpheme or its meaning.

    One link may join discontinuous grammatical markers to a single ending.
    Language order may differ. A grammatical correspondence still needs L review.
    """
    references = pronoun_references(pair)
    if 'ko_emphasis_spans' in pair or 'en_emphasis_spans' in pair:
        raise ValueError('Replace legacy ko_emphasis_spans/en_emphasis_spans with reviewed bilingual emphasis_links')
    if 'emphasis_links' not in pair:
        if required or 'emphasis_note' in pair:
            raise ValueError('Current hints require explicit bilingual emphasis_links')
        return {'en': [], 'ko': []}
    links = pair['emphasis_links']
    if not isinstance(links, list):
        raise ValueError('emphasis_links must be a list of bilingual grammar links')
    note = pair.get('emphasis_note')
    if not links:
        if not isinstance(note, str) or not note.strip() or any(ord(c) < 32 for c in note):
            raise ValueError('Empty emphasis_links require an emphasis_note explaining the absent overt counterpart')
    elif note is not None:
        raise ValueError('emphasis_note is only for an empty emphasis_links exception')
    result = {'en': [], 'ko': []}
    word = r"(?:p\.p\.?|[A-Za-z]+(?:['’-][A-Za-z]+)*)"
    patterns = {'en': word + '(?: ' + word + ')*',
                'ko': r'[가-힣]+(?: [가-힣]+)*'}
    for link in links:
        if not isinstance(link, dict) or set(link) != {'en_spans', 'ko_spans'}:
            raise ValueError('Each emphasis_links entry requires en_spans and ko_spans only')
        for language in ('en', 'ko'):
            spans = link[language + '_spans']
            if not isinstance(spans, list) or not spans:
                raise ValueError('Each emphasis link needs nonempty ranges in both languages')
            previous = 0
            for selected in spans:
                if (not isinstance(selected, list) or len(selected) != 2 or
                        any(type(x) is not int for x in selected)):
                    raise ValueError('emphasis_links requires integer start/end pairs')
                start, end = selected
                if not previous <= start < end <= len(pair[language]):
                    raise ValueError('emphasis_links ranges must be ordered within each link and inside display text')
                if not re.fullmatch(patterns[language], pair[language][start:end]):
                    raise ValueError('emphasis_links must select language text without brackets, punctuation or edge whitespace')
                if language == 'ko' and any(
                        start < ref['ko_reference_span'][1] and ref['ko_pronoun_span'][0] < end
                        for ref in references):
                    raise ValueError('emphasis_links must leave the Korean pronoun and its bracketed referent plain')
                result[language].append((start, end))
                previous = end
    for spans in result.values():
        spans.sort()
        if any(left[1] > right[0] for left, right in zip(spans, spans[1:])):
            raise ValueError('emphasis_links must not reuse or overlap text across links')
    return result


def aligned_display_segments(pair, language):
    """Keep every character, including unstyled brackets; style only linked text."""
    spans = emphasis_spans(pair)[language]
    result, cursor = [], 0
    for start, end in spans:
        if cursor < start:
            result.append((False, pair[language][cursor:start]))
        result.append((True, pair[language][start:end]))
        cursor = end
    if cursor < len(pair[language]):
        result.append((False, pair[language][cursor:]))
    return result


def _validate_omitted_marker(hint, pairs, *, conjunction=False):
    """Validate one visible editorial supplement, not whether omission is grammatical.

    The added marker is confined to the hint display. Its source counterpart
    remains absent; check_learning_content verifies the remaining exact excerpt.
    L review must still certify the relative/conjunction choice and Korean function.
    """
    kind = 'conjunction' if conjunction else 'relative'
    field = 'omitted_' + kind
    marker = hint.get(field)
    allowed = {'that'} if conjunction else OMITTED_RELATIVES
    if not isinstance(marker, str) or marker not in allowed:
        raise ValueError(field + ' must be reviewed that' if conjunction else
                         'omitted_relative must be a reviewed relative pronoun or relative adverb')
    label = hint.get('structure_label', '')
    required_label = '접속사' if conjunction else '관계'
    if (not isinstance(label, str) or required_label not in label or '생략' not in label or
            (conjunction and '관계' in label)):
        raise ValueError('Omitted-' + kind + ' display requires a ' + kind + '-omission structure_label')
    if len(pairs) != 1:
        raise ValueError('Omitted-' + kind + ' hints require exactly one English/Korean pair')
    pair = pairs[0]
    english, korean = pair['en'], pair['ko']
    en_brackets, ko_brackets = bracket_spans(english), korean_grammar_bracket_spans(pair)
    if len(en_brackets) != 1 or len(ko_brackets) != 1:
        raise ValueError('Omitted-' + kind + ' display requires one bracket pair in each language')
    left, right = en_brackets[0]
    supplement = '(' + marker + ')'
    if (english.count('(') != 1 or english.count(')') != 1 or
            not english[left + 1:right - 1].startswith(supplement + ' ') or
            not english[left + 1 + len(supplement):right - 1].strip()):
        raise ValueError('The single omitted-' + kind + ' supplement must immediately follow the opening bracket')
    emphasis_spans(pair, required=True)
    marker_span = [left + 2, left + 2 + len(marker)]
    links = pair['emphasis_links']
    if len(links) != 1 or links[0]['en_spans'] != [marker_span]:
        raise ValueError('Omitted-' + kind + ' emphasis must select only the supplied marker, without parentheses')
    korean_spans = links[0]['ko_spans']
    ko_left, ko_right = ko_brackets[0]
    # Korean correspondences include relative endings/adverb expressions and
    # noun-clause endings. Do not infer semantics or impose a syllable whitelist.
    # The independent reviewer chooses the smallest meaningful surface span.
    # An authored clause formula may mark both the subject particle and the
    # clause ending. Do not mark the intervening content words as a shortcut.
    selected = {pos for start, end in korean_spans for pos in range(start, end)}
    constituent = {pos for pos in range(ko_left + 1, ko_right - 1) if not korean[pos].isspace()}
    if (any(not ko_left + 1 <= start < end <= ko_right - 1 for start, end in korean_spans)
            or constituent <= selected):
        raise ValueError('Omitted ' + kind + ' needs selected Korean grammatical ranges inside its bracket, not the whole bracket')


def validate_omitted_relative(hint, pairs):
    _validate_omitted_marker(hint, pairs)


def validate_omitted_conjunction(hint, pairs):
    _validate_omitted_marker(hint, pairs, conjunction=True)


def omitted_relative_source_text(hint):
    """Strip only a validated hint-only supplement for an exact source check."""
    pair = display_pairs(hint, require_alignment=True)[0]
    if hint.get('display_mode') != 'omitted-relative':
        raise ValueError('Source supplement removal requires omitted-relative mode')
    english = pair['en'].replace('(' + hint['omitted_relative'] + ') ', '', 1)
    return english.replace('[', '').replace(']', '')


def omitted_conjunction_source_text(hint):
    """Remove only the validated hint-only (that), never alter original data."""
    pair = display_pairs(hint, require_alignment=True)[0]
    if hint.get('display_mode') != 'omitted-conjunction':
        raise ValueError('Source supplement removal requires omitted-conjunction mode')
    english = pair['en'].replace('(' + hint['omitted_conjunction'] + ') ', '', 1)
    return english.replace('[', '').replace(']', '')


def display_pairs(hint, *, required=True, require_alignment=False):
    """Validate explicit student mappings and a short structural label.

    Current tense/voice combinations display a source verb phrase and separate
    formula_label. Other combinations keep formula + lexical form. Legacy input
    remains readable without being silently rewritten or certified current.
    Paired structures map selected source fragments to their Korean parts.
    Labels identify an already reviewed structure; this does not infer grammar.
    """
    if not isinstance(hint, dict):
        raise ValueError('Structure hint must be an object')
    lexical_step(hint)
    category = hint.get('category')
    mode = hint.get('display_mode')
    ko_only_verb = 'emphasis_policy' in hint
    if ko_only_verb:
        # This declaration is authored and independently reviewed. A label's
        # spelling cannot establish whether the excerpt is a verb construction.
        if hint['emphasis_policy'] != VERB_CONSTRUCTION_EMPHASIS:
            raise ValueError('Unknown structure hint emphasis_policy')
        if category in {'function-combination', 'paired-structure'} or mode in OMITTED_MODES:
            raise ValueError('Verb-construction emphasis_policy requires a general structure hint')
    if 'display_mode' in hint:
        valid_mode = ((category == 'function-combination' and mode in {'modal-perfect-verb', 'verb-function'}) or
                      (category not in {'function-combination', 'paired-structure'} and
                       mode in {'split-phrasal-verb', *OMITTED_MODES}))
        if not valid_mode:
            raise ValueError('Unknown or misplaced structure hint display_mode')
    if 'display_span' in hint and mode not in {'modal-perfect-verb', 'verb-function'}:
        raise ValueError('display_span requires verb-function or legacy modal-perfect-verb mode')
    if 'formula_label' in hint and mode != 'verb-function':
        raise ValueError('formula_label requires verb-function display_mode')
    if require_alignment and mode == 'modal-perfect-verb':
        raise ValueError('Current tense/voice hints require verb-function mode and formula_label; legacy modal-perfect-verb is not current')
    if 'display_spans' in hint and category != 'paired-structure' and mode != 'split-phrasal-verb':
        raise ValueError('display_spans requires paired-structure or split-phrasal-verb mode')
    if 'omitted_relative' in hint and mode != 'omitted-relative':
        raise ValueError('omitted_relative requires omitted-relative display_mode')
    if 'omitted_conjunction' in hint and mode != 'omitted-conjunction':
        raise ValueError('omitted_conjunction requires omitted-conjunction display_mode')
    label = hint.get('structure_label', '')
    if (require_alignment and isinstance(label, str) and '관계' in label and '생략' in label
            and mode != 'omitted-relative'):
        raise ValueError('Current omitted-relative hints require omitted-relative mode and a bilingual marker link')
    if (require_alignment and isinstance(label, str) and '접속사' in label and '생략' in label
            and mode != 'omitted-conjunction'):
        raise ValueError('Current omitted-conjunction hints require omitted-conjunction mode and a bilingual marker link')
    if ('display_pairs' not in hint and not required and category != 'paired-structure'
            and mode is None and not ko_only_verb):
        return []
    pairs = hint.get('display_pairs')
    if not isinstance(pairs, list) or not 1 <= len(pairs) <= 3:
        raise ValueError('Hint display_pairs requires one to three English/Korean pairs')
    for pair in pairs:
        if not isinstance(pair, dict):
            raise ValueError('Hint display pair must be an object')
        for language, pattern in [('en', r'[A-Za-z]'), ('ko', r'[가-힣]')]:
            value = pair.get(language)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f'Hint display {language} requires nonempty text')
            if value != value.strip() or any(ord(c) < 32 for c in value):
                raise ValueError('Hint display lines must be trimmed and contain no control characters')
            if not re.search(pattern, value):
                raise ValueError(f'Hint display {language} must contain its stated language')
        if re.search(r'[가-힣]', pair['en']):
            raise ValueError('Hint display English line cannot contain Korean commentary')
        if mode not in OMITTED_MODES and PARENTHETICAL_RELATIVE.search(pair['en']):
            raise ValueError('A supplied parenthetical relative or that conjunction requires its explicit omitted display_mode')
        if category == 'function-combination' and 'pronoun_refs' in pair:
            raise ValueError('Function-combination hints do not use pronoun_refs')
        emphasis_spans(pair, required=require_alignment or ko_only_verb)
        if ko_only_verb and not pair['emphasis_links']:
            raise ValueError('Verb-construction emphasis_policy retains nonempty bilingual emphasis_links')
        en_spans, ko_spans = bracket_spans(pair['en']), korean_grammar_bracket_spans(pair)
        if len(en_spans) != len(ko_spans):
            raise ValueError('Hint display English/Korean bracket counts must match')
        if not en_spans and category not in {'function-combination', 'paired-structure'}:
            raise ValueError('Structural hint pairs require corresponding brackets')
    if category == 'paired-structure':
        if len(pairs) != 1:
            raise ValueError('Paired-structure hints require exactly one English/Korean pair')
        if 'structure_label' in hint or 'display_en' in hint:
            raise ValueError('Paired-structure hints use display_pairs without structure_label or display_en')
        spans = hint.get('display_spans')
        if (not isinstance(spans, list) or not spans or
                any(not isinstance(s, list) or len(s) != 2 or
                    any(type(x) is not int for x in s) or not 0 <= s[0] < s[1]
                    for s in spans)):
            raise ValueError('Paired-structure display_spans require nonempty integer source ranges')
        if any(left[1] > right[0] for left, right in zip(spans, spans[1:])):
            raise ValueError('Paired-structure display_spans must be ordered and nonoverlapping')
    elif category == 'function-combination':
        if len(pairs) != 1:
            raise ValueError('Function-combination hints require exactly one compact pair, not stages')
        if '[' in pairs[0]['en']:
            raise ValueError('Function-combination hints use a formula + source lexical form without brackets')
        if mode == 'verb-function':
            validate_verb_function(hint, pairs[0])
        elif mode == 'modal-perfect-verb':
            selected = hint.get('display_span')
            if (not isinstance(selected, list) or len(selected) != 2 or
                    any(type(x) is not int for x in selected) or not 0 <= selected[0] < selected[1]):
                raise ValueError('Modal-perfect display_span requires one integer source range')
            verb = MODAL_PERFECT_VERB.fullmatch(pairs[0]['en'])
            if verb is None or verb['participle'].casefold() in {'a', 'b', 'v', 'p', 'pp'}:
                raise ValueError('Modal-perfect display must contain only the literal modal, have and source participle')
        else:
            parts = pairs[0]['en'].split(' + ')
            if len(parts) < 2 or any(not part.strip() or not re.search(r'[A-Za-z]', part) or '+' in part for part in parts):
                raise ValueError('Function-combination English must be formula + source lexical form')
            reject_split_modal_perfect(parts)
            if require_alignment and any(VERB_FUNCTION_FORMULA.fullmatch(part.strip()) or
                                         MODAL_FORM.fullmatch(part.strip()) for part in parts[:-1]):
                raise ValueError('Current tense/voice hints require verb-function mode and formula_label')
        if hint.get('structure_label') is not None:
            raise ValueError('A function-combination hint must not append a structure_label')
    else:
        if mode == 'split-phrasal-verb':
            if len(pairs) != 1:
                raise ValueError('Split-phrasal-verb hints require exactly one English/Korean pair')
            spans = hint.get('display_spans')
            if (not isinstance(spans, list) or len(spans) != 2 or
                    any(not isinstance(s, list) or len(s) != 2 or
                        any(type(x) is not int for x in s) or not 0 <= s[0] < s[1]
                        for s in spans) or spans[0][1] >= spans[1][0]):
                raise ValueError('Split-phrasal-verb display_spans require two ordered source ranges with a gap')
        label = hint.get('structure_label')
        if not isinstance(label, str) or not label.strip():
            raise ValueError('General hint requires a short structure_label')
        if (label != label.strip() or len(label) > 60 or
                any(ord(c) < 32 for c in label) or any(c in label for c in '()[]') or
                not re.search(r'[가-힣]', label)):
            raise ValueError('structure_label must be one short Korean label without surrounding brackets or control characters')
        if mode == 'omitted-relative':
            validate_omitted_relative(hint, pairs)
        elif mode == 'omitted-conjunction':
            validate_omitted_conjunction(hint, pairs)
    return pairs


def display_lines(hint):
    pairs = display_pairs(hint)
    if hint.get('display_mode') == 'verb-function':
        step = lexical_step(hint)
        if step is not None:
            return [step['form'] + '(' + step['meaning_ko'] + ') → ' +
                    pairs[0]['en'] + '(' + pairs[0]['ko'] + ') (' + hint['formula_label'] + ')']
        return [pairs[0]['en'] + ' → ' + pairs[0]['ko'] + ' (' + hint['formula_label'] + ')']
    if hint.get('category') in {'function-combination', 'paired-structure'}:
        return [pair['en'] + ' → ' + pair['ko'] for pair in pairs]
    # Keep one logical line; Word may wrap naturally at the existing width.
    value = ' / '.join(pair['en'] + ' → ' + pair['ko'] for pair in pairs)
    return [value + ' (' + hint['structure_label'] + ')']
