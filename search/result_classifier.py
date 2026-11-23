
from urllib.parse import urlparse


DIRECTORY_DOMAINS = {
    "tourradar.com",
    "tripadvisor.com",
    "taan.org.np",
}


ARTICLE_KEYWORDS = {
    "how to",
    "guide",
    "tips",
    "everything you need to know",
    "why you should",
    "top 10",
    "top 5",
    "top 20",
    "best routes",
    "trekking routes",
    "complete-list",
    "complete list",
    "list of trekking companies",
    "best trekking companies",
    "top trekking companies",
}


DIRECTORY_KEYWORDS = {
    "members",
    "directory",
    "list-of-companies",
}


BUSINESS_KEYWORDS = {
    "trekking",
    "trekking company",
    "trekking agency",
    "trekking experts",
    "trekking services",
    "tour operator",
    "tour operators",
    "travel agency",
    "travel company",
    "adventure company",
    "adventure travel",
    "adventure tours",
    "hiking company",
    "hiking tours",
    "expedition",
    "mountaineering",
    "mountain climbing",
    "peak climbing",
    "outdoor adventure",
    "guided tours",
    "travel services",
    "hiking team",
    "trekking team",
    "adventure team",
    "expedition company",
    "travel experts",
}


def classify_result(result):

    url = result.url.lower()
    title = result.title.lower()
    snippet = result.snippet.lower()

    domain = urlparse(url).netloc.lower()
    domain = domain.removeprefix("www.")

    # 1. Check known directory platforms
    if any(
        domain == item or domain.endswith("." + item)
        for item in DIRECTORY_DOMAINS
    ):
        return "directory"

    # 2. Check article URL patterns
    # Check article URL paths, not domain names
    url_path = urlparse(url).path.lower()

    if any(keyword in url_path for keyword in ARTICLE_KEYWORDS):
        return "article"

    # 3. Check directory-related title keywords
    if any(keyword in title for keyword in DIRECTORY_KEYWORDS):
        return "directory"

    # 4. Check article title patterns
    if any(keyword in title for keyword in ARTICLE_KEYWORDS):
        return "article"

    # 5. Check business keywords
    if any(
        keyword in title or keyword in snippet
        for keyword in BUSINESS_KEYWORDS
    ):
        return "business"

    # 6. No matching category
    return "unknown"
