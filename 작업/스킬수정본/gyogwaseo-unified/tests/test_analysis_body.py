import copy
import importlib.util
from pathlib import Path
import unittest

MODULE = Path(__file__).parent / '../scripts/analysis_body.py'
spec = importlib.util.spec_from_file_location('analysis_body', MODULE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def fixture():
    text = '“① It isn’t 2²,” Mina said; she smiled.'
    split = text.index('she smiled')
    return {'sentences': [{'source_id': 'main', 'id': 's1', 'text': text,
                          'chunks': [{'start': 0, 'end': split - 1,
                                      'ko': '“① 그것은 2²가 아니야.”라고 Mina는 말했다;'},
                                     {'start': split, 'end': len(text), 'ko': '그녀는 미소 지었다.'}],
                          'natural_ko': 'Mina는 “① 그것은 2²가 아니야.”라고 말하며 미소 지었다.'}],
            'units': [{'source_id': 'main', 'sentence_ids': ['s1']}]}


class AnalysisBodyTests(unittest.TestCase):
    def test_three_roles_no_separate_model_or_literal(self):
        result = module.build_analysis_bodies(fixture())
        record = result['units'][0]['sentences'][0]
        self.assertEqual([x['role'] for x in record['blocks']],
                         ['analysis_english_chunks', 'analysis_korean_chunks',
                          'analysis_natural_translation'])
        self.assertFalse(result['standalone_model_translation_section'])
        self.assertEqual(result['semantic_review'], 'NOT_PERFORMED')

    def test_exact_source_symbols_and_semicolon_survive(self):
        data = fixture()
        result = module.build_analysis_bodies(data)
        record = result['units'][0]['sentences'][0]
        self.assertEqual(record['original'], data['sentences'][0]['text'])
        self.assertEqual(' '.join(record['blocks'][0]['chunks']), record['original'])

    def test_no_fallback_from_legacy_literal_to_natural(self):
        data = fixture()
        sentence = data['sentences'][0]
        del sentence['natural_ko']
        sentence['literal'] = '기존 직역으로 대체하지 않는다.'
        with self.assertRaisesRegex(ValueError, 'natural_ko'):
            module.build_analysis_bodies(data)

    def test_missing_korean_chunk_rejected(self):
        data = fixture()
        data['sentences'][0]['chunks'][1]['ko'] = ''
        with self.assertRaisesRegex(ValueError, 'Korean chunk'):
            module.build_analysis_bodies(data)

    def test_missing_punctuation_rejected(self):
        data = fixture()
        data['sentences'][0]['chunks'][0]['start'] = 1
        with self.assertRaisesRegex(ValueError, 'omit source'):
            module.build_analysis_bodies(data)

    def test_overlapping_chunks_rejected(self):
        data = fixture()
        data['sentences'][0]['chunks'][1]['start'] = 0
        with self.assertRaisesRegex(ValueError, 'overlap'):
            module.build_analysis_bodies(data)

    def test_repeated_unit_sentence_rejected(self):
        data = fixture()
        data['units'][0]['sentence_ids'].append('s1')
        with self.assertRaisesRegex(ValueError, 'repeated'):
            module.build_analysis_bodies(data)

    def test_omitted_source_sentence_rejected(self):
        data = fixture()
        second = copy.deepcopy(data['sentences'][0])
        second['id'] = 's2'
        data['sentences'].append(second)
        with self.assertRaisesRegex(ValueError, 'omit source sentences'):
            module.build_analysis_bodies(data)

    def test_source_order_reversal_rejected(self):
        data = fixture()
        second = copy.deepcopy(data['sentences'][0])
        second['id'] = 's2'
        data['sentences'].append(second)
        data['units'][0]['sentence_ids'] = ['s2', 's1']
        with self.assertRaisesRegex(ValueError, 'change source sentence order'):
            module.build_analysis_bodies(data)

    def test_independent_source_order_reversal_rejected(self):
        data = fixture()
        second = copy.deepcopy(data['sentences'][0])
        second['source_id'] = 'additional'
        data['sentences'].append(second)
        data['units'].insert(0, {'source_id': 'additional', 'sentence_ids': ['s1']})
        with self.assertRaisesRegex(ValueError, 'change source sentence order'):
            module.build_analysis_bodies(data)


if __name__ == '__main__':
    unittest.main()
