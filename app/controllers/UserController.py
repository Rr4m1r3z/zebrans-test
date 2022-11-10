import uuid
import hashlib
from flask_jwt import jwt_required
from werkzeug.security import safe_str_cmp
from flask import request, abort, make_response, jsonify
from marshmallow import ValidationError
from models.Schema import User
from validations.UserValidation import UserSchema, UserUpdateSchema

from sqlalchemy.exc import OperationalError, PendingRollbackError, DataError, IntegrityError, NoResultFound
from marshmallow.exceptions import ValidationError

class UserClass():

    def index():
        try:
            if request.method == 'POST':

                data = request.get_json()
                session = User.session

                users = session.query(
                    User.iduser,
                    User.idrol,
                    User.name,
                    User.email,
                    User.password
                ).filter(
                    User.email == data['username']
                ).one()

                for data_user in users:
                    data_password = data_user.password

                password = hashlib.md5( bytes('{}'.format(data['password']),'utf-8') )
                if data['username'] and safe_str_cmp(data_user.password,password.hexdigest()):
                    return data_user.name
                else:
                    abort(make_response(jsonify(message="Invalid credentials"), 401))

        except ValidationError as e:
            return jsonify(e)

    @jwt_required()
    def store():
        try:
            if request.method == 'POST':
                data = request.get_json()
                session = User.session

                UserSchema().load(data)

                insert = User(
                    iduser = uuid.uuid4().hex,
                    idrol = data['idrol'],
                    name = data['name'],
                    psurname = data['psurname'],
                    msurname = data['msurname'],
                    email = data['email'],
                    password = hashlib.md5(data['password'].encode('utf-8')).hexdigest(),
                    status = data['status'])

                session.add(insert)
                session.commit()
                session.close()

                abort(make_response(jsonify(description="User created successfully",
                status_code=201), 201))

        except (OperationalError, PendingRollbackError, DataError, ValidationError) as inst:
            print(type(inst), (inst.args), (inst))
            abort(make_response(jsonify(description="Something went wrong, please contact to the administrator",
                error="Error",
                status_code=401), 401))
        except (IntegrityError) as e:
            session.rollback()
            errorInfo = e.orig.args
            print(errorInfo[0])
            print(errorInfo[1])
            print(type(e), (e.args[0]), (e))
            abort(make_response(jsonify(description=errorInfo[1],
                error="Duplicate entry",
                status_code=401), 401))

    @jwt_required()
    def show(user_id):
        try:
            if user_id:
                session = User.session

                user = session.query(
                    User.idrol,
                    User.name,
                    User.psurname,
                    User.msurname,
                    User.email,
                    User.status,
                    User.created
                ).filter(
                    User.iduser == user_id
                ).one()

                session.close()

                return {
                    "idrol":user[0],
                    "name":user[1],
                    "psurname":user[2],
                    "msurname":user[3],
                    "email":user[4],
                    "status":user[5],
                    "created":user[6]
                    }

        except (OperationalError, PendingRollbackError, DataError, ValidationError, KeyError, TypeError) as inst:
            print(type(inst), (inst.args), (inst))
            abort(make_response(jsonify(description="Something went wrong, please contact to the administrator",
                error="Error",
                status_code=401), 401))
        except (NoResultFound) as inst:
            print(type(inst), (inst.args), (inst))
            abort(make_response(jsonify(description="No row was found when one was required",
                error="Not found",
                status_code=401), 401))

    @jwt_required()
    def update():
        try:
            if request.method == 'PUT':
                data = request.get_json()
                UserUpdateSchema().load(data)
                session = User.session

                user = session.query(User).filter(User.iduser == data['iduser']).first()

                if user:
                    user.idrol = data['idrol']
                    user.name = data['name']
                    user.psurname = data['psurname']
                    user.msurname = data['msurname']
                    user.status = data['status']

                    session.add(user)
                    session.commit()
                    session.close()

                    abort(make_response(jsonify(description="User update successfully",
                        status_code=201), 201))

                abort(make_response(jsonify(description="Something went wrong, please contact to the administrator",
                    error="User does not exist.",
                    status_code=401), 401))

        except (OperationalError, PendingRollbackError, DataError, ValidationError, KeyError, TypeError) as inst:
            print(type(inst), (inst.args), (inst))
            abort(make_response(jsonify(description="Something went wrong, please contact to the administrator",
                error="Error",
                status_code=401), 401))

    @jwt_required()
    def delete():
        try:
            if request.method == 'DELETE':
                data = request.get_json()
                session = User.session

                user = session.query(User).filter(User.iduser == data['user_id']).first()
                user.status = data['status']

                session.add(user)
                session.commit()
                session.close()

                abort(make_response(jsonify(description="User delete successfully",
                status_code=201), 201))
        except (OperationalError, PendingRollbackError, DataError, ValidationError) as inst:
            print(type(inst), (inst.args), (inst))
            abort(make_response(jsonify(description="Something went wrong, please contact to the administrator",
                error="Error",
                status_code=401), 401))
