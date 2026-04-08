import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Optional imports (EDA reports)
import sweetviz as sv
from ydata_profiling import ProfileReport

st.set_page_config(page_title="EDA App", layout="wide")

st.title("📊 Exploratory Data Analysis App")

# Upload file
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, sep=';')

    st.subheader("🔍 Data Preview")
    st.dataframe(df.head())

    # Basic info
    st.subheader("📈 Data Summary")
    st.write(df.describe())

    st.subheader("ℹ️ Data Info")
    buffer = []
    df.info(buf=buffer)
    info_str = "\n".join(buffer)
    st.text(info_str)

    # Missing values
    st.subheader("❗ Missing Values")
    missing = df.isnull().sum()
    st.dataframe(missing)

    # Bar chart (categorical column selection)
    st.subheader("📊 Bar Chart")

    col = st.selectbox("Select a column for bar chart", df.columns)

    if df[col].dtype == "object":
        counts = df[col].value_counts()

        fig, ax = plt.subplots()
        counts.plot(kind="bar", ax=ax)
        ax.set_title(f"Count of {col}")
        st.pyplot(fig)
    else:
        st.warning("Please select a categorical column for bar chart")

    # Numeric column histogram
    st.subheader("📉 Histogram")

    num_col = st.selectbox("Select numeric column", df.select_dtypes(include=['int64', 'float64']).columns)

    fig2, ax2 = plt.subplots()
    df[num_col].plot(kind="hist", bins=20, ax=ax2)
    ax2.set_title(f"Distribution of {num_col}")
    st.pyplot(fig2)

    # Sweetviz report
    st.subheader("📋 Sweetviz Report")

    if st.button("Generate Sweetviz Report"):
        report = sv.analyze(df)
        report.show_html("sweetviz_report.html")
        with open("sweetviz_report.html", "r", encoding="utf-8") as f:
            st.components.v1.html(f.read(), height=800, scrolling=True)

    # YData Profiling report
    st.subheader("📑 Profiling Report")

    if st.button("Generate Profiling Report"):
        profile = ProfileReport(df, title="EDA Report", explorative=True)
        profile.to_file("profile_report.html")

        with open("profile_report.html", "r", encoding="utf-8") as f:
            st.components.v1.html(f.read(), height=800, scrolling=True)

else:
    st.info("👆 Upload a CSV file to begin")
