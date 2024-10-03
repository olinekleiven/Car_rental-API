# app.py
from flask import Flask
from flask_cors import CORS
from query_api import routes  

app = Flask(__name__)
CORS(app)

app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)