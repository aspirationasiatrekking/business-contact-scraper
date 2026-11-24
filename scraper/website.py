
import requests
from bs4 import BeautifulSoup

from extractors.address_extractor import extract_address
from extractors.business_name import extract_business_name
from extractors.phone_extractor import extract_phone_numbers
from extractors.contacts import extract_emails, extract_mailto_emails

from scraper.contact_page_finder import find_contact_pages
from models.business import Business


def scrape_website(url, category=""):

    try:
        # 1. Download homepage
        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.content,
            "html.parser"
        )

        # 2. Extract business name
        business_name = extract_business_name(soup)

        print(f"Extracted business name: {business_name}")

        # 3. Extract homepage address
        address_data = extract_address(
            soup,
            business_name=business_name
        ) or {}

        # 4. Extract homepage emails and phone numbers
        text_content = soup.get_text(
            separator="\n",
            strip=True
        )

        emails = extract_emails(text_content)
        emails.extend(extract_mailto_emails(soup))

        phone_numbers = extract_phone_numbers(text_content)

        # 5. Discover contact and about pages
        contact_pages = find_contact_pages(
            soup,
            response.url
        )

        print(
            f"Found {len(contact_pages)} contact/about pages"
        )

        # 6. Visit contact and about pages
        for index, page_url in enumerate(
            contact_pages,
            start=1
        ):

            print(f"  Contact page {index}: {page_url}")

            try:
                page_response = requests.get(
                    page_url,
                    timeout=15,
                    headers={"User-Agent": "Mozilla/5.0"}
                )

                page_response.raise_for_status()

                page_soup = BeautifulSoup(
                    page_response.content,
                    "html.parser"
                )

                page_text = page_soup.get_text(
                    separator="\n",
                    strip=True
                )

                # Extract emails
                page_emails = extract_emails(page_text)

                page_emails.extend(
                    extract_mailto_emails(page_soup)
                )

                emails.extend(page_emails)

                # Extract phone numbers
                page_phones = extract_phone_numbers(
                    page_text
                )

                phone_numbers.extend(page_phones)

                # Extract address if homepage data is incomplete
                page_address = extract_address(
                    page_soup,
                    business_name=business_name
                ) or {}

                for field in [
                    "address",
                    "city",
                    "state_province",
                    "country"
                ]:

                    if not address_data.get(field) and page_address.get(field):
                        address_data[field] = page_address[field]

                # Preserve the source of each extracted field
                for field in [
                    "address_source",
                    "city_source",
                    "country_source"
                ]:

                    if not address_data.get(field) and page_address.get(field):
                        address_data[field] = page_address[field]

            except requests.RequestException as error:

                print(
                    f"Contact page failed: {page_url} - {error}"
                )

        # 7. Remove duplicate contact details
        emails = list(dict.fromkeys(emails))

        phone_numbers = list(
            dict.fromkeys(phone_numbers)
        )

        # 8. Return Business object
        return Business(
            name=business_name,
            website=response.url,
            category=category,

            emails=emails,
            phone_numbers=phone_numbers,

            address=address_data.get("address", ""),
            city=address_data.get("city", ""),
            state_province=address_data.get("state_province", ""),
            country=address_data.get("country", ""),

            address_source=address_data.get("address_source", ""),
            city_source=address_data.get("city_source", ""),
            country_source=address_data.get("country_source", ""),

            source_url=response.url,
            contact_page_urls=contact_pages,

            extraction_status="scraped"
        )

    except requests.RequestException as error:

        print(f"Failed: {url} - {error}")

        return None
