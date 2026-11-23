
import json

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

        # Check whether this is the requested business
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
                result = find_address_data(value, business_name)

                if result:
                    return result

    return None



    


def extract_address(soup, business_name=None):

    scripts = soup.find_all(
        "script",
        type="application/ld+json"
    )

    for script in scripts:

        try:
            data = json.loads(script.get_text(strip=True))

        except json.JSONDecodeError:
            continue

        address_data = find_address_data(data, business_name)

        if not address_data:
            continue

        country = address_data.get("addressCountry", "")

        # Sometimes country is itself a dictionary
        if isinstance(country, dict):
            country = country.get("name", "")

        address = address_data.get("streetAddress", "")

        city = address_data.get("addressLocality", "")
        state_province = address_data.get("addressRegion", "")

        # Fallback: identify missing city and country from address text
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
                "json_ld"
                if address
                else ""
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
