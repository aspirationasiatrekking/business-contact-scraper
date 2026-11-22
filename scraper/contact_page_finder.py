
from urllib.parse import urljoin, urlparse


CONTACT_KEYWORDS = {
    "contact",
    "contact-us",
    "contactus",
}

ABOUT_KEYWORDS = {
    "about",
    "about-us",
    "aboutus",
}


def find_contact_pages(soup, base_url):

    contact_pages = []
    about_pages = []

    links = soup.select("a[href]")

    base_domain = urlparse(base_url).netloc.lower()

    for link in links:

        href = link.get("href")

        if not href:
            continue

        full_url = urljoin(base_url, href)

        parsed_url = urlparse(full_url)

        # Ignore external websites
        if parsed_url.netloc.lower() != base_domain:
            continue

        # Ignore fragments and query parameters
        path = parsed_url.path.strip("/").lower()

        

        if path in CONTACT_KEYWORDS:
            contact_pages.append(full_url)

        elif path in ABOUT_KEYWORDS:
            about_pages.append(full_url)

    # Contact pages should be visited before about pages
    return list(dict.fromkeys(contact_pages + about_pages))
