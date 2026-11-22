
import re


EMAIL_PATTERN = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"


def extract_emails(text):
    emails = re.findall(EMAIL_PATTERN, text)

    return list(dict.fromkeys(emails))


def extract_mailto_emails(soup):

    emails = []

    links = soup.select('a[href^="mailto:"]')

    for link in links:

        email = link.get("href").replace("mailto:", "", 1)

        # Remove optional query parameters
        email = email.split("?")[0].strip()

        if re.fullmatch(EMAIL_PATTERN, email):
            emails.append(email)

    return list(dict.fromkeys(emails))
