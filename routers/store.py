from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
import models, schemas, oauth2
from utils import hash_password
from database import get_db

router = APIRouter(
    prefix="/store",
    tags=["Store"],
)

@router.post('/{advert_package_id}', response_model=schemas.UserOut)
def buy_advert_package(advert_package_id: int, current_user: int = Depends(oauth2.get_current_user), db: Session=Depends(get_db)):
    
    advert_package = db.query(models.AdvertPackages).filter(models.AdvertPackages.id == advert_package_id).first()
    if not advert_package:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Advert package with id {advert_package_id} not found")
    
    user = db.query(models.User).filter(models.User.id == current_user.id).first()

    if advert_package in user.advert_packages:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You already own this package")

    user.advert_packages.append(advert_package)
    
    if user.credits < advert_package.price:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not enough credits to buy this package")
    
    user.credits -= advert_package.price
    
    db.commit()
    db.refresh(user)
    return user