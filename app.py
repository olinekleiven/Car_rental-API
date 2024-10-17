# app.py
#import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from query_api import routes  
from db_connect import Neo4jConnection as nc
import logging
from flask import Blueprint
app = Flask(__name__)
CORS(app)   
car_api = Blueprint('car_api', __name__)
app.register_blueprint(routes)

logging.basicConfig(level=logging.DEBUG)

# Kode for å legge inn POST /cars
@app.route('/add_car', methods=['POST'])
def add_car():

    # Henter data fra forespørselen (JSON format)
    data = request.json
    make = data.get('make')
    model = data.get('model')
    year = data.get('year')
    location = data.get('location')
    status = data.get('status')

# Connect to Neo4j and add the car
    conn = nc()
    query = """
    CREATE (c:Car {make: $make, model: $model, year: $year, location: $location, status: $status})
    RETURN c
    """
    parameters = {'make': make, 'model': model, 'year': year, 'location': location, 'status': status}
    result = conn.query(query, parameters)
    conn.close()

    # Extract the properties of the created car node
    car = result[0]['c']._properties if result else {}

    response = {
        "message": "Car added successfully",
        "car": car
    }
    return jsonify(response), 201


@app.route('/get_cars', methods=['GET'])
def get_cars():
    conn = nc()
    query = """
    MATCH (c:Car)
    RETURN c
    """
    try:
        result = conn.query(query)
        conn.close()
        if not result:
            app.logger.debug("No cars found in the database.")
            return jsonify({"message": "No cars found"}), 404
        # Convert Node objects to dictionaries
        cars = [record['c']._properties for record in result]
        app.logger.debug(f"Returning cars: {cars}")
        return jsonify(cars), 200
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

@app.route('/update_car', methods=['POST'])
def update_car():
    data = request.json
    make = data.get('make')
    model = data.get('model')
    year = data.get('year')
    location = data.get('location')
    status = data.get('status')

    conn = nc()
    query = """
    MATCH (c:Car {make: $make, model: $model})
    SET c.year = $year, c.location = $location, c.status = $status
    RETURN c
    """

    parameters = {'make': make, 'model': model, 'year': year, 'location': location, 'status': status}
    result = conn.query(query, parameters)
    conn.close()
    # Extract the properties of the created car node
    car = result[0]['c']._properties if result else {}

    response = {
        "message": "Car updated successfully",
        "status": status,
        "car": car
    }
    return jsonify(response), 201

@app.route('/delete_car', methods=['POST'])
def delete_car():
    data = request.json
    make = data.get('make')
    model = data.get('model')

    conn = nc()
    query = """
    MATCH (c:Car {make: $make, model: $model})
    DETACH DELETE c
    """

    parameters = {'make': make, 'model': model}
    conn.query(query, parameters)
    conn.close()

    response = {
        "message": "Car deleted successfully",
        "make": make,
        "model": model
    }
    return jsonify(response), 200 

@app.route('/add_customer', methods=['POST'])
def add_customer():
    data = request.json
    name = data.get('name')
    age = data.get('age')
    adress = data.get('adress')

    conn = nc()
    query = """
    CREATE (c:Customer {name: $name, age: $age, adress: $adress})
    RETURN c
    """
    parameters = {'name': name, 'age': age, 'adress': adress}
    result = conn.query(query, parameters)
    conn.close()

    customer = result[0]['c']._properties if result else {}

    response = {
        "message": "Customer added successfully",
        "customer": customer
    }
    return jsonify(response), 201

#GET COSYUMER
@app.route('/get_customers', methods=['GET'])
def get_customer():
    conn = nc()
    query = """
    MATCH (c:Customer)
    RETURN c
    """
    try:
        result = conn.query(query)
        conn.close()
        
        customers = [record['c']._properties for record in result]
        return jsonify(customers), 200
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

#UPDATE CUSTOMER

@app.route('/update_customer', methods=['POST'])
def update_customer():
    data = request.json
    name = data.get('name')
    age = data.get('age')
    adress = data.get('adress')
 
    conn = nc()
    query = """
    MATCH (c:Customer {name: $name})
    SET c.name = $name, c.age = $age, c.adress = $adress
    RETURN c
    """
        # sjøl om vi skriver name her kunne vi hatt id

    parameters = {'name': name, 'age': age, 'adress': adress,}
    result = conn.query(query, parameters)
    conn.close()
    # Extract the properties of the created car node
    customer = result[0]['c']._properties if result else {}

    response = {
        "message": "Customer updated sucessfully",
        "customer": customer
    }
    return jsonify(response), 201


@app.route('/delete_customer', methods=['POST'])
def delete_customer():
    data = request.json
    name = data.get('name')
    age = data.get('age')
    adress = data.get('adress')

    conn = nc()
    query = """
    MATCH (c:Customer {name: $name})
    DETACH DELETE c
    """

    parameters = {'name': name, 'age': age, 'adress': adress}
    conn.query(query, parameters)
    conn.close()

    response = {
        "message": "Customer deleted successfully",
        "name": name,
        "age": age,
        "adress": adress
    }
    return jsonify(response), 200 


#emplyee

@app.route('/add_employee', methods=['POST'])
def add_employee():
    data = request.json
    name = data.get('name')
    adress = data.get('adress')
    branch = data.get('branch')

    conn = nc()
    query = """
    CREATE (e:Employee {name: $name, adress: $adress, branch: $branch})
    RETURN e
    """
    parameters = {'name': name, 'adress': adress, 'branch': branch}
    result = conn.query(query, parameters)
    conn.close()

    employee = result[0]['e']._properties if result else {}

    response = {
        "message": "Employee added successfully",
        "employee": employee
    }
    return jsonify(response), 201

#GET EMPLOYEE
@app.route('/get_employees', methods=['GET'])
def get_employee():
    conn = nc()
    query = """
    MATCH (e:Employee)
    RETURN e
    """
    try:
        result = conn.query(query)
        conn.close()
        
        employees = [record['e']._properties for record in result]
        return jsonify(employees), 200
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
    
#UPDATE EMPLOYEE
@app.route('/update_employee', methods=['POST'])
def update_employee():
    data = request.json
    name = data.get('name')
    adress = data.get('adress')
    branch = data.get('branch')
 
    conn = nc()
    query = """
    MATCH (e:Employee {name: $name})
    SET e.name = $name, e.adress = $adress, e.branch = $branch
    RETURN e
    """

    parameters = {'name': name, 'branch': branch, 'adress': adress,}
    result = conn.query(query, parameters)
    conn.close()
    # Extract the properties of the created car node
    employee = result[0]['e']._properties if result else {}

    response = {
        "message": "Employee updated sucessfully",
        "employee": employee
    }
    return jsonify(response), 201


#DELETE EMPLOYEE
@app.route('/delete_employee', methods=['POST'])
def delete_employee():
    data = request.json
    name = data.get('name')
    adress = data.get('adress')
    branch = data.get('branch')

    conn = nc()
    query = """
    MATCH (e:Employee {name: $name})
    DETACH DELETE e
    """

    parameters = {'name': name, 'branch': branch, 'adress': adress,}
    result = conn.query(query, parameters)

    conn.close()

    employee = result[0]['e']._properties if result else {}

    response = {
        "message": "Employee updated sucessfully",
        "employee": employee
    }
    return jsonify(response), 200 



# Endepunkt for å slette alle noder
@app.route("/delete_all", methods=['POST'])
def delete_all():
    conn = nc()
    query = """
    MATCH (n)
    DETACH DELETE n
    """
    try:
        conn.query(query)
        conn.close()
        return jsonify({"message": "All nodes deleted"}), 200
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)