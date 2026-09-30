"""Local copy (2과 Further Reading, 2026-09-29): passive p.p. + to V complement."""
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / '../scripts'))
from check_learning_content import verb_construction_review, verb_form_review

TEXT = 'The words are believed to warn of hardships and to urge people to be prepared.'


def gloss(headword='believed to V', links=None, lemma='believe', kind='to-complement'):
    b = TEXT.index('believed')
    t1 = TEXT.index('to warn')
    t2 = TEXT.index('to urge')
    links = [[t1, t1 + 2], [t2, t2 + 2]] if links is None else links
    return {'id': 'g', 'kind': 'lexical', 'headword': headword, 'meaning_ko': '~하는 것으로 여겨지는',
            'spans': [[b, b + 8]] + links,
            'verb_form': {'usage': 'passive-participle', 'source_span': [b, b + 8], 'lemma': 'believe',
                          'function_gloss_id': 'f'},
            'verb_construction': {'kind': kind, 'verb_span': [b, b + 8], 'lemma': lemma,
                                  'link_spans': links, 'review_record': '병렬 보충 to V'}}


def check(g):
    verb_form_review(g, TEXT)
    verb_construction_review(g, TEXT)


class PassiveToComplement(unittest.TestCase):
    def test_actual_pp_with_parallel_to_is_accepted(self):
        check(gloss())

    def test_single_to_is_accepted(self):
        t1 = TEXT.index('to warn')
        check(gloss(links=[[t1, t1 + 2]]))

    def test_lemma_headword_is_rejected(self):
        with self.assertRaises(ValueError):
            check(gloss(headword='believe to V'))

    def test_bare_pp_headword_without_frame_is_rejected(self):
        with self.assertRaises(ValueError):
            check(gloss(headword='believed'))

    def test_non_to_link_is_rejected(self):
        o = TEXT.index('of')
        with self.assertRaises(ValueError):
            check(gloss(links=[[o, o + 2]]))

    def test_passive_verb_frame_is_not_opened(self):
        with self.assertRaises(ValueError):
            check(gloss(kind='verb-frame'))


if __name__ == '__main__':
    unittest.main()
