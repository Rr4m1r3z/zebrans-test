from flask import Blueprint

from controllers.ProductController import ProductClass

ProductRoutes = Blueprint('ProductRoutes', __name__)

ProductRoutes.route('/api/v1/create', methods=['POST'])(ProductClass.save)
ProductRoutes.route('/api/v1/update', methods=['PATCH'])(ProductClass.update)
ProductRoutes.route('/api/v1/delete', methods=['DELETE'])(ProductClass.delete)
ProductRoutes.route('/api/v1/<string:product_id>', methods=['GET'])(ProductClass.show)