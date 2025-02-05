import json
import os
from chains import load_embedding_model
from utils import create_constraints, create_vector_index
from langchain_community.graphs import Neo4jGraph

url = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

embedding_model_name = os.getenv("EMBEDDING_MODEL")
ollama_base_url = os.getenv("OLLAMA_BASE_URL")
# Remapping for Langchain Neo4j integration
os.environ["NEO4J_URL"] = url


neo4j_graph = Neo4jGraph(
    url=url, username=username, password=password, refresh_schema=False
)

embeddings, dimension = load_embedding_model(
    embedding_model_name, config={"ollama_base_url": ollama_base_url}
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
    phone_call['transcript'] = get_transcript(phone_call, logger)
    phone_call['embedding'] = embeddings.embed_query(phone_call.get('transcript'))
    if my_number:
        import_query = f"""
        MERGE (me:PhoneNumber {{number: '{my_number}'}})
        MERGE (them:PhoneNumber {{number: '{other_number}'}})
        MERGE (callNum:uuid {{number: '{call_id}'}})
        SET callNum.transcript = '{phone_call.get('transcript')}'
        SET callNum.embedding = '{phone_call.get('embedding')}'
        MERGE (me)-[:SPOKE_TO]-(them)
        MERGE (me)-[:MADE_CALL]-(callNum)
        MERGE (them)-[:MADE_CALL]-(callNum)
        """
        #logger.info("Executing Cypher query: " + import_query)
        # Execute the query using your Neo4j driver here
    neo4j_graph.query(import_query, {"data":phone_call})

def get_transcript(phone_call, logger):
    # Parse each utterance in the phone call to get its text, joining them together with newlines
    #logger.info("GETTING TRANSCRIPT")
    transcript = "".join([utterance.get('text').replace("'", "\\'") + "\n" for utterance in phone_call.get('utterances')])
    return str(transcript)
