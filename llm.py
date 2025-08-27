# llm.py
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_groq(prompt, model="llama3-70b-8192", max_tokens=256):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            model=model,
            temperature=0.3,
            max_tokens=max_tokens
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error calling Groq: {str(e)}"

def generate_metta_query(question):
    """Use LLM to convert natural language to MeTTa query"""
    prompt = f"""
    You are a MeTTa query translator for a healthcare knowledge system.
    Convert the user's question into a MeTTa function call.
    Only output the MeTTa expression. No explanations.

    Available functions:
    - (getCauses $symptom)
    - (getSymptoms $condition)
    - (getTreatment $condition)
    - (getPrevention $condition)
    - (explain-cause $condition $symptom)

    Examples:
    "What causes chest pain?" → (getCauses ChestPain)
    "How is malaria treated?" → (getTreatment Malaria)
    "What are the symptoms of anxiety?" → (getSymptoms Anxiety)
    "Why does HeartAttack cause chest pain?" → (explain-cause HeartAttack ChestPain)

    Question: {question}
    →
    """
    return call_groq(prompt, max_tokens=64)