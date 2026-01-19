import streamlit as st
import pandas as pd
import os
import MySQLdb
from config.config import HOST,USER,PASSWD,DB,PORT
@st.cache_resource
def get_conn():
    return MySQLdb.connect(
        host= HOST,
        user=USER,
        passwd=PASSWD,
        db=DB,
        port=PORT,
        charset="utf8mb4",
        )
@st.cache_data(ttl=600)
def load_faq_df():
    """
    DB의 faq 테이블에서 FAQ 전체를 DataFrame으로 로드
    - 테이블/컬럼명이 다르면 아래 SQL을 너희 스키마에 맞춰 수정하면 됨
    """
    conn = get_conn()

    sql = """
    SELECT
        company,
        category,
        question_text,
        answer_text
    FROM faq
    """

    return pd.read_sql(sql, conn)

# ----------------------------
# 공통 FAQ 표시 로직 (내부 함수)
# ----------------------------
def display_brand_faq(brand_name, select_key):
    try:
        df = load_faq_df()  
        
        # 1. 해당 브랜드 데이터만 필터링 (company 컬럼 기준)
        brand_df = df[df['company'] == brand_name]
        
        if brand_df.empty:
            st.warning(f"{brand_name}에 해당하는 데이터가 없습니다.")
            return

        # 2. 카테고리 선택 (해당 브랜드 내의 카테고리만 추출)
        category_list = brand_df['category'].unique().tolist()
        selected_cat = st.selectbox("카테고리를 선택하세요", category_list, key=select_key)
        
        st.write("---")
        
        # 3. 카테고리 필터링
        filtered_df = brand_df[brand_df['category'] == selected_cat]
        
        # 4. FAQ 출력
        for _, row in filtered_df.iterrows():
            # 4-1) 질문 리스트 노출, 4-2) 클릭 시 답변 노출
            with st.expander(row['question_text']):
                st.write(row['answer_text'])
                
    except Exception as e:
        st.error(f"{brand_name} 데이터를 로드하는 중 오류 발생: {e}")

# ----------------------------
# 인터페이스용 개별 함수 (app.py에서 호출)
# ----------------------------
def showhyundaifaq():
    display_brand_faq('hyundai', 'hyundai_select')

def showkiafaq():
    display_brand_faq('kia', 'kia_select')

def showgenesisfaq():
    display_brand_faq('genesis', 'genesis_select')