import hashlib
from werkzeug.security import safe_str_cmp
from controllers.LoginController import LoginClass
from flask import abort, make_response, jsonify

class SecurityClass():

	def authenticate(username,password):

		username = username.strip()
		password = password.strip()

		user = LoginClass.find_by_username(str(username))
		password = hashlib.md5( bytes('{}'.format(password),'utf-8') )

		if user and safe_str_cmp(user.password,password.hexdigest()):
			return user
		else:
			abort(make_response(jsonify(
				description="Invalid credentials",
				error="Bad Request",
				status_code=401), 401))

	def identity(payload):

		user_id = payload['identity']
		return LoginClass.find_by_id(str(user_id))