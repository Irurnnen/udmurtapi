from fastapi import FastAPI


app = FastAPI()


@app.get("/news")
async def get_news(count: int, offset: int = 0):
    return [{"name": "AAAA"}] * count


@app.get("/news/all")
async def get_all_news():
    return 'Return All News'


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
