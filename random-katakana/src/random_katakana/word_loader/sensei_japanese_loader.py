from .word_loader import WordLoader
from requests import get
from lxml import etree
from .word import Word


class SenseiJapaneseLoader(WordLoader):
    def load(self) -> list[Word]:
        RESPONSE = get(
            "https://senseijapanese.com/beginning-with-japanese/most-used-250-katakana-words/"
        ).text

        PARSED_HTML = etree.HTML(RESPONSE)
        TABLE_BODIES = PARSED_HTML.xpath("//table//tbody")

        COLUMNS: list[str] = [
            COLUMN.text or ""
            for BODY in TABLE_BODIES
            for COLUMN in BODY.xpath(".//td")[3:]
        ]

        # COLUMNS: list[str] = []
        # for BODY in TABLE_BODIES:
        #     # BODY.xpath(...) should normally return a list; guard against unexpected types
        #     cells = BODY.xpath(".//td")
        #     if not isinstance(cells, (list, tuple)):
        #         continue
        #     for COLUMN in cells[3:]:
        #         COLUMNS.append(COLUMN.text or "")

        WORDS: list[Word] = [
            {"katakana": k, "romanji": r, "meaning": m}
            for k, r, m in zip(*(iter(COLUMNS),) * 3)
        ]

        return WORDS
