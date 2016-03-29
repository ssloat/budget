#!flask/bin/python
from config import SQLALCHEMY_DATABASE_URI
from mysite import db
db.create_all()
