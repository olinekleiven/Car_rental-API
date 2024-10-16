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

@routes.route('/add-record', methods=['POST'])
def add_record():
    data = request.json

    name = data.get('name')
    age = data.get('age')
    
    conn = nc()
    query = """
    CREATE (p:Person {name: $name, age: $age})
    name = data.get("name")
    age = data.get("age")
    conn = nc()
    query = """ 
    CREATE (p:person {name: $name, age: $age})
    RETURN p
    """
    parameters = {'name': name, 'age': age}
    result = conn.query(query, parameters)
    conn.close()
    
    result_dicts = [record['p']._properties for record in result]
    return jsonify(result_dicts)


    return jsonify([record['p'] for record in result])

if __name__ == '__main__':
    app.run(debug=True)

