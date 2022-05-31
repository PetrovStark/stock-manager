# Error Handlers
from stock_manager import app
from flask import jsonify

@app.errorhandler(400)
def forbidden(e):
    return jsonify({
        'status': 400,
        'code': 'bad_request',
        'message': str(e)
    }), 400

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'status': 404,
        'code': 'not_found',
        'message': str(e)
    }), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({
        'status': 500,
        'code': 'internal_server_error',
        'message': str(e)
    }), 500