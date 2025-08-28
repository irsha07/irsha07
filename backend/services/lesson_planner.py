# services/lesson_planner.py
from openai import OpenAI
from services.rag_engine import get_rag_context_and_sources
import os
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_lesson_plan_step(subject: str, grade: str, topic: str, previous_chunks: str = ""):
    """
    Generates a single, context-aware lesson step.
    """
    
    # KEY CHANGE: Create a smarter query for the RAG engine based on previous content.
    if previous_chunks:
        rag_query = f"In a lesson about '{topic}', what is the next logical sub-topic to teach after covering the following information: '{previous_chunks}'? Base the answer on the provided textbook."
    else: # For the very first step
        rag_query = f"Provide a brief, engaging introduction for a lesson on '{topic}' for a grade {grade} student, based on the textbook."

    # Get both the context and the raw source text from the RAG engine
    context, source_chunks = get_rag_context_and_sources(rag_query, subject)

    tools = [
        {
            "type": "function",
            "function": {
                "name": "format_lesson_step",
                "description": "Formats a single step of a lesson plan.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string", "enum": ['introduction', 'guided_practice', 'independent_work', 'assessment', 'recap']},
                        "voice": {"type": "string", "description": "The exact script for the AI teacher to say for this step."},
                        "prompt": {"type": "string", "description": "A simple on-screen prompt for the student."},
                        "response_type": {"type": "string", "enum": ['text', 'multiple_choice', 'none']},
                        "visual": {"type": "string", "description": "Optional. A descriptive label for a visual asset."}
                    },
                    "required": ["type", "voice", "prompt", "response_type"]
                }
            }
        }
    ]

    system_prompt = f"""
    You are LearnPal, an expert AI curriculum developer. Your task is to create the *next* engaging lesson step
    for a grade {grade} student studying {subject}. The overall topic is "{topic}".
    The previous step covered: "{previous_chunks if previous_chunks else 'the beginning'}".
    
    Based *only* on the following context from the textbook, generate the next logical step.
    Do not repeat information from the previous step.
    
    --- TEXTBOOK CONTEXT ---
    {context}
    --- END TEXTBOOK CONTEXT ---
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "system", "content": system_prompt}],
            tools=tools,
            tool_choice={"type": "function", "function": {"name": "format_lesson_step"}}
        )
        
        lesson_block = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
        
        # Return both the AI's formatted step and the source text it used
        return lesson_block, source_chunks

    except Exception as e:
        print(f"Error calling OpenAI for lesson step: {e}")
        error_block = {
            "type": "recap",
            "voice": "I'm having a little trouble. Let's try that again in a moment!",
            "prompt": "Error generating lesson step.",
            "response_type": "none"
        }
        return error_block, ""
