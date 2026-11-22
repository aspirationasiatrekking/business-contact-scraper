import phonenumbers


def extract_phone_numbers(text):

    numbers = []

    for match in phonenumbers.PhoneNumberMatcher(text, "NP"):

        number = match.number

        if phonenumbers.is_valid_number(number):

            formatted_number = phonenumbers.format_number(
                number,
                phonenumbers.PhoneNumberFormat.E164
            )

            numbers.append(formatted_number)

    return list(dict.fromkeys(numbers))


def is_nepal_phone_number(number):

    try:
        parsed_number = phonenumbers.parse(number, "NP")

        return (
            phonenumbers.is_valid_number(parsed_number)
            and phonenumbers.region_code_for_number(parsed_number) == "NP"
        )

    except phonenumbers.NumberParseException:
        return False