import os
import uuid
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_jwt import jwt_required, current_identity
from flask import request, abort, make_response, jsonify

from sqlalchemy.exc import OperationalError, PendingRollbackError, DataError, IntegrityError, NoResultFound
from marshmallow import ValidationError
from marshmallow.exceptions import ValidationError

from models.Schema import Product, User, Track
from validations.ProductValidation import ProductSchema, ProductUpdateSchema, ProductIdSchema
from helper.PermissionsHelper import HelperClass

class ProductClass():

	@jwt_required()
	def show(product_id):
		try:
			ProductIdSchema().load({"idproduct":product_id})
			session=Product.session

			product = session.query(Product).filter(
						Product.idproduct == product_id
						).first()

			if not HelperClass.check(current_identity.idrol):
				ProductClass.__log(current_identity.id,product_id)

			return product.serialize

		except (OperationalError, PendingRollbackError, DataError, ValidationError, TypeError, NoResultFound, AttributeError) as inst:
			print(type(inst), (inst.args), (inst))
			abort(make_response(jsonify(
				description="Something went wrong, please contact to the administrator",
				error="Error",
				status_code=401), 401))
		except (IntegrityError) as e:
			session.rollback()
			errorInfo = e.orig.args
			print(errorInfo[0], errorInfo[1], type(e), (e.args[0]), (e))
			abort(make_response(jsonify(description=errorInfo[1],
				error="Duplicate entry",
				status_code=401), 401))

	@jwt_required()
	def save():
		try:
			data=request.get_json()
			ProductSchema().load(data)
			session=Product.session

			if HelperClass.check(current_identity.idrol):

				insert=Product(
						idproduct=uuid.uuid4().hex,
						idbrand=data['idbrand'],
						sku=data['sku'],
						name=data['name'],
						price=data['price'])

				idProduct=insert.idproduct

				session.add(insert)
				session.commit()
				session.close()

				ProductClass.__sent_email(current_identity.id,'creado',idProduct)

				abort(make_response(jsonify(
					description="Product created successfully",
					status_code=201), 201))

			else:
				abort(make_response(jsonify(
					description="Insufficient permissions",
					status_code=401), 401))

		except (OperationalError, PendingRollbackError, DataError, ValidationError, TypeError) as inst:
			print(type(inst), (inst.args), (inst))
			abort(make_response(jsonify(
				description="Something went wrong, please contact to the administrator",
				error="Error",
				status_code=401), 401))
		except (IntegrityError) as e:
			session.rollback()
			errorInfo = e.orig.args
			print(errorInfo[0], errorInfo[1], type(e), (e.args[0]), (e))
			abort(make_response(jsonify(description=errorInfo[1],
				error="Duplicate entry",
				status_code=401), 401))

	@jwt_required()
	def update():

		try:
			data=request.get_json()
			ProductUpdateSchema().load(data)
			session=Product.session

			if HelperClass.check(current_identity.idrol):

				product = session.query(Product).filter(
						Product.idproduct == data['idproduct']
						).first()

				if product:

					product.idbrand=data['idbrand']
					product.sku=data['sku']
					product.name=data['name']
					product.price=data['price']

					session.add(product)
					session.commit()
					session.close()

					ProductClass.__sent_email(current_identity.id,'actualizado',data['idproduct'])

					abort(make_response(jsonify(
						description="Product updated successfully",
						status_code=201), 201))
				else:
					abort(make_response(jsonify(
						description="Product not found",
						status_code=201), 201))
			else:
				abort(make_response(jsonify(
					description="Insufficient permissions",
					status_code=401), 401))

		except (OperationalError, PendingRollbackError, DataError, ValidationError, TypeError, NoResultFound) as inst:
			print(type(inst), (inst.args), (inst))
			abort(make_response(jsonify(
				description="Something went wrong, please contact to the administrator",
				error="Error",
				status_code=401), 401))
		except (IntegrityError) as e:
			session.rollback()
			errorInfo = e.orig.args
			print(errorInfo[0], errorInfo[1], type(e), (e.args[0]), (e))
			abort(make_response(jsonify(description=errorInfo[1],
				error="Duplicate entry",
				status_code=401), 401))

	@jwt_required()
	def delete():

		try:
			data=request.get_json()
			ProductIdSchema().load(data)
			session=Product.session

			if HelperClass.check(current_identity.idrol):

				result=session.query(Product).filter(Product.idproduct == data['idproduct']).delete()
				session.commit()
				session.close()

				if result == 1:

					ProductClass.__sent_email(current_identity.id,'borrado',data['idproduct'])

					abort(make_response(jsonify(
						description="Product deleted successfully",
						status_code=201), 201))

				else:
					abort(make_response(jsonify(
						description="Product not found",
						status_code=401), 401))

		except (OperationalError, PendingRollbackError, DataError, ValidationError, TypeError, NoResultFound) as inst:
			print(type(inst), (inst.args), (inst))
			abort(make_response(jsonify(
				description="Something went wrong, please contact to the administrator",
				error="Error",
				status_code=401), 401))
		except (IntegrityError) as e:
			session.rollback()
			errorInfo = e.orig.args
			print(errorInfo[0], errorInfo[1], type(e), (e.args[0]), (e))
			abort(make_response(jsonify(description=errorInfo[1],
				error="Duplicate entry",
				status_code=401), 401))

	@jwt_required()
	def __sent_email(idRemitente,action,idProduct):

		session=User.session
		users = session.query(User).filter(
						User.idrol == 1
						).all()

		destinatarios=''
		for user in users:
			destinatarios+=user.name+' <'+user.email+'>,'

		remitter = os.environ['EMAIL']
		addressee=destinatarios[:-1]
		asunto = "Nuevo movimiento en el catalogo de productos"
		body = """Buen día!<br/> <br/>
		Se informa que el usuario <b>%s</b> a <b>%s</b> el registro con ID <b>%s</b>
		"""%(user.name+' '+user.psurname+' '+user.msurname,action,idProduct)

		msg = MIMEMultipart()
		msg['From'] = remitter
		msg['password'] = os.environ['PASS']
		msg['To'] = addressee
		msg['Subject'] = asunto

		msg.attach(MIMEText(body, 'html'))
		server = smtplib.SMTP('smtp-mail.outlook.com: 587')

		server.starttls()
		server.login(msg['From'], msg['password'])
		texto = msg.as_string()
		server.sendmail(msg['From'], msg['To'].split(","), texto)
		server.quit()

	@jwt_required()
	def __log(idUser,idProduct):

		session=Track.session

		insert=Track(
				iduser=idUser,
				idproduct=idProduct)

		session.add(insert)
		session.commit()
		session.close()
