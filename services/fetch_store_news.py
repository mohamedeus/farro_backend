from datetime import datetime
from dateutil import parser
import requests
import os
import logging
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models.news import NewsModel
from flask import current_app, jsonify
from resources.product import ProductList
from schemas import PlainNewsSchema

NEWS_API_KEY = os.getenv('NEWS_API_KEY')  # Set this in your environment or replace with your key

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_and_store_news():
    with current_app.app_context():
        product_list = ProductList()
        products_response = product_list.get().get_json()
        
        if not isinstance(products_response, list):
            logger.error("Unexpected response format from product REST API.")
            logger.error(type(products_response))
            return

        news_items = []
        
        for product in products_response:
            logger.info("Iterating through products")
            
            product_name = product.get("product_name")
            category = product.get("category")

            # Prepare the NewsAPI request
            url = f"https://newsapi.org/v2/everything"
            params = {
                "q": f"{product_name}-{category}",
                "apiKey": NEWS_API_KEY,
                "pageSize": 3,  # Limit to 3 articles
                "language": "en",
                "sortBy": "relevancy"
            }
            response = requests.get(url, params=params, verify=False)

            if response.status_code == 200:
                articles = response.json().get('articles', [])
                # Add top 3 articles to the news database
                for article in articles:
                    try:
                        # published_at_str = article.get('publishedAt', '')
                        # published_at = None
                        # if published_at_str:
                        #     # Use dateutil to parse the ISO 8601 datetime string
                        #     published_at = parser.parse(published_at_str)

                        news_item = NewsModel(
                            publisher=article.get('source', {}).get('name', 'Unknown Publisher'),
                            author=article.get('author', 'Unknown Author'),
                            title=article.get('title', ''),
                            description=article.get('description', ''),
                            article_url=article.get('url', ''),
                            image_url=article.get('urlToImage', ''),
                            # time_published=published_at,
                            product_id=product.get("product_id")
                        )
                        # Append the NewsModel instance directly
                        news_items.append(news_item)

                    except SQLAlchemyError as e:
                        db.session.rollback()
                        logger.error(f"Error occurred while inserting news for product {product_name}: {e}")
            else:
                logger.error(f"Failed to fetch news for product {product_name}. Status Code: {response.status_code}")

        if news_items:
            try:
                # Add NewsModel instances directly to the session
                db.session.add_all(news_items)
                db.session.commit()
                logger.info("Successfully committed all news articles.")

                # Serialize the news_items using Marshmallow
                news_schema = PlainNewsSchema(many=True)
                news_items_serialized = news_schema.dump(news_items)
                
                # Return the serialized data if needed
                logger.info(f"Serialized news items: {news_items_serialized}")
                
            except SQLAlchemyError as e:
                db.session.rollback()
                logger.error(f"Error occurred during committing articles: {e}")
