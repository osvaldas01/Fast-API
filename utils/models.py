from sqlalchemy import Column, Integer, String, ForeignKey, Table, DATE
from sqlalchemy.orm import relationship
from utils.database import Base
from datetime import datetime


user_advert_association = Table(
    'user_advert_association', 
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('advert_package_id', Integer, ForeignKey('advert_packages.id'))
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    credits = Column(Integer, nullable=False, default=500)
    time_created = Column(String, nullable=False, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    advert_packages = relationship("AdvertPackages", secondary=user_advert_association)

class AdvertPackages(Base):
    __tablename__ = "advert_packages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)


class CarAdverts(Base):
    __tablename__ = 'car_adverts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    make = Column(String, default=None)
    model = Column(String, default=None)
    phone_number = Column(String, default=None)
    contact_name = Column(String, default=None)
    city = Column(String, default=None)
    price = Column(Integer, default=None)
    year = Column(Integer, default=None)
    first_registration = Column(String, default=None)
    engine_type = Column(String, default=None)
    body_type = Column(String, default=None)
    wheels_size = Column(String, default=None)
    climate_control = Column(String, default=None)
    defects = Column(String, default=None)
    mileage = Column(Integer, default=None)
    fuel_type = Column(String, default=None)
    gearbox = Column(String, default=None)
    color = Column(String, default=None)
    advert_id = Column(String, default=None, unique=True)
    url = Column(String, default=None)