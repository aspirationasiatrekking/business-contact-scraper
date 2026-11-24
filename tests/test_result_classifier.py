
from search.base import SearchResult
from search.result_classifier import classify_result


def create_result(title, url, snippet=""):
    return SearchResult(
        title=title,
        url=url,
        snippet=snippet,
        provider="test"
    )


def test_business():
    result = create_result(
        "Nepal Hiking Team",
        "https://www.nepalhikingteam.com/",
        "Trusted trekking company in Nepal"
    )

    assert classify_result(result) == "business"


def test_directory():
    result = create_result(
        "10 Best Nepal Trekking Companies",
        "https://www.tourradar.com/hg/nepal-companies"
    )

    assert classify_result(result) == "directory"


def test_article():
    result = create_result(
        "How to Choose a Trekking Company",
        "https://example.com/how-to-choose-a-trekking-company"
    )

    assert classify_result(result) == "article"


def test_unknown():
    result = create_result(
        "Beautiful Mountains of Nepal",
        "https://example.com/mountains"
    )

    assert classify_result(result) == "unknown"


def run_tests():
    tests = [
    test_business,
    test_directory,
    test_article,
    test_unknown,
    test_business_without_obvious_keywords,
    test_trekking_article,
    test_directory_with_company_keyword,
    test_empty_snippet,
    test_everything_you_need_article,
    test_why_you_should_article,
    test_top_routes_article,
    test_nepal_guide_trekking_business
]

    for test in tests:
        test()
        print(f"PASSED: {test.__name__}")

    print("\nAll classifier tests passed!")



def test_nepal_guide_trekking_business():
    result = create_result(
        "Trekking Agency in Kathmandu | Trekking in Nepal",
        "https://nepalguidetrekking.com/",
        "Local trekking agency offering trekking services in Nepal"
    )

    assert classify_result(result) == "business"


def test_business_without_obvious_keywords():
    result = create_result(
        "Nepal Hiking Team",
        "https://www.nepalhikingteam.com/",
        "Explore the Himalayas with our experienced local team"
    )

    assert classify_result(result) == "business"


def test_trekking_article():
    result = create_result(
        "Trekking in Nepal: A Complete Beginner's Guide",
        "https://example.com/trekking-nepal-guide",
        "Everything you need to know before trekking"
    )

    assert classify_result(result) == "article"


def test_directory_with_company_keyword():
    result = create_result(
        "Directory of Trekking Companies",
        "https://example.com/directory"
    )

    assert classify_result(result) == "directory"


def test_empty_snippet():
    result = create_result(
        "Nepal Hiking Team",
        "https://www.nepalhikingteam.com/",
        ""
    )

    assert classify_result(result) == "business"

def test_everything_you_need_article():
    result = create_result(
        "Everything You Need to Know About Trekking in Nepal",
        "https://example.com/trekking-nepal"
    )

    assert classify_result(result) == "article"


def test_why_you_should_article():
    result = create_result(
        "Why You Should Visit the Himalayas",
        "https://example.com/visit-himalayas"
    )

    assert classify_result(result) == "article"


def test_top_routes_article():
    result = create_result(
        "Top 10 Trekking Routes in Nepal",
        "https://example.com/top-routes"
    )

    assert classify_result(result) == "article"


if __name__ == "__main__":
    run_tests()