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
    #logger.info("PARSING PHONE CALL")
    #logger.info(phone_call)
    
    my_number = phone_call.get('my_number')
    other_number = phone_call.get('other_party_number')
    call_id = phone_call.get('uuid')
    if my_number:
        import_query = f"""
        MERGE (me:PhoneNumber {{number: '{my_number}'}})
        MERGE (them:PhoneNumber {{number: '{other_number}'}})
        MERGE (callNum:uuid {{number: '{call_id}'}})
        MERGE (me)-[:SPOKE_TO]-(them)
        MERGE (me)-[:MADE_CALL]-(callNum)
        MERGE (them)-[:MADE_CALL]-(callNum)
        """
        #logger.info("Executing Cypher query: " + import_query)
        # Execute the query using your Neo4j driver here
    neo4j_graph.query(import_query, {"data":phone_call})


