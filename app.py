import streamlit as st
import datetime
import calendar
import json
import os

calendar.setfirstweekday(6)
st.set_page_config(page_title="서하의 플래너", page_icon="🤍", layout="centered")

st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    html, body, [class*="css"], .stApp {
        font-family: 'Pretendard', -apple-system, sans-serif !important;
        background-color: #FDFBF7 !important;
    }
    
    /* 버튼의 검정색 제거 및 깔끔한 테두리 */
    button {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        color: #334155 !important;
        border-radius: 8px !important;
    }

    /* 🚨 세로보기에서 날짜 칸이 넓어지는 현상 방지: 비율 고정 */
    [data-testid="column"] {
        flex: 1 1 14% !important;
        max-width: 14% !important;
        padding: 2px !important;
    }
    
    /* 날짜 버튼 디자인 */
    div.stButton > button {
        width: 100% !important;
        aspect-ratio: 1/1 !important; /* 가로세로 비율 1:1 강제 */
        padding: 0px !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        white-space: pre-line !important;
    }

    .apple-title { color: #1D1D1F !important; text-align: center; font-weight: 800 !important; font-size: 1.5rem !important; }
    .tip-box { background: #E6F4FF; padding: 15px; border-radius: 12px; margin: 15px 0; border-left: 5px solid #007AFF; }
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

st.markdown("<div class='apple-title'>✨ 서하의 스마트 플래너 ✨</div>", unsafe_allow_html=True)

# 언니의 꿀팁 복원
st.markdown("""
<div class='tip-box'>
    <b>💡 언니의 공부 꿀팁:</b><br>
    "서하야, 모르는 문제랑 씨름할 땐 <b>타이머를 10분만</b> 맞춰봐! 
    시간이 지나도 안 풀리면 바로 해설지를 보되, <b>'왜 이렇게 생각 못 했지?'</b>라는 
    핵심 문장만 딱 한 줄 적어두면 그게 진짜 네 실력이 돼! 오늘도 화이팅!"
</div>
""", unsafe_allow_html=True)

# 달력 출력 (비율 유지)
cal = calendar.monthcalendar(datetime.date.today().year, datetime.date.today().month)
for week in cal:
    cols = st.columns(7)
    for i, day in enumerate(week):
        if day != 0:
            cols[i].button(f"{day}\n·")
        else:
            cols[i].write("")

st.write("---")
st.info("이제 아이폰 세로 화면에서도 달력이 예쁘게 정렬됩니다!")
