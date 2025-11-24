from .word_loader import WordLoader
from requests import get
from lxml import etree
from lxml.etree import _Element
from ..word import Word


class SenseiJapaneseLoader(WordLoader):
    def load(self) -> list[Word]:
        RESPONSE = get(
            "https://senseijapanese.com/beginning-with-japanese/most-used-250-katakana-words/"
        ).text

        PARSED_HTML = etree.HTML(RESPONSE)
        TABLE_BODIES: list[_Element] = PARSED_HTML.xpath("//table//tbody")

        COLUMNS: list[list[str]] = [
            COLUMN.text or ""
            for BODY in TABLE_BODIES
            for COLUMN in BODY.xpath(".//td")[3:]
        ]

        WORDS: list[Word] = [
            {"katakana": k, "romanji": r, "meaning": m}
            for k, r, m in zip(*(iter(COLUMNS),) * 3)
        ]

        return WORDS
