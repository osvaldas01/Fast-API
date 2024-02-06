from pydantic import BaseModel, EmailStr
from typing import Optional

class AdvertPackage(BaseModel):
    name: str
    price: int
    
    class Config:
        from_attributes = True

class UserOut(BaseModel):
    email: EmailStr
    credits: int
    packages: list[AdvertPackage]
    
    class Config:
        from_attributes = True    

    
class UserOutAfterPasswordChange(BaseModel):
    email: EmailStr
    msg: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    user_email: Optional[str] = None
    user_id: Optional[int] = None

class CarAdvert(BaseModel):
    Skelbimo_id: int
    make: str = None
    model: str = None
    phone_number: str = None
    contact_name: str = None
    city: str = None
    price: str = None
    year: str = None
    first_registration: str = None
    engine_type: str = None
    body_type: str = None
    wheels_size: str = None
    climate_control: str = None
    defects: str = None
    mileage: str = None
    fuel_type: str = None
    gearbox: str = None
    color: str = None
    
    class Config:
        from_attributes = True
        

class Car(BaseModel):
    make: str = None

class CarModel(BaseModel):
    model: str = None