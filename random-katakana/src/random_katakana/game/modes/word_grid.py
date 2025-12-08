from collections import Counter

from ...ui.ui import UI
from .grid_generator import WordGrid
from .mode import Mode
from ...word_loader.word import Word


class WordSearchPuzzle(Mode):
    _GRID_GENERATOR = WordGrid()

    def __init__(self, UI: UI, words: list[Word]):
        super().__init__(UI, words)

    def start(self) -> None:
        DEBUG = True

        UNIQUE_LETTERS = {
            LETTER for WORD in self.WORDS for LETTER in WORD.get("katakana")
        }
        FILLER_LETTERS = frozenset({"ー"} if DEBUG else UNIQUE_LETTERS)
        RESULT = self._GRID_GENERATOR.generate_grid(self.WORDS, 3, FILLER_LETTERS)

        for ROW in RESULT["grid"]:
            self.UI.show_text(f"{" ".join(ROW)}")

        ANSWER = RESULT.get("words")

        if DEBUG:
            self.UI.show_text(f"Spoilers: {ANSWER}\n")

        RESPONSE = self.UI.request_input(
            "Which words can you spot? Enter all 3 separated by commas:\n"
        )

        if Counter(RESPONSE.split(",")) == Counter(ANSWER):
            return self.UI.show_text("Correct!")

        return self.UI.show_text(f"Wrong! The correct answers were: {ANSWER}")
