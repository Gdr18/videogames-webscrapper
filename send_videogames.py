from dotenv import load_dotenv
import os
import requests

load_dotenv(".env.prod")

def post_games(videogames: list[dict]) -> int:
	url = f"{os.getenv("API_URL")}/games"
	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {os.getenv("API_TOKEN")}"
	}
	success_count = 0
	for videogame in videogames:
		response = requests.post(url, json={"videogames": videogame}, headers=headers)
	
		if response.status_code == 201:
			success_count += 1
		else:
			print(f"Failed to post videogames. Status code: {response.status_code}, Response: {response.text}")
	
	return success_count