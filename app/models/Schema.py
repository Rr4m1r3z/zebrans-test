import os
import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, engine, Numeric
from sqlalchemy.dialects.mysql import TINYTEXT

import config

conf = config.SQLALCHEMY_DATABASE_URI
engine = create_engine(conf)
Base = declarative_base()

class User(Base):
	__tablename__='user'

	iduser=Column(String(45), primary_key=True, unique=True)
	idrol=Column(Integer(), ForeignKey('rol.idrol'))
	name=Column(String(45))
	psurname=Column(String(45))
	msurname=Column(String(45))
	email=Column(String(65),unique=True)
	password=Column(String(45))
	status=Column(Integer())
	created=Column(DateTime, default=datetime.datetime.utcnow)

	def __init__(self, iduser=None, idrol=None, name=None, psurname=None, msurname=None, email=None, password=None, status=None, created=None):

		self.iduser=iduser
		self.idrol=idrol
		self.name=name
		self.psurname=psurname
		self.msurname=msurname
		self.email=email
		self.password=password
		self.status=status
		self.created=created

	@property
	def serialize(self):
		return {
			'iduser':self.iduser,
			'idrol':self.idrol,
			'name':self.name,
			'psurname':self.psurname,
			'msurname':self.msurname,
			'email':self.email,
			'password':self.password,
			'status':self.status,
			'created':self.created
		}

	Session=sessionmaker(engine)
	session=Session()


class Rol(Base):
	__tablename__='rol'

	idrol = Column(Integer(), unique=True, primary_key=True, autoincrement=True)
	type = Column(String(15))

	def __init__(self, idrol=None, type=None):

		self.idrol=idrol
		self.type=type

	@property
	def serialize(self):
		return {
			'idrol':self.idrol,
			'type':self.type
		}

	Session=sessionmaker(engine)
	session=Session()


class Product(Base):
	__tablename__='product'

	idproduct=Column(String(45), primary_key=True, unique=True)
	idbrand=Column(Integer(), ForeignKey('brand.idbrand'))
	sku=Column(String(12), unique=True)
	name=Column(String(55), unique=True)
	price=Column(Numeric(5,2))

	def __init__(self, idproduct=None, idbrand=None, sku=None, name=None, price=None):
		self.idproduct=idproduct
		self.idbrand=idbrand
		self.sku=sku
		self.name=name
		self.price=price

	@property
	def serialize(self):
		return {
			'idproduct':self.idproduct,
			'idbrand':self.idbrand,
			'sku':self.sku,
			'name':self.name,
			'price':self.name
		}

	Session=sessionmaker(engine)
	session=Session()


class Brand(Base):
	__tablename__='brand'

	idbrand=Column(Integer(), unique=True, primary_key=True, autoincrement=True)
	name=Column(String(45), unique=True)

	def __init__(self, idbrand=None, name=None):
		self.idbrand=idbrand
		self.name=name

	@property
	def serialize(self):
		return {
			'idbrand':self.idbrand,
			'type':self.name
		}

	Session=sessionmaker(engine)
	session=Session()


class Track(Base):
	__tablename__='track'

	idtrack=Column(Integer(), unique=True, primary_key=True, autoincrement=True)
	iduser=Column(String(45), ForeignKey('user.iduser'))
	idproduct=Column(String(45), ForeignKey('product.idproduct'))
	created=Column(DateTime, default=datetime.datetime.utcnow)

	def __init__(self, idtrack=None,iduser=None, idproduct=None, created=None):
		self.idtrack=idtrack
		self.iduser=iduser
		self.idproduct=idproduct
		self.created=created

	@property
	def serialize(self):
		return {
			'idtrack':self.idtrack,
			'iduser':self.iduser,
			'idproduct':self.idproduct,
			'created':self.created
		}

	Session=sessionmaker(engine)
	session=Session()