from flask import Blueprint

from controllers.UserController import UserClass

UserRoutes = Blueprint('UserRoutes', __name__)

UserRoutes.route('/api/v1/create', methods=['POST'])(UserClass.save)
UserRoutes.route('/api/v1/<string:word>', methods=['GET'])(UserClass.show)
UserRoutes.route('/api/v1/update', methods=['PUT'])(UserClass.update)
UserRoutes.route('/api/v1/delete', methods=['DELETE'])(UserClass.delete)