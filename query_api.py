from db_connect import Neo4jConnection as nc
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/add-record', methods=['POST'])
def add_record():
    data = request.json
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

    return jsonify([record['p'] for record in result])

if __name__ == '__main__':
    app.run(debug=True)