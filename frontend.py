# frontend.py
import streamlit as st
import requests

st.title("🏥 MediBot – MeTTa-Powered Healthcare Assistant")

question = st.text_input("Ask a medical question:")
if st.button("Ask"):
    with st.spinner("Thinking..."):
        response = requests.post(
            "http://localhost:5000/ask",
            json={"question": question}
        ).json()
        
        st.write("### 💡 Answer")
        st.write(response["answer"])
        
        st.write("### 🔍 Facts Used")
        st.write(response["facts_used"])
        
        st.write("### 🧠 Knowledge Graph Query")
        st.code(f"MeTTa: getCauses ChestPain → {response['facts_used']}")