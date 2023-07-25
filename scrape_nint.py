import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import json

check = open("scraped_data.txt", "w+")

def scrape_nintendo_site():
    url = "https://www.nintendo.com/store/games/best-sellers/"
    page = requests.get(url)
    index_soup = bs(page.text, "html.parser")
    page_json = index_soup.find("script", attrs={"id": "__NEXT_DATA__"})
    page_json = str(page_json)[str(page_json).find("{"):-9]
    return page_json

def get_image_urls(keyword):
    url = "https://bing-image-search1.p.rapidapi.com/images/search"

    querystring = {"q":keyword}

    headers = {
	    "X-RapidAPI-Key": "1ac03e599emshccabdf7a33bff3dp15eb97jsnff32f92c9de9",
	    "X-RapidAPI-Host": "bing-image-search1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    img_url = response.json()['value']

    for img in img_url:
        if(img['width'] > img['height']):
            continue
        else:
            img_url = img['contentUrl']
            break

    return img_url

def collect_game_data():
    page_json = json.loads(scrape_nintendo_site())
    page_json = page_json['props']['pageProps']['page']['content']['merchandisedGrid']
    # name, genres, franchise,
    page_json = page_json[:-85]
    clean_page_json = []

    for i in page_json:
        insert_dict = dict([])

        insert_dict["name"] = i["name"]
        insert_dict["genres"] = i["genres"]
        insert_dict["locale"] = i["locale"]
        insert_dict["price"] = i["prices"]["minimum"]["finalPrice"]
        insert_dict["releaseDate"] = i["releaseDate"][:-14]

        insert_dict["next_url"] = "https://www.nintendo.com/store/products/" + i["urlKey"]

        image_url = get_image_urls(i["name"] + " switch cover")
        insert_dict["image"] = image_url

        clean_page_json.append(insert_dict)

    return clean_page_json

if(__name__ == "__main__"):
    collect_game_data()