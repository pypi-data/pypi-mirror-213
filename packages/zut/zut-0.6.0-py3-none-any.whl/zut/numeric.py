from __future__ import annotations
from decimal import Decimal, InvalidOperation
from locale import getlocale
from .misc import Literal
from .text import ValueString


def human_bytes(value: int, *, unit: str = 'iB', divider: int = 1024, decimals: int = 2, decimal_separator: str = None, thousands_separator: str = None, max_multiple: Literal['K']|Literal['M']|Literal['G']|Literal['T'] = None):
    return human_number(value, unit=unit, divider=divider, decimals=decimals, decimal_separator=decimal_separator, thousands_separator=thousands_separator, max_multiple=max_multiple)


def human_number(value: int, *, unit: str = '', divider: int = 1000, decimals: int = 2, decimal_separator: str = None, thousands_separator: str = None, max_multiple: Literal['K']|Literal['M']|Literal['G']|Literal['T'] = None):
    if value is None:
        return ValueString('', None)

    suffixes = []

    # Append non-multiple suffix (bytes)
    # (if unit is 'iB' we dont display the 'i' as it makes more sens to display "123 B" than "123 iB")
    if unit:
        suffixes.append(' ' + (unit[1:] if len(unit) >= 2 and unit[0] == 'i' else unit))
    else:
        suffixes.append('')

    # Append multiple suffixes
    for multiple in ['K', 'M', 'G', 'T']:
        suffixes.append(f' {multiple}{unit}')
        if max_multiple and max_multiple.upper() == multiple:
            break

    i = 0
    suffix = suffixes[i]
    divided_value = value

    while divided_value > 1000 and i < len(suffixes) - 1:
        divided_value /= divider
        i += 1
        suffix = suffixes[i]

    # Format value
    if i == 0:
        formatted_value = '{value:,.0f}'.format(value=divided_value)
    else:
        formatted_value = ('{value:,.'+str(decimals)+'f}').format(value=divided_value)

    #  Replace separators
    if decimal_separator is not None or thousands_separator is not None:
        chars = formatted_value
        formatted_value = ''
        for c in chars:
            if c == ',' and thousands_separator is not None:
                formatted_value += thousands_separator
            elif c == '.' and decimal_separator is not None:
                formatted_value += decimal_separator
            else:
                formatted_value += c

    # Display formatted value with suffix
    return ValueString(f'{formatted_value}{suffix}', value)


def parse_decimal(value: float|Decimal|str|None) -> float|Decimal:
    """
    Parse a decimal with variable decimal separator: may be formatted with comma decimal separator instead of dot.
    """
    if value is None or value == "":
        return None
        
    if isinstance(value, (float,Decimal)):
        return value   

    value = str(value).replace(',', '.')

    try:
        return Decimal(value)
    except InvalidOperation:
        raise ValueError(f"invalid decimal value: {value}") from None


def get_default_decimal_separator():
    locale = getlocale()
    if locale and locale[0] and locale[0].startswith('fr'):
        return ','
    else:
        return '.'

