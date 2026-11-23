
from urllib.parse import urlparse


DIRECTORY_DOMAINS = {
    "tourradar.com",
    "tripadvisor.com",
}

ASSOCIATION_DOMAINS = {
    "taan.org.np",
    "taanpokhara.org",
}

NON_BUSINESS_DOMAINS = {
    "youtube.com",
    "youtu.be",
    "vimeo.com",
    "tiktok.com",
    "facebook.com",
    "instagram.com",
    "linkedin.com",
    "reddit.com",
}

ARTICLE_PATHS = (
    "/blog/",
    "/news/",
    "/articles/",
    "/article/",
)

# Strong signals that a result is an informational article.
ARTICLE_PHRASES = {
    "how to",
    "everything you need to know",
    "why you should",
    "complete guide",
    "beginner's guide",
    "beginners guide",
    "top 10",
    "top 15",
    "top 20",
    "list of trekking companies",
    "best trekking companies",
    "top trekking companies",
    "best routes",
    "trekking routes",
}

DIRECTORY_PHRASES = {
    "business directory",
    "company directory",
    "company listings",
    "business listings",
    "list of companies",
    "directory of",
}

ASSOCIATION_PHRASES = {
    "trekking agencies association",
    "tourism association",
    "members association",
    "federation of",
}

# Strong evidence that a website represents a relevant business.
BUSINESS_PHRASES = {
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
    "trekking and tours",
    "treks and tours",
    "tourism company",
    "tourism agency",
    "travel operator",
    "tour company",
}

# Supporting evidence. These words alone are not enough.
SERVICE_WORDS = {
    "trekking",
    "hiking",
    "expedition",
    "adventure",
    "mountaineering",
    "climbing",
    "tours",
    "travel",
}

BUSINESS_CONTEXT_WORDS = {
    "book",
    "booking",
    "trips",
    "holidays",
    "itineraries",
    "destinations",
    "guided",
    "organize",
    "organised",
    "organized",
    "operator",
    "agency",
    "company",
    "team",
    "experiences",
}


def matches_domain(domain, known_domains):

    return any(
        domain == item or domain.endswith("." + item)
        for item in known_domains
    )


def contains_phrase(text, phrases):

    return any(
        phrase in text
        for phrase in phrases
    )


def classify_result(result):

    url = (result.url or "").strip().lower()
    title = (result.title or "").strip().lower()
    snippet = (result.snippet or "").strip().lower()

    parsed_url = urlparse(url)

    domain = parsed_url.netloc.lower().removeprefix("www.")
    url_path = parsed_url.path.lower()

    if matches_domain(domain, NON_BUSINESS_DOMAINS):
        return "unknown"

    # 1. Known associations
    if matches_domain(domain, ASSOCIATION_DOMAINS):
        return "association"

    if contains_phrase(
        title,
        ASSOCIATION_PHRASES
    ):
        return "association"

    # 2. Known directory platforms
    if matches_domain(domain, DIRECTORY_DOMAINS):
        return "directory"

    if contains_phrase(
        title,
        DIRECTORY_PHRASES
    ):
        return "directory"

    # 3. Strong article URL signals
    if any(path in url_path for path in ARTICLE_PATHS):
        return "article"

    # 4. Strong article title signals
    if contains_phrase(title, ARTICLE_PHRASES):
        return "article"

    # 5. Score business evidence
    score = 0

    # Strong business phrases in the title
    if contains_phrase(title, BUSINESS_PHRASES):
        score += 3

    # Business phrases in the snippet
    if contains_phrase(snippet, BUSINESS_PHRASES):
        score += 2

    # Supporting evidence in the title
    title_has_service = any(
        word in title
        for word in SERVICE_WORDS
    )

    title_has_business_context = any(
        word in title
        for word in BUSINESS_CONTEXT_WORDS
    )

    if title_has_service:
        score += 1

    if title_has_business_context:
        score += 1

    # Supporting evidence in the snippet
    snippet_has_service = any(
        word in snippet
        for word in SERVICE_WORDS
    )

    snippet_has_business_context = any(
        word in snippet
        for word in BUSINESS_CONTEXT_WORDS
    )

    if snippet_has_service and snippet_has_business_context:
        score += 1

    # 6. Decide whether this is a potential business candidate
    if score >= 2:
        return "business"

    return "unknown"
