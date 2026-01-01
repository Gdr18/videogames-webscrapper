from flask import current_app
import requests
from typing import Literal

from src.platform_enum import PlatformDBEnum

def http_request(url: str, method: Literal["get", "post"] = "get", payload: dict = None, token: str = None) -> requests.Response:
	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {token}" if token else None
	}
	
	if method == "post":
		return requests.post(url, json=payload, headers=headers)
	
	return requests.get(url)

	

def login_api() -> str:
	url = f"{current_app.config["API_URL"]}/auth/login"
	payload = {
		"email": current_app.config["API_EMAIL"],
		"password": current_app.config["API_PASSWORD"]
	}
	response = http_request(url, "post", payload)
	
	if response.status_code != 200:
		raise Exception(f"Fallo en el login: {response.status_code} - {response.text}")
	
	return response.json().get("access_token", "")


def post_game_api(videogame: dict) -> bool:
	valid_platforms = [platform.value for platform in PlatformDBEnum]
	if not videogame.get("platform") in valid_platforms:
		raise ValueError(f"Plataformas válidas para el registro: {valid_platforms}")
	
	token = login_api()
	
	if not token:
		raise Exception("No se pudo obtener el token de autenticación")
	
	url = f"{current_app.config["API_URL"]}/games/"

	response = http_request(url, "post", videogame, token)

	if response.status_code != 201:
		print(f"Fallo en el registro. Status code: {response.status_code}, Response: {response.text}")
		return False
	
	return True
	