import os
from utils import create_constraints, create_vector_index
from langchain_community.graphs import Neo4jGraph

url = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

# Remapping for Langchain Neo4j integration
os.environ["NEO4J_URL"] = url

neo4j_graph = Neo4jGraph(
    url=url, username=username, password=password, refresh_schema=False
)

create_constraints(neo4j_graph)
create_vector_index(neo4j_graph)

def parse_calls(data, logger):
    logger.info("PARSING " + str(len(data)) + " CALLS")
    for phone_call in data:
        parse_phone_call(phone_call, logger)

def parse_phone_call(phone_call, logger):
    logger.info("PARSING PHONE CALL")
    logger.info(phone_call)
    
    my_number = phone_call.get('my_number')
    if my_number:
        import_query = f"""
        MERGE (n:PhoneNumber {{number: '{my_number}'}})
        """
        logger.info("Executing Cypher query: " + import_query)
        # Execute the query using your Neo4j driver here
    neo4j_graph.query(import_query, {"data":phone_call})


