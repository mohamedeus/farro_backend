from marshmallow import Schema, fields

class PlainProductSchema(Schema):
    
    product_id = fields.Int(dump_only=True)
    product_name = fields.Str(required=True)
    category = fields.Str()
    description = fields.Str()
    unit = fields.Str()
    
    
class PlainNewsSchema(Schema):
    news_id = fields.Int(dump_only=True)
    publisher = fields.Str(required=True)
    author = fields.Str()
    title = fields.Str(required=True)
    description = fields.Str()
    article_url = fields.Str(required=True)
    image_url = fields.Str()
    time_published = fields.DateTime()
    

class ProductSchema(PlainProductSchema):
    news = fields.List(fields.Nested(PlainNewsSchema), dump_only=True)
    
class NewsSchema(PlainNewsSchema):
    product_id = fields.Int(required=True, load_only=True)
    product = fields.Nested(PlainProductSchema, required = True, dump_only=True)
    