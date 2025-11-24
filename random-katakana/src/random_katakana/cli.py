from pprint import pprint
from .word_loader.word_loader import WordLoader
from .word import Word
from random import sample, choice
from abc import ABC, abstractmethod
from .word_loader.sensei_japanese_loader import SenseiJapaneseLoader


class Grid:
    rows: list[list[str]]


class Mode(ABC):

    @abstractmethod
    def question(self):
        pass

    @abstractmethod
    def validate(self):
        pass


class WordSearchPuzzle(Mode):
    def __init__(self, words: list[Word]):
        self.words = words

    def question(self):
        pass

    def validate(self):
        pass


class StandardQuiz(Mode):
    def __init__(self, LOADER: WordLoader = SenseiJapaneseLoader):
        super().__init__()

    def question(self):
        pass

    def validate(self):
        pass


class Game:
    def __init__(self, MODE: Mode):
        self.MODE = MODE


class CLI:
    _words: list[Word] = []

    def __init__(self, LOADER: WordLoader):
        self._words = LOADER.load()
        while True:
            mode = input(
                """Choose a mode:
    1. Word Search Puzzle
    2. Standard Quiz\n"""
            )

            

            if mode == "1":


    def createWordFinder(self):
        WORDS: list[Word] = sample(self._words, 3)

    def suggestWord(self):
        WORD: Word = choice(self._words)
        KATAKANA = WORD.get("katakana")
        MEANING = WORD.get("meaning")
        ROMANJI = WORD.get("romanji")

        HINT = iter(MEANING)

        retry = True
        currentHint = ""

        while retry:
            retry = False

            ANSWER = input(
                f"What is the meaning of the word: {KATAKANA} \n{f"Hint: {currentHint}" if currentHint != '' else ''}\n"
            )

            if ANSWER == MEANING:
                print(f"Correct! {MEANING} means {KATAKANA} ({ROMANJI})")
            elif ANSWER == ROMANJI:
                print("Correct! This is the romanji reading. What is the meaning?")
                retry = True
            else:
                print(f"Wrong!")
                TRY_AGAIN = input("Do you want to try again? (y/N/hint)\n")
                if TRY_AGAIN == "y":
                    retry = True
                elif TRY_AGAIN == "hint":
                    retry = True
                    currentHint = f"{currentHint}{next(HINT)}"
                else:
                    print(f"The correct answer is: {MEANING} ({ROMANJI})")

            print("\n")
