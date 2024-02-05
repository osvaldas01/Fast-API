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
    Marke: str = None
    Modelis: str = None
    Telefono_nr: str = None
    Kontakto_vardas: str = None
    Miestas: str = None
    Kaina: str = None
    Metai: str = None
    Pirma_registracija: str = None
    Variklis: str = None
    Kebulas: str = None
    Ratai: str = None
    Klimatas: str = None
    Defektai: str = None
    Rida: str = None
    Kuras: str = None
    Deze: str = None
    Spalva: str = None
    
    class Config:
        from_attributes = True
        

class Car(BaseModel):
    Marke: str = None

class CarModel(BaseModel):
    Modelis: str = None