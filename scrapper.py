import requests
from bs4 import BeautifulSoup
from enum_platforms import Platform

def take_data(platform: str, page: int) -> dict:
	url = f'https://www.3djuegos.com/{platform}/juegos/mejores/{page if page > 1 else ""}'
	web_data = requests.get(url)
	soup = BeautifulSoup(web_data.content, 'html.parser')
	# links_games = soup.find_all('.s18i col_plat_i')
	links_games = soup.find_all('a', class_='s18i col_plat_i')
	games_descriptions = soup.find_all("p", class_="mar_t3 mar_b5 c5")
	
	for link, game in zip(links_games, games_descriptions):
		url = link.get('href')
		web_data_game = requests.get(url)
		soup_game = BeautifulSoup(web_data_game.content, 'html.parser')
		data_game = {
			"title": soup_game.find("h1", class_="s22").text,
			"description": game.text,
			"platform": getattr(Platform, platform.replace("-", "_").upper(), None).value,
			"gender": soup_game.find_all("a", class_="col_plat"),
			"img_url": soup_game.find("img", class_="dib"),
			"price": soup_game.find("div", class_="c0").text[:-2],
			"pegi": soup_game.find("span", class_="c6").text[7:-2],
			"release": soup_game.find("dt", text="Lanzamiento:").get("dd")
		}
		print(data_game)
	# 	print(url)
	# print(web_data.content)
	# print(links_games)
	

take_data('nintendo-switch', 0)
# Validar data


	
	