from marshmallow import Schema, fields, validate

class ProductSchema(Schema):

	idbrand=fields.Integer(required=True,validate=validate.Range(min=1, max=5))
	sku=fields.String(
		required=True,
		validate=[
			validate.Length(
				min=8,
				max=12,
				error="SKU must have between {min} and {max} characters."
			),validate.Regexp(
				r"[a-zA-Z0-9]*$",
				error="SKU must not contain special characters")
		])
	name=fields.String(
		required=True,
		validate=[
			validate.Length(
				min=4,
				max=55,
				error="Name must have between {min} and {max} characters."
			),validate.Regexp(
				r"[a-zA-Z\u00C0-\u017F ]*$",
				error="Name must not contain special characters")
		])
	price=fields.Float(allow_none=True)

class ProductUpdateSchema(ProductSchema):

	idproduct=fields.String(
		required=True,
		validate=[
			validate.Length(
				min=32,
				max=32,
				error="Error"
			),validate.Regexp(
				r"[a-zA-Z0-9]*$",
				error="Id must not contain special characters")
		])

class ProductIdSchema(Schema):

	idproduct=fields.String(
		required=True,
		validate=[
			validate.Length(
				min=32,
				max=32,
				error="Error"
			),validate.Regexp(
				r"[a-zA-Z0-9]*$",
				error="Id must not contain special characters")
		])