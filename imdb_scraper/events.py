from .const import BASE_IMDB_URL, HEADERS, EntityType
import requests
from bs4 import BeautifulSoup
from .norm import parse_entity_id
from json import JSONDecoder


def get_event(event_id, year, event_cache=None):
    """

    Args:
        event_id (_type_): _description_
        year (_type_): _description_
        event_cache (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    if event_cache is not None and (event_id, year) in event_cache:
        return event_cache[event_id, year]

    page = requests.get(f"{BASE_IMDB_URL}/event/{event_id}/{year}", headers=HEADERS)
    soup = BeautifulSoup(page.text, "html.parser")

    react_script_span = (
        soup.find("span", {"class": "ab_widget"})
        .find("script", {"type": "text/javascript"})
        .text
    )
    react_data = react_script_span[react_script_span.find('{"nomineesWidgetModel') :]
    bracket_count = 0
    end = len(react_data)
    for idx, char in enumerate(react_data):
        if char == "{":
            bracket_count += 1
        elif char == "}":
            bracket_count -= 1
        if bracket_count == 0:
            end = idx + 1
            break

    react_data = react_data[:end]
    react_json = JSONDecoder().decode(react_data)

    awards = react_json["nomineesWidgetModel"]["eventEditionSummary"]["awards"]
    event = []

    for award in awards:
        award_name = award["awardName"]
        for category in award["categories"]:
            formatted_category = {
                "award": award_name,
                "category": category["categoryName"],
                "noms": [],
            }

            for nom in category["nominations"]:
                if len(nom["primaryNominees"]) == 0:
                    continue
                formatted_category["noms"].append(
                    {
                        "name": nom["primaryNominees"][0]["name"],
                        "is_winner": nom["isWinner"],
                        "secondary_names": [
                            secondary["name"] for secondary in nom["secondaryNominees"]
                        ],
                        "secondary_ids": [
                            secondary["const"] for secondary in nom["secondaryNominees"]
                        ],
                        **parse_entity_id(nom["primaryNominees"][0]["const"]),
                    }
                )

            event.append(formatted_category)
    if event_cache is not None:
        event_cache[(event_id, year)] = event
    return event
