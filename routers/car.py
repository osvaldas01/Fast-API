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

@router.get('/makes', response_model=List[schemas.Car])
async def get_car_makes(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    makes = db.query(models.CarAdverts.Marke).distinct().all()
    current_user = db.query
    return makes

@router.get('/models', response_model=List[schemas.CarModel])
async def get_car_models(make: str, db: Session = Depends(get_db)):
    modelis = db.query(models.CarAdverts.Modelis).filter(models.CarAdverts.Marke.ilike(make)).distinct().all()
    return modelis

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
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    year_from: int = Query(None, ge=1900),
    year_to: int = Query(None, le=2022),
    price_from: float = Query(None, ge=0),
    price_to: float = Query(None, ge=0),
    mileage_from: int = Query(None, ge=0),
    mileage_to: int = Query(None, ge=0),
    page: int = Query(1, ge=1),

):
    
    limit = 8
    offset = (page - 1) * limit
    cars = db.query(models.CarAdverts).filter(models.CarAdverts.Marke.ilike(car_make))

    if car_model:
        cars = cars.filter(models.CarAdverts.Modelis.ilike(car_model))
        
    if year_from:
        cars = cars.filter(models.CarAdverts.Metai >= year_from)
    if year_to:
        cars = cars.filter(models.CarAdverts.Metai <= year_to)
    if price_from:
        cars = cars.filter(models.CarAdverts.Kaina >= price_from)
    if price_to:
        cars = cars.filter(models.CarAdverts.Kaina <= price_to)
    if mileage_from:
        cars = cars.filter(models.CarAdverts.Rida >= mileage_from)
    if mileage_to:
        cars = cars.filter(models.CarAdverts.Rida <= mileage_to)
        
    pages_amount = cars.count() / limit

    cars = cars.offset(offset).limit(limit).all()

    if not cars:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Car with make {car_make} and model {car_model} not found"
        )

    return templates.TemplateResponse(name="cars.html", context={"request": request, "cars": cars, "pages_amount": int(round(pages_amount)), "car_make": car_make, "current_user": current_user})
