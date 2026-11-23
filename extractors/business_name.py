
import json
import html


BUSINESS_SCHEMA_TYPES = {
    "organization",
    "localbusiness",
    "travelagency",
    "touristinformationcenter",
}

NON_BUSINESS_SCHEMA_TYPES = {
    "article",
    "person",
    "postaladdress",
    "thing",
    "webpage",
    "website",
}


def schema_types(data):

    schema_type = data.get("@type", [])

    if isinstance(schema_type, str):
        schema_type = [schema_type]

    return {
        item.rstrip("/").split("/")[-1].lower()
        for item in schema_type
        if isinstance(item, str)
    }


def is_business_schema_entity(data):

    types = schema_types(data)
    if types.intersection(BUSINESS_SCHEMA_TYPES):
        return True

    has_contact_data = bool({"address", "telephone", "email"}.intersection(data))
    return has_contact_data and (
        not types or bool(types - NON_BUSINESS_SCHEMA_TYPES)
    )


def find_schema_business_name(data):

    if isinstance(data, list):

        for item in data:
            name = find_schema_business_name(item)

            if name:
                return name

    elif isinstance(data, dict):

        if is_business_schema_entity(data):

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


def extract_microdata_name(soup):

    business_scopes = soup.find_all(
        attrs={"itemscope": True, "itemtype": True}
    )

    for scope in business_scopes:
        item_type = scope.get("itemtype", "")
        if not isinstance(item_type, str):
            continue

        schema_type = item_type.rstrip("/").split("/")[-1].lower()
        has_contact_property = scope.find(
            attrs={"itemprop": lambda value: value and
                   {"address", "telephone", "email"}.intersection(
                       value.split()
                   )}
        )
        if (
            schema_type not in BUSINESS_SCHEMA_TYPES
            and (
                schema_type in NON_BUSINESS_SCHEMA_TYPES
                or not has_contact_property
            )
        ):
            continue

        name_element = scope.find(
            attrs={"itemprop": lambda value: value and "name" in value.split()}
        )
        if name_element:
            name = name_element.get("content") or name_element.get_text(
                strip=True
            )
            if name:
                return html.unescape(name.strip())

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

    # 3. Try Schema.org microdata
    name = extract_microdata_name(soup)

    if name:
        return name

    # 4. Try standard application metadata
    application_name = soup.find(
        "meta",
        attrs={"name": "application-name"}
    )

    if application_name:
        name = application_name.get("content", "").strip()

        if name:
            return html.unescape(name).strip()

    # 5. Fallback to HTML title
    if soup.title:
        title = soup.title.get_text(strip=True)

        if title:
            return html.unescape(title).strip()

    return "Unknown Business"
