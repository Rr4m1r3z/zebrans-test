from models.Schema import User
from sqlalchemy.exc import NoResultFound

from flask import abort
from flask import jsonify
from flask import make_response

class LoginClass(object):
    def __init__(self,iduser,idrol,name, username,password):

        self.id = iduser
        self.idrol = idrol
        self.name = name
        self.email = username
        self.password = password

    @classmethod
    def find_by_username(cls,username):

        try:
            session = User.session

            row = session.query(
                User.iduser,
                User.idrol,
                User.name,
                User.email,
                User.password
            ).filter(
                User.email == username,
                User.status == 1
            ).one()

            if row:
                cls.idrol = row[1]
                cls.name = row[2]

                user = cls(*row)
            else:
                user = None

            return user

        except (NoResultFound) as inst:
            print(type(inst)), (inst)
            abort(make_response(jsonify(
                description="Something went wrong, try again",
                error="Bad Request",
                status_code=401), 401))

    @classmethod
    def find_by_id(cls,idUser):

        try:
            session = User.session

            row = session.query(
                User.iduser,
                User.idrol,
                User.name,
                User.email,
                User.password
            ).filter(
                User.iduser == idUser,
                User.status == 1
            ).one()

            if row:
                user = cls(*row)
            else:
                user = None

            return user

        except (NoResultFound) as inst:
            print(type(inst)), (inst)
            abort(make_response(jsonify(description="Something went wrong, try again",
                error="Bad Request",
                status_code=401), 401))

    @classmethod
    def check_jwt(jwt):

        try:
            session = User.session

            row = session.query().count()

            return row
        except (NoResultFound) as inst:
            print(type(inst)), (inst)
            abort(make_response(jsonify(description="Something went wrong, try again",
                error="Bad Request",
                status_code=401), 401))