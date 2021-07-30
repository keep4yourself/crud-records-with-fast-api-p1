from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI

class RaceCar(BaseModel):
    id: Optional[int] = None
    car_number: int
    driver_name: str
    team_name: str

app = FastAPI(
    title="Example-02-CRUD-part-1",
    description="keep-4-yourself-example-02",
)

@app.get("/")
def say_hello():
    return {"hello": "world "}

@app.get("/race-cars")
def get_all_cars():
    return {"cars": ["all"]}

@app.get("/race-cars/{car_id}")
def get_car(
    car_id: int
):
    return {"car": [f"returning details for {car_id}"]}

@app.put("/race-cars/{car_id}")
def edit_car(
    car_id: int
):
    return {"car": [f"editing details for {car_id}"]}

@app.post("/race-cars/")
def create_car(
    race_car: RaceCar
):
    return {"car": race_car}

@app.delete("/race-cars/{car_id}")
def delete_car(
    car_id: int
):
    return {"car": [f"delete car {car_id}"]}
