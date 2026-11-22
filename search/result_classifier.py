from urllib.parse import urlparse


DIRECTORY_DOMAINS = {
    "tourradar.com",
    "tripadvisor.com",
    "taan.org.np",
}

ARTICLE_KEYWORDS = {
    "how-to",
    "best-trekking-companies",
    "complete-list",
    "top-10",
}

DIRECTORY_KEYWORDS = {
    "members",
    "directory",
    "list-of-companies",
}


def classify_result(result):

    url = result.url.lower()
    title = result.title.lower()
    snippet = result.snippet.lower()

    domain = urlparse(url).netloc.lower()
    domain = domain.removeprefix("www.")

    # Check known directory platforms
    if any(domain == item or domain.endswith("." + item)
           for item in DIRECTORY_DOMAINS):
        return "directory"

    # Check article URL patterns
    if any(keyword in url for keyword in ARTICLE_KEYWORDS):
        return "article"

    # Check directory-related keywords
    if any(keyword in title for keyword in DIRECTORY_KEYWORDS):
        return "directory"

    # Check for informational articles
    if any(keyword in title for keyword in {"how to", "guide", "tips"}):
        return "article"

    business_keywords = {
    "trekking company",
    "trekking agency",
    "trekking experts",
    "trekking services",
    "tour operator",
    "hiking company",
    "trekking in nepal",
    "trekking in kathmandu",
    "trekking in pokhara",
   }

    if any(keyword in title or keyword in snippet
           for keyword in business_keywords):
        return "business"

    return "unknown"