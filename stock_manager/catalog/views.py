from flask import request, jsonify, Blueprint, abort
from flask.views import MethodView
from stock_manager import db, app
from stock_manager.catalog.models import Product


catalog = Blueprint('catalog', __name__)

@catalog.route('/')
@catalog.route('/home')
def home():
    return jsonify({
        'message': 'Sistema gerenciador de estoque',
        'version': '1.0',
        'author': 'SamuraiPetrus'
    })

class ProductView(MethodView):
    def get(self, id=None, page=1):
        res = {}

        if not id:
            # List all products.
            products = Product.query.paginate(page, 10).items

            for product in products:
                res[product.id] = {
                    'name': product.name,
                    'price': Product.get_formatted_price(product)
                }
        else:
            # List ptoduct by ID.
            product = Product.query.filter_by(id=id).first()

            if not product:
                abort(404)
            
            res = {
                'name': product.name,
                'price': Product.get_formatted_price(product)
            }
        
        return jsonify(res)
    
    def post(self):
        req = request.get_json()
        product = Product(req['name'], req['price'])
        db.session.add(product)
        db.session.commit()

        return jsonify({
            product.id: {
                'name': product.name,
                'price': Product.get_formatted_price(product)
            }
        })

product_view = ProductView.as_view('product_view')

app.add_url_rule(
    '/product/', view_func=product_view, methods=['GET', 'POST']
)

app.add_url_rule(
    '/product/<int:id>', view_func=product_view, methods=['GET']
)