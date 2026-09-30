"""Lesson-kind identity tests; no textbook content or layout is fabricated here."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent / '../scripts'))
from source_contract import course_policy, display_lesson, lesson_identity, normalize_course


class SpecialLessonTests(unittest.TestCase):
    def test_regular_lesson_keeps_kind_display_and_input(self):
        for value in ['UNIT03', 'LESSON 3', '제3과', '3과', '03', 3]:
            with self.subTest(value=value):
                metadata = {'lesson': value, 'lesson_id': 'UNIT03', 'lesson_number': '03'}
                cover = {'lesson_label': 'LESSON', 'lesson_number': '03'}
                before = deepcopy((metadata, cover))
                self.assertEqual(lesson_identity(metadata, cover),
                    {'number': 3, 'kind': 'lesson', 'internal_id': 'UNIT03', 'display': '3과'})
                self.assertEqual(display_lesson(metadata, cover), '3과')
                self.assertEqual((metadata, cover), before)

    def test_special_lesson_accepts_original_and_internal_forms(self):
        for value in ['Special Lesson 1', 'SPECIAL LESSON 01', 'special lesson 1', 'SL01', 'sl 1']:
            with self.subTest(value=value):
                metadata = {'lesson': value, 'lesson_id': 'SL01', 'lesson_number': '01'}
                cover = {'lesson_label': 'SPECIAL LESSON', 'lesson_number': '01'}
                before = deepcopy((metadata, cover))
                self.assertEqual(lesson_identity(metadata, cover),
                    {'number': 1, 'kind': 'special', 'internal_id': 'SL01', 'display': 'Special Lesson 1'})
                self.assertEqual(display_lesson(metadata, cover), 'Special Lesson 1')
                self.assertEqual((metadata, cover), before)
        self.assertEqual(lesson_identity({'lesson': 'Special Lesson 2'}, {'lesson_number': 2})['internal_id'], 'SL02')

    def test_conflicting_kinds_numbers_and_unverified_labels_fail(self):
        cases = [({'lesson': 'Special Lesson 1', 'lesson_id': 'UNIT01'}, None),
                 ({'lesson': 'Special Lesson 1', 'lesson_number': '1과'}, None),
                 ({'lesson': 'UNIT01', 'lesson_id': 'SL01'}, None),
                 ({'lesson': 'Special Lesson 1'}, {'lesson_number': '02'}),
                 ({'lesson': 'Special Lesson 1'}, {'lesson_number': 'UNIT01'}),
                 ({'lesson': 'Special Lesson 1'}, {'lesson_label': 'LESSON', 'lesson_number': '01'}),
                 ({'lesson': 'UNIT01'}, {'lesson_label': 'SPECIAL LESSON', 'lesson_number': '01'})]
        for metadata, cover in cases:
            with self.subTest(metadata=metadata, cover=cover), self.assertRaisesRegex(ValueError, 'Lesson identity conflict'):
                lesson_identity(metadata, cover)
        for value in ['Special Reading', 'Special Lesson', 'SL', 'Special Lesson -1', True, -1]:
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, 'numeric lesson identity'):
                lesson_identity({'lesson': value})

    def test_latest_course_alias_and_grade_policies_are_preserved(self):
        for course in ['영어II', '영어Ⅱ', '영어2', '영어 2']:
            with self.subTest(course=course):
                self.assertEqual(normalize_course(course), '영어2')
                self.assertEqual(course_policy(course),
                    {'course': '영어2', 'reference_grade': 2, 'mock_questions_per_round': 7})
        for course in ['공통영어1', '공통영어2']:
            self.assertEqual(course_policy(course),
                {'course': course, 'reference_grade': 1, 'mock_questions_per_round': 5})


if __name__ == '__main__':
    unittest.main()
