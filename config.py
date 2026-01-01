import os
from dotenv import load_dotenv

load_dotenv(".env.prod")

class Config:
	PORT = int(os.getenv("PORT", 4000))
	API_URL = os.getenv("API_URL")
	API_EMAIL = os.getenv("API_EMAIL")
	API_PASSWORD = os.getenv("API_PASSWORD")
	URL_PARSER = os.getenv("URL_PARSER")
	URL_PARSER_SWITCH_2 = os.getenv("URL_PARSER_SWITCH_2")

class DevelopmentConfig(Config):
	DEBUG = True
	
class ProductionConfig(Config):
	DEBUG = False
	
environments = {
	"development": DevelopmentConfig,
	"production": ProductionConfig,
}

CONFIG = environments[os.getenv("environment")]

