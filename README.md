# Car_rental-API

Welcome to our Car Rental API project! This project is an interesting exercise in developing a web API using the Flask framework and integrating it with a Neo4j graph database. We are also practicing collaborative software development and version control using Git and GitHub.

## Purpose
The purpose of this project is to:
- Practice web API development with the Flask framework.
- Practice database application development with Neo4j.
- Practice using Git and GitHub for collaborative software development.

## Tasks
In this project, we will practice collaborative software development and version control using Git. Here are the steps we are following:

1. **Create a Remote Repository:**
   - One team member (the "admin") creates a remote repository containing a Flask web-API project.

2. **Database Responsibility:**
   - Another team member takes responsibility for setting up and managing a Neo4j graph database.

3. **Collaborative Development:**
   - All team members implement different parts of the Flask web-API project. Each member clones the admin’s repository to create a local copy of the project on their computer.

4. **Database Interaction:**
   - The web-APIs will interact with the Neo4j graph database to store and retrieve information.

5. **Push Changes:**
   - All changes are pushed to the GitHub repository to keep the project up-to-date.

## WebAPI Development with Flask Framework
We are implementing WebAPIs for a car rental company. Customers can rent cars for an unlimited time without considering the date/time of rental. For example, if car #1 is available, it can be rented to a customer named John. If car #1 is booked for John, it cannot be booked by any other customer. If John has booked a car, he cannot book any other car. If John returns car #1, he is allowed to rent other cars.

### Functionalities to Implement
- **CRUD Operations for Cars:**
  - Create, Read, Update, and Delete cars with basic information (e.g., make, model, year, location, status: available, booked, rented, damaged).
  
- **CRUD Operations for Customers:**
  - Create, Read, Update, and Delete customers with basic information (e.g., name, age, address).
  
- **CRUD Operations for Employees:**
  - Create, Read, Update, and Delete employees with basic information (e.g., name, address, branch).
  
- **Order Car Endpoint:**
  - Implement an endpoint `order-car` where customer-id and car-id are passed as parameters.
  - The system checks that the customer with customer-id has not booked other cars.
  - The system changes the status of the car with car-id from 'available' to 'booked'.
  
- **Cancel Order Car Endpoint:**
  - Implement an endpoint `cancel-order-car` where customer-id and car-id are passed as parameters.
  - The system checks that the customer with customer-id has booked the car.
  - If the customer has booked the car, the car becomes available.
  
- **Rent Car Endpoint:**
  - Implement an endpoint `rent-car` where customer-id and car-id are passed as parameters.
  - The system checks that the customer with customer-id has a booking for the car.
  - The car’s status is changed from 'booked' to 'rented'.
  
- **Return Car Endpoint:**
  - Implement an endpoint `return-car` where customer-id and car-id are passed as parameters.
  - Car’s status (e.g., ok or damaged) during the return will also be sent as a parameter.
  - The system checks that the customer with customer-id has rented the car.
  - The car’s status is changed from 'booked' to 'available' or 'damaged'.
  
- **Testing with Postman:**
  - Use Postman to check the functionality of the implemented endpoints.

## What to Submit
We will submit a report of our work with this project, detailing the implementation and testing of the web APIs.