from urllib.parse import urljoin, urlparse


CONTACT_KEYWORDS = {
    "contact",
    "contact-us",
    "contactus",
    "about",
    "about-us",
    "aboutus",
}


def find_contact_pages(soup, base_url):

    contact_pages = []

    links = soup.select("a[href]")

    for link in links:

        href = link.get("href")
        text = link.get_text(" ", strip=True).lower()

        if not href:
            continue

        combined_text = f"{text} {href.lower()}"

        if any(keyword in combined_text for keyword in CONTACT_KEYWORDS):

            full_url = urljoin(base_url, href)

            # Keep links within the same website
            if urlparse(full_url).netloc == urlparse(base_url).netloc:
                contact_pages.append(full_url)

    return list(dict.fromkeys(contact_pages))