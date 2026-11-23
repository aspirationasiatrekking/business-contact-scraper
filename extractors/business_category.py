import json
import re

from extractors.business_name import (
    BUSINESS_SCHEMA_TYPES,
    NON_BUSINESS_SCHEMA_TYPES,
    is_business_schema_entity,
)


GENERIC_SCHEMA_TYPES = {
    "organization",
    "localbusiness",
}

SCHEMA_TYPE_LABELS = {
    "localbusiness": "Local Business",
    "organization": "Organization",
    "touristinformationcenter": "Tourist Information Center",
    "travelagency": "Travel Agency",
}

def _iter_schema_objects(data):

    if isinstance(data, dict):
        yield data

        for value in data.values():
            yield from _iter_schema_objects(value)

    elif isinstance(data, list):
        for item in data:
            yield from _iter_schema_objects(item)


def _format_category(schema_type):

    normalized_type = schema_type.lower()
    if normalized_type in SCHEMA_TYPE_LABELS:
        return SCHEMA_TYPE_LABELS[normalized_type]

    words = re.sub(r"([a-z])([A-Z])", r"\1 \2", schema_type)
    return words.replace("_", " ").strip()


def extract_business_category(soup):

    categories = []

    for script in soup.find_all(
        "script",
        type="application/ld+json"
    ):
        try:
            data = json.loads(script.get_text(strip=True))
        except (json.JSONDecodeError, TypeError):
            continue

        for entity in _iter_schema_objects(data):
            if not is_business_schema_entity(entity):
                continue

            schema_type = entity.get("@type", [])
            if isinstance(schema_type, str):
                schema_type = [schema_type]

            types = [
                item.rstrip("/").split("/")[-1]
                for item in schema_type
                if isinstance(item, str)
                and item.rstrip("/").split("/")[-1].lower()
                not in NON_BUSINESS_SCHEMA_TYPES
            ]
            specific_types = [
                item for item in types
                if item.lower() not in GENERIC_SCHEMA_TYPES
            ]
            categories.extend(specific_types or types)

    if categories:
        return _format_category(categories[0])

    for scope in soup.find_all(
        attrs={"itemscope": True, "itemtype": True}
    ):
        item_type = scope.get("itemtype", "")
        if not isinstance(item_type, str):
            continue

        schema_type = item_type.rstrip("/").split("/")[-1]
        has_business_properties = scope.find(
            attrs={
                "itemprop": lambda value: value and
                {"address", "telephone", "email"}.intersection(value.split())
            }
        )
        if (
            schema_type.lower() in BUSINESS_SCHEMA_TYPES
            or has_business_properties
        ):
            return _format_category(schema_type)

    return ""
