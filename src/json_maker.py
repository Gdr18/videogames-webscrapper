import json
import os
from datetime import datetime

def create_json_file(data: list[dict]) -> tuple:
	filename = f"videogames_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
	filepath = os.path.join('src/temp', filename)
	
	os.makedirs('src/temp', exist_ok=True)
	
	with open(filepath, 'w', encoding='utf-8') as f:
		json.dump(data, f, ensure_ascii=False, indent=4)
		
	return filepath, filename