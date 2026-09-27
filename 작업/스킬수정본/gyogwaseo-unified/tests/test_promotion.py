import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'../scripts'))
from test_learning_content import fixture
import build_promotion as p


def sample():
    data=fixture(['They repair useful tools to protect local resources.',
                  'We save valuable materials.', 'I protect local resources.'])
    s=data['sentences'][0];at=s['text'].index(' to ')
    s['chunks']=[{'start':0,'end':at,'ko':'그들은 유용한 도구를 고친다'},
                 {'start':at+1,'end':len(s['text']),'ko':'지역 자원을 지키기 위해'}]
    return data


class PromotionTests(unittest.TestCase):
    def test_source_preview_and_current_translation(self):
        data=sample();data['sentences'][0]['natural_ko']='확정 자연 해석 시험'
        result=p.render(data)
        self.assertIn('They repair useful tools / to protect local resources.',result['blog'])
        self.assertIn('[분석지 해석 예시] 확정 자연 해석 시험',result['blog'])
        self.assertNotIn('모범 해석',result['blog'])
        self.assertIn('미정',result['cafe1'])
        self.assertNotIn('올려',result['cafe2'])

    def test_link_without_evidence_rejected(self):
        data=sample();data['promotion']={'links':{'blog':{'url':'https://example.com'}}}
        with self.assertRaisesRegex(ValueError,'verification'):p.render(data)


if __name__=='__main__':unittest.main()
