from marshmallow import Schema, fields, validate

class UserSchema(Schema):

	idrol = fields.Integer(required=True,validate=validate.OneOf([1,2]))
	name = fields.String(
		required=True,
		validate=[
			validate.Length(
				min=4,
				max=20,
				error="User name must have between {min} and {max} characters."
			),validate.Regexp(
				r"[a-zA-Z\u00C0-\u017F_\-]*$",
				error="User name must not contain special characters"
				"(except _ and -)")
		])
	psurname = fields.String(
		required=True,
		validate=[
			validate.Length(
				min=4,
				max=20,
				error="Psurname must have between {min} and {max} characters."
			),validate.Regexp(
				r"[a-zA-Z\u00C0-\u017F_\-]*$",
				error="Psurname must not contain special characters"
				"(except _ and -)")
		])
	msurname = fields.String(
		required=True,
		validate=[
			validate.Length(
				min=4,
				max=20,
				error="Msurname must have between {min} and {max} characters."
			),validate.Regexp(
				r"[a-zA-Z\u00C0-\u017F_\-]*$",
				error="Msurname must not contain special characters"
				"(except _ and -)")
		])
	email = fields.Str(required=True, validate=validate.Email(error="Not a valid email address"))
	password = fields.String(
		required=True,
		validate=[
			validate.Length(
				min=4,
				max=20,
				error="Password must have between {min} and {max} characters."
			),validate.Regexp(
				r"[a-zA-Z0-9]*$",
				error="Password must not contain special characters")
		])
	status = fields.Integer(required=True,validate=validate.Range(min=1, max=1))

class UserUpdateSchema(Schema):
	iduser = fields.String(required=True,
		validate=[
			validate.Length(
				min=1,
				max=60,
				error="IDuser must have between {min} and {max} characters."
			),validate.Regexp(
				r"[a-zA-Z0-9]*$",
				error="IDuser must not contain special characters")
		])
	idrol = fields.Integer(required=True,validate=validate.Range(min=1, max=1))
	name = fields.String(required=True,
		validate=[
			validate.Length(
				min=4,
				max=20,
				error="User name must have between {min} and {max} characters."
			),validate.Regexp(
				r"[a-zA-Z\u00C0-\u017F_\-]*$",
				error="User name must not contain special characters"
				"(except _ and -)")
		])
	psurname = fields.String(required=True,
		validate=[
			validate.Length(
				min=4,
				max=20,
				error="Psurname must have between {min} and {max} characters."
			),validate.Regexp(
				r"[a-zA-Z\u00C0-\u017F_\-]*$",
				error="Psurname must not contain special characters"
				"(except _ and -)")
		])
	msurname = fields.String(required=True,
		validate=[
			validate.Length(
				min=4,
				max=20,
				error="Msurname must have between {min} and {max} characters."
			),validate.Regexp(
				r"[a-zA-Z\u00C0-\u017F_\-]*$",
				error="Msurname must not contain special characters"
				"(except _ and -)")
		])
	status = fields.Integer(required=True,validate=validate.Range(min=1, max=1))