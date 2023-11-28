import os
import config
import log
from helper import *
# import telegram as tlgr

import requests
import time
import re
import logging
import pandas as pd
import numpy as np
import json

from bs4 import BeautifulSoup


def search_ebay_ads(keyword: dict) -> None:
    """ Searches ebay. """
    items = []
    logging.info("Searching for " + keyword["name"])

    #TODO URL in config
    url = "https://www.ebay-kleinanzeigen.de/s-pc-zubehoer-software/41065/anzeige:angebote/preis:"+ keyword["start_price"] + ":"+ keyword["end_price"] + "/"+ keyword["name"] + "/k0c225l1967r"+ keyword["search_radius"]

    response = requests.get(url=url, headers=config.headers)
    response.encoding = "utf-8"
    page = response.content
    soup = BeautifulSoup(page, "html.parser")

    # Get the search results html-element, called srchrslt-adtable
    search_results_content = soup.find("ul", id="srchrslt-adtable")
    
    # Highlighted and top ad  are not getting recognized. Top Ads have the class 'ad-listitem lazyload-item  badge-topad is-topad' and highlighted ones 'ad-listitem lazyload-item  is-highlight'
    try:
        search_results = search_results_content.find_all("li", {"class":"ad-listitem lazyload-item"})
    except AttributeError as at_ex:
        logging.error("AttributeError")
        logging.error(at_ex)
        print_terminal_output("AttributeError, check logs")
        search_results = []

    # Look through each search result
    for search_result in search_results:
        """
        if (int(search_radius) >= 100):
            return
        """
        item = {}

        # Clean Data
        place_with_plz_raw = search_result.find("div", {"class":"aditem-main--top--left"})
        place_with_plz = place_with_plz_raw.getText().strip()
        plz = place_with_plz[0:5]

        # find distance in brackets with some regex magic
        r3 = re.compile("(.*?)\s*\((.*?)\)")
        m3 = r3.match(place_with_plz[6:])
        place = m3.group(1)
        distance = m3.group(2)

        title_raw = search_result.find("a", {"class":"ellipsis"})

        # There sometimes is a weird bug, that says that title_raw is of NoneType. 
        # This very crude code logs it and goes to the next item
        if title_raw == None:
            logging.error(search_result)
            logging.error("Something is fishy here...")
            continue

        title = title_raw.getText().strip()

        # We want to filter out certain words in a text, so we do this here for the title
        try:
            filter_text(title)
        except FilteredWordInAdEx:
            # Skip this item if we find a word, we do this via this Exception
            break

        ebay_link = "https://www.ebay-kleinanzeigen.de" + title_raw["href"]

        description_raw = search_result.find("p", {"class":"aditem-main--middle--description"})
        description = description_raw.getText().strip()

        # We want to filter out certain words in a text, so we do this here for the description
        try:
            filter_text(description)
        except FilteredWordInAdEx:
            break
        

        ebay_date_raw = search_result.find("div", {"class":"aditem-main--top--right"})
        ebay_date = ebay_date_raw.getText().strip()

        # The date we get from ebay is kinda weird, we want a nicely formatted and human readable one
        date_formatted = format_date(ebay_date)

        shipping_raw = search_result.find("span", {"class":"simpletag tag-small"})

        # shipping_raw is of type none when the item doesn't have 'Versand möglich'
        if(shipping_raw != None):
            shipping = shipping_raw.getText().strip()
        else:
            shipping = "Nur Abholung"

        prices_raw = search_result.find("p", {"class":"aditem-main--middle--price"})
        prices = prices_raw.getText().strip()

        if(prices.find("VB") >= 0):
            is_vb = "Yes"
        else:
            is_vb = "No"

        # Delete euro symbol and VB from string to only get a number
        price_without_symbol = remove_chars_from_prices_string(prices)

        # Get the ID, we use the number at the end of the url which looks like this: 2162148233-225-1896
        item_idr = re.search("[0-9.]*\-[0-9.]*\-[0-9.]*$", ebay_link)
        item_id = item_idr.group()

        #TODO: Remember the search result, maybe via the id in the url, check if this even is an id
        # https://www.ebay-kleinanzeigen.de/s-anzeige/atx-600w-netzteil-lc-power-lc6600gp2-v2-3-lcpower-pfc-rechnung/1189420375-225-1188 -> 1189420375-225-1188
        print(item_id, date_formatted, keyword["name"], title, plz, place, distance, price_without_symbol, shipping, is_vb, ebay_link)
        print("---------------------")

        item["item_id"] = item_id
        item["ebay_date"] = date_formatted
        item["category"] = keyword["name"]
        item["title"] = title
        item["plz"] = plz
        item["place"] = place
        item["distance"] = distance
        item["price"] = price_without_symbol
        item["shipping"] = shipping
        item["is_vb"] = is_vb
        item["ebay_link"] = ebay_link

        # Skipping insert items that are already in the csv
        # We can't open the csv file in the first run of the bot, because the csv is not yet created and it would throw an error
        if not config.first_run:
            # TODO: Path into config
            df_in = pd.read_csv(r"/mnt/d/Coding/Python/scrapi/items.csv", sep=";")
            
            # Check if the row "item_id" contains the current item_id
            # If not, insert it into the dict, otherwise don't insert
            if not (df_in["item_id"] == item_id).any():
                logging.info("Inserting...") # TODO: Delete, just for a big debug run
                items.insert(len(items),item)
            else:
                print("not inserting " + item_id)
        else:
            items.insert(len(items),item)

    df_out = pd.DataFrame(items)
    # TODO: Path into config
    df_out.to_csv("/mnt/d/Coding/Python/scrapi/items.csv", sep=";", mode="a", header=not os.path.exists("/mnt/d/Coding/Python/scrapi/items.csv"), index=False)


def main():
    log.create_logger()
    logging.info("Bot is starting...")
    print_terminal_output("Bot is starting...")
    while True:
        # TODO: start with a small radius and increase it if no results are shown
        for keyword in config.keywords:
            search_ebay_ads(keyword)
            # We don't want to flood the site with requests, so we wait a certain time between each keyword search
            time.sleep(config.wait_inbetween_keywords_time)

        config.first_run = False
        logging.info("Going to sleep...")
        time.sleep(config.sleep_time)

if __name__ == "__main__":
    main()