# src/agents/research_planner.py
import os
import re
import ast
from dotenv import load_dotenv
from typing import Dict
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

client = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="deepseek-r1-distill-llama-70b"  
)


prompt = ChatPromptTemplate.from_messages([
    ("system", 
    """You are a world-class research analyst and investigative journalist.

For any research query—across science, sports, politics, technology, or culture—you identify the most important, newsworthy, and insightful subtopics.

For broad or ambiguous queries, always include:
- Recent events or developments
- Recent conflicts between historical places or people
- Key figures, organizations, or locations  
- Historical context or background  
- Major controversies, achievements, or milestones  
- Data, statistics, or performance highlights (if relevant)  
- Underlying causes, implications, or future directions  

Rules:
- Output only a valid Python list of short string subtopics
- Do NOT include explanations, markdown, or formatting
- Do NOT inject hardcoded country names, events, or assumptions
- Do NOT include <think> or </think> blocks in your response
- Infer what is most relevant for the query
"""),
    
    ("human", 
    """Break down the following research topic into 5–7 concise and meaningful subtopics.

Topic: {query}

Rules:
- Output a valid Python list of short string subtopics
- Do NOT include explanations, markdown, or formatting
- Do NOT add unrelated or speculative subtopics
- Do NOT include <think> or </think> blocks in your response
- Stay tightly focused on the core aspects of the original topic
""")
])




chain = prompt | client

def research_planner(state: Dict) -> Dict:
    query = state["query"]
    response = chain.invoke({"query": query})
    content = response.content
    
    # Clean up any think blocks from the response
    if "<think>" in content and "</think>" in content:
        print(f"⚠️  Found think block in research planner response for query: {query}")
        think_match = re.search(r'<think>.*?</think>', content, flags=re.DOTALL)
        if think_match:
            print(f"   Think block content: {think_match.group(0)[:100]}...")
            content = content.replace(think_match.group(0), "").strip()
    
    # Try to find the first list in the response (between [ and ])
    start = content.find('[')
    end = content.rfind(']')
    if start != -1 and end != -1:
        list_str = content[start:end+1]
        try:
            # Use ast.literal_eval instead of eval for safety
            subtopics = ast.literal_eval(list_str)
            # Ensure subtopics is a list
            if not isinstance(subtopics, list):
                subtopics = [content]
        except (ValueError, SyntaxError):
            # If parsing fails, try to extract individual items
            try:
                # Remove brackets and split by comma
                items = list_str[1:-1].split(',')
                subtopics = [item.strip().strip('"\'') for item in items if item.strip()]
                if not subtopics:
                    subtopics = [content]
            except:
                subtopics = [content]
    else:
        subtopics = [content]
    
    # Clean up each subtopic to remove any remaining think blocks
    cleaned_subtopics = []
    for subtopic in subtopics:
        if isinstance(subtopic, str):
            clean_subtopic = subtopic
            if "<think>" in subtopic and "</think>" in subtopic:
                print(f"⚠️  Found think block in subtopic: {subtopic[:50]}...")
                think_match = re.search(r'<think>.*?</think>', subtopic, flags=re.DOTALL)
                if think_match:
                    clean_subtopic = subtopic.replace(think_match.group(0), "").strip()
            if clean_subtopic:
                cleaned_subtopics.append(clean_subtopic)
    
    return {**state, "subtopics": cleaned_subtopics if cleaned_subtopics else subtopics}
