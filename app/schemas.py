from pydantic import BaseModel


class News(BaseModel):
    image_id: int
    title: str
    timestamp: int
    content: str


class Place(BaseModel):
    title: str
    region_id: int
    city_id: int
    youtube_id: str
    images_id: int
    content: str


class CardPlace(BaseModel):
    title: str
    image_id: int
    city_id: int
    query_content: str
