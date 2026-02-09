import streamlit as st
import sqlite3

# 1. 데이터베이스 설정 (결과 저장을 위한 SQL)
def init_db():
    conn = sqlite3.connect('publishing_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (email TEXT, type TEXT)''')
    conn.commit()
    return conn

# 2. 웹페이지 레이아웃
st.set_page_config(page_title="독립출판 유형 테스트", page_icon="📚")
st.title("📚 나에게 맞는 독립출판 유형 찾기")
st.write("작년 한 해 동안 정리된 데이터를 기반으로 당신의 출판 성향을 분석합니다.")

# 3. 질문지 구성
with st.form("test_form"):
    st.subheader("질문에 답해주세요!")
    
    q1 = st.radio("1. 책 재고가 집에 쌓이는 것이 걱정되나요?", 
                  ("전혀 상관없다 (직접 소장하고 싶다)", "매우 걱정된다 (재고 없는 게 최고다)"))
    
    q2 = st.radio("2. ISBN(국제표준도서번호)을 발급받아 대형서점에 유통하고 싶나요?", 
                  ("네, 교보문고 등에 입고하고 싶어요", "아니오, 독립서점 감성이 좋아요"))
    
    email = st.text_input("결과 분석을 위해 이메일을 입력해주세요 (뉴스레터 구독)")
    
    submitted = st.form_submit_button("결과 확인하기")

# 4. 결과 도출 로직 및 DB 저장
if submitted:
    if not email:
        st.error("이메일을 입력해야 결과를 볼 수 있습니다!")
    else:
        # 간단한 알고리즘 로직
        res_type = ""
        if q1.startswith("전혀") and q2.startswith("네"):
            res_type = "A 유형: 올라운더 작가 (인쇄 + 대형유통)"
        elif q1.startswith("전혀") and q2.startswith("아니오"):
            res_type = "B 유형: 독립서점 낭만파 (인쇄 + 소규모유통)"
        elif q1.startswith("매우") and q2.startswith("네"):
            res_type = "C 유형: 스마트 POD 작가 (주문생산 + 대형유통)"
        else:
            res_type = "D 유형: 디지털 노마드 (전자책 전용)"

        # DB 저장
        conn = init_db()
        c = conn.cursor()
        c.execute("INSERT INTO users (email, type) VALUES (?, ?)", (email, res_type))
        conn.commit()
        conn.close()

        # 결과 화면 출력
        st.success(f"🎉 테스트 완료! 당신은 [{res_type}] 입니다.")
        st.balloons()
        st.info(f"{email}님께 곧 맞춤형 가이드를 보내드릴게요!")
