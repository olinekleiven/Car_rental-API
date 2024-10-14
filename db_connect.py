from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

# Laste inn variabler fra .env
load_dotenv()

class Neo4jConnection:
    def __init__(self):
        uri = os.getenv("URI")
        user = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self._driver.close()
    
    def query(self, query, parameters=None):
        with self._driver.session() as session:
            result = session.run(query, parameters)
            return [record for record in result]

