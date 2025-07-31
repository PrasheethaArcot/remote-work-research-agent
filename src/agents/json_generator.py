import json
import os
from typing import Dict, List
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

client = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a knowledge graph generator. Create a comprehensive JSON with detailed nodes and edges from research content.

Create 8-15 nodes and 10-20 edges representing key entities and relationships.

Node format: {{"data": {{"id": "unique_id", "label": "TYPE", "name": "display_name", "description": "detailed_description", "attributes": {{"key1": "value1", "key2": "value2"}}}}}}
Edge format: {{"data": {{"id": "edge_id", "source": "node_id", "target": "node_id", "label": "RELATIONSHIP", "description": "relationship_description"}}}}

Guidelines:
- Infer node types and relationships from the research content
- Create meaningful, descriptive labels for nodes and edges
- Include relevant attributes for each entity based on the content
- Extract specific facts, dates, numbers, achievements, and relationships
- Make relationships logical and meaningful based on the research context

Output ONLY valid JSON, no explanations."""),
    
    ("human", """
Research Report:
{report}

Create a comprehensive knowledge graph JSON with detailed nodes and edges. Extract specific facts, relationships, and attributes from the research content. Let the content guide the node types and relationships. Output only the JSON.
""")
])

chain = prompt | client

def json_generator(state: Dict) -> Dict:
    """
    This function takes research results and creates a knowledge graph JSON file.
    Think of it like taking a research report and turning it into a visual map of ideas.
    """
    
    # Step 1: Get the research report from our data
    # We look for the report in different possible places in our data
    report = state.get("final_report") or state.get("report", "")
    
    # Step 2: If we don't have a report, create a simple fallback
    if not report:
        # Create a basic graph with just the research question
        simple_graph = {
            "nodes": [
                {"data": {"id": "query", "label": "QUERY", "name": state.get("query", "Research Query")}}
            ], 
            "edges": []
        }
        # Save this simple graph to a file
        with open("data.json", "w") as f:
            json.dump(simple_graph, f, indent=2)
        return {**state, "knowledge_graph": simple_graph}
    
    # Step 3: Try to create a detailed graph using AI
    try:
        # Ask the AI to create a knowledge graph from our research
        ai_response = chain.invoke({"report": report})
        ai_text = ai_response.content.strip()
        
        # Step 4: Extract the JSON that the AI created
        # Find where the JSON starts and ends in the AI's response
        json_start = ai_text.find('{')
        json_end = ai_text.rfind('}') + 1
        
        # Get the JSON part of the AI's response
        json_text = ai_text[json_start:json_end] if json_start != -1 else "{}"
        
        # Step 5: Convert the text into actual JSON data
        graph = json.loads(json_text)
        
        # Step 6: Save the graph to a file so we can use it later
        with open("data.json", "w") as f:
            json.dump(graph, f, indent=2)
        
        # Step 7: Return the graph along with our original data
        return {**state, "knowledge_graph": graph}
        
    # Step 8: If anything goes wrong, create a simple fallback
    except:
        # Create a basic graph with just the research question
        simple_graph = {
            "nodes": [
                {"data": {"id": "query", "label": "QUERY", "name": state.get("query", "Research Query")}}
            ], 
            "edges": []
        }
        # Save this simple graph to a file
        with open("data.json", "w") as f:
            json.dump(simple_graph, f, indent=2)
        return {**state, "knowledge_graph": simple_graph} 