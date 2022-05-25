import json
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

import stock_manager.errorhandlers
from stock_manager.catalog.views import catalog

app.register_blueprint(catalog)
db.create_all()