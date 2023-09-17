from pydantic import BaseModel


class CreateUser(BaseModel):
    login: str
    password: str


class UserID(BaseModel):
    user_id: int


class Region(BaseModel):
    region_id: int
    region_name: str


class AddRegion(BaseModel):
    region_name: str


class City(BaseModel):
    city_id: int
    region_id: int
    region_name: str
    city_name: str


class AddCity(BaseModel):
    city_name: str
    region_id: int


class CityID(BaseModel):
    city_id: int


class News(BaseModel):
    news_id: int
    image_id: int
    title: str
    timestamp: int
    content: str


class NewsID(BaseModel):
    news_id: int


class AddNews(BaseModel):
    image_id: int
    title: str
    content: str


class Place(BaseModel):
    place_id: int
    title: str
    city_id: int
    image_id: int
    youtube_id: str
    content: str
    latitude: float
    longitude: float


class AddPlace(BaseModel):
    title: str
    city_id: int
    image_id: int
    youtube_link: str
    content: str
    latitude: float
    longitude: float


class PlaceID(BaseModel):
    place_id: int


class ImageID(BaseModel):
    image_id: int

class AddImage(BaseModel):
    extension: str