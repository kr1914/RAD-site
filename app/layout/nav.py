# layout/menu.py

import streamlit as st

def display_menu():
    # 사이드바 네비게이션 메뉴
    st.sidebar.title("Lorelime 실험실")

    menu = None
    submenu = None

    # 스타일 설정
    st.markdown(
        """
        <style>
        .stButton > button {
            background-color: transparent;
            border: none;
            color: #000;
            padding: 10px;
            font-size: 15px;
        }
        .stButton > button:hover {
            color: #007BFF;
            background-color: #f0f0f0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.sidebar.expander("시스템관리"):
        if st.button("설정관리"):
            menu = "시스템관리"
            submenu = "설정관리"

    with st.sidebar.expander("데이터분석"):
        if st.button("CSV 분석"):
            menu = "데이터분석"
            submenu = "csv분석"
        if st.button("이미지 분석"):
            menu = "데이터분석"
            submenu = "이미지분석"

    with st.sidebar.expander("실험실"):
        if st.button("얼굴인식"):
            menu = "실험실"
            submenu = "얼굴인식"
        if st.button("얼굴위변조"):
            menu = "실험실"
            submenu = "얼굴위변조"
        if st.button("OCR"):
            menu = "실험실"
            submenu = "OCR"

    return menu, submenu
