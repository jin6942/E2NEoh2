import copy
import importlib.util
from pathlib import Path
import unittest

script = Path(__file__).parent / '../scripts/question_source.py'
spec = importlib.util.spec_from_file_location('question_source', script)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def checked_view(source, question):
    from revision_fixtures import length_review
    q=copy.deepcopy(question)
    q['length_review']=length_review(q['type'])
    return m.build_view(source,q)


def fixture():
    # Artificial token corpus for mechanical tests, not educational content.
    sentences, texts, offset = [], [], 0
    for n in range(10):
        text = ' '.join(f'Word{n}_{i}' for i in range(10)) + '.'
        sentences.append({'id': f's{n}', 'start': offset, 'end': offset + len(text)})
        texts.append(text)
        offset += len(text) + 2
    return ({'id': 'reading', 'text': '\n\n'.join(texts), 'sentences': sentences},
            {'source_id': 'reading', 'first_sentence': 's0', 'last_sentence': 's9', 'type': '주제'})


class QuestionSourceTests(unittest.TestCase):
    def test_no_fixed_100_word_cutoff_and_shortness_is_reported(self):
        source, q = fixture()
        view = checked_view(source, q)
        self.assertEqual(view['word_count'], 100)
        self.assertEqual(view['passage'], source['text'])
        old = 'Word9_9.'
        source['text'] = source['text'][:-len(old)]
        source['sentences'][-1]['end'] -= len(old)
        view=checked_view(source,q)
        self.assertEqual(view['word_count'],99)
        self.assertTrue(view['length_comparison']['independent_review_required'])

    def test_word_count_keeps_contractions_hyphens_and_numbers(self):
        self.assertEqual(m.word_count("can't state-of-the-art 62 million — / ①"), 5)

    def test_exact_punctuation_and_symbols_not_stripped(self):
        source, q = fixture()
        source['text'] = source['text'].replace('Word0_0', '“A①²”!!')
        self.assertEqual(len('Word0_0'), len('“A①²”!!'))
        view = checked_view(source, q)
        self.assertTrue(view['passage'].startswith('“A①²”!!'))

    def test_omitted_sentence_and_unknown_source_fail(self):
        source, q = fixture()
        source['sentences'].pop(3)
        with self.assertRaisesRegex(ValueError, 'omit text'):
            checked_view(source, q)
        source, q = fixture()
        q['source_id'] = 'another book'
        with self.assertRaisesRegex(ValueError, 'identity'):
            checked_view(source, q)

    def test_reversed_or_missing_range_fails(self):
        source, q = fixture()
        q.update(first_sentence='s9', last_sentence='s0')
        with self.assertRaisesRegex(ValueError, 'Reversed'):
            checked_view(source, q)
        q['first_sentence'] = 'missing'
        with self.assertRaisesRegex(ValueError, 'Unknown'):
            checked_view(source, q)

    def test_blank_exact_reconstruction_and_16_underscores(self):
        source, q = fixture()
        q.update(type='빈칸', replacement_span=[0, 7])
        v = checked_view(source, q)
        self.assertTrue(v['passage'].startswith('_' * 16 + ' '))
        self.assertEqual(v['replacement']['original'], 'Word0_0')
        self.assertEqual(v['source_reconstruction'], 'PASS')

    def test_insertion_given_removed_once_and_slots_distinct(self):
        source, q = fixture()
        starts = [r['start'] for r in source['sentences']]
        q.update(type='삽입', given_sentence='s2', insertion_slots=[starts[i] for i in (0, 2, 4, 6, 8)])
        v = checked_view(source, q)
        self.assertEqual(v['answer'], 2)
        self.assertNotIn(v['given'], v['passage'])
        self.assertEqual(len(v['annotations']), 5)
        q['insertion_slots'] = [starts[i] for i in (0, 2, 3, 6, 8)]
        with self.assertRaisesRegex(ValueError, 'collapse'):
            checked_view(source, q)

    def test_insertion_missing_given_rejected(self):
        source, q = fixture()
        q['type'] = '삽입'
        with self.assertRaisesRegex(ValueError, 'given'):
            checked_view(source, q)

    def test_ordering_resolves_source_order_with_original_spaces(self):
        source, q = fixture()
        s = source['sentences']
        q.update(type='순서', block_spans={'given': [0, s[1]['start']],
                 'A': [s[4]['start'], s[7]['start']], 'B': [s[7]['start'], len(source['text'])],
                 'C': [s[1]['start'], s[4]['start']]})
        v = checked_view(source, q)
        self.assertEqual(v['correct_order'], ['C', 'A', 'B'])
        self.assertEqual(v['given'] + ''.join(v['blocks'][x] for x in v['correct_order']), source['text'])
        q['block_spans']['A'][0] += 1
        with self.assertRaisesRegex(ValueError, 'partition'):
            checked_view(source, q)

    def test_vocabulary_replacement_shifts_later_annotations(self):
        source, q = fixture()
        q.update(type='어휘', replacement_span=[8, 15], replacement='Different',
                 vocabulary_marks=[[i * 8, i * 8 + 7] for i in range(5)])
        v = checked_view(source, q)
        self.assertEqual(v['answer'], 2)
        self.assertEqual(v['annotations'][1]['span'], [8, 17])
        self.assertEqual(v['annotations'][2]['span'], [18, 25])
        q['replacement'] = 'two words'
        with self.assertRaisesRegex(ValueError, 'one word'):
            checked_view(source, q)

    def test_unrelated_added_sentence_excluded_from_word_count(self):
        source, q = fixture()
        q.update(type='무관한 문장', addition_offset=source['sentences'][2]['start'],
                 addition='A deliberately inserted test sentence.',
                 sentence_marks=['s0', 's1', '@added', 's2', 's3'])
        v = checked_view(source, q)
        self.assertEqual(v['word_count'], 100)
        self.assertEqual(v['answer'], 3)
        self.assertIn(q['addition'], v['passage'])
        self.assertEqual(v['source_reconstruction'], 'PASS')

    def test_out_of_range_target_rejected(self):
        source, q = fixture()
        q.update(type='함축 의미', target_span=[0, len(source['text']) + 1])
        with self.assertRaisesRegex(ValueError, 'outside'):
            checked_view(source, q)


if __name__ == '__main__':
    unittest.main()
