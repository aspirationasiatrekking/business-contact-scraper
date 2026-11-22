import phonenumbers


numbers = [
    "9841234567",
    "+977 9812345678",
    "01-4567890",
    "+1 415 555 2671",
    "2012 - 2026",
]

for value in numbers:

    try:
        number = phonenumbers.parse(value, "NP")

        print(
            value,
            "| Valid:", phonenumbers.is_valid_number(number),
            "| Country:", phonenumbers.region_code_for_number(number)
        )

    except phonenumbers.NumberParseException:
        print(value, "| Invalid format")