import json
from flask import abort, make_response, jsonify

from sqlalchemy import func
from marshmallow import ValidationError
from marshmallow.exceptions import ValidationError
from flask_jwt import jwt_required, current_identity
from sqlalchemy.exc import OperationalError, PendingRollbackError, DataError, NoResultFound

from models.Schema import Product, User, Track
from helper.PermissionsHelper import HelperClass

class SearchesClass():

	@jwt_required()
	def show(word):

		try:
			if HelperClass.check(current_identity.idrol):
				session = Track.session
				searches_list = []

				if word != 'all':

					searches = session.query(
						User.name,
						User.psurname,
						User.msurname,
						Product.sku,
						Product.name,
						Track.created
					).join(
						User, Track.iduser==User.iduser
					).join(
						Product, Track.idproduct==Product.idproduct
					).filter(
						func.CONCAT_WS(' ',User.name,User.psurname,User.msurname,Product.sku,Product.name)
						.like('%'+word+'%')
					).all()

				else:

					searches = session.query(
						User.name,
						User.psurname,
						User.msurname,
						Product.sku,
						Product.name,
						Track.created
					).join(
						User, Track.iduser==User.iduser
					).join(
						Product, Track.idproduct==Product.idproduct
					).all()

				session.close()

				if len(searches) > 0:

					for searche in searches:
						user_obj = {
							"name":searche[0] + ' ' + searche[1] + ' ' + searche[2],
							"sku":searche[3],
							"product":searche[4],
							"created":searche[5]
						}
						searches_list.append(user_obj)

				return json.dumps(searches_list, default=str)

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