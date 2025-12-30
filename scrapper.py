import requests
import re
from bs4 import BeautifulSoup

from videogame_model import VideogameModel
from enum_platforms import Platform

def get_data(platform: str, page: int) -> list[dict]:
	url = f'https://www.3djuegos.com/{platform}/juegos/mejores/{page if page > 1 else ""}'
	web_data = requests.get(url)
	soup = BeautifulSoup(web_data.content, 'html.parser')
	
	links_games = soup.find_all('a', class_='s18i col_plat_i')
	games_descriptions = soup.find_all("p", class_="mar_t3 mar_b5 c5")
	
	games_data = []
	
	for link, description in zip(links_games, games_descriptions):
		url = link.get('href')
		web_data_game = requests.get(url)
		soup_game = BeautifulSoup(web_data_game.content, 'html.parser')
		
		videogame = soup_game.find("article")
		
		release_and_pegi = videogame.find("dt", string="Lanzamiento:").next_sibling.text.strip()
		limit = release_and_pegi.find(" (")
		release = release_and_pegi[:limit]
		pegi = release_and_pegi[limit + 8:-1]
		tag_price = videogame.find("a", string=lambda t: t and "€" in t)
		price = None
		if tag_price:
			tag_price = tag_price.text.strip()
			limit = tag_price.find("€")
			price = tag_price[limit - 5:limit].replace(",", ".")
		data_game = {
			"title": videogame.find("h1").text,
			# "description": videogame.find("p", id="adpepito").text,
			"description": description.text,
			"platform": getattr(Platform, platform.replace("-", "_").upper(), None).value,
			"gender": videogame.find("dt", class_="edit_tematicas").next_element.next_element.next_element.text,
			"img_url": videogame.find("img", class_="dib mar_b10").get("data-src"),
			"release": release,
			"pegi": pegi,
			"price": price
		}

		try:
			videogame = VideogameModel(**data_game)
			games_data.append(videogame.dict())
		except Exception as e:
			print(f"Error de validación '{data_game['title']}': {e}")
			continue

	return games_data
	