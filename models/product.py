from db import db

class ProductModel(db.Model):    
    
    __tablename__ = 'product'

    # Define columns
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    unit = db.Column(db.String(50), nullable=False)
    
    news = db.relationship("NewsModel", back_populates="product")