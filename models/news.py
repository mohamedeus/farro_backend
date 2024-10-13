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
    # time_published = db.Column(db.DateTime, nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))

    # Relationship to Product table
    product = db.relationship('ProductModel', back_populates='news')
    
    def to_dict(self):
        return {
            "news_id": self.news_id,
            "publisher": self.publisher,
            "author": self.author,
            "title": self.title,
            "description": self.description,
            "article_url": self.article_url,
            "image_url": self.image_url,
            # "time_published": self.time_published.isoformat() if self.time_published else None,
            "product_id": self.product_id
        } 