from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Request, Response, status
# declarative_base class, Column, Integer and String
# will all be used for the race_car table model
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String
# Session will be used together wiith create_engine 
# for the connection session
from sqlalchemy.orm import Session

# my database is on the same machine 
# you should change the localhost with the IP of 
# your database
DB_HOST = "localhost" 
# the database we created in the previous article
# https://keepforyourself.com/databases/mysql/how-to-install-mysql-on-your-linux-system/
DATABASE = "playground"

engine = create_engine(f"mysql+pymysql://root:pass123@{DB_HOST}/{DATABASE}")
DBSession = Session(engine)

DB_BASE_ORM = declarative_base()

class RaceCar(BaseModel):
    id: Optional[int] = None
    car_number: int
    driver_name: str
    team_name: str

class RaceCarORM(DB_BASE_ORM):
    __tablename__ = "race_cars"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    car_number = Column(Integer, index=False)
    driver_name = Column(String, index=False)
    team_name = Column(String, index=False)

app = FastAPI(
    title="Example-02-CRUD-part-2",
    description="keep-4-yourself-example-03",
)

@app.get("/")
def say_hello():
    return {"hello": "world"}

@app.get("/race-cars")
def get_all_cars():
    return {"cars": ["all"]}

@app.get("/race-cars/{car_id}")
def get_car(
    car_id: int
):
    return {"car": [f"returning details for {car_id}"]}

@app.put("/race-cars")
def edit_car(
    request: Request,
    response: Response,
    race_car: RaceCar,
):
    return {"car": race_car}

# remove the ending / that will cause a redirect for the post request
# issue hit by the green guy :D
@app.post("/race-cars")
def create_car(
    request: Request,
    response: Response,
    race_car: RaceCar,
):
    try:
        DBSession.begin()
        race_car_record = RaceCarORM(**dict(race_car))
        DBSession.add(race_car_record)
        DBSession.commit()
        race_car.id = race_car_record.id
        return race_car
    except Exception as e:
        DBSession.rollback()
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "error": e,
            "error_details": e.orig.args if hasattr(e, 'orig') else f"{e}"
        }

@app.delete("/race-cars/{car_id}")
def delete_car(
    car_id: int
):
    return {"car": [f"delete car {car_id}"]}
