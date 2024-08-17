import pandas as pd
import streamlit as st
from streamlit_pandas_profiling import st_profile_report
from pandas_profiling import ProfileReport

st.header("CSV 분석")
uploaded_file = st.file_uploader("Choose a CSV file")

if uploaded_file is not None:
    try:
        # Read the uploaded file
        df = pd.read_csv(uploaded_file, encoding='utf-8')
    
        profile = ProfileReport(df, title="Pandas Profiling Report")
        
        # Display the profiling report
        st_profile_report(profile)
        st.write('')
    except Exception as e:
        st.error(f"Error: {e}")


    