from extractors.phone_extractor import extract_phone_numbers

sample_text = """
Contact us:
Mobile: +977 981-2345678
Telephone: 01-4567890

Established: 2012 - 2026
Price: 5500 - 6500
"""

print("\nTesting mixed website text:")

numbers = extract_phone_numbers(sample_text)

for number in numbers:
    print(number)