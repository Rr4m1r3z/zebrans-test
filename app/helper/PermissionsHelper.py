from flask_jwt import jwt_required
from flask import abort, make_response, jsonify

class HelperClass():

    @jwt_required()
    def check(data):

        try:
            return True if data == 1 else False
        except Exception as inst:
            print(type(inst), (inst.args), (inst))
            abort(make_response(jsonify(description="Something went wrong, please contact to the administrator",
                error="Error",
                status_code=401), 401))