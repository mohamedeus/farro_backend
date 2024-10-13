from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from sqlalchemy.exc import SQLAlchemyError


from models.news import NewsModel
from schemas import NewsSchema

from db import db
from services.fetch_store_news import fetch_and_store_news


blp = Blueprint("news", __name__, description="Operations on news")

@blp.route("/news/<int:product_id>")
class News(MethodView):
    
    blp.response(201, NewsSchema)
    def get(self, news_id):
        news = NewsModel.query.get_or_404(news_id)
        return news
    
    def delete(self, news_id):
        news = NewsModel.query.get_or_404(news_id)
        
        db.session.delete(news)
        db.session.commit()
        return {"message":"News Deleted"}, 200
        
            
        #TODO implement update


@blp.route("/news")
class NewsList(MethodView):
    
    blp.response(200, NewsSchema(many=True))
    def get(self):
        
        news_items = NewsModel.query.all()
        if not news_items:
            news_items = NewsModel.query.all()
        if not news_items:
            abort(404, message="No news found.")
        fetch_and_store_news()
        
        # Mod 10/11
        # news_schema = NewsSchema(many=True)
        serialized_news = [news_item.to_dict() for news_item in news_items]
        return serialized_news
        
        
        # return news_items
    
    @blp.arguments(NewsSchema)
    @blp.response(201, NewsSchema)
    def post(self, news_data):
        
        news = NewsModel(**news_data)
        
        try:
            db.session.add(news)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting news")
            
        return news