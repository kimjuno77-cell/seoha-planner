import streamlit as st
import datetime
import calendar
import json
import os

# 💡 달력 시작을 '일요일'로 강제 설정
calendar.setfirstweekday(6)

st.set_page_config(page_title="서하의 갓생 플래너", page_icon="💖", layout="wide")

# 💡 다크모드 방지 및 예쁜 UI CSS
st.markdown("""
<style>
    .stApp, .main { background-color: #FDFBF7 !important; }
    h1, h2, h3, p, span, div, label { color: #334155 !important; }
    
    .pink-title {
        color: #db2777 !important;
        text-align: center;
        font-weight: 900 !important;
        margin-bottom: 20px;
    }

    .weekday-header {
        text-align: center;
        font-weight: 900;
        font-size: 1.2rem;
        padding-bottom: 10px;
        border-bottom: 2px solid #fce7f3;
        margin-bottom: 10px;
    }

    div[data-testid="stButton"] > button {
        height: 100px !important;
        width: 100% !important;
        border-radius: 16px !important;
        border: 2px solid #fce7f3 !important;
        background-color: #ffffff !important;
        color: #475569 !important;
        font-weight: 800 !important;
        font-size: 14px !important;
        white-space: pre-wrap !important;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.02) !important;
        transition: all 0.2s ease-in-out !important;
    }
    
    div[data-testid="stButton"] > button:hover {
        border-color: #f472b6 !important;
        background-color: #fdf2f8 !important;
        transform: translateY(-2px);
    }

    /* ✨ '오늘' 날짜 강조 ✨ */
    div[data-testid="stButton"] > button[kind="primary"] {
        background: linear-gradient(135deg, #f472b6, #db2777) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0px 6px 15px rgba(219, 39, 119, 0.4) !important;
        transform: scale(1.05);
    }
    div[data-testid="stButton"] > button[kind="primary"] * {
        color: white !important;
    }

    .stTextInput > div > div > input {
        background-color: #ffffff !important;
        color: #334155 !important;
        border: 2px solid #fbcfe8 !important;
        border-radius: 10px !important;
    }
    
    .letter-box {
        background: linear-gradient(135deg, #4c1d95, #312e81);
        padding: 25px;
        border-radius: 20px;
        margin-top: 40px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    .letter-box p, .letter-box span { color: white !important; }
</style>
""", unsafe_allow_html=True)

# --- 💡 요일별 기본 미션 자동 생성기 ---
def get_default_tasks(year, month, day):
    wd = datetime.date(year, month, day).weekday() # 0:월 ~ 6:일
    if wd == 0: # 월요일
        return [
            {"id": 1, "text": "영어/수학 학원 및 학교 숙제 깔끔하게 클리어하기 🎒", "done": False},
            {"id": 2, "text": "오늘 1시간 완전 휴식 (넷플릭스/아이돌 영상 허용! 🎁)", "done": False}
        ]
    elif wd in [1, 3, 5]: # 화, 목, 토
        if wd == 1:
            return [{"id": 1, "text": "수학 취약 단원 개념 인강 1개 보고 바로 예제 풀기 📐", "done": False},
                    {"id": 2, "text": "국어 문학 시어의 의미 대조 비교 분석하기 🌸", "done": False}]
        elif wd == 3:
            return [{"id": 1, "text": "수학 취약 유형 10문제 풀기 (시간 타이머 재기) ⏱️", "done": False},
                    {"id": 2, "text": "국어 비문학 구조도 그리며 읽는 연습 ✍️", "done": False}]
        else:
            return [{"id": 1, "text": "수학 이번 주 오답 선별해서 한 번 더 완전 정복 🔥", "done": False},
                    {"id": 2, "text": "국어 문법/고전시가 취약 파트 개념 정리 📚", "done": False}]
    else: # 수, 금, 일
        if wd == 2:
            return [{"id": 1, "text": "영어 모의고사 오답노트 (오답 선택지 매력 분석) 🇺🇸", "done": False},
                    {"id": 2, "text": "탐구 과목 흐름 연표/목차에 키워드 가리고 채우기 🧪", "done": False}]
        elif wd == 4:
            return [{"id": 1, "text": "영어 단어 누적 100개 셀프 테스트 해보기 💯", "done": False},
                    {"id": 2, "text": "탐구 기출문제 풀고 틀린 선지 개념서에 밑줄 치기 ✍️", "done": False}]
        else:
            return [{"id": 1, "text": "영어 지문 통째로 보면서 주제 한 문장으로 요약하기 📝", "done": False},
                    {"id": 2, "text": "한 주간 정리한 나만의 단어/오답 수첩 정독하기 📖", "done": False}]

# --- 데이터 관리 로직 ---
DATA_FILE = "planner_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if 'planner_data' not in st.session_state:
    st.session_state.planner_data = load_data()

real_today = datetime.date.today()

if 'view_year' not in st.session_state:
    st.session_state.view_year = real_today.year
if 'view_month' not in st.session_state:
    st.session_state.view_month = real_today.month
if 'selected_day' not in st.session_state:
    st.session_state.selected_day = real_today.day

def get_month_key(year, month):
    return f"{year}_{month}"

def get_day_data(year, month, day):
    month_key = get_month_key(year, month)
    day_str = str(day)
    
    if month_key not in st.session_state.planner_data:
        st.session_state.planner_data[month_key] = {}
        
    # 💡 해당 날짜의 기록이 아예 없다면 '기본 미션'을 셋팅해 줌
    if day_str not in st.session_state.planner_data[month_key]:
        st.session_state.planner_data[month_key][day_str] = {
            "tasks": get_default_tasks(year, month, day),
            "sticker": ""
        }
    return st.session_state.planner_data[month_key][day_str]

def update_day_data(year, month, day, new_data):
    month_key = get_month_key(year, month)
    day_str = str(day)
    st.session_state.planner_data[month_key][day_str] = new_data
    save_data(st.session_state.planner_data)

# 💡 매일 자동으로 업데이트 되는 편지
daily_letters = [
    "서하야, 이번 달의 첫날이야! 새로운 마음으로 기분 좋게 시작해 보자. 넌 충분히 해낼 수 있어! 💖",
    "오늘 하루도 수고 많았어. 계획대로 안 된 날도 있겠지만, 책상에 앉은 것만으로도 대단해! 🌟",
    "서하의 노력은 결코 배신하지 않을 거야. 지금 흘린 땀방울이 모여 큰 바다가 될 테니까! 🌊",
    "조금 느려도 괜찮아. 방향만 맞다면 반드시 목표에 도달할 수 있어. 서하만의 속도로 나아가자. 🐢",
    "힘들 땐 잠시 쉬어가도 좋아. 쉼표가 있어야 마침표도 예쁘게 찍을 수 있는 법이니까. ☕",
    "오늘 풀리지 않던 문제도, 내일 다시 보면 신기하게 풀릴 때가 있어. 너무 스트레스받지 마! 🧩",
    "서하야, 매일 빽빽한 일정표 보느라 고생이 많지? 엄마는 항상 널 응원하고 있어. 화이팅! 👩‍👧",
    "어려운 과목을 먼저 끝내면 하루가 훨씬 가벼워질 거야. 가장 싫은 것부터 해치우는 마법! 🪄",
    "공부하다 졸리면 과감하게 10분만 엎드려 자! 맑은 머리로 공부하는 게 훨씬 효율적이야. 😴",
    "서하가 좋아하는 음악 한 곡 들으면서 기분 전환해 봐. 노래가 끝난 후엔 다시 집중 모드! 🎧",
    "작은 성취가 모여 큰 자신감을 만들어. 오늘 세운 미션 하나만 달성해도 넌 오늘 성공한 거야! 🏆",
    "남과 비교하지 마. 서하는 서하만의 특별한 매력과 잠재력이 있으니까. 너 자신을 믿어! ✨",
    "실수는 누구나 해. 중요한 건 그 실수에서 무엇을 배우느냐야. 오답노트가 너의 무기가 될 거야. ⚔️",
    "가끔은 아무것도 안 하고 멍때리는 시간도 필요해. 뇌에게도 휴가를 줘. 🌴",
    "서하야, 넌 이미 충분히 잘하고 있어. 너무 완벽해지려고 자신을 괴롭히지 마. 🫂",
    "오늘 하루, 정말 치열하게 보냈구나. 거울 보면서 스스로에게 칭찬 한마디 해줘! '잘했어, 서하야' 🪞",
    "지칠 때는 네가 꿈꾸는 미래의 멋진 모습을 상상해 봐. 그 모습이 널 다시 뛰게 할 거야. 🏃‍♀️",
    "모르는 걸 부끄러워하지 마. 질문하는 용기가 널 더 똑똑하게 만들어줄 테니까. 🙋‍♀️",
    "서하의 긍정적인 에너지가 주위 사람들에게도 힘이 돼. 항상 밝게 웃어줘서 고마워! 😊",
    "오늘따라 집중이 안 된다면 장소를 조금 바꿔보는 건 어때? 카페나 도서관도 좋아. ☕",
    "포기하고 싶은 순간이 온다면, 왜 이 일을 시작했는지 처음의 마음을 떠올려 봐. 🔙",
    "건강이 최우선이야! 밥 잘 챙겨 먹고, 틈틈이 스트레칭하는 거 잊지 마. 🍎",
    "서하야, 넌 생각보다 훨씬 강하고 똑똑한 사람이야. 네 안의 거인을 깨워봐! 🦸‍♀️",
    "모든 걸 다 잘할 필요는 없어. 네가 잘하는 것, 좋아하는 것에 집중해도 괜찮아. 🎯",
    "오늘의 작은 노력이 내일의 큰 기적을 만들 거야. 매일매일 조금씩 성장하는 서하를 응원해! 🌱",
    "가끔은 친구들과 수다 떨면서 스트레스 푸는 시간도 꼭 필요해. 즐거운 시간 보내! 👯‍♀️",
    "어려운 문제를 혼자 힘으로 풀어냈을 때의 그 짜릿함! 오늘도 그 기분을 느껴보길 바라. ⚡",
    "서하야, 밤새우지 말고 푹 자. 충분한 수면이 기억력을 높여준다는 사실, 알고 있지? 🛌",
    "지금의 고생이 훗날 널 빛나게 해줄 거야. 묵묵히 너의 길을 걸어가는 널 존경해. 👑",
    "이번 달도 거의 끝나가네. 마지막까지 유종의 미를 거둘 수 있도록 조금만 더 힘내자! 🔥",
    "한 달 동안 정말 고생 많았어, 서하야! 네가 자랑스러워. 맛있는 거 먹고 푹 쉬어! 🍰"
]
today_letter = daily_letters[(real_today.day - 1) % len(daily_letters)]

# --- 상단 타이틀 및 월 이동 ---
st.markdown("<h1 class='pink-title'>✨ 서하의 스마트 효율 메이커 ✨</h1>", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns([1, 2, 3, 2, 1])
with col2:
    if st.button("◀️ 이전 달", use_container_width=True):
        if st.session_state.view_month == 1:
            st.session_state.view_month = 12
            st.session_state.view_year -= 1
        else:
            st.session_state.view_month -= 1
        st.session_state.selected_day = 1
        st.rerun()
with col3:
    st.markdown(f"<h3 style='text-align: center;'>{st.session_state.view_year}년 {st.session_state.view_month}월</h3>", unsafe_allow_html=True)
with col4:
    if st.button("다음 달 ▶️", use_container_width=True):
        if st.session_state.view_month == 12:
            st.session_state.view_month = 1
            st.session_state.view_year += 1
        else:
            st.session_state.view_month += 1
        st.session_state.selected_day = 1
        st.rerun()

st.write("---")

tab1, tab2 = st.tabs(["📅 다이어리 꾸미기", "✨ 언니의 팩폭 꿀팁"])

with tab1:
    col_cal, col_tasks = st.columns([4, 3])
    
    # [왼쪽] 달력 영역
    with col_cal:
        st.markdown("### 🗓️ 이달의 스케줄러")
        
        cols = st.columns(7)
        weekdays = ["일", "월", "화", "수", "목", "금", "토"]
        for i, wd in enumerate(weekdays):
            color = "#ef4444" if i == 0 else "#3b82f6" if i == 6 else "#64748b"
            cols[i].markdown(f"<div class='weekday-header' style='color: {color};'>{wd}</div>", unsafe_allow_html=True)
            
        cal = calendar.monthcalendar(st.session_state.view_year, st.session_state.view_month)
        for week in cal:
            cols = st.columns(7)
            for i, day in enumerate(week):
                if day != 0:
                    is_real_today = (st.session_state.view_year == real_today.year and 
                                     st.session_state.view_month == real_today.month and 
                                     day == real_today.day)
                    
                    day_data = get_day_data(st.session_state.view_year, st.session_state.view_month, day)
                    sticker = day_data.get("sticker", "")
                    
                    tasks = day_data.get("tasks", [])
                    total_t = len(tasks)
                    done_t = sum(1 for t in tasks if t["done"])
                    
                    prog_str = ""
                    if total_t > 0:
                        if done_t == total_t:
                            prog_str = "💯"
                        else:
                            prog_str = f"({done_t}/{total_t})"
                    
                    if is_real_today:
                        label = f"👑오늘👑\n{day}일\n{sticker} {prog_str}"
                        btn_type = "primary"
                    else:
                        marker = "📍" if day == st.session_state.selected_day else ""
                        label = f"{marker} {day} \n{sticker}\n{prog_str}"
                        btn_type = "secondary"
                    
                    if cols[i].button(label, key=f"day_{day}", type=btn_type, use_container_width=True):
                        st.session_state.selected_day = day
                        st.rerun()

    # [오른쪽] 상세 미션 관리 영역
    with col_tasks:
        s_year = st.session_state.view_year
        s_month = st.session_state.view_month
        s_day = st.session_state.selected_day
        day_date = datetime.date(s_year, s_month, s_day)
        wd_idx = day_date.weekday()
        
        # 💡 요일에 따른 타이틀 출력
        day_type = "🇺🇸 영어+탐구 찢기"
        if wd_idx == 0: day_type = "🍯 서하의 힐링 먼데이"
        elif wd_idx in [1, 3, 5]: day_type = "📐 수학+국어 깊이파기"
        
        st.markdown(f"<h3 style='color:#db2777;'>💖 {s_day}일 미션: <span style='font-size:18px;'>{day_type}</span></h3>", unsafe_allow_html=True)
        
        day_data = get_day_data(s_year, s_month, s_day)
        tasks = day_data.get("tasks", [])
        
        if not tasks:
            st.info("등록된 일정이 없어! 아래에서 추가해 봐 ✏️")
        else:
            for idx, task in enumerate(tasks):
                col_cb, col_del = st.columns([6, 1])
                with col_cb:
                    new_status = st.checkbox(task['text'], value=task['done'], key=f"task_{s_month}_{s_day}_{idx}")
                    if new_status != task['done']:
                        day_data['tasks'][idx]['done'] = new_status
                        update_day_data(s_year, s_month, s_day, day_data)
                        st.rerun()
                with col_del:
                    if st.button("🗑️", key=f"del_{s_month}_{s_day}_{idx}"):
                        day_data['tasks'].pop(idx)
                        update_day_data(s_year, s_month, s_day, day_data)
                        st.rerun()
                        
        st.write("---")
        with st.form(key=f"add_task_form_{s_day}", clear_on_submit=True):
            new_task_text = st.text_input("새로운 미션 추가...")
            submitted = st.form_submit_button("➕ 추가하기")
            if submitted and new_task_text.strip():
                new_task = {"id": len(tasks)+1, "text": new_task_text.strip(), "done": False}
                day_data['tasks'].append(new_task)
                update_day_data(s_year, s_month, s_day, day_data)
                st.rerun()

        st.markdown("---")
        st.markdown("**🎀 오늘 기분 스티커**")
        emoji_cols = st.columns(6)
        emojis = ['🌸', '🔥', '🔋', '🫠', '👑', '💖']
        for i, emoji in enumerate(emojis):
            if emoji_cols[i].button(emoji, key=f"emoji_{s_day}_{emoji}"):
                day_data['sticker'] = emoji
                update_day_data(s_year, s_month, s_day, day_data)
                st.rerun()
                
        if day_data.get("sticker"):
            if st.button("🔄 스티커 지우기"):
                day_data['sticker'] = ""
                update_day_data(s_year, s_month, s_day, day_data)
                st.rerun()

        total_t = len(tasks)
        done_t = sum(1 for t in tasks if t["done"])
        progress = int((done_t / total_t) * 100) if total_t > 0 else 0
        st.write(f"**오늘의 달성률 {progress}%**")
        st.progress(progress)

with tab2:
    st.subheader("성적 수직 상승 명문대 선배의 팩트폭격 👩‍🏫")
    tips = [
        {"title": "하루에 4과목 넘게 공부하는 서하에게.. 🧠", "content": "국어 풀다가 영어 외우고 수학 끄적이고... 뇌한테 미안해야 해! 과목 바뀔 때마다 뇌가 적응하느라 피곤해. 하루 딱 2과목만 깊게 파보자! 🔥"},
        {"title": "월요일 텐션 바닥? 🙋‍♀️", "content": "월요일은 '완벽주의'를 내려놓자! 가벼운 숙제만 하고 1시간은 시원하게 멍때리는 '리커버리 타임'! 그래야 화요일에 집중력이 폭발해. 😉"},
        {"title": "눈으로만 보는 건 '독서'지 공부가 아냐 📖", "content": "개념서 형광펜 칠하고 '알겠군' 하는 건 네 실력이 아니야! 진짜 공부는 '인출(Output)'. 책 덮고 백지에 써보거나 인형한테 가르쳐봐! ✍️"},
        {"title": "오답노트 예쁘게 '그리는' 중? 🎨", "content": "오답노트에 가위로 문제 예쁘게 오려 붙이는 건 미술 시간! 오답 분석은 머리로 하는 거야. 틀린 길목에 깃발 꽂고 다음날 백지에 다시 풀기!"},
        {"title": "영단어 100개 외우고 90개 까먹어? 🧐", "content": "한 번에 다 외우려고 하지 마! 단어는 '자주 마주치기'가 핵심! 틈새시간을 지배하는 서하가 1등급 지배자! 🏆"}
    ]
    for tip in tips:
        with st.expander(f"📌 {tip['title']}"):
            st.write(tip['content'])

# --- 💌 하단 고정 편지 ---
st.markdown(f"""
<div class="letter-box">
    <span style="background-color: rgba(255,255,255,0.2); padding: 3px 10px; border-radius: 10px; font-size: 12px; font-weight: bold;">
        💖 오늘 서하에게 도착한 편지 ({real_today.month}/{real_today.day})
    </span>
    <p style="margin-top: 15px; font-size: 16px; font-weight: bold; line-height: 1.5;">"{today_letter}"</p>
</div>
""", unsafe_allow_html=True)
