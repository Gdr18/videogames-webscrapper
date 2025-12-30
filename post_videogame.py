from dotenv import load_dotenv
import os
import requests

from platform_enum import PlatformEnum

load_dotenv(".env.prod")

def login_api() -> str:
	url = f"{os.getenv("API_URL")}/auth/login"
	payload = {
		"email": os.getenv("API_EMAIL"),
		"password": os.getenv("API_PASSWORD")
	}
	headers = {
		"Content-Type": "application/json"
	}
	response = requests.post(url, json=payload, headers=headers)
	
	if response.status_code != 200:
		raise Exception(f"Fallo en el login: {response.status_code} - {response.text}")
	return response.json().get("access_token", "")


def post_game(videogame: dict) -> str:
	valid_platforms = [platform.value for platform in PlatformEnum]
	if not videogame.get("platform") in valid_platforms:
		raise ValueError(f"Plataformas válidas para el registro: {valid_platforms}")
	
	token = login_api()
	
	if not token:
		raise Exception("No se pudo obtener el token de autenticación")
	
	url = f"{os.getenv("API_URL")}/games/"
	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {token.strip()}"
	}

	response = requests.post(url, json=videogame, headers=headers)

	if response.status_code == 201:
		return "success"
	
	print(f"Fallo en el post del videojuego. Status code: {response.status_code}, Response: {response.text}")
	return "failure"
	