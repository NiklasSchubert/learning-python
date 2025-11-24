from ..ui.ui import UI
from ..word_loader.word import Word
from ..word_loader.word_loader import WordLoader
from .modes.mode import Mode
from .modes.quiz import StandardQuiz
from .modes.word_grid import WordSearchPuzzle


class Game:
    GAME_MODES: dict[int, type[Mode]] = {1: StandardQuiz, 2: WordSearchPuzzle}
    GAME_OPTIONS: dict[int, str] = {
        1: "Standard Quiz",
        2: "Word Search",
        3: "Exit Game",
    }

    _WORDS: list[Word] = []

    def __init__(self, LOADER: WordLoader, UI: UI):
        self._WORDS = LOADER.load()

        while True:
            try:
                RESPONSE = UI.ask_option(
                    "What mode do you want to play?", self.GAME_OPTIONS
                )

                GAME_MODE = self.GAME_MODES.get(RESPONSE, None)
                if GAME_MODE != None:
                    MODE = GAME_MODE(self._WORDS)
                    MODE.question()

                if RESPONSE == 3:
                    break
            except Exception as e:
                print(f"An error occurred: {e} \n")
                input()
