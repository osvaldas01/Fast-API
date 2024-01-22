from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base
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
    Marke = Column(String, default=None)
    Modelis = Column(String, default=None)
    Telefono_nr = Column(String, default=None)
    Kontakto_vardas = Column(String, default=None)
    Miestas = Column(String, default=None)
    Kaina = Column(String, default=None)
    Metai = Column(String, default=None)
    Pirma_registracija = Column(String, default=None)
    Variklis = Column(String, default=None)
    Kebulas = Column(String, default=None)
    Ratai = Column(String, default=None)
    Klimatas = Column(String, default=None)
    Defektai = Column(String, default=None)
    Rida = Column(String, default=None)
    Kuras = Column(String, default=None)
    Deze = Column(String, default=None)
    Spalva = Column(String, default=None)
    Skelbimo_id = Column(String, default=None, unique=True)
    URL = Column(String, default=None)