from flask import Blueprint

from controllers.UserController import UserClass

UserRoutes = Blueprint('UserRoutes', __name__)

UserRoutes.route('/api/v1/create', methods=['POST'])(UserClass.store)
UserRoutes.route('/api/v1/<string:user_id>', methods=['GET'])(UserClass.show)
UserRoutes.route('/api/v1/edit', methods=['PUT'])(UserClass.update)
UserRoutes.route('/api/v1/destroy', methods=['DELETE'])(UserClass.delete)