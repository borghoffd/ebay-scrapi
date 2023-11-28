from datetime import datetime, timedelta
from config import word_filters
import logging

class FilteredWordInAdEx(Exception):
    """ Dummy Class. """
    pass

def print_terminal_output(message: str):
    """ For a better output in the terminal. """
    now = datetime.now()
    prefix = "[" + now.strftime("%H:%M:%S") + "] - "
    print(prefix + message)


def remove_chars_from_prices_string(prices: str) -> str:
    """ Used to only have the price without any not used characters. """
    chars_to_remove = "€VB"
    price_without_symbol = prices
    for char in chars_to_remove:
        price_without_symbol = price_without_symbol.replace(char, "")
    return price_without_symbol


def format_date(date: str) -> str:
    """ Displays the date in a better format. """
    if "Heute" in date or "heute" in date:
        date = datetime.strptime(datetime.today().strftime('%d.%m.%Y ')+date, '%d.%m.%Y Heute, %H:%M')
    elif "Gestern" in date:
        yesterday = datetime.today() - timedelta(1)
        date = datetime.strptime(yesterday.strftime('%d.%m.%Y ')+date, '%d.%m.%Y Gestern, %H:%M')
    elif date:
        date = datetime.strptime(date, '%d.%m.%Y')
    return date


def filter_text(text: str) -> FilteredWordInAdEx:
    """ Filters out ads based on certain keywords. """
    for word_filter in word_filters:
        if word_filter in text:
            # TODO: Bessere Ausgabe WAS genau gefunden wurde
            logging.info("found a filtered word in " + text)
            raise FilteredWordInAdEx