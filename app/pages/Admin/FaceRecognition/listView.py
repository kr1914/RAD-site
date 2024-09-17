import random
import pandas as pd
import streamlit as st

df = pd.DataFrame(
    {

    }
)

inqury_button = st.button("조회")

if inqury_button:
    df = pd.DataFrame(
        {
            "index" : [i for i in range(10) ]
            , "issue_date" : [ "2024-08-17" for i in range(10) ]
            , "issue_time" : [ "13:51:22" for i in range(10) ]
            , "refer_no" : [ "202402840285205" for i in range(10) ]
            , "status" : [ "완료" for i in range(10) ]
            , "similarity" : [ "87%" for i in range(10) ]
            , "liveness" : [ "77%" for i in range(10) ]
            , "enroll_face" : [ "3건" for i in range(10) ]
            , "attemp_face" : [ "1건" for i in range(10) ]
        }
    )

st.dataframe(
    df,
    column_config={
        "index" : "구분",
        "issue_date": "신청일자",
        "issue_time" : "신청시간",
        "refer_no" : "고객코드",
        "status" : "신청상태",
        "similarity" : "인식률",
        "liveness" : "생동률",
        "enroll_face" : "등록얼굴정보",
        "attemp_face" : "신청얼굴정보",
        "stars": st.column_config.NumberColumn(
            "Github Stars",
            help="Number of stars on GitHub",
            format="%d ⭐",
        ),
        "url": st.column_config.LinkColumn("App URL"),
    },
    hide_index=True,
)