from bs4 import BeautifulSoup

from extractors.address_extractor import extract_address


html = """
<html>
<head>
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "TravelAgency",
    "name": "Nepal Hiking Team",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Nayabazar-16, Kathmandu, Nepal",
        "addressLocality": "Kathmandu",
        "addressRegion": "Bagmati",
        "postalCode": "44600",
        "addressCountry": "NP"
    }
}
</script>
</head>
<body>
    <h1>Nepal Hiking Team</h1>
</body>
</html>
"""


soup = BeautifulSoup(html, "html.parser")

address = extract_address(soup)

print("Extracted address:")
print(address)


string_address_html = """
<html>
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "TravelAgency",
    "name": "Example Adventures",
    "address": "Thamel, Kathmandu, Nepal"
}
</script>
</html>
"""

string_soup = BeautifulSoup(
    string_address_html,
    "html.parser"
)

string_address = extract_address(string_soup)

print("\nTesting string address:")
print(string_address)


graph_html = """
<html>
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "WebSite",
            "name": "Example Adventures"
        },
        {
            "@type": "TravelAgency",
            "name": "Example Adventures",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "Thamel",
                "addressLocality": "Kathmandu",
                "addressRegion": "Bagmati",
                "addressCountry": "NP"
            }
        }
    ]
}
</script>
</html>
"""

graph_soup = BeautifulSoup(graph_html, "html.parser")

graph_address = extract_address(graph_soup)

print("\nTesting @graph:")
print(graph_address)


multiple_businesses_html = """
<html>
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "TravelAgency",
            "name": "Mountain Adventures",
            "address": {
                "streetAddress": "Thamel, Kathmandu",
                "addressLocality": "Kathmandu",
                "addressCountry": "NP"
            }
        },
        {
            "@type": "TravelAgency",
            "name": "Example Adventures",
            "address": {
                "streetAddress": "Lakeside, Pokhara",
                "addressLocality": "Pokhara",
                "addressRegion": "Gandaki",
                "addressCountry": "NP"
            }
        }
    ]
}
</script>
</html>
"""

multiple_soup = BeautifulSoup(
    multiple_businesses_html,
    "html.parser"
)

correct_address = extract_address(
    multiple_soup,
    "Example Adventures"
)

print("\nTesting multiple businesses:")
print(correct_address)


missing_fields_html = """
<html>
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "TravelAgency",
    "name": "Incomplete Adventures",
    "address": {
        "addressCountry": "NP"
    }
}
</script>
</html>
"""

missing_soup = BeautifulSoup(
    missing_fields_html,
    "html.parser"
)

missing_address = extract_address(
    missing_soup,
    "Incomplete Adventures"
)

print("\nTesting missing address fields:")
print(missing_address)