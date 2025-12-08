from secrets import choice
from typing import Generator
from ...ui.ui import UI
from .mode import Mode
from ...word_loader.word import Word


class StandardQuiz(Mode):
    def __init__(self, UI: UI, WORDS: list[Word]):
        super().__init__(UI, WORDS)

    def _progressive_reveal(self, word: str, MAX_CALLS: int) -> Generator[str]:
        LEGNTH = len(word)

        for INDEX in range(1, MAX_CALLS + 1):
            PERCENT = INDEX / MAX_CALLS
            REVEAL_COUNT = int(LEGNTH * PERCENT)
            REVEALED = f"{word[:REVEAL_COUNT]}{"_" * (LEGNTH - REVEAL_COUNT)}"
            yield REVEALED

    def start(self) -> None:
        WORD: Word = choice(self.WORDS)
        KATAKANA: str = WORD.get("katakana")
        MEANING: str = WORD.get("meaning")
        ROMANJI: str = WORD.get("romanji")

        HINT_GENERATOR: Generator[str] = self._progressive_reveal(MEANING, 3)
        hint = ""

        while True:
            HINT_TEXT = f"Hint: {hint}" if hint != "" else ""
            ANSWER = self.UI.request_input(
                text=f"{HINT_TEXT}\nWhat is the meaning of the word: {KATAKANA}\n"
            )

            if ANSWER.lower() == MEANING.lower():
                self.UI.show_text(f"Correct! {MEANING} means {KATAKANA} ({ROMANJI})")
                break
            elif ANSWER.lower() == ROMANJI.lower():
                self.UI.show_text(
                    "Correct! This is the romanji reading. What is the meaning?"
                )
                continue

            self.UI.show_text(f"Wrong!")
            TRY_AGAIN = self.UI.request_input("Do you want to try again? (y/N/hint)\n")

            if TRY_AGAIN == "hint":
                hint = next(HINT_GENERATOR)
            elif TRY_AGAIN == "N":
                self.UI.show_text(f"The correct answer is: {MEANING} ({ROMANJI})")
                break
