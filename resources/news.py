import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import NewsSchema

blp = Blueprint("news", __name__, description="Operations on news")

@blp.route("/news/<int:product_id>")
class News(MethodView):
    
    blp.response(201, NewsSchema)
    def get(self, news_id):
        return "News Article"
    
    def delete(self, news_id):
        return "Deleted news"



@blp.route("/news>")
class NewsList(MethodView):
    
    blp.response(200, NewsSchema(many=True))
    def get(self):
        return "News List"
    
    @blp.arguments(NewsSchema)
    @blp.response(201, NewsSchema)
    def post(self, news_data):
        return "News Posted"