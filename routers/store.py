from fastapi import Depends, HTTPException, status, APIRouter, Form
from sqlalchemy.orm import Session
import models, schemas, oauth2
from utils import hash_password
from database import get_db
from fastapi.templating import Jinja2Templates
from fastapi import Request
from typing import List
from fastapi.encoders import jsonable_encoder


templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/store",
    tags=["Store"],
)

@router.get('/buycredits/')
async def buy_credits_get(request: Request, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    return templates.TemplateResponse("credits_store.html", {"request": request, "current_user": current_user})

@router.post('/buycredits/')
async def buy_credits_post(
    request: Request,
    cardNumber: int = Form(...),
    expiryDate: int = Form(...),
    cvv: int = Form(...),
    cardHolder: str = Form(...),
    credits: int = Form(...),
    current_user: int = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
):

    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if user:
        user.credits += credits
        db.commit()
        db.refresh(user)
        return {"message": "Credits added successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {current_user.id} not found")
    



@router.get('/', response_model=List[schemas.AdvertPackage])
async def get_packages(request: Request,current_user: int = Depends(oauth2.get_current_user) , db: Session = Depends(get_db)):
    packages = db.query(models.AdvertPackages).all()
    user_packages = []
    for advert_package in packages:
        if advert_package in current_user.advert_packages:
            user_packages.append(advert_package)
    return templates.TemplateResponse(name="store.html", context={"request": request, "packages": packages, "user_packages": user_packages, "current_user": current_user})

@router.post('/{advert_package_id}')
async def buy_advert_package(advert_package_id: int, current_user: int = Depends(oauth2.get_current_user), db: Session=Depends(get_db)):
    
    advert_package = db.query(models.AdvertPackages).filter(models.AdvertPackages.id == advert_package_id).first()
    if not advert_package:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Advert package with id {advert_package_id} not found")
    
    
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    print(user)

    if advert_package in user.advert_packages:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You already own this package")

    user.advert_packages.append(advert_package)
    
    if user.credits < advert_package.price:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not enough credits to buy this package")
    
    user.credits -= advert_package.price
    
    db.commit()
    db.refresh(user)

    return {"message": "Package bought successfully"}
