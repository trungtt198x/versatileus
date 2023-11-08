""""
Copyright © antonionardella 2023 - https://github.com/antonionardella (https://antonionardella.it)
Description:
Currency formatting functions
Version: 5.5.0
"""
async def format_currency(value, currency_symbol="$"):
    # Split integer and decimal parts if there is a decimal point
    parts = str(value).split('.')
    integer_part = parts[0]
    decimal_part = parts[1] if len(parts) > 1 else ""

    # Determine the number of decimal places based on the value
    num_decimal_places = 2 if int(integer_part) > 0 else 5

    # Limit decimal part to the specified number of digits
    if decimal_part and len(decimal_part) > num_decimal_places:
        decimal_part = decimal_part[:num_decimal_places]

    # Format integer part with commas
    formatted_integer_part = ""
    for i in range(len(integer_part), 0, -3):
        formatted_integer_part = "," + integer_part[max(i-3, 0):i] + formatted_integer_part

    # Remove leading comma if present
    if formatted_integer_part and formatted_integer_part[0] == ",":
        formatted_integer_part = formatted_integer_part[1:]

    # Combine integer and decimal parts with appropriate separator
    formatted_value = formatted_integer_part + ("." + decimal_part if decimal_part else "")

    # Add the currency symbol and return the formatted string
    return f"{currency_symbol} {formatted_value}"


async def format_shimmer_amount(value):
    # Convert the number to a float and then format it with 2 decimal places
    formatted_value = '{:.2f}'.format(float(value) / 1000000)
    return formatted_value