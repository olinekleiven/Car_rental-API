# app.py
#import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

from db_connect import Neo4jConnection as nc
import logging
from flask import Blueprint
app = Flask(__name__)
CORS(app)   
car_api = Blueprint('car_api', __name__)


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
    car_id=data.get('car_id')

# Connect to Neo4j and add the car
    conn = nc()
    query = """
    CREATE (c:Car {make: $make, model: $model, year: $year, location: $location, status: $status, car_id: $car_id})
    RETURN c
    """
    parameters = {'make': make, 'model': model, 'year': year, 'location': location, 'status': status, 'car_id':car_id}
    result = conn.query(query, parameters)
    conn.close()

    # Extract the properties of the created car node
    car = result[0]['c']._properties if result else {}

    response = {
        "message": "Car added successfully",
        "car": car
    }
    return jsonify(response), 201


@app.route('/get_car', methods=['GET'])
def get_cars():
    data=request.json
    car_id=data.get('car_id')
    conn = nc()
    query = """
    MATCH (c:Car {car_id: $car_id})
    RETURN c
    """
    parameters = {'car_id': car_id}
    try:
        result = conn.query(query, parameters)
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
    car_id=data.get('car_id')
    conn = nc()
    query = """
    MATCH (c:Car {car_id: $car_id})})
    SET c.year = $year, c.location = $location, c.status = $status
    RETURN c
    """

    parameters = {'car_id':car_id, 'make': make, 'model': model, 'year': year, 'location': location, 'status': status}
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
    car_id = data.get('car_id')

    conn = nc()
    query = """
    MATCH (c:Car {car_id: $car_id})
    DETACH DELETE c
    """

    parameters = {'car_id': car_id}
    conn.query(query, parameters)
    conn.close()

    response = {
        "message": "Car deleted successfully",
        "car_id": car_id
    }
    return jsonify(response), 200 

@app.route('/add_customer', methods=['POST'])
def add_customer():
    data = request.json
    name = data.get('name')
    age = data.get('age')
    adress = data.get('adress')
    customer_id=data.get('customer_id')

    conn = nc()
    query = """
    CREATE (c:Customer {name: $name, age: $age, adress: $adress, customer_id: $customer_id})
    RETURN c
    """
    parameters = {'name': name, 'age': age, 'adress': adress, 'customer_id': customer_id}
    result = conn.query(query, parameters)
    conn.close()

    customer = result[0]['c']._properties if result else {}

    response = {
        "message": "Customer added successfully",
        "customer": customer
    }
    return jsonify(response), 201

#GET COSYUMER
@app.route('/get_customer', methods=['GET'])
def get_customer():
    data=request.json
    customer_id=data.get('customer_id')
    conn = nc()
    query = """
    MATCH (c:Customer {customer_id: $customer_id})
    RETURN c
    """
    try:
        parameters = {'customer_id': customer_id}
        result = conn.query(query,parameters)
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
    customer_id=data.get('customer_id')
 
    conn = nc()
    query = """
    MATCH (c:Customer {customer_id: $customer_id})
    SET c.name = $name, c.age = $age, c.adress = $adress
    RETURN c
    """
        # sjøl om vi skriver name her kunne vi hatt id

    parameters = {'name': name, 'age': age, 'adress': adress, 'customer_id': customer_id}
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
    customer_id=data.get('customer_id')

    conn = nc()
    query = """
    MATCH (c:Customer {customer_id: $customer_id})
    DETACH DELETE c
    """

    parameters = {'customer_id': customer_id}
    conn.query(query, parameters)
    conn.close()

    response = {
        "message": "Customer deleted successfully",
        "customer_id": customer_id
    }
    return jsonify(response), 200 


#emplyee

@app.route('/add_employee', methods=['POST'])
def add_employee():
    data = request.json

    name = data.get('name')
    adress = data.get('adress')
    branch = data.get('branch')
    employee_id=data.get('employee_id')

    conn = nc()
    query = """
    CREATE (e:Employee {name: $name, adress: $adress, branch: $branch, employee_id: $employee_id})
    RETURN e
    """
    parameters = {'name': name, 'adress': adress, 'branch': branch, 'employee_id': employee_id}
    result = conn.query(query, parameters)
    
    conn.close()

    employee = result[0]['e']._properties if result else {}
    response = {
        "message": "Employee added successfully",
        "employee": employee,
    }
    return jsonify(response), 201

#GET EMPLOYEE
@app.route('/get_employee', methods=['GET'])
def get_employee():
    data=request.json
    employee_id=data.get('employee_id')
    conn = nc()
    query = """
    MATCH (e:Employee{employee_id: $employee_id})
    RETURN e
    """
    try:
        parameters = {'employee_id': employee_id}
        result = conn.query(query,parameters)
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
    employee_id=data.get('employee_id')
 
    conn = nc()
    query = """
    MATCH (e:Employee {employee_id: $employee_id})
    SET e.name = $name, e.adress = $adress, e.branch = $branch
    RETURN e
    """

    parameters = {'employee_id':employee_id,'name': name, 'branch': branch, 'adress': adress, 'employee_id': employee_id}
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
    employee_id=data.get('employee_id')

    conn = nc()
    query = """
    MATCH (e:Employee {employee_id: $employee_id})
    DETACH DELETE e
    """

    parameters = {'employee_id': employee_id}
    result = conn.query(query, parameters)

    conn.close()

    employee = result[0]['e']._properties if result else {}

    response = {
        "message": "Employee updated sucessfully",
        "employee": employee
    }
    return jsonify(response), 200 

#order car api
@app.route('/add_order', methods=['POST'])
def add_order():
    data = request.json
    customer_id = data.get('customer_id')
    car_id = data.get('car_id')

    conn = nc()
    query = """
    MATCH (cust:Customer {customer_id: $customer_id})
    MATCH (c:Car {car_id: $car_id})
    CREATE (o:Order {date: date(), price: 100, status: 'booked'})
    CREATE (cust)-[:ORDERED]->(o)-[:FOR]->(c)
    SET c.status = 'not available'
    RETURN o, id(o) as order_id
    """
    parameters = {'customer_id': customer_id, 'car_id': car_id}
    result = conn.query(query, parameters)
    conn.close()

    if result:
        order_id = result[0]['order_id']
        response = {
            "message": "Order added successfully",
            "order_id": order_id
        }
    else:
        response = {
            "message": "Failed to add order",
            "order": {},
            "order_id": None
        }

    return jsonify(response), 201

#cancel order
@app.route('/cancel_order', methods=['POST'])
def cancel_order():
    data = request.json
    customer_id = data.get('customer_id')
    car_id = data.get('car_id')

    conn = nc()
    query = """
    MATCH (cust:Customer {customer_id: $customer_id})-[:ORDERED]->(o:Order)-[:FOR]->(c:Car {car_id: $car_id})
    SET c.status = 'available'
    DETACH DELETE o
    RETURN o
    """
    parameters = {'customer_id': customer_id, 'car_id': car_id}
    result = conn.query(query, parameters)
    conn.close()

    if result:
        response = {
            "message": "Order cancelled successfully",
            "customer_id": customer_id,
            "car_id": car_id
        }
    else:
        response = {
            "message": "No matching order found",
            "customer_id": customer_id,
            "car_id": car_id
        }

    return jsonify(response), 200

@app.route('/rent_car', methods=['POST'])
def rent_car():
    data = request.json
    customer_id = data.get('customer_id')
    car_id = data.get('car_id')

    conn = nc()
    query = """
    MATCH (cust:Customer {customer_id: $customer_id})-[:ORDERED]->(o:Order)-[:FOR]->(c:Car {car_id: $car_id})
    SET o.status = 'Rented'
    RETURN o
    """
    parameters = {'customer_id': customer_id, 'car_id': car_id}
    result = conn.query(query, parameters)
    conn.close()

    if result:
        response = {
            "message": "Rented successfully",
            "customer_id": customer_id,
            "car_id": car_id
        }
    else:
        response = {
            "message": "No matching order found",
            "customer_id": customer_id,
            "car_id": car_id
        }

    return jsonify(response), 200

@app.route('/return_car', methods=['POST'])
def return_car():
    data = request.json
    customer_id = data.get('customer_id')
    car_id = data.get('car_id')
    status = data.get('status')
    conn = nc()
    query = """
    MATCH (cust:Customer {customer_id: $customer_id})-[:ORDERED]->(o:Order)-[:FOR]->(c:Car {car_id: $car_id})
    SET c.status = $status
    DETACH DELETE o
    RETURN c.status
    """
    parameters = {'customer_id': customer_id, 'car_id': car_id, 'status': status}
    result = conn.query(query, parameters)
    conn.close()

    if result:
        response = {
            "message": "Returned successfully",
            "customer_id": customer_id,
            "car_id": car_id
        }
    else:
        response = {
            "message": "No matching order found",
            "customer_id": customer_id,
            "car_id": car_id
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