from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

class VideogameModel(BaseModel):
	model_config = {
		"serialize_by_alias": True
	}
	
	title: str = Field(required=True, min_length=1, max_length=50)
	description: str = Field(required=True, min_length=1, max_length=1500)
	gender: str = Field(required=True, min_length=1, max_length=30)
	img_url: str = Field(required=True, pattern=r"^https?:\/\/\S+", serialization_alias="imgUrl")
	pegi: str = Field(required=True, pattern=r"^\+\d+\b")
	platform: Literal["Nintendo Switch", "Nintendo Switch 2", "PlayStation 4", "PlayStation 5", "Xbox Series", "Xbox One", "PC", "Android"] = Field(required=True)
	price: float = Field(required=True, gt=0)
	release: int = Field(required=True, range=(1975, datetime.now().year))
