import time


class VowelReaderService:
    VOWELS = 'aeiouáéíóúãõ'
    CONSONANTS = 'bcdfghjklmnpqrstvwxyzç'

    @classmethod
    def get_reading_data(cls, data: str) -> dict:
        start = time.time_ns()
        vowel = cls.get_vowel(data)
        end = time.time_ns()

        return {
            "string": data,
            "vogal": vowel,
            "tempoTotal": f"{(end - start) * 1e3:.2f}ms"
        }

    @classmethod
    def get_vowel(cls, chars: str) -> str | None:
        already_found_vowels = []
        candidate_vowels = []

        for i in range(2, len(chars)):
            current_char = chars[i]
            past_char = chars[i - 1]
            double_past_char = chars[i - 2]

            if not cls.is_in_alphabet(current_char):
                continue

            if (
                    current_char not in already_found_vowels
                    and
                    cls.is_vowel(double_past_char)
                    and
                    cls.is_consonant(past_char)
                    and
                    cls.is_vowel(current_char)
            ):
                candidate_vowels.append(current_char)

            if cls.is_vowel(current_char):
                already_found_vowels.append(current_char)

        for candidate_vowel in candidate_vowels:
            if already_found_vowels.count(candidate_vowel) == 1:
                return candidate_vowel

        return None

    @classmethod
    def is_vowel(cls, char: str) -> bool:
        return char.lower() in cls.VOWELS

    @classmethod
    def is_consonant(cls, char: str) -> bool:
        return char.lower() in cls.CONSONANTS

    @classmethod
    def is_in_alphabet(cls, char: str) -> bool:
        return (
                char.lower() in (cls.VOWELS + cls.CONSONANTS)
                or
                char.isalpha()
        )
