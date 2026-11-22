from bs4 import BeautifulSoup

from scraper.contact_page_finder import find_contact_pages


html = """
<html>
    <body>
        <a href="/contact">Contact Us</a>
        <a href="/about-us">About Us</a>
        <a href="/services">Our Services</a>
        <a href="https://example.org/contact">External Contact</a>
    </body>
</html>
"""

soup = BeautifulSoup(html, "html.parser")

pages = find_contact_pages(
    soup,
    "https://example.com"
)

for page in pages:
    print(page)