from db_connect import Neo4jConnection as nc
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

routes = Blueprint('routes', __name__)

@routes.route("/")
def home():
    return "Welcome to the car rental api"

@routes.route('/test-query', methods=['GET'])
def test_query():
    conn = nc()
    result = conn.query("MATCH (n) RETURN n LIMIT 5")
    conn.close()
    result_dicts = [record['n']._properties for record in result]
    return jsonify(result_dicts)