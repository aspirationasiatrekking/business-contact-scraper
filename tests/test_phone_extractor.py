
from extractors.phone_extractor import extract_phone_numbers


sample_text = """
Contact us:

Nepal: +977 981-2345678
USA: +1 202-555-0123
UK: +44 20 7946 0958
Switzerland: +41 44 668 18 00
Japan: +81 3-1234-5678

Established: 2012 - 2026
Price: 5500 - 6500
"""

print("\nTesting international phone extraction:")

numbers = extract_phone_numbers(sample_text)

for number in numbers:
    print(number)


# Test local numbers with a specified country
print("\nTesting local Nepal numbers:")

nepal_text = """
Mobile: 9812345678
Telephone: 01-4567890
"""

nepal_numbers = extract_phone_numbers(nepal_text, "NP")

for number in nepal_numbers:
    print(number)
