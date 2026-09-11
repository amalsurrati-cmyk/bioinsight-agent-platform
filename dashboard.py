import streamlit as st
import requests

st.title("BioInsight")
st.write("Upload a biological data file (CSV or FASTA) to get an AI-generated analysis report.")

uploaded_file = st.file_uploader("Choose a file", type=["csv", "fasta", "fa"])

if uploaded_file is not None:
    with st.spinner("Analyzing your file..."):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        response = requests.post("http://127.0.0.1:8000/analyze", files=files)

    if response.status_code == 200:
        report = response.json()["report"]
        st.markdown(report)
    else:
        st.error(f"Something went wrong: {response.status_code}")