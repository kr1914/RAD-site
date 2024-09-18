import streamlit as st
from layout.nav import display_menu

pages = {
    "데이터 분석": [
        st.Page(title="CSV", page="pages/DataAnalysis/csvAnalysis.py"),
        st.Page(title="이미지", page="pages/DataAnalysis/imageAnalysis.py"),
        st.Page(title="네트워크", page="pages/DataAnalysis/NetDepAnalysis.py"),
        #st.Page(title="네트워크2", page="pages/DataAnalysis/plotly_test.py")
    ],
    
    "연구실" : [
        st.Page(title="얼굴진위여부", page="pages/FaceRecognition/faceAntiSpoofing.py"),
        st.Page(title="얼굴인식", page="pages/FaceRecognition/faceEmbedding.py"),
        st.Page(title="글자인식", page="pages/OCR/paddle_ocr.py")
    ],
    "현황조회" : [
        st.Page(title="얼굴인식시도내역조회", page="pages/Admin/FaceRecognition/listView.py")
    ]
}

st.sidebar.header("페이지 네비게이션")
#title("📂 페이지 네비게이션")
pg = st.navigation(pages)
#pg.title("페이지 네비게이션")

pg.run()
