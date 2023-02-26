""" Normalizing IMDB fields """
from .const import EntityType
import json


def pretty_print(obj):
    print(json.dumps(obj), indent=4)


def parse_href(href):
    if len(href) == 0:
        raise Exception("Empty href")
    if href[0] == "/":
        href = href[1:]

    href_parts = href.split("/")
    if len(href_parts) < 2:
        raise Exception("href too short to be parsed")

    entity_type = HREF_TO_ENTITY[href_parts[0]]
    entity_id = href_parts[1]
    if entity_type == EntityType.EVENT:
        if len(href_parts) < 3:
            raise Exception("event href too short to be parsed")
        return {
            "entity_type": entity_type,
            "entity_id": entity_id,
            "year": href_parts[2],
        }

    return {entity_type, entity_id}


def parse_entity_id(entity_id):
    if len(entity_id) < 3:
        raise Exception(f"entity_id '{entity_id}' too short")
    if entity_id[:2] == "tt":
        return {"entity_type": EntityType.TITLE, "entity_id": entity_id}
    elif entity_id[:2] == "nm":
        return {"entity_type": EntityType.NAME, "entity_id": entity_id}
    elif entity_id[:2] == "ev":
        return {"entity_type": EntityType.EVENT, "entity_id": entity_id}
    elif entity_id[:2] == "co":
        return {"entity_type": EntityType.COMPANY, "entity_id": entity_id}
    else:
        raise Exception(f"can't parse entity_id '{entity_id}'")


HREF_TO_ENTITY = {
    "title": EntityType.TITLE,
    "name": EntityType.NAME,
    "event": EntityType.EVENT,
    "company": EntityType.COMPANY,
}


def normalize_oscar_category(name):
    if name is None:
        return ""
    if name in OSCAR_CATEGORIES_NORM:
        return OSCAR_CATEGORIES_NORM[name]
    return name


OSCAR_CATEGORIES_NORM = {
    "Best Motion Picture of the Year": "PICTURE",
    "Best Picture": "PICTURE",
    "Best Performance by an Actor in a Leading Role": "ACTOR_LEAD",
    "Best Actor in a Leading Role": "ACTOR_LEAD",
    "Best Performance by an Actress in a Leading Role": "ACTRESS_LEAD",
    "Best Actress in a Leading Role": "ACTRESS_LEAD",
    "Best Performance by an Actor in a Supporting Role": "ACTOR_SUP",
    "Best Actor in a Supporting Role": "ACTOR_SUP",
    "Best Performance by an Actress in a Supporting Role": "ACTRESS_SUP",
    "Best Actress in a Supporting Role": "ACTRESS_SUP",
    "Best Achievement in Directing": "DIRECTOR",
    "Best Director": "DIRECTOR",
    "Best Original Screenplay": "SCREENPLAY_OG",
    "Best Writing, Screenplay Based on Material from Another Medium": "SCREENPLAY_OG",
    "Best Adapted Screenplay": "SCREENPLAY_AD",
    "Best Writing, Adapted Screenplay": "SCREENPLAY_AD",
    "Best Achievement in Cinematography": "CINEMATOGRAPHY",
    "Best Cinematography": "CINEMATOGRAPHY",
    "Best Achievement in Film Editing": "EDITING",
    "Best Film Editing": "EDITING",
    "Best Achievement in Production Design": "DESIGN_PROD",
    "Best Art Direction-Set Decoration": "DESIGN_PROD",
    "Best Achievement in Costume Design": "DESIGN_COST",
    "Best Costume Desgin": "DESIGN_COST",
    "Best Sound": "SOUND",
    "Best Achievement in Makeup and Hairstyling": "MAKEUP",
    "Best Achievement in Music Written for Motion Pictures (Original Score)": "MUSIC_SCORE",
    "Best Achievement in Music Written for Motion Pictures, Original Score": "MUSIC_SCORE",
    "Best Achievement in Music Written for Motion Pictures (Original Song)": "MUSIC_SONG",
    "Best Achievement in Visual Effects": "VFX",
    "Best Effects, Special Visual Effects": "VFX",
    # Miscs
    "Best Documentary Feature": "DOC_FEAT",
    "Best Documentary Short Subject": "DOC_SHORT",
    "Best Animated Feature Film": "ANIMATED_FEAT",
    "Best Animated Short Film": "ANIMATED_SHORT",
    "Best Live Action Short Film": "LIVE_SHORT",
    "Best International Feature Film": "INTERNATIONAL",
}
