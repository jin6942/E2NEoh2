"""Narrow US/name-link regressions; synthetic data is not student content."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))

import check_learning_content as m
from test_learning_content import fixture


def gloss_for(sentence, surface, occurrence=0):
    return [g for g in sentence['glosses'] if g['headword'] == surface][occurrence]


def country_gloss(sentence, occurrence=0, headword='US', meaning='미국'):
    gloss = gloss_for(sentence, 'US', occurrence)
    gloss.update(headword=headword, meaning_ko=meaning)
    gloss.pop('referent_ko', None)
    return gloss


def repeat(sentence, surface, first_id, occurrence=0):
    gloss = gloss_for(sentence, surface, occurrence)
    sentence['glosses'].remove(gloss)
    row = next(c for c in sentence['lexical_coverage'] if c.get('gloss_id') == gloss['id'])
    row.update(gloss_id=None, exemption='proper-name-repeat',
               first_gloss_id=first_id, reason='Synthetic reviewed same-name link')
    return row


def two_sources(first_text, second_text):
    data = fixture([first_text, 'We save valuable materials.', 'I protect local resources.'])
    other = fixture([second_text, 'We save valuable materials.', 'I protect local resources.'])
    other['sources'][0]['id'] = 'src2'
    other['paragraphs'][0].update(id='p2', source_id='src2')
    other['units'][0].update(id='u2', source_id='src2', paragraph_ids=['p2'])
    other['units'][0]['today_words'][0]['source_gloss_id'] = 'other-g1-1'
    for sentence in other['sentences']:
        sentence['source_id'] = 'src2'
        for gloss in sentence['glosses']:
            gloss['id'] = 'other-' + gloss['id']
        for row in sentence['lexical_coverage']:
            row['gloss_id'] = 'other-' + row['gloss_id']
    for key in ('sources', 'paragraphs', 'units', 'sentences'):
        data[key].extend(other[key])
    return data


class GlossIdentityTests(unittest.TestCase):
    def accepted(self, data):
        before = deepcopy(data)
        result = m.check(data, scope='learning')
        self.assertEqual(result['status'], 'STRUCTURE_PASS')
        self.assertEqual(data, before)
        return result

    def test_us_country_uses_existing_explicit_gloss_without_referent(self):
        for headword in ('US', 'the US', 'The US'):
            for meaning in ('미국', '미합중국'):
                with self.subTest(headword=headword, meaning=meaning):
                    data = fixture(['They visit the US.', 'We save valuable materials.',
                                    'I protect local resources.'])
                    country_gloss(data['sentences'][0], headword=headword, meaning=meaning)
                    self.accepted(data)

    def test_actual_multiword_country_gloss_needs_no_pronoun_referent(self):
        data = fixture(['They visit the US.', 'We save valuable materials.',
                        'I protect local resources.'])
        sentence = data['sentences'][0]
        gloss = country_gloss(sentence, headword='the US')
        article = gloss_for(sentence, 'the')
        gloss['spans'][0][0] = article['spans'][0][0]
        sentence['glosses'].remove(article)
        next(c for c in sentence['lexical_coverage'] if c['gloss_id'] == article['id'])['gloss_id'] = gloss['id']
        self.accepted(data)

    def test_country_repeat_links_to_reviewed_country_gloss(self):
        data = fixture(['They visit the US.', 'They leave the US.', 'I protect local resources.'])
        first = country_gloss(data['sentences'][0])
        repeat(data['sentences'][1], 'US', first['id'])
        self.accepted(data)

    def test_country_repeat_in_same_sentence_still_requires_earlier_occurrence(self):
        data = fixture(['They visit US and US.', 'We save valuable materials.',
                        'I protect local resources.'])
        first = country_gloss(data['sentences'][0])
        repeat(data['sentences'][0], 'US', first['id'], occurrence=1)
        self.accepted(data)

    def test_country_future_occurrence_in_same_sentence_is_rejected(self):
        data = fixture(['They visit US and US.', 'We save valuable materials.',
                        'I protect local resources.'])
        later = country_gloss(data['sentences'][0], occurrence=1)
        repeat(data['sentences'][0], 'US', later['id'])
        with self.assertRaisesRegex(ValueError, 'must precede'):
            m.check(data, scope='learning')

    def test_country_repeat_cannot_cross_independent_sources(self):
        data = two_sources('They visit the US.', 'They leave the US.')
        first = country_gloss(data['sentences'][0])
        repeat(data['sentences'][3], 'US', first['id'])
        with self.assertRaisesRegex(ValueError, 'same independent source'):
            m.check(data, scope='learning')

    def test_uppercase_pronouns_keep_mandatory_referents(self):
        for word, meaning in (('US', '우리를'), ('us', '우리를'),
                              ('THEY', '그들은'), ('THEIR', '그들의'),
                              ('US', '미국의 우리들'), ('US', '시험용 뜻')):
            with self.subTest(word=word, meaning=meaning):
                data = fixture([f'They help {word} today.', 'We save valuable materials.',
                                'I protect local resources.'])
                gloss = gloss_for(data['sentences'][0], word)
                gloss['meaning_ko'] = meaning
                gloss.pop('referent_ko')
                with self.assertRaisesRegex(ValueError, 'Mandatory pronoun referent'):
                    m.check(data, scope='learning')

    def test_country_meaning_does_not_exempt_lowercase_or_other_tokens(self):
        for word in ('us', 'Us', 'THEY', 'THEM', 'HIS'):
            with self.subTest(word=word):
                data = fixture([f'They help {word} today.', 'We save valuable materials.',
                                'I protect local resources.'])
                gloss = gloss_for(data['sentences'][0], word)
                gloss.update(headword='US', meaning_ko='미국')
                gloss.pop('referent_ko')
                with self.assertRaisesRegex(ValueError, 'Mandatory pronoun referent'):
                    m.check(data, scope='learning')

    def test_country_meaning_alone_does_not_exempt_unrelated_headword(self):
        data = fixture(['They help US today.', 'We save valuable materials.',
                        'I protect local resources.'])
        country_gloss(data['sentences'][0], headword='us')
        with self.assertRaisesRegex(ValueError, 'Mandatory pronoun referent'):
            m.check(data, scope='learning')

    def test_uppercase_pronoun_with_referent_still_passes(self):
        data = fixture(['THEY help US today.', 'We save valuable materials.',
                        'I protect local resources.'])
        self.accepted(data)

    def test_us_basic_word_exemption_remains_rejected(self):
        data = fixture(['They help US today.', 'We save valuable materials.',
                        'I protect local resources.'])
        row = repeat(data['sentences'][0], 'US', 'unused')
        row.update(exemption='below-middle1-unneeded', level='below-middle1')
        with self.assertRaisesRegex(ValueError, 'Missing required gloss'):
            m.check(data, scope='learning')

    def test_us_repeat_cannot_use_pronoun_gloss_as_country_identity(self):
        data = fixture(['They help US today.', 'They help US again.', 'I protect local resources.'])
        first = gloss_for(data['sentences'][0], 'US')
        first['meaning_ko'] = '우리를'
        repeat(data['sentences'][1], 'US', first['id'])
        with self.assertRaisesRegex(ValueError, 'Missing required gloss'):
            m.check(data, scope='learning')

    def test_legacy_country_referent_is_preserved_without_rewriting(self):
        data = fixture(['They visit the US.', 'We save valuable materials.',
                        'I protect local resources.'])
        gloss = country_gloss(data['sentences'][0], headword='the US')
        gloss['referent_ko'] = 'the United States의 약자'
        self.accepted(data)

    def test_possessive_name_identity_in_both_directions(self):
        for first, later in (('Lee', 'Lee'), ('Lee', "Lee's"), ('Lee', 'Lee’s'),
                             ("Lee's", 'Lee'), ('Lee’s', 'Lee'), ("Lee's", 'Lee’s'),
                             ('Magrath', 'Magrath’s'), ("O'Neil", "O'Neil's")):
            with self.subTest(first=first, later=later):
                data = fixture([f'{first} repairs useful tools.', f'{later} saves valuable materials.',
                                'I protect local resources.'])
                repeat(data['sentences'][1], later, 'g1-0')
                self.accepted(data)

    def test_possessive_normalization_is_not_general_name_fuzzing(self):
        for first, later in (('Lee', 'Leeds'), ('Lee', 'Lees'), ('Lee', "Lee'd"),
                             ('Lee', "Lee's's"), ('Lees', "Lee's"),
                             ("O'Neil", 'O’Neil’s'), ('Magrath', 'Lee’s')):
            with self.subTest(first=first, later=later):
                data = fixture([f'{first} repairs useful tools.', f'{later} saves valuable materials.',
                                'I protect local resources.'])
                repeat(data['sentences'][1], later, 'g1-0')
                with self.assertRaisesRegex(ValueError, 'different original name'):
                    m.check(data, scope='learning')

    def test_possessive_repeat_cannot_cross_independent_sources(self):
        data = two_sources('Lee repairs useful tools.', 'Lee’s repairs useful tools.')
        repeat(data['sentences'][3], 'Lee’s', 'g1-0')
        with self.assertRaisesRegex(ValueError, 'same independent source'):
            m.check(data, scope='learning')

    def test_possessive_repeat_cannot_link_to_a_future_sentence(self):
        data = fixture(['Lee’s repairs useful tools.', 'Lee saves valuable materials.',
                        'I protect local resources.'])
        repeat(data['sentences'][0], 'Lee’s', 'g2-0')
        with self.assertRaisesRegex(ValueError, 'earlier gloss'):
            m.check(data, scope='learning')

    def test_possessive_repeat_cannot_link_to_a_future_same_sentence_gloss(self):
        data = fixture(['Lee’s helps Lee today.', 'We save valuable materials.',
                        'I protect local resources.'])
        repeat(data['sentences'][0], 'Lee’s', 'g1-2')
        with self.assertRaisesRegex(ValueError, 'must precede'):
            m.check(data, scope='learning')

    def test_possessive_repeat_requires_a_real_first_gloss(self):
        data = fixture(['Lee repairs useful tools.', 'Lee’s saves valuable materials.',
                        'I protect local resources.'])
        repeat(data['sentences'][1], 'Lee’s', 'missing')
        with self.assertRaisesRegex(ValueError, 'earlier gloss'):
            m.check(data, scope='learning')


if __name__ == '__main__':
    unittest.main()
