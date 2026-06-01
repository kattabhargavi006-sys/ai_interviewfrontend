import streamlit as st
import requests
server_loc=st.secrets["server_url"].rstrip("/")
st.title("Interview preparation Bot")
with st.form("details"):
    topic=st.text_input("enter here")
    level=st.selectbox("choose from:",["easy","medum","advanced"])
    ways=st.multiselect("choose from here:",["mcqs","theory questions","coding questions"])
    if st.form_submit_button():
        prompt=f"""
         i need to prepare interview and give me the best content and i want {topic} related these list of items in ways {ways}
         at level {level}
        """
        response=requests.post(f"{server_loc}/generate",json={"prompt":prompt})
        if response.status_code == 200:
         st.write(response.json()["response"])
        else:
         st.error(f"Error: {response.status_code}")
    