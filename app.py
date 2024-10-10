# app.py
#import logging
from flask import Flask
from flask_cors import CORS
from query_api import routes  

app = Flask(__name__)
CORS(app)

app.register_blueprint(routes)

#logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    app.run(debug=True)