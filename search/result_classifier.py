
from urllib.parse import urlparse


# Known directory platforms
DIRECTORY_DOMAINS = {
    "tourradar.com",
    "tripadvisor.com",
}


# Known association domains
ASSOCIATION_DOMAINS = {
    "taan.org.np",
    "taanpokhara.org",
}


# URL paths that commonly indicate articles
ARTICLE_PATHS = {
    "/blog/",
    "/news/",
    "/articles/",
    "/article/",
}


# Article and informational page keywords
ARTICLE_KEYWORDS = {
    "how to",
    "guide",
    "tips",
    "everything you need to know",
    "why you should",
    "best routes",
    "trekking routes",
    "complete-list",
    "complete list",
    "list of trekking companies",
    "best trekking companies",
    "top trekking companies",
    "companies in pokhara",
    "agency in pokhara 2025",
}


# Directory keywords
DIRECTORY_KEYWORDS = {
    "directory",
    "list-of-companies",
    "company listings",
    "business listings",
}


# Association keywords
ASSOCIATION_KEYWORDS = {
    "association",
    "trekking agencies association",
    "tourism association",
    "members association",
    "federation",
}


# Business keywords
# Avoid generic words such as "trekking" alone.
BUSINESS_KEYWORDS = {
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
    "expedition company",
    "mountaineering company",
    "mountain climbing",
    "peak climbing",
    "outdoor adventure",
    "guided tours",
    "travel services",
    "hiking team",
    "trekking team",
    "adventure team",
    "travel experts",
        "nepali agency",
    "local agency",
    "trekking and tours",
    "treks and tours",
    "tourism company",
    "tourism agency",
    "travel operator",
    "tour company",
}


def matches_domain(domain, known_domains):

    return any(
        domain == item or domain.endswith("." + item)
        for item in known_domains
    )


def classify_result(result):

    url = (result.url or "").lower()
    title = (result.title or "").lower()
    snippet = (result.snippet or "").lower()

    parsed_url = urlparse(url)

    domain = parsed_url.netloc.lower()
    domain = domain.removeprefix("www.")

    url_path = parsed_url.path.lower()

    # Combine searchable text
    page_text = f"{title} {snippet}"

    # 1. Check known associations
    if matches_domain(domain, ASSOCIATION_DOMAINS):
        return "association"

    if any(
        keyword in page_text
        for keyword in ASSOCIATION_KEYWORDS
    ):
        return "association"

    # 2. Check known directory platforms
    if matches_domain(domain, DIRECTORY_DOMAINS):
        return "directory"

    if any(
        keyword in title
        for keyword in DIRECTORY_KEYWORDS
    ):
        return "directory"

    # 3. Check article URL patterns
    if any(
        path in url_path
        for path in ARTICLE_PATHS
    ):
        return "article"

    # 4. Check article keywords in URL path
    if any(
        keyword.replace(" ", "-") in url_path
        or keyword.replace(" ", "") in url_path
        for keyword in ARTICLE_KEYWORDS
    ):
        return "article"

    # 5. Check article keywords in title
    if any(
        keyword in title
        for keyword in ARTICLE_KEYWORDS
    ):
        return "article"

    # 6. Check business keywords
    if any(
        keyword in page_text
        for keyword in BUSINESS_KEYWORDS
    ):
        return "business"

    # 7. No matching category
    return "unknown"
