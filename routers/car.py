from fastapi import Depends, HTTPException, status, APIRouter, Query, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import models, schemas, oauth2
from database import get_db
from typing import List
from fastapi import Query
import os

templates = Jinja2Templates(directory="templates")
router = APIRouter(
    tags = ['Car_info'],
    prefix="/cars" 
)

@router.get('/{car_id}', response_model=schemas.CarAdvert)
async def get_car_info(car_id: int, request: Request, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    car = db.query(models.CarAdverts).filter(models.CarAdverts.Skelbimo_id == str(car_id)).first()
    num_of_pictures = len(os.listdir(f"static/Skelbimu_Images/{car_id}"))
    print(num_of_pictures)
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Car with id {car_id} not found")
    return templates.TemplateResponse(name="car.html", context={"request": request, "car": car, "num_of_pictures": num_of_pictures})

@router.get('/', response_model=List[schemas.CarAdvert])
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
    cars = db.query(models.CarAdverts).filter(models.CarAdverts.Marke.ilike(car_make))

    if car_model:
        cars = cars.filter(models.CarAdverts.Modelis.ilike(car_model))
        
    pages_amount = cars.count() / limit

    cars = cars.offset(offset).limit(limit).all()

    if not cars:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Car with make {car_make} and model {car_model} not found"
        )

    return templates.TemplateResponse(name="cars.html", context={"request": request, "cars": cars})