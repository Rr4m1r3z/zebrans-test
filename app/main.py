import json
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt import jwt_required, JWT, current_identity

from controllers.SecurityController import SecurityClass

app = Flask(__name__)
db = SQLAlchemy(app)

db.init_app(app)
app.config.from_object('config')
migrate = Migrate(app, db)

jwt = JWT(app, SecurityClass.authenticate, SecurityClass.identity)

@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
	return jsonify({
					'access_token': access_token.decode('utf-8'),
					'idUser' : identity.id,
					'idRol' : identity.idrol,
					'name': identity.name
					})

CORS(app)

@app.route('/protected')
@jwt_required()
def protected():
	return '%s' % current_identity.id

@app.route('/')
@jwt_required()
def hello():
	return "You shouldn't be here"

if __name__ == '__main__':
    app.debug = True
    app.run()