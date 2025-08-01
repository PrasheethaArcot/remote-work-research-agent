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
    ("system", """You are an expert at creating knowledge graphs from research reports. 
    
Create 8-15 nodes and 10-20 edges representing key entities and relationships.

IMPORTANT: Output ONLY valid JSON in this exact format:
{{
  "nodes": [
    {{"data": {{"id": "unique_id", "label": "TYPE", "name": "display_name", "description": "detailed_description"}}}},
    {{"data": {{"id": "unique_id2", "label": "TYPE2", "name": "display_name2", "description": "detailed_description2"}}}}
  ],
  "edges": [
    {{"data": {{"id": "edge_id", "source": "node_id", "target": "node_id", "label": "RELATIONSHIP", "description": "relationship_description"}}}},
    {{"data": {{"id": "edge_id2", "source": "node_id2", "target": "node_id3", "label": "RELATIONSHIP2", "description": "relationship_description2"}}}}
  ]
}}

Guidelines:
- Infer node types and relationships from the research content
- Use meaningful labels like PERSON, ORGANIZATION, TECHNOLOGY, CONCEPT, EVENT, LOCATION, etc.
- Extract specific facts, dates, numbers, achievements, and relationships
- Make relationships logical and meaningful based on the research context
- Use unique IDs for all nodes and edges
- Ensure all source and target IDs in edges correspond to actual node IDs

Output ONLY the JSON object, no explanations or additional text."""),
    
    ("human", """
Research Report:
{report}

Create a comprehensive knowledge graph JSON with detailed nodes and edges. Extract specific facts, relationships, and attributes from the research content. Let the content guide the node types and relationships. Output only the JSON.
""")
])

chain = prompt | client



def json_generator(state: Dict) -> Dict:
    """Generate a knowledge graph JSON from research results"""
    
    # Get the research report
    report = state.get("final_report") or state.get("report", "")
    
    # If no report, create a simple fallback
    if not report:
        simple_graph = {
            "nodes": [
                {"data": {"id": "query", "label": "QUERY", "name": state.get("query", "Research Query")}}
            ], 
            "edges": []
        }
        with open("data.json", "w") as f:
            json.dump(simple_graph, f, indent=2)
        return {**state, "knowledge_graph": simple_graph}
    
    # Generate knowledge graph using AI
    ai_response = chain.invoke({"report": report})
    ai_text = ai_response.content.strip()
    
    # Extract JSON from AI response
    json_start = ai_text.find('{')
    json_end = ai_text.rfind('}') + 1
    json_text = ai_text[json_start:json_end] if json_start != -1 else "{}"
    
    # Parse JSON
    graph = json.loads(json_text)
    
    # Save and return the graph
    with open("data.json", "w") as f:
        json.dump(graph, f, indent=2)
    
    return {**state, "knowledge_graph": graph}
        
 