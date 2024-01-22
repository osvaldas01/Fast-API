from fastapi import Depends, HTTPException, status, APIRouter, Query
from sqlalchemy.orm import Session
import models, schemas, oauth2
from utils import hash_password
from database import get_db
from typing import List
from fastapi.security import HTTPBearer
from fastapi import Request
from oauth2 import verify_access_token

router = APIRouter(
    tags = ['Car_info'],
    prefix="/cars" 
)

@router.get('/{car_id}', response_model=schemas.CarAdvert)
async def get_car_info(request: Request, car_id: int, db: Session=Depends(get_db)):
    verify_access_token(request.cookies.get("access_token"), HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"}) )
    car = db.query(models.CarAdverts).filter(models.CarAdverts.id == car_id).first()
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Car with id {car_id} not found")
    return car

@router.get('/', response_model=List[schemas.CarAdvert])
async def get_car_info(car_make: str, car_model: str = Query(None), db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    
    cars = db.query(models.CarAdverts).filter(models.CarAdverts.Marke == car_make)
 
    if car_model:
        cars = cars.filter(models.CarAdverts.Modelis == car_model).all()
  
    if not cars:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Car with make {car_make} and model {car_model} not found")
 
    return cars