import unittest

from api.services.vowel_reader import VowelReaderService


class VowelReaderTestCase(unittest.TestCase):
    def test_reader__on_happy_path__should_return_vowel(self):
        input_string = " aAbBABacafe"
        vowel = VowelReaderService.get_vowel(input_string)
        self.assertEqual(vowel, "e")


    def test_reader__no_valid_vowels__should_return_none(self):
        input_string = " aAbBABacaf"
        vowel = VowelReaderService.get_vowel(input_string)
        self.assertEqual(vowel, None)
