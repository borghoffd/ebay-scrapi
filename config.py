first_run = True
sleep_time = 60 # This is in seconds
wait_inbetween_keywords_time = 6 # This is in seconds
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59',
}


#####################
# Keywords
#####################

keywords = [
    {   "name": "ddr3 ram",
        "start_price": "1",
        "end_price": "60",
        "search_radius": "90"
    }, 
    {   "name": "cpu",
        "start_price": "1",
        "end_price": "130",
        "search_radius": "90"
    }, 
    {   "name": "500W netzteil",
        "start_price": "1",
        "end_price": "20",
        "search_radius": "90"
    }, 
    {   "name": "550W netzteil",
        "start_price": "1",
        "end_price": "20",
        "search_radius": "90"
    },
    {   "name": "600W netzteil",
        "start_price": "1",
        "end_price": "20",
        "search_radius": "90"
    },
    {   "name": "650W netzteil",
        "start_price": "1",
        "end_price": "20",
        "search_radius": "90"
    },
    {   "name": "700W netzteil",
        "start_price": "1",
        "end_price": "20",
        "search_radius": "90"
    },
    {   "name": "grafikkarte",
        "start_price": "1",
        "end_price": "110",
        "search_radius": "90"
    }, 
    {   "name": "mainboard",
        "start_price": "1",
        "end_price": "130",
        "search_radius": "90"
    }, 
    {   "name": "konvolut",
        "start_price": "1",
        "end_price": "200",
        "search_radius": "90"
    }, 
    {   "name": "defekt",
        "start_price": "1",
        "end_price": "200",
        "search_radius": "90"
    }, 
    {   "name": "bastler",
        "start_price": "1",
        "end_price": "200",
        "search_radius": "90"
    }
]

#TODO: maybe even implement it for every keyword
word_filters = ["Wasserkühlung", "Tausch", "SSD", "Drucker", "Druckerpatronen", "Canon", "Epson", "HP", "Brother"]

#####################
# DATABASE
#####################
db_filename = "ebay-ads.db"