import json
import uuid
import hashlib

from sqlalchemy import func
from marshmallow import ValidationError
from marshmallow.exceptions import ValidationError
from flask_jwt import jwt_required, current_identity
from flask import request, abort, make_response, jsonify
from sqlalchemy.exc import OperationalError, PendingRollbackError, DataError, IntegrityError, NoResultFound

from models.Schema import User, Rol
from helper.PermissionsHelper import HelperClass
from validations.UserValidation import UserSchema, UserUpdateSchema

class UserClass():

	@jwt_required()
	def save():

		try:
			if HelperClass.check(current_identity.idrol):
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

			else:
				abort(make_response(jsonify(
					description="Insufficient permissions",
					status_code=401), 401))

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
	def show(word):

		try:
			if HelperClass.check(current_identity.idrol):
				session = User.session
				users_list = []

				if word != 'all':

					users = session.query(
						User.iduser,
						Rol.type,
						User.name,
						User.psurname,
						User.msurname,
						User.email,
						User.status,
						User.created
					).join(
						Rol, User.idrol==Rol.idrol
					).filter(
						func.CONCAT_WS(' ',User.name,User.psurname,User.msurname,User.email,Rol.type,User.created)
						.like('%'+word+'%')
					).all()

				else:

					users = session.query(
						User.iduser,
						Rol.type,
						User.name,
						User.psurname,
						User.msurname,
						User.email,
						User.status,
						User.created
					).join(
						Rol, User.idrol==Rol.idrol
					).all()

				session.close()

				if len(users) > 0:

					for user in users:
						user_obj = {
							"id":user[0],
							"rol":user[1],
							"name":user[2] + ' ' + user[3] + ' ' + user[4],
							"email":user[5],
							"status":'Activado' if user[6] == 1 else 'Desactivado',
							"created":user[7]
						}
						users_list.append(user_obj)

				return json.dumps(users_list, default=str)

			else:
				abort(make_response(jsonify(
					description="Insufficient permissions",
					status_code=401), 401))

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
			if HelperClass.check(current_identity.idrol):
				data = request.get_json()
				UserUpdateSchema().load(data)
				session = User.session

				user = session.query(User).filter(User.iduser == data['iduser']).first()

				if user:
					user.idrol = data['idrol']
					user.name = data['name']
					user.psurname = data['psurname']
					user.msurname = data['msurname']
					user.email = data['email']

					session.add(user)
					session.commit()
					session.close()

					abort(make_response(jsonify(description="User update successfully",
						status_code=201), 201))

				abort(make_response(jsonify(description="Something went wrong, please contact to the administrator",
					error="User does not exist.",
					status_code=401), 401))

			else:
				abort(make_response(jsonify(
					description="Insufficient permissions",
					status_code=401), 401))

		except (OperationalError, PendingRollbackError, DataError, ValidationError, KeyError, TypeError, NoResultFound) as inst:
			print(type(inst), (inst.args), (inst))
			abort(make_response(jsonify(description="Something went wrong, please contact to the administrator",
				error="Error",
				status_code=401), 401))

	@jwt_required()
	def delete():

		try:
			if HelperClass.check(current_identity.idrol):
				data = request.get_json()
				session = User.session

				user = session.query(User).filter(User.iduser == data['iduser']).first()

				if user:
					user.status = 0

					session.add(user)
					session.commit()
					session.close()

					abort(make_response(jsonify(description="User deleted successfully",
					status_code=201), 201))
				abort(make_response(jsonify(description="Something went wrong, please contact to the administrator",
					error="User does not exist.",
					status_code=401), 401))

			else:
				abort(make_response(jsonify(
					description="Insufficient permissions",
					status_code=401), 401))

		except (OperationalError, PendingRollbackError, DataError, ValidationError, NoResultFound) as inst:
			print(type(inst), (inst.args), (inst))
			abort(make_response(jsonify(description="Something went wrong, please contact to the administrator",
				error="Error",
				status_code=401), 401))
