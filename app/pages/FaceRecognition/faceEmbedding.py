import streamlit as st
from streamlit_image_comparison import image_comparison
import cv2 as cv
import numpy as np
import tools.tool as tool



st.header("얼굴비교 페이지")
# value = streamlit_image_coordinates("https://plantuml.com/imgw/img-e890b0fb49cf18a254ed383fa4710f81.png")
# st.write(value)
st.write("이미지 분석 페이지입니다.")


uploaded_files = st.file_uploader(
    "Choose a CSV file", accept_multiple_files=True
)
if len(uploaded_files) != 2:
    st.toast('이미지가 2장 필요합니다.', icon='❌')

images = []

for uploaded_file in uploaded_files:
    if uploaded_file is not None:
        try:
            # Read the uploaded file
            bytes_data = uploaded_file.getvalue()
        
            image = tool.bytes_to_image(bytes_data)
            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            # Display the profiling report
            images.append(image)
            #value = streamlit_image_coordinates(image)
            #st.write(value)
        except Exception as e:
            st.error(f"Error: {e}")
            
# set page config
#st.set_page_config(page_title="Image-Comparison Example", layout="centered")

if len(images) == 2:
    col1, col2 = st.columns(2)

    # 각 열에 이미지 표시
    with col1:
        st.image(images[0], caption='Image 1')

    with col2:
        st.image(images[1], caption='Image 2')