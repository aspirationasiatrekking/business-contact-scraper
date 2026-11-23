from bs4 import BeautifulSoup

from extractors.address_extractor import extract_address
from extractors.business_category import extract_business_category
from extractors.business_name import extract_business_name


def test_microdata_extracts_name_and_business_type_without_keywords():
    soup = BeautifulSoup(
        """
        <div itemscope itemtype="https://schema.org/TravelAgency">
            <span itemprop="name">Himalayan Horizons</span>
        </div>
        """,
        "html.parser"
    )

    assert extract_business_name(soup) == "Himalayan Horizons"
    assert extract_business_category(soup) == "Travel Agency"


def test_json_ld_business_type_is_used_as_category():
    soup = BeautifulSoup(
        """
        <script type="application/ld+json">
        {
            "@type": ["Organization", "TouristInformationCenter"],
            "name": "Mountain Visitor Center"
        }
        </script>
        """,
        "html.parser"
    )

    assert extract_business_category(soup) == "Tourist Information Center"


def test_unlisted_microdata_business_type_is_derived_from_schema():
    soup = BeautifulSoup(
        """
        <div itemscope itemtype="https://schema.org/ProfessionalService">
            <span itemprop="name">North Ridge Studio</span>
            <span itemprop="telephone">+1 555 0100</span>
        </div>
        """,
        "html.parser"
    )

    assert extract_business_name(soup) == "North Ridge Studio"
    assert extract_business_category(soup) == "Professional Service"


def test_microdata_extracts_address_components_without_labels():
    soup = BeautifulSoup(
        """
        <div itemscope itemtype="https://schema.org/TravelAgency">
            <span itemprop="name">Himalayan Horizons</span>
            <div itemprop="address" itemscope
                 itemtype="https://schema.org/PostalAddress">
                <span itemprop="streetAddress">12 Summit Road</span>
                <span itemprop="addressLocality">Pokhara</span>
                <span itemprop="addressRegion">Gandaki</span>
                <span itemprop="addressCountry">Nepal</span>
            </div>
        </div>
        """,
        "html.parser"
    )

    result = extract_address(soup, "Himalayan Horizons")

    assert result == {
        "address": "12 Summit Road",
        "city": "Pokhara",
        "state_province": "Gandaki",
        "country": "Nepal",
        "address_source": "microdata",
        "city_source": "microdata",
        "country_source": "microdata",
    }
