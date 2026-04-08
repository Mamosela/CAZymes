import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

    # Bar graph for missing values
    st.subheader("📉 Missing Values Bar Chart")
    fig, ax = plt.subplots()
    missing.plot(kind='bar', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Select column for visualization
    st.subheader("📊 Column Visualization")
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

    if numeric_cols:
        selected_col = st.selectbox("Select a numeric column", numeric_cols)

        fig2, ax2 = plt.subplots()
        sns.histplot(df[selected_col], kde=True, ax=ax2)
        st.pyplot(fig2)

    # Bar chart for categorical data
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

    if categorical_cols:
        st.subheader("📊 Categorical Bar Chart")
        selected_cat = st.selectbox("Select a categorical column", categorical_cols)

        fig3, ax3 = plt.subplots()
        df[selected_cat].value_counts().plot(kind='bar', ax=ax3)
        plt.xticks(rotation=45)
        st.pyplot(fig3)

    # Optional: Profiling report
    if st.checkbox("Generate Profiling Report (can be slow)"):
        from ydata_profiling import ProfileReport
        from streamlit.components.v1 import components

        profile = ProfileReport(df, explorative=True)
        profile.to_file("report.html")

        with open("report.html", "r", encoding="utf-8") as f:
            html = f.read()

        components.html(html, height=800, scrolling=True)
