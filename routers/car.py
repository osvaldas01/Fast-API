from fastapi import Depends, HTTPException, status, APIRouter, Query, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import models, schemas, oauth2
from database import get_db
from typing import List
from fastapi import Query

templates = Jinja2Templates(directory="templates")
router = APIRouter(
    tags = ['Car_info'],
    prefix="/cars" 
)

@router.get('/{car_id}', response_model=schemas.CarAdvert)
async def get_car_info(car_id: int, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    car = db.query(models.CarAdverts).filter(models.CarAdverts.id == car_id).first()
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Car with id {car_id} not found")
    return car

@router.get('/', response_model=List[schemas.IndexedCarAdvert])
async def get_car_info(
    request: Request,
    car_make: str,
    car_model: str = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(8, ge=1),
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    offset = (page - 1) * limit
    cars = db.query(models.CarAdverts).filter(models.CarAdverts.Marke == car_make)

    if car_model:
        cars = cars.filter(models.CarAdverts.Modelis == car_model)

    cars = cars.offset(offset).limit(limit).all()

    if not cars:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Car with make {car_make} and model {car_model} not found"
        )

    # Enumerate cars and convert to dictionary
    cars = [{"index": i+1, "car": car} for i, car in enumerate(cars)]

    return templates.TemplateResponse(name="cars.html", context={"request": request, "cars": cars})