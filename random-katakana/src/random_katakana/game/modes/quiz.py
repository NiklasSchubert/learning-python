from secrets import choice
from typing import Generator
from .mode import Mode
from ...word_loader.word import Word


class StandardQuiz(Mode):
    def __init__(self, WORDS: list[Word]):
        super().__init__(WORDS)

    def _progressive_reveal(self, word: str, MAX_CALLS: int) -> Generator[str]:
        LEGNTH = len(word)

        for INDEX in range(1, MAX_CALLS + 1):
            PERCENT = INDEX / MAX_CALLS
            REVEAL_COUNT = int(LEGNTH * PERCENT)
            REVEALED = f"{word[:REVEAL_COUNT]}{"_" * (LEGNTH - REVEAL_COUNT)}"
            yield REVEALED

    def question(self) -> str:
        WORD: Word = choice(self.WORDS)
        KATAKANA: str = WORD.get("katakana")
        MEANING: str = WORD.get("meaning")
        ROMANJI: str = WORD.get("romanji")

        HINT: Generator[str] = self._progressive_reveal(MEANING, 3)
        current_hint = ""

        while True:
            HINT_TEXT = f"Hint: {current_hint}" if current_hint != "" else ""
            ANSWER = input(
                f"{HINT_TEXT}\nWhat is the meaning of the word: {KATAKANA}\n"
            )

            if ANSWER.lower() == MEANING.lower():
                return f"Correct! {MEANING} means {KATAKANA} ({ROMANJI})"
            elif ANSWER.lower() == ROMANJI.lower():
                print("Correct! This is the romanji reading. What is the meaning?")
                continue

            print(f"Wrong!")
            TRY_AGAIN = input("Do you want to try again? (y/N/hint)\n")

            if TRY_AGAIN == "hint":
                current_hint = next(HINT)
            elif TRY_AGAIN == "N":
                return f"The correct answer is: {MEANING} ({ROMANJI})"
            print("\n")

        return ""
