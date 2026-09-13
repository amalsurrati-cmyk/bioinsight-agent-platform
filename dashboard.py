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

st.divider()
st.subheader("Past Reports")

history_response = requests.get("http://127.0.0.1:8000/history")
if history_response.status_code == 200:
    reports = history_response.json()["reports"]
    for r in reports:
        if st.button(f"{r['filename']} ({r['created_at'][:16]})", key=r['id']):
            past_report = requests.get(f"http://127.0.0.1:8000/report/{r['id']}").json()["report"]
            st.markdown(past_report)