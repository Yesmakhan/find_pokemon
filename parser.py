from bs4 import BeautifulSoup, SoupStrainer, Tag
import requests
import json

def get_names():

    POKEMON_PAGE_PREFIX = "https://scrapeme.live/shop/"
    POKEMON_LIST_PAGE_PREFIX = "https://scrapeme.live/shop/page/"

    page_number = 0
    pokemon_names = list()

    while True:
        page_number = page_number + 1

        resp = requests.get(POKEMON_LIST_PAGE_PREFIX + str(page_number))
        if resp.status_code == 404:
            break    
        html = resp.text
        soup =  BeautifulSoup(html, parse_only=SoupStrainer('a'), features="html.parser")

        for link in soup:
            if link.has_attr('href') and link['href'].startswith(POKEMON_PAGE_PREFIX):
                pokemon_name = link['href'][len(POKEMON_PAGE_PREFIX):-1] 
                if not pokemon_name or pokemon_name[0].islower():
                    continue
                pokemon_names.append(pokemon_name)
        
        print(f"Got page {page_number}")

    return pokemon_names

def get_pokemon(pokemon_name):
    print(f"Parsing {pokemon_name}")

    POKEMON_PAGE_PREFIX = "https://scrapeme.live/shop/"
    
    pokemon = dict()
    
    resp = requests.get(POKEMON_PAGE_PREFIX + pokemon_name)
    html = resp.text
    soup =  BeautifulSoup(html, features="html.parser")

    pokemon["name"] = pokemon_name
    pokemon["price"] = soup.find("p", {"class": "price"}).text
    pokemon["description"] = soup.find("div", {"class": "woocommerce-product-details__short-description"}).text
    pokemon["sku"] = soup.find("span", {"class": "sku"}).text
    pokemon["categories"] = [child.text for child in soup.find("span", {"class": "posted_in"}).children if isinstance(child, Tag)]
    pokemon["tags"] = [child.text for child in soup.find("span", {"class": "tagged_as"}).children if isinstance(child, Tag)]
    return pokemon


print("Start parsing names")
pokemon_names = get_names()
print("Finish parsing names")

print("Start parsing pokemons")
pokemons = list()
for pokemon_name in pokemon_names:
    pokemons.append(get_pokemon(pokemon_name))
print("Finish parsing pokemons")

with open('result.json', 'w') as fp:
    json.dump(pokemons, fp)