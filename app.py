from flask import Flask, request,jsonify
from flask_cors import CORS
import datetime


date = datetime.datetime.now()

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})
    
@app.route('/data')
def get_time():
    
    return {
        'Name':"geek", 
        "Age":"22",
        "Date":date, 
        "programming":"python"
        }
      
    
if __name__ == '__main__':
    app.run(debug=True)