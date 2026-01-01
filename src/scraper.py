from flask import current_app

from src.videogame_model import VideogameModel
from src.platform_enum import PlatformScrapperEnum
from src.app_requests import http_request
from src.parsers import parse_list_games, parse_game

def get_data(platform: str, page: int) -> list[dict]:
	platform_formatted = PlatformScrapperEnum[platform.replace("-", "_").upper()]
	url_page = (current_app.config["URL_PARSER_SWITCH"] if platform_formatted == PlatformScrapperEnum.NINTENDO_SWITCH_2 else current_app.config["URL_PARSER"])
	url_formatted = url_page.format(platform=platform, page=("" if page == 0 else page))
	
	html_web = http_request(url_formatted).content
	
	urls_games, games_descriptions = parse_list_games(html_web)
	
	games_data = []
	
	for url, description in zip(urls_games, games_descriptions):
		try:
			html_game = http_request(url).content
			parsed_game = parse_game(html_game)
			game = {**parsed_game, "description": description, "platform": platform_formatted}

			videogame = VideogameModel(**game)
			games_data.append(videogame.model_dump())
		except Exception as e:
			print(f"Error scraping '{game['title']}': {e}")
			continue

	return games_data
	