import unittest

from bs4 import BeautifulSoup

from extractors.address_extractor import extract_address


class AddressExtractionTests(unittest.TestCase):

    def test_extracts_explicit_address_without_recognized_city_or_country(self):
        soup = BeautifulSoup(
            "<address>Suite 4, 12 Summit Road</address>",
            "html.parser"
        )

        result = extract_address(soup)

        self.assertEqual(result["address"], "Suite 4, 12 Summit Road")
        self.assertEqual(result["address_source"], "visible_text")

    def test_extracts_address_from_map_marker_contact_block(self):
        soup = BeautifulSoup(
            """
            <div class="contact-info__item">
                <i class="fa-map-marker"></i>
                <span class="contact-info__item__text">
                    Suite 4, 12 Summit Road
                </span>
            </div>
            """,
            "html.parser"
        )

        result = extract_address(soup)

        self.assertEqual(result["address"], "Suite 4, 12 Summit Road")
        self.assertEqual(result["address_source"], "visible_text")


if __name__ == "__main__":
    unittest.main()
