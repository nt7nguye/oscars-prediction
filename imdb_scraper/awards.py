from .const import BASE_IMDB_URL, HEADERS, EntityType
import requests
from bs4 import BeautifulSoup


def get_awards(
    entity_type,
    entity_id,
    awards_cached=None,
):
    if awards_cached is not None and (entity_type, entity_id) in awards_cached:
        return awards_cached[(entity_type, entity_id)]
    if entity_type == EntityType.EVENT:
        raise Exception(f"Entity type not supported {entity_type}")
    page = requests.get(
        f"{BASE_IMDB_URL}/{entity_type}/{entity_id}/awards", headers=HEADERS
    )
    soup = BeautifulSoup(page.text, "html.parser")
    awards = parse_awards(soup)
    if awards_cached is not None:
        awards_cached[(entity_type, entity_id)] = awards
    return awards


def parse_awards(soup):
    events = []

    event_h3 = (
        soup.find("div", {"class": ["article", "listo"]})
        .find("div", {"class": "header"})
        .find_next_sibling("h3")
    )
    while event_h3:
        award_table = event_h3.find_next_sibling("table")
        award_outcomes = award_table.find_all(
            "td", {"class": "title_award_outcome"}, recursive=True
        )
        award_descs = award_table.find_all(
            "td", {"class": "award_description"}, recursive=True
        )

        cat_idx = 0
        for award_outcome in award_outcomes:
            span = award_outcome["rowspan"]
            for i in range(int(span)):
                award_desc = award_descs[cat_idx]
                outcome = {
                    "result": award_outcome.b.text,
                    "award": award_outcome.span.text,
                    "category": award_desc,
                }
                events.append(outcome)
                cat_idx += 1

        event_h3 = event_h3.find_next_sibling("h3")
    return events
