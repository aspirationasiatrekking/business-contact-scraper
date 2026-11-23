from bs4 import BeautifulSoup

from extractors.business_name import extract_business_name


def test_json_ld_name():

    html = """
    <html>
        <head>
            <script type="application/ld+json">
            {
                "@type": "TravelAgency",
                "name": "Nepal Hiking Team"
            }
            </script>
        </head>
    </html>
    """

    soup = BeautifulSoup(html, "html.parser")

    assert extract_business_name(soup) == "Nepal Hiking Team"


def test_open_graph_name():

    html = """
    <html>
        <head>
            <meta property="og:site_name"
                  content="Green Valley Nepal Treks">
            <title>Welcome to our website</title>
        </head>
    </html>
    """

    soup = BeautifulSoup(html, "html.parser")

    assert extract_business_name(soup) == "Green Valley Nepal Treks"


def test_title_fallback():

    html = """
    <html>
        <head>
            <title>Info Nepal Treks</title>
        </head>
    </html>
    """

    soup = BeautifulSoup(html, "html.parser")

    assert extract_business_name(soup) == "Info Nepal Treks"


def run_tests():

    tests = [
        test_json_ld_name,
        test_open_graph_name,
        test_title_fallback
    ]

    for test in tests:
        test()
        print(f"PASSED: {test.__name__}")

    print("\nAll business name tests passed!")


if __name__ == "__main__":
    run_tests()
    