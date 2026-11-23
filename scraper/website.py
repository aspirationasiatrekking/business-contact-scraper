from extractors.address_extractor import extract_address
import requests
from bs4 import BeautifulSoup
from extractors.phone_extractor import extract_phone_numbers
from extractors.contacts import extract_emails, extract_mailto_emails
from scraper.contact_page_finder import find_contact_pages
from models.business import Business

def scrape_website(url):
    try:
        # 1. Download homepage
        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        address_data = extract_address(soup) or {}

        # 2. Extract website title
        title = (
            soup.title.get_text(strip=True)
            if soup.title else "No title found"
        )

        # 3. Extract homepage text and emails
        text_content = soup.get_text(
            separator="\n",
            strip=True
        )

        emails = extract_emails(text_content)
        emails.extend(extract_mailto_emails(soup))
        phone_numbers = extract_phone_numbers(text_content)

        # 4. Discover contact and about pages
        contact_pages = find_contact_pages(
            soup,
            response.url
        )

        print(
            f"Found {len(contact_pages)} contact/about pages"
        )

        # 5. Visit discovered pages
        for index, page_url in enumerate(contact_pages, start=1):
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

                page_emails = extract_emails(page_text)
                page_emails.extend(extract_mailto_emails(page_soup))

                emails.extend(page_emails)
                page_phones = extract_phone_numbers(page_text)
                phone_numbers.extend(page_phones)

            except requests.RequestException as error:
                print(
                    f"Contact page failed: {page_url} - {error}"
                )

        # 6. Remove duplicate emails
        emails = list(dict.fromkeys(emails))
        phone_numbers = list(dict.fromkeys(phone_numbers))  
   

        # 7. Return extracted information
        return Business(
            name=title,
            website=response.url,
            emails=emails,
            phone_numbers=phone_numbers,
            address=address_data.get("address", ""),
            city=address_data.get("city", ""),
            state_province=address_data.get("state_province", ""),
            country=address_data.get("country", ""),
            extraction_status="scraped"
        )   


    except requests.RequestException as error:
        print(f"Failed: {url} - {error}")
        return None
