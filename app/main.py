from os import listdir
from fastapi import FastAPI
from app.schemas import News, CardPlace, Place


app = FastAPI()


@app.get("/news")
async def get_news(count: int, offset: int = 0):
    aa = News(
        image_id="1", title="Как хорошо живется на свете!", timestamp=1694881412, content="Лучшее место на планете земля!")
    aa1 = [aa] * count
    return aa1


@app.get("/news/all")
async def get_all_news():
    return News()


@app.get("/news/{news_id}")
async def get_news_by_id(news_id: int):
    return 'News №' + str(news_id)


# TODO: add methods for User


@app.get("/place/all")
async def get_all_place():
    return "All places"


@app.get("/place/{place_id}")
async def get_place_by_id(place_id):
    return "Place #" + str(place_id)
