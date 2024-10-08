import datetime
from db import db



class NewsModel(db.Model):
    __tablename__ = 'news'

    # Define columns
    news_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    publisher = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    article_url = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=True)
    time_published = db.Column(db.DateTime, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))

    # Relationship to Product table
    product = db.relationship('ProductModel', back_populates='news')