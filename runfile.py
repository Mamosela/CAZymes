import streamlit as st
import pandas as pd
import sweetviz as sv
from streamlit.components.v1 import html

st.set_page_config(page_title="EDA App", layout="wide")

st.title("📊 Exploratory Data Analysis App")

# Upload file
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Read data
    df = pd.read_csv(uploaded_file, sep=';')

    st.subheader("🔍 Data Preview")
    st.dataframe(df.head())

    st.subheader("📈 Basic Information")
    col1, col2 = st.columns(2)

    with col1:
        st.write("Shape:", df.shape)
        st.write("Columns:", df.columns.tolist())

    with col2:
        st.write("Data Types:")
        st.write(df.dtypes)

    st.subheader("📊 Summary Statistics")
    st.dataframe(df.describe())

    st.subheader("❗ Missing Values")
    missing = df.isnull().sum()
    st.dataframe(missing)

    # Sweetviz Report
    st.subheader("📊 Sweetviz Report")

    if st.button("Generate Sweetviz Report"):
        report = sv.analyze(df)
        report_path = "sweetviz_report.html"
        report.show_html(report_path)

        with open(report_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        html(html_content, height=1000, scrolling=True)
