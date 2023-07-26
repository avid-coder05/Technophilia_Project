import requests
from bs4 import BeautifulSoup as bs
import json

check = open("scraped_data.txt", "w+")

def scrape_nintendo_site():
    url = "https://www.nintendo.com/store/games/best-sellers/"
    page = requests.get(url)
    index_soup = bs(page.text, "html.parser")
    page_json = index_soup.find("script", attrs={"id": "__NEXT_DATA__"})
    page_json = str(page_json)[str(page_json).find("{"):-9]
    return page_json

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

        image_url = "https://assets.nintendo.com/image/upload/ar_16:9,b_auto:border,c_lpad/b_white/f_auto/q_auto/dpr_1.5/c_scale,w_300/"
        image_part = i["productImage"]["publicId"]

        insert_dict["image"] = image_url + image_part

        clean_page_json.append(insert_dict)

    return clean_page_json

if(__name__ == "__main__"):
    collect_game_data()