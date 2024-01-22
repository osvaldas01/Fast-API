from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
import models, schemas, oauth2
from utils import hash_password, verify_password
from database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get('/', response_model=schemas.UserOut)
def get_user(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found") 
    packages = []
    
    for advert_package in user.advert_packages:
        packages.append(schemas.AdvertPackage(name=advert_package.name, price=advert_package.price))
        
    return schemas.UserOut(email=user.email, credits=user.credits, packages=packages)
