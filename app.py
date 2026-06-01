import streamlit as st
import requests
import json

server_location =st.secrets["server_location"].rstrip("/")
st.title("AI Interview Chat Bot 🚀")

with st.form("Details"):

    topic = st.text_input("Enter Language Topic")
    level = st.selectbox("Choose Level", ["Easy", "Medium", "Hard", "Advanced"])
    qtype = st.multiselect("Choose type", ["MCQS", "Theory", "Coding"])

    submit = st.form_submit_button("Generate")

if submit:

    prompt = f"""
Generate exactly 10 {level} interview questions on {topic}.

Selected Types: {qtype}

IMPORTANT:

If Question Type contains MCQS, every question MUST be:

{{
    "type":"MCQS",
    "question":"What is Python?",
    "options":[
        "A. Operating System",
        "B. Programming Language",
        "C. Database",
        "D. Browser"
    ],
    "answer":"B. Programming Language"
}}

if Question Type contains Coding:

{{
    "type":"Coding",
    "question":"Write a Python program to reverse a string",
    "answer":"def reverse(s): return s[::-1]"
}}

If Question Type contains Theory:

{{
    "type":"Theory",
    "question":"What is Python?",
    "answer":"Python is ..."
}}


Return ONLY a JSON array of objects:

[
  {{
    "question": "What is Python?",
    "answer": "Python is a high-level programming language..."
  }}
]

Rules:
- No markdown
- No explanation
- Only valid JSON
"""

try:
    response = requests.post(
        f"{server_location}/generate",
        json={"prompt": prompt}
    )

    st.write("Status Code:", response.status_code)
    st.write("Response Text:")
    st.code(response.text)

except Exception as e:
    st.error(f"Connection Error: {e}")

    st.write("Status:", response.status_code)

    if response.status_code != 200:
        st.error(response.text)
        st.stop()

    res = response.json()

    data = json.loads(res["object"])

    st.subheader("Interview Q&A")

    for i, item in enumerate(data, start=1):

        qtype = item.get("type", "Theory")

        with st.expander(f"{qtype} Q{i}: {item['question']}"):

            # MCQ Questions
            if qtype == "MCQS":

                st.radio(
                    "Choose an option:",
                    item.get("options", []),
                    key=f"mcq_{i}"
                )

                if st.button("Show Answer", key=f"answer_{i}"):
                    st.success(item["answer"])

            # Coding Questions
            elif qtype == "Coding":

                st.write("### Solution")
                st.code(item["answer"], language="python")

            # Theory Questions
            else:
                st.write(item["answer"])