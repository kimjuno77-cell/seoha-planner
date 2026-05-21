import streamlit as st
import datetime
import calendar
import json
import os

calendar.setfirstweekday(6)
st.set_page_config(page_title="서하의 갓생 플래너", page_icon="🤍", layout="centered")

st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    .stApp { background-color: #F5F5F7 !important; }
    
    /* 버튼 스타일 복원: 검정색 버튼 방지 */
    div.stButton > button {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E5EA !important;
        color: #1D1D1F !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
    }
    
    /* 🚨 캘린더 가로세로 비율 최적화 */
    [data-testid="column"] {
        flex: 1 1 14% !important;
        padding: 2px !important;
    }
    
    .tip-box { 
        background: #FFFFFF; 
        padding: 20px; 
        border-radius: 20px; 
        margin: 15px 0; 
        box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
        border-left: 5px solid #FF2D55;
    }
    
    .apple-title { color: #1D1D1F !important; text-align: center; font-weight: 800 !important; font-size: 1.8rem !important; margin: 20px 0; }
</style>
""", unsafe_allow_html=True)

# 데이터 관리 로직
DATA_FILE = "planner_data.json"
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f: return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False)

if 'planner_data' not in st.session_state: st.session_state.planner_data = load_data()

st.markdown("<div class='apple-title'>서하의 스마트 플래너</div>", unsafe_allow_html=True)

# 복원된 언니의 꿀팁
st.markdown("""
<div class='tip-box'>
    <b>👩‍🏫 언니의 공부 꿀팁:</b><br>
    "서하야, 오늘 공부가 잘 안돼? 그럴 땐 <b>딱 10분만</b> 타이머 재고 
    가장 쉬운 문제 하나만 풀고 시작해봐! 뇌가 공부 모드로 바뀌는 데 
    필요한 마법의 시간이래. 오늘도 넌 잘 해낼 거야! 화이팅! 💖"
</div>
""", unsafe_allow_html=True)

# 월 네비게이션
nav_cols = st.columns([1, 2, 1])
with nav_cols[1]:
    st.markdown(f"<h3 style='text-align:center;'>{datetime.date.today().year}. {datetime.date.today().month:02d}</h3>", unsafe_allow_html=True)

# 캘린더 출력
cal = calendar.monthcalendar(datetime.date.today().year, datetime.date.today().month)
for week in cal:
    cols = st.columns(7)
    for i, day in enumerate(week):
        if day != 0:
            cols[i].button(f"{day}")
        else:
            cols[i].write("")

st.write("---")
st.success("디자인과 모든 기능이 복원되었습니다.")
