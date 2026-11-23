
from geotext import GeoText


addresses = [
    "Puskar Hotel, Thamel, Kathmandu, Nepal",
    "Bahnhofstrasse 10, Zurich, Switzerland",
    "Bahnhofstrasse 10, Zurich, Switzerland",
"Bahnhofstrasse 10, Zürich, Schweiz",
    "5th Avenue, New York, United States",
    "Shibuya, Tokyo, Japan",
    "Oxford Street, London, United Kingdom",
    "Queen Street, Auckland, New Zealand"
]


for address in addresses:

    places = GeoText(address)

    print("\nAddress:", address)
    print("Cities:", places.cities)
    print("Countries:", places.countries)
