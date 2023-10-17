# Before Python 3.10
# from typing import List, Optional
import uvicorn
from fastapi import FastAPI, HTTPException
from schemas import load_db, CarInput, CarOutput, save_db

app = FastAPI()
db = load_db()


@app.get("/api/cars/")
def get_cars(size: str | None = None, doors: int | None = None) -> list:
    # def get_cars(size: Optional[str] = None, doors: Optional[str] = None) -> List:
    result = db
    if size:
        result = [car for car in result if car.size == size]
    if doors:
        result = [car for car in result if car.doors >= doors]
    return result


@app.get("/api/cars/{id}")
def car_by_id(id: int) -> dict:
    result = [car for car in db if car.id == id]
    if result:
        return result[0]
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")


@app.post("/api/cars")
def add_car(car: CarInput) -> CarOutput:
    new_car = CarOutput(
        size=car.size,
        fuel=car.fuel,
        doors=car.doors,
        tranmission=car.tranmission,
        id=len(db) + 1,
    )
    db.append(new_car)
    save_db(db)
    return new_car


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
