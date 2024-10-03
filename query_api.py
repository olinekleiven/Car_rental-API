from db_connect import Neo4jConnection as nc
from flask import Flask, request, jsonify, Blueprint

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return "Welcome to the Car Rental API!"

@routes.route('/test-query', methods=['GET'])
def test_query():
    conn = nc()
    result = conn.query("MATCH (n) RETURN n LIMIT 5")
    conn.close()
    return jsonify([record['n'] for record in result])

@routes.route('/add-record', methods=['POST'])
def add_record():
    data = request.json
    name = data.get('name')
    age = data.get('age')
    
    conn = nc()
    query = """
    CREATE (p:Person {name: $name, age: $age})
    RETURN p
    """
    parameters = {'name': name, 'age': age}
    result = conn.query(query, parameters)
    conn.close()
    
    return jsonify([record['p'] for record in result])