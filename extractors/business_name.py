
import json
import html


BUSINESS_SCHEMA_TYPES = {
    "organization",
    "localbusiness",
    "travelagency",
    "touristinformationcenter",
}


def find_schema_business_name(data):

    if isinstance(data, list):

        for item in data:
            name = find_schema_business_name(item)

            if name:
                return name

    elif isinstance(data, dict):

        schema_type = data.get("@type", [])

        if isinstance(schema_type, str):
            schema_type = [schema_type]

        normalized_types = {
            item.rstrip("/").split("/")[-1].lower()
            for item in schema_type
            if isinstance(item, str)
        }

        if normalized_types.intersection(BUSINESS_SCHEMA_TYPES):

            name = data.get("name")

            if isinstance(name, str) and name.strip():
                return html.unescape(name.strip())

        # Search nested objects, including @graph
        for value in data.values():

            if isinstance(value, (dict, list)):
                name = find_schema_business_name(value)

                if name:
                    return name

    return None


def extract_business_name(soup):

    # 1. Try Schema.org JSON-LD
    scripts = soup.find_all(
        "script",
        type="application/ld+json"
    )

    for script in scripts:

        try:
            data = json.loads(script.get_text(strip=True))

        except (json.JSONDecodeError, TypeError):
            continue

        name = find_schema_business_name(data)

        if name:
            return name

    # 2. Try Open Graph site name
    og_name = soup.find(
        "meta",
        property="og:site_name"
    )

    if og_name:
        name = og_name.get("content", "").strip()

        if name:
            return html.unescape(name).strip()

    # 3. Fallback to HTML title
    if soup.title:
        title = soup.title.get_text(strip=True)

        if title:
            return html.unescape(title).strip()

    return "Unknown Business"
