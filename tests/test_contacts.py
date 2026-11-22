
from bs4 import BeautifulSoup

from extractors.contacts import (
    extract_emails,
    extract_mailto_emails
)


sample_text = """
Contact us:
info@example.com
sales@example.org
"""

html = """
<html>
    <body>
        <a href="mailto:hello@example.com">Email Us</a>
        <a href="mailto:sales@example.org?subject=Inquiry">Sales</a>
    </body>
</html>
"""

soup = BeautifulSoup(html, "html.parser")

text_emails = extract_emails(sample_text)
mailto_emails = extract_mailto_emails(soup)

all_emails = list(dict.fromkeys(text_emails + mailto_emails))

print("Text emails:", text_emails)
print("Mailto emails:", mailto_emails)
print("All emails:", all_emails)


import requests
from bs4 import BeautifulSoup

url = "https://www.greenvalleynepaltreks.com/contact-us"

response = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=15
)

soup = BeautifulSoup(response.content, "html.parser")

for tag in soup.find_all(True):

    for attribute, value in tag.attrs.items():

        if "email" in str(value).lower() or "mailto" in str(value).lower():

            print(tag.name, attribute, value)   