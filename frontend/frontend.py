import streamlit as st
import requests
import plotly.graph_objects as go

st.set_page_config(page_title="Project Insight", layout="centered")
st.title(" Project Insight")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
query = st.text_input("Ask a question about your data")

if st.button("Generate Chart") and uploaded_file and query:
    with st.spinner("Analyzing."):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/api/visualize",
                files={"file": uploaded_file.getvalue()},
                data={"query": query},
            )

            if response.status_code == 200:
                chart = response.json()
                fig = go.Figure(data=chart["data"], layout=chart["layout"])
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("Error: " + response.json().get("error", "Unknown error"))

        except Exception as e:
            st.error(f"Exception occurred: {e}")
else:
    st.info("Please upload a CSV and enter a question.")
