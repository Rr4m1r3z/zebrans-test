from flask import Blueprint

from controllers.SearchesController import SearchesClass

SearchRoutes = Blueprint('SearchRoutes', __name__)
SearchRoutes.route('/api/v1/<string:word>', methods=['GET'])(SearchesClass.show)