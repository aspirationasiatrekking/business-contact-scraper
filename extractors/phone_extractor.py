
import phonenumbers


def extract_phone_numbers(text, default_region=None):

    numbers = []

    for match in phonenumbers.PhoneNumberMatcher(
        text,
        default_region
    ):

        number = match.number

        if phonenumbers.is_valid_number(number):

            formatted_number = phonenumbers.format_number(
                number,
                phonenumbers.PhoneNumberFormat.E164
            )

            numbers.append(formatted_number)

    return list(dict.fromkeys(numbers))
