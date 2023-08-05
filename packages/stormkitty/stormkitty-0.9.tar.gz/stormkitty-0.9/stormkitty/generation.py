import csv
import random
import requests

class generation():
    
    def generate_random_deck(faction, display=False):
        portable_variables = {"max_deck_count":12, "begin_count":0, "CSV_URL":r'https://www.dropbox.com/s/acfzhdsostyd08s/cards.csv?dl=1'}
        CSV_URL = portable_variables["CSV_URL"]
        main_deck = []
        max_deck_count = portable_variables["max_deck_count"]
        begin_count = portable_variables["begin_count"]
        while begin_count != max_deck_count:
            with requests.Session() as s:
                download = s.get(CSV_URL)
                decoded_content = download.content.decode('utf-8')
                cards_url = csv.reader(decoded_content.splitlines(), delimiter=',')
                cards = list(cards_url)
                chosen_row = random.choice(list(cards))
                found_faction = str(chosen_row[3])
                if found_faction == str(faction) or found_faction == "neutral":
                    main_deck.append(chosen_row[0])
                    begin_count += 1
                    if display == True:
                        print(main_deck)
                else:
                    if display == True:
                        print("->", end="")

        return main_deck
