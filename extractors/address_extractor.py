
import json
import re

from geotext import GeoText


def find_address_data(data, business_name=None):

    if isinstance(data, list):

        for item in data:
            result = find_address_data(item, business_name)

            if result:
                return result

    elif isinstance(data, dict):

        address = data.get("address")
        name = data.get("name", "")

        if not isinstance(name, str):
            name = ""

        name_matches = (
            business_name is None
            or name.strip().casefold() == business_name.strip().casefold()
        )

        if name_matches:

            if isinstance(address, dict):
                return address

            if isinstance(address, str) and address.strip():
                return {
                    "streetAddress": address.strip()
                }

        # Search nested objects, including @graph
        for value in data.values():

            if isinstance(value, (dict, list)):

                result = find_address_data(
                    value,
                    business_name
                )

                if result:
                    return result

    return None


def extract_visible_address(soup):

    # Find elements containing a map-marker icon
    markers = soup.find_all(
        "i",
        class_="fa-map-marker"
    )

    for marker in markers:

        # Find the contact item containing the icon
        container = marker.find_parent(
            class_="contact-info__item"
        )

        if not container:
            continue

        # Find the corresponding text
        text_element = container.find(
            class_="contact-info__item__text"
        )

        if not text_element:
            continue

        address = text_element.get_text(
            separator=" ",
            strip=True
        )

        if address:
            return address

    return ""



def build_address_result(
    address,
    city="",
    state_province="",
    country="",
    source=""
):

    return {
        "address": address,
        "city": city,
        "state_province": state_province,
        "country": country,

        "address_source": source,

        "city_source": (
            source if city else ""
        ),

        "country_source": (
            source if country else ""
        )
    }


def extract_address_from_json_ld(soup, business_name=None):

    scripts = soup.find_all(
        "script",
        type="application/ld+json"
    )

    for script in scripts:

        try:
            data = json.loads(
                script.get_text(strip=True)
            )

        except (json.JSONDecodeError, TypeError):
            continue

        address_data = find_address_data(
            data,
            business_name
        )

        if not address_data:
            continue

        country = address_data.get("addressCountry", "")

        if isinstance(country, dict):
            country = country.get("name", "")

        address = address_data.get("streetAddress", "")

        city = address_data.get("addressLocality", "")
        state_province = address_data.get("addressRegion", "")

        # GeoText fallback
        if address:

            places = GeoText(address)

            if not city and places.cities:
                city = places.cities[0]

            if not country and places.countries:
                country = places.countries[0]

        return {
            "address": address,
            "city": city,
            "state_province": state_province,
            "country": country,

            "address_source": (
                "json_ld" if address else ""
            ),

            "city_source": (
                "json_ld"
                if address_data.get("addressLocality")
                else "geotext"
                if city
                else ""
            ),

            "country_source": (
                "json_ld"
                if address_data.get("addressCountry")
                else "geotext"
                if country
                else ""
            )
        }

    return None


def _itemprop_tokens(element):

    value = element.get("itemprop", "")
    if isinstance(value, str):
        return value.split()
    if isinstance(value, list):
        return value
    return []


def _microdata_value(element):

    for attribute in ("content", "datetime", "href"):
        value = element.get(attribute)
        if value:
            return str(value).strip()

    return element.get_text(separator=" ", strip=True)


def _microdata_properties(scope):

    properties = {}

    for element in [scope] + scope.find_all(attrs={"itemprop": True}):
        value = _microdata_value(element)
        if not value:
            continue

        for token in _itemprop_tokens(element):
            properties.setdefault(token.lower(), value)

    return properties


def extract_address_from_microdata(soup, business_name=None):

    candidates = []

    for element in soup.find_all(attrs={"itemprop": True}):
        if "address" in _itemprop_tokens(element):
            candidates.append(element)

    for element in soup.find_all(
        attrs={"itemscope": True, "itemtype": True}
    ):
        item_type = element.get("itemtype", "")
        if (
            isinstance(item_type, str)
            and item_type.rstrip("/").split("/")[-1].lower()
            == "postaladdress"
        ):
            candidates.append(element)

    for element in candidates:
        scope = (
            element
            if element.has_attr("itemscope")
            else element.find_parent(attrs={"itemscope": True})
        )
        scope = scope or element

        properties = _microdata_properties(scope)
        names = properties.get("name", "").strip()
        ancestor_scopes = scope.find_parents(attrs={"itemscope": True})
        for ancestor in ancestor_scopes:
            ancestor_name = _microdata_properties(ancestor).get(
                "name",
                ""
            ).strip()
            if ancestor_name:
                names = ancestor_name
                break

        if (
            business_name
            and names
            and names.casefold() != business_name.strip().casefold()
        ):
            continue

        address = (
            properties.get("streetaddress")
            or properties.get("address")
            or _microdata_value(element)
        )
        city = properties.get("addresslocality", "")
        state_province = properties.get("addressregion", "")
        country = properties.get("addresscountry", "")

        if address or city or state_province or country:
            return build_address_result(
                address=address,
                city=city,
                state_province=state_province,
                country=country,
                source="microdata"
            )

    return None


def extract_address_from_visible_text(soup):

    candidates = []

    # 1. Find semantic address elements
    elements = soup.find_all(
        ["address", "p", "li", "div", "span"]
    )

    for element in elements:

        attributes = " ".join(
            element.get("class", [])
        )

        attributes += " " + element.get("id", "")

        attributes = attributes.lower()

        text = element.get_text(
            separator=" ",
            strip=True
        )

        if not text:
            continue

        # Ignore excessively large content blocks
        if len(text) > 300:
            continue

        # Look for address-related HTML attributes
        if (
            element.name == "address"
            or "address" in attributes
            or "location" in attributes
        ):

            candidates.append(text)

        # Look for explicitly labelled addresses
        elif re.search(
            r"\b(address|office address|our location|office location)\b",
            text,
            re.IGNORECASE
        ):

            candidates.append(text)

    # Remove duplicate candidates
    candidates = list(dict.fromkeys(candidates))

    # 2. Inspect candidates
    for candidate in candidates:

        # Remove common address labels
        address = re.sub(
            r"^(office address|address|our location|office location)\s*[:\-]?\s*",
            "",
            candidate,
            flags=re.IGNORECASE
        ).strip()

        if len(address) < 5:
            continue

        places = GeoText(address)

        city = places.cities[0] if places.cities else ""
        country = places.countries[0] if places.countries else ""

        return build_address_result(
            address=address,
            city=city,
            country=country,
            source="visible_text"
        )

    return None


def extract_address(soup, business_name=None):

    # Priority 1: JSON-LD
    address_data = extract_address_from_json_ld(
        soup,
        business_name
    )

    if address_data:
        return address_data

    # Priority 2: Schema.org microdata
    address_data = extract_address_from_microdata(
        soup,
        business_name
    )

    if address_data:
        return address_data

    # Priority 3: Visible HTML text
    address = extract_visible_address(soup)

    if address:
        places = GeoText(address)
        return build_address_result(
            address=address,
            city=places.cities[0] if places.cities else "",
            country=places.countries[0] if places.countries else "",
            source="visible_text"
        )

    address_data = extract_address_from_visible_text(
        soup
    )

    if address_data:
        return address_data

    return None
