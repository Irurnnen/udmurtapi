import sqlite3
import logging
from app import schemas
from time import time
import re


DB_PATH = "./data/db.db"
YOUTUBE_ID_PATTERN = "((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)"


class DB:
    def __new__(cls, *args, **kwds):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwds)
        return it

    def init(self):
        self.con = sqlite3.connect(DB_PATH)
        self.cur = self.con.cursor()

    ################    NEWS    ################

    def get_news(self, count: int, offset: int) -> list[schemas.News]:
        print(2)
        res = self.cur.execute(f"""SELECT * FROM news ORDER BY news_id DESC
                                LIMIT {count} OFFSET {offset}""")
        answer = list()
        for row in res.fetchall():
            answer.append(schemas.News(news_id=row[0], title=row[1],
                                       image_id=row[2], timestamp=row[3], content=row[4]))
        return answer

    def get_all_news(self) -> list[schemas.News]:
        res = self.cur.execute("SELECT * FROM news ORDER BY news_id DESC")
        answer = list()
        for row in res.fetchall():
            answer.append(schemas.News(news_id=row[0], title=row[1],
                                       image_id=row[2], timestamp=row[3], content=row[4]))
        return answer

    def post_news(self, title: str, image_id: int, content: str) -> schemas.NewsID:
        res = self.cur.execute(
            f"""INSERT INTO news (title, image_id, creation_time, content) 
            VALUES ("{title}", {image_id}, {int(time())}, "{content}")""")
        self.con.commit()
        res = self.cur.execute(
            f"SELECT news_id FROM news ORDER BY news_id DESC LIMIT 1")
        return schemas.NewsID(news_id=res.fetchone()[0])

    def get_news_by_id(self, news_id: int) -> schemas.NewsID:
        res = self.cur.execute(f"SELECT * FROM news WHERE news_id={news_id} LIMIT 1")
        resp = res.fetchall()[0]
        answer = schemas.News(news_id=resp[0], title=resp[1],
                              image_id=resp[2], timestamp=resp[3], content=resp[4])
        return answer

    ################    CITY    ################

    def get_city_by_id(self, city_id: int) -> schemas.City:
        city_res = self.cur.execute(
            f"SELECT city_id, region_id, name FROM cities WHERE city_id={city_id}")
        resp = city_res.fetchall()[0]
        region_res = self.cur.execute(
            f"SELECT name FROM regions WHERE region_id={resp[1]}")
        resp_region = city_res.fetchall()[0]
        answer = schemas.City(
            city_id=resp[0], region_id=resp[1], city_name=resp[2], region_name=resp_region[0] )
        return answer

    def add_city(self, region_id: int, name: str) -> schemas.CityID:
        res = self.cur.execute(
            f"""INSERT INTO cities (region_id, name) VALUES ({region_id}, "{name}")""")
        self.con.commit()
        res = self.cur.execute(
            f"SELECT city_id FROM cities ORDER BY city_id DESC LIMIT 1")
        return schemas.CityID(city_id=res.fetchone()[0])

    def get_all_cities(self) -> list[schemas.City]:
        res = self.cur.execute(
            f"SELECT city_id, region_id, name FROM cities ORDER BY city_id DESC")
        answer = list()
        for row in res.fetchall():
            region_res = self.cur.execute(
                f"SELECT name FROM regions WHERE region_id={answer[1]}")
            region_name = region_res.fetchall()[0]
            answer.append(schemas.City(city_id=row[0], region_id=row[1],
                                       region_name=region_name, city_name=row[1]))
        return answer
    
    ################    Region    ################

    def get_cities_by_region_ID(self, region_id: int) -> list[schemas.City]:
        res = self.cur.execute(
            f"SELECT name FROM regions WHERE region_id={region_id}")
        region_name = res.fetchall()[0][0]
        res = self.cur.execute(
            f"SELECT city_id, name FROM cities WHERE region_id={region_id}")
        answer = list()
        for row in res.fetchall():
            answer.append(schemas.City(city_id=row[0], region_id=region_id,
                                       region_name=region_name, city_name=row[1]))
        return answer

    def get_region_by_ID(self, region_id: int) -> schemas.Region:
        res = self.cur.execute(
            f"SELECT name from regions WHERE region_id={region_id} LIMIT 1")
        answer = schemas.Region(region_id=region_id,
                                region_name=res.fetchall()[0][0])
        return answer

    def post_region(self, region_name: str) -> schemas.Region:
        res = self.cur.execute(
            f"""INSERT INTO regions (name) VALUES ("{region_name}")""")
        self.con.commit()
        res = self.cur.execute(
            f"SELECT region_id FROM regions ORDER BY region_id DESC LIMIT 1")
        return schemas.Region(region_id=res.fetchone()[0], region_name=region_name)

    def get_all_regions(self) -> list[schemas.Region]:
        res = self.cur.execute(
            f"SELECT region_id, name from regions ORDER BY region_id DESC")
        answer = list()
        for row in res.fetchall():
            print(row)
            answer.append(schemas.Region(region_id=row[0], region_name=row[1]))
        return answer

    ################    Place    ################

    def add_place(self, title: str, city_id: int, youtube_link: str,
                        image_id: int, content: str, latitude: float,
                        longitude: float) -> schemas.PlaceID:
        youtube_id = re.search(YOUTUBE_ID_PATTERN, youtube_link)[0]
        res = self.cur.execute(
            f"""INSERT INTO places (title, city_id, image_id, youtube_id, 
            content, latitude, longitude) VALUES ("{title}", {city_id}, 
            {image_id}, "{youtube_id}", "{content}", {latitude}, {longitude})""")
        self.con.commit()
        res = self.cur.execute(
            f"SELECT place_id FROM places ORDER BY place_id DESC LIMIT 1")
        return schemas.PlaceID(place_id=res.fetchone()[0])

    def get_places(self, count: int, offset: int) -> list[schemas.Place]:
        res = self.cur.execute(
            f"""SELECT place_id, title, city_id, image_id, youtube_id,
             content, latitude, longitude FROM places 
            ORDER BY place_id DESC LIMIT {count} OFFSET {offset}""")
        answer = list()

        for row in res.fetchall():
            answer.append(schemas.Place(place_id=row[0], title=row[1],
                                        city_id=row[2], image_id=row[3],
                                        youtube_id=row[4], content=row[5],
                                        latitude=row[6], longitude=row[7]))

        return answer

    def get_places_by_city_id(self, city_id: int, count: int, offset: int) -> schemas.Place:
        res = self.cur.execute(
            f"""SELECT place_id, title, city_id, image_id, youtube_id,
            content, latitude, longitude FROM places WHERE city_id="{city_id}"
            ORDER BY place_id DESC LIMIT {count} OFFSET {offset}""")

        answer = list()
        for row in res.fetchall():
            answer.append(schemas.Place(place_id=row[0], title=row[1],
                                        city_id=row[2], image_id=row[3],
                                        youtube_id=row[4], content=row[5],
                                        latitude=row[6], longitude=row[7]))
        return answer

    def get_places_by_region_id(self, region_id: int, count: int, offset: int) -> schemas.Place:
        cities = self.get_cities_by_region_ID(region_id)
        answer = list()
        for city in cities:
            res = self.cur.execute(
                f"""SELECT place_id, title, city_id, image_id, youtube_id,
                content, latitude, longitude FROM places WHERE 
                city_id={city.city_id} ORDER BY place_id DESC LIMIT {count}
                OFFSET {offset}""")
            for row in res.fetchall():
                answer.append(schemas.Place(place_id=row[0], title=row[1],
                                            city_id=row[2], image_id=row[3],
                                            youtube_id=row[4], content=row[5],
                                            latitude=row[6], longitude=row[7]))
        return answer

    def get_all_places(self) -> list[schemas.Place]:
        res = self.cur.execute(
            f"""SELECT place_id, title, city_id, image_id, youtube_id,
             content, latitude, longitude FROM places 
            ORDER BY place_id DESC""")

        answer = list()
        for row in res.fetchall():
            answer.append(schemas.Place(place_id=row[0], title=row[1],
                                        city_id=row[2], image_id=row[3],
                                        youtube_id=row[4], content=row[5],
                                        latitude=row[6], longitude=row[7]))
        return answer

    def get_place_by_id(self, place_id: int) -> schemas.Place:
        res = self.cur.execute(
            f"""SELECT place_id, title, city_id, image_id, youtube_id,
             content, latitude, longitude FROM places WHERE place_id={place_id}""")

        row = res.fetchall()[0]
        return schemas.Place(place_id=row[0], title=row[1], city_id=row[2], 
                             image_id=row[3], youtube_id=row[4], content=row[5], 
                             latitude=row[6], longitude=row[7])

    def add_user(self, login: str, password: str) -> schemas.UserID:
        res = self.cur.execute(f"""INSERT INTO user (login, password) VALUES ("{login}", "{password}")""")
        self.con.commit()
        
        res = self.cur.execute(
            f"SELECT user_id FROM user ORDER BY user_id DESC LIMIT 1")
        return schemas.CityID(news_id=res.fetchone()[0])
    
    def add_image(self, extension: str) -> schemas.ImageID:
        res = self.cur.execute(f"""INSERT INTO images (extension) VALUES ("{extension}")""")
        self.con.commit()

        res = self.cur.execute("SELECT image_id FROM images ORDER BY image_id DESC LIMIT 1")
        return schemas.ImageID(image_id=res.fetchone()[0])
    
    def get_extension(self, image_id: int) -> str:
        res = self.cur.execute(f"SELECT extension FROM images WHERE image_id={image_id}")
        return res.fetchall()[0][0]
    