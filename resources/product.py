import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db

from models.product import ProductModel
from schemas import ProductSchema

blp = Blueprint("product", __name__, description="Operations on products")

@blp.route("/product/<int:product_id>")
class Product(MethodView):
    
    @blp.response(200, ProductSchema)
    def get(self, product_id):
        return "Created product"
    
    def delete(self, product_id):
        return "Deleted product"



@blp.route("/product")
class ProductList(MethodView):
    
    @blp.response(200, ProductSchema)
    def get(self):
        return "Product Lists"
    
    @blp.arguments(ProductSchema)
    @blp.response(201, ProductSchema)
    def post(self, product_data):
        product = ProductModel(**product_data)
        
        try:
            db.session.add(product)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting product")
            
        return product
            