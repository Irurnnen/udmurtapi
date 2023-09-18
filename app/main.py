from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.db import DB
from app import schemas



app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")
database = DB()
prefics = '/v1'

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# News
# TODO: token: Annotated[str, Depends(oauth2_scheme)]
@app.post(prefics + "/news/add", tags=["News"])
async def post_news(add_news: schemas.AddNews) -> schemas.NewsID:
    """Post new news."""
    return database.post_news(add_news.title, add_news.image_id, add_news.content)


@app.get(prefics + "/news", tags=["News"])
async def get_news(count: int, offset: int = 0) -> list[schemas.News]:
    """Get latest news."""
    return database.get_news(count, offset)


@app.get(prefics + "/news/all", tags=["News"])
async def get_all_news() -> list[schemas.News]:
    return database.get_all_news()


@app.get(prefics + "/news/{news_id}", tags=["News"])
async def get_news_by_id(news_id: int) -> schemas.News:
    return database.get_news_by_id(news_id)


# User
@app.post(prefics + "/user/add", tags=["User"])
async def add_user(createUser: schemas.CreateUser) -> schemas.UserID:
    return database.add_user(createUser.login, createUser.password)


# TODO: add methods for User


# Cities
@app.post(prefics + "/city/add", tags=["City"])
async def add_new_city(addCity: schemas.AddCity) -> schemas.CityID:
    return database.add_city(addCity.region_id, addCity.city_name)

@app.get(prefics + "/city/all", tags=["City"])
async def get_all_cities() -> list[schemas.City]:
    return database.get_all_cities()

@app.get(prefics + "/city/{city_id}", tags=["City"])
async def get_city_by_ID(city_id: int) -> schemas.City:
    return database.get_city_by_id(city_id)


# Regions
@app.post(prefics + "/region/add", tags=["Region"])
async def add_region(addRegion: schemas.AddRegion) -> schemas.Region:
    return database.post_region(addRegion.region_name)

@app.get(prefics + "/region/all", tags=["Region"])
async def get_all_regions() -> list[schemas.Region]:
    return database.get_all_regions()

@app.get(prefics + "/region/{region_id}/cities", tags=["Region"])
async def get_cities_by_region_ID(region_id: int) -> list[schemas.City]:
    return database.get_cities_by_region_ID(region_id)


@app.get(prefics + "/region/{region_id}", tags=["Region"])
async def get_region_by_ID(region_id: int) -> schemas.Region:
    return database.get_region_by_ID(region_id)


# Places
@app.post(prefics + "/place/add", tags=["Place"])
async def add_place(addPlace: schemas.AddPlace) -> schemas.PlaceID:
    return database.add_place(addPlace.title, addPlace.city_id, addPlace.youtube_link,
                              addPlace.content, addPlace.latitude, 
                              addPlace.longitude) 


@app.get(prefics + "/place", tags=["Place"])
async def get_places(count: int, offset: int = 0, region_id: int = 0,
                         city_id: int = 0) -> list[schemas.Place]:
    if city_id != 0:
        return database.get_places_by_city_id(city_id, count, offset)
    if region_id != 0:
        return database.get_places_by_region_id(region_id, count, offset)
    return database.get_places(count, offset)


@app.get(prefics + "/place/all", tags=["Place"])
async def get_all_places() -> list[schemas.Place]:
    return database.get_all_places()


@app.get(prefics + "/place/{place_id}", tags=["Place"])
async def get_place_by_id(place_id) -> schemas.PlaceImages:

    return database.get_place_by_id(place_id)


@app.post(prefics + "/image/add", tags=["Image"])
async def add_image(files: list[UploadFile], place_id: int = 0) -> list[schemas.ImageID]:
    ImagesID = list()
    for file in files:
        ImagesID.append(database.add_image(file.filename.split(".")[-1]))
        with open(f'images/{ImagesID[-1].image_id}.{file.filename.split(".")[-1]}', 'wb') as image:
            image.write(file.file.read())
        if place_id != 0:
            database.place_and_images(place_id, ImagesID[-1].image_id)
    return ImagesID


@app.get(prefics + "/image/{image_id}", tags=["Image"])
async def get_image(image_id: int):
    extension = database.get_extension(image_id)
    return FileResponse(path=f'images/{image_id}.{extension}', filename='image.{extension}',
                        media_type="multipart/form-data")

