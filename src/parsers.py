from bs4 import BeautifulSoup
from typing import Union

def parse_list_games(html_content: str) -> tuple[list, list]:
	soup = BeautifulSoup(html_content, 'html.parser')
	
	links_games = soup.find_all('a', class_='s18i col_plat_i')
	games_descriptions = soup.find_all("p", class_="mar_t3 mar_b5 c5")
	
	urls_list = [link.get('href') for link in links_games]
	descriptions_list = [desc.get_text(strip=True) for desc in games_descriptions]
	
	return urls_list, descriptions_list

def parse_game(html_content: str) -> Union[dict, None]:
	soup_game = BeautifulSoup(html_content, 'html.parser')
	
	videogame = soup_game.find("article")
	
	release_and_pegi = videogame.find("dt", string="Lanzamiento:").next_sibling.get_text(strip=True)
	if not "Pegi" in release_and_pegi:
		raise ValueError("Falta información para el campo 'pegi'")
	
	tag_price = videogame.find("a", string=lambda t: t and "€" in t)
	if not tag_price:
		raise ValueError("Falta información para el campo 'price'")
	
	limit_release = release_and_pegi.find("(")
	release = (release_and_pegi[:limit_release] if limit_release != -1 else release_and_pegi).strip()[-4:]
	if not release.isdigit():
		raise ValueError("El campo 'release' no son dígitos")
	
	pegi = release_and_pegi[limit_release + 7:-1]
	
	tag_price = tag_price.get_text(strip=True)
	limit_pegi = tag_price.find("€")
	price = tag_price[limit_pegi - 5:limit_pegi].replace(",", ".")
	
	return {
		"title": videogame.find("h1").get_text(strip=True),
		"gender": videogame.find("dt", class_="edit_tematicas").next_element.next_element.next_element.get_text(strip=True),
		"img_url": videogame.find("img", class_="dib mar_b10").get("data-src"),
		"release": int(release),
		"pegi": pegi,
		"price": price
	}