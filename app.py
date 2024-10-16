# app.py
#import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from query_api import routes  

app = Flask(__name__)
CORS(app)

app.register_blueprint(routes)

#logging.basicConfig(level=logging.DEBUG)

# Kode for å legge inn POST /cars
@app.route('/cars', methods=['POST'])
def add_car():
    # Henter data fra forespørselen (JSON format)
    data = request.json
    make = data.get('make')
    model = data.get('model')
    year = data.get('year')
    location = data.get('location')
    status = data.get('status')

    # Simulerer at vi legger bilen til ved å returnere dataene i JSON
    response = {
        "message": "Car added successfully",
        "car": {
            "make": make,
            "model": model,
            "year": year,
            "location": location,
            "status": status
        }
    }
    return jsonify(response), 201


# Legg til GET /cars ruten med logging
@app.route('/cars', methods=['GET'])
def get_cars():
    cars = [
        {"make": "Toyota", "model": "Corolla", "year": 2020, "location": "Oslo", "status": "available"},
    ]
    app.logger.debug(f"Returning cars: {cars}")
    return jsonify(cars), 200

if __name__ == '__main__':
    app.run(debug=True)