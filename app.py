# app.py
from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
from metta import MeTTaEngine
from llm import call_groq, generate_metta_query
import json
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
CORS(app)

metta = MeTTaEngine()

# High-risk conditions for escalation
HIGH_RISK_CONDITIONS = ["HeartAttack", "Stroke", "Cancer"]

# Serve the frontend
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get("question", "").strip()
    if not question:
        return jsonify({"answer": "Please ask a question."})

    # Initialize session history
    history = session.get('history', [])
    history.append({"role": "user", "content": question})

    # Step 1: Use LLM to generate a MeTTa query (Semantic Routing)
    metta_expr = generate_metta_query(question)
    
    if not metta_expr or "Error" in metta_expr or "Unknown" in metta_expr:
        answer = "I didn't understand your question. Try asking about causes, symptoms, or treatments of a condition."
        facts_used = "No valid query generated."
    else:
        # Step 2: Execute the MeTTa query
        result = metta.query(metta_expr)
        facts_used = ", ".join(result) if isinstance(result, list) and result else "Not found in knowledge base."

        # Add safety warning if high-risk condition
        if any(cond in facts_used for cond in HIGH_RISK_CONDITIONS):
            facts_used += " ⚠️ This may indicate a medical emergency. Seek immediate help."

        # Step 3: Build prompt with conversation history
        hist_str = "\n".join([f"{m['role']}: {m['content']}" for m in history[-4:]])
        
        prompt = f"""
        Conversation history:
        {hist_str}

        Current question: {question}
        Relevant facts: {facts_used}

        Provide a clear, natural language answer. Be concise and avoid giving medical advice.
        If the facts are insufficient, say 'I don't have enough information.'
        """
        answer = call_groq(prompt)

    # Save bot response to history
    history.append({"role": "bot", "content": answer})
    session['history'] = history

    return jsonify({
        "question": question,
        "meTTa_query": metta_expr,
        "facts_used": facts_used,
        "answer": answer.strip()
    })

@app.route('/learn', methods=['POST'])
def learn():
    data = request.json
    fact = data.get("fact")
    if not fact:
        return jsonify({"error": "No fact provided"}), 400
    result = metta.add_knowledge(fact)
    return jsonify({"status": "Learned", "fact": fact})

@app.route('/suggest-fact', methods=['POST'])
def suggest_fact():
    data = request.json
    user_input = data.get("input")
    if not user_input:
        return jsonify({"suggestion": None, "message": "No input provided."})

    prompt = f"""
    Extract a valid MeTTa-style fact from this statement:
    "{user_input}"
    Only output the MeTTa expression. No explanations.
    Example: (causes LongCovid ChestPain)
    """
    suggested_fact = call_groq(prompt, max_tokens=64)
    
    if "(" in suggested_fact and ")" in suggested_fact:
        return jsonify({
            "suggestion": suggested_fact,
            "message": "Would you like to add this to the knowledge base?"
        })
    else:
        return jsonify({
            "suggestion": None,
            "message": "Could not extract a valid MeTTa fact. Try rephrasing."
        })

@app.route('/explain', methods=['POST'])
def explain():
    data = request.json
    fact = data.get("fact", "")
    # Simple explanation based on known patterns
    if "causes" in fact:
        parts = fact.split()
        if len(parts) == 3 and parts[0] == "causes":
            cause, symptom = parts[1], parts[2]
            return jsonify({
                "fact": fact,
                "explanation": f"I know {cause} causes {symptom} because it is defined in the medical knowledge base.",
                "source": f"(causes {cause} {symptom})",
                "confidence": "High"
            })
    return jsonify({
        "fact": fact,
        "explanation": "Explanation not available.",
        "source": "Unknown",
        "confidence": "Low"
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)