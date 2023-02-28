from enum import Enum

BASE_IMDB_URL = "https://imdb.com"

EVENT_CODES = {
    "OSCARS": "ev0000003",
    "GOLDEN_GLOBES": "ev0000292",
    "CRITICS_CHOICE": "ev0000133",
    "DIRECTORS_GUILD": "ev0000212",
    "BAFTA": "ev0000123",
    "PRODUCERS_GUILD": "ev0000531",
    "SCREEN_ACTORS_GUILD": "ev0000598",
    "FILM_INDEPENDENT_SPIRIT": "ev0000349",
    # Add film festivals: SUNDANCE, TORONTO, BERLIN, VENICE, CANNES
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "Referer": "https://targetwebsite.com/page1",
}


class EntityType(str, Enum):
    TITLE = "title"
    NAME = "name"
    EVENT = "event"
    COMPANY = "company"


HREF_TO_ENTITY = {
    "title": EntityType.TITLE,
    "name": EntityType.NAME,
    "event": EntityType.EVENT,
    "company": EntityType.COMPANY,
}
