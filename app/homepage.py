import streamlit as st
from layout.nav import display_menu

pages = {
    "데이터 분석": [
        st.Page(title="CSV 분석", page="pages/DataAnalysis/csvAnalysis.py"),
        st.Page(title="이미지 분석", page="pages/DataAnalysis/imageAnalysis.py")
    ],
    "연구실" : [
        st.Page(title="얼굴진위여부", page="pages/FaceRecognition/faceAntiSpoofing.py"),
        st.Page(title="얼굴인식", page="pages/FaceRecognition/faceEmbedding.py"),
        st.Page(title="글자인식", page="pages/OCR/paddle_ocr.py")
    ],
    
}
pg = st.navigation(pages)

# st.sidebar.selectbox("Group", ["A","B","C"], key="group")
# st.sidebar.slider("Size", 1, 5, key="size")

pg.run()