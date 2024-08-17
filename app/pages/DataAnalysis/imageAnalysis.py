import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
import cv2 as cv
import numpy as np
import tools.tool as tool



st.header("이미지 분석")
# value = streamlit_image_coordinates("https://plantuml.com/imgw/img-e890b0fb49cf18a254ed383fa4710f81.png")
# st.write(value)
st.write("이미지 분석 페이지입니다.")

uploaded_file = st.file_uploader("Choose a CSV file")

if uploaded_file is not None:
    try:
        # Read the uploaded file
        bytes_data = uploaded_file.getvalue()
    
        image = tool.bytes_to_image(bytes_data)
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        # Display the profiling report
        value = streamlit_image_coordinates(image)
        st.write(value)
    except Exception as e:
        st.error(f"Error: {e}")