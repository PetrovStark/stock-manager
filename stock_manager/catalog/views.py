from flask import request, jsonify, Blueprint, abort
from flask.views import MethodView
from stock_manager import db, app
from stock_manager.catalog.models import Product

catalog = Blueprint('catalog', __name__)

class ProductView(MethodView):
    def get(self, id=None, page=1):
        args = request.args.to_dict()
        res = []

        if not id:
            if args.get('page') is not None:
                page = int(args.get('page'))

            # List all products.
            products = Product.query.paginate(page, 10).items

            for product in products:
                res.append({
                    'id': product.id,
                    'name': product.name,
                    'price': Product.get_formatted_price(product)
                })
        else:
            # List ptoduct by ID.
            product = Product.query.filter_by(id=id).first()

            if not product:
                abort(404, 'This product does not exist')
            
            res = {
                'id': product.id,
                'name': product.name,
                'price': Product.get_formatted_price(product)
            }
        
        return jsonify(res)
    
    def post(self):
        req = request.get_json()
        product = Product(req['name'], req['price'])
        
        if Product.is_product_already_exists(Product, req['name']):
            abort(400, 'There\'s another product with the same name.')

        db.session.add(product)
        db.session.commit()

        return jsonify({
            'id': product.id,
            'name': product.name,
            'price': Product.get_formatted_price(product)
        })

product_view = ProductView.as_view('product_view')

app.add_url_rule(
    '/product/', view_func=product_view, methods=['GET', 'POST']
)

app.add_url_rule(
    '/product/<int:id>', view_func=product_view, methods=['GET']
)