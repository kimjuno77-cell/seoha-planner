import streamlit as st
import datetime
import calendar
import json
import os

# 💡 달력 시작을 '일요일'로 강제 설정
calendar.setfirstweekday(6)

# 페이지 설정
st.set_page_config(page_title="서하의 플래너", page_icon="🤍", layout="centered")

# 🚨 어떤 아이폰/다크모드에서도 절대 무너지지 않는 무적의 CSS 🚨
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    /* 1. 다크모드 완전 차단 및 기본 폰트 설정 */
    html, body, [class*="css"], .stApp {
        font-family: 'Pretendard', -apple-system, sans-serif !important;
        background-color: #FDFBF7 !important; /* 강제 밝은 배경 */
    }
    
    /* 메뉴바 등 불필요한 요소 숨김 */
    #MainMenu, header, footer { visibility: hidden; }

    /* 2. 모든 글씨 색상을 강제로 어두운 색 고정 (검정 화면 방지) */
    p, span, div, label, h1, h2, h3, h4, h5, h6, li {
        color: #334155 !important;
    }

    /* 3. 🚨 가장 중요: 모바일에서 세로로 떨어지는 현상 원천 차단 🚨 */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: stretch !important;
        width: 100% !important;
        gap: 4px !important;
        margin-bottom: 6px !important;
    }
    [data-testid="column"] {
        min-width: 0 !important;
        flex: 1 1 0% !important;
        padding: 0 !important;
    }

    /* 4. 버튼 디자인 (검정 박스 방지 및 애플 스타일 둥근 사각형) */
    button[kind="secondary"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        color: #334155 !important;
        padding: 4px !important;
        height: 100% !important;
        min-height: 50px !important;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.02) !important;
    }
    button[kind="secondary"] * {
        color: #334155 !important;
        font-weight: 600 !important;
    }

    /* ✨ 오늘 날짜 강조 버튼 (포인트 핑크) */
    button[kind="primary"] {
        background: linear-gradient(135deg, #FF4B6E 0%, #FF2D55 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 4px !important;
        height: 100% !important;
        min-height: 50px !important;
        box-shadow: 0px 4px 10px rgba(255, 45, 85, 0.3) !important;
    }
    button[kind="primary"] * {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }

    /* 5. 입력창 및 체크박스 하얗게 고정 */
    .stTextInput input {
        background-color: #FFFFFF !important;
        color: #334155 !important;
        border: 2px solid #E2E8F0 !important;
        border-radius: 10px !important;
    }
    
    /* 6. 타이틀 및 요일 헤더 */
    .apple-title {
        color: #1D1D1F !important;
        text-align: center;
        font-weight: 800 !important;
        font-size: 1.8rem !important;
        margin-top: 10px;
    }
    .weekday-header {
        text-align: center;
        font-weight: 700;
        font-size: 0.85rem;
        padding-bottom: 5px;
    }

    /* 7. 하단 핑크 편지 박스 */
    .letter-box {
        background: linear-gradient(135deg, #FF6B8B 0%, #FF2D55 100%);
        padding: 24px;
        border-radius: 20px;
        margin-top: 30px;
        box-shadow: 0px 8px 20px rgba(255, 45, 85, 0.2);
    }
    .letter-box * { color: #FFFFFF !important; }

    /* 모바일 달력 글씨 크기 최적화 (글자 깨짐 방지) */
    @media (max-width: 768px) {
        button[kind="secondary"] p, button[kind="primary"] p {
            font-size: 10.5px !important;
            line-height: 1.3 !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- 💡 요일별 기본 미션 데이터 베이스 ---
def get_default_tasks(year, month, day):
    wd = datetime.date(year, month, day).weekday()
    if wd == 0:
        return [
            {"id": 1, "text": "영어/수학 학원 및 숙제 클리어 🎒", "done": False},
            {"id": 2, "text": "수학 1시간 완전 휴식 (넷플릭스 등 허용) 🎁", "done": False}
        ]
    elif wd in [1, 3, 5]:
        if wd == 1:
            return [{"id": 1, "text": "수학 취약단원 인강 1개 및 예제 풀기 📐", "done": False},
                    {"id": 2, "text": "국어 문학 시어 의미 대조 분석 🌸", "done": False}]
        elif wd == 3:
            return [{"id": 1, "text": "수학 취약유형 10문제 (타이머) ⏱️", "done": False},
                    {"id": 2, "text": "국어 비문학 과학/기술 지문 완벽 해부 🧠", "done": False}]
        else:
            return [{"id": 1, "text": "수학 이번 주 오답노트 완벽 정복 🔥", "done": False},
                    {"id": 2, "text": "국어 고전시가 모르는 단어 정리 📜", "done": False}]
    else:
        if wd == 2:
            return [{"id": 1, "text": "영어 모의고사 오답노트 (선택지 분석) 🇺🇸", "done": False},
                    {"id": 2, "text": "통합사회/과학 흐름표 키워드 채우기 🧪", "done": False}]
        elif wd == 4:
            return [{"id": 1, "text": "영단어 누적 100개 셀프 테스트 💯", "done": False},
                    {"id": 2, "text": "통과 기출문제 풀고 오답 밑줄 치기 🧪", "done": False}]
        else:
            return [{"id": 1, "text": "영어 지문 읽고 주제 한 문장 요약 📝", "done": False},
                    {"id": 2, "text": "통사 교과서 날개 질문에 스스로 답하기 🗺️", "done": False}]

# --- 💡 감성 편지 리스트 ---
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
today_letter = daily_letters[(real_today.day - 1) % len(daily_letters)]

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
        
    if day_str not in st.session_state.planner_data[month_key]:
        st.session_state.planner_data[month_key][day_str] = {
            "tasks": get_default_tasks(year, month, day),
            "sticker": "",
            "initialized": True
        }
    elif not st.session_state.planner_data[month_key][day_str].get("initialized"):
        st.session_state.planner_data[month_key][day_str]["tasks"] = get_default_tasks(year, month, day)
        st.session_state.planner_data[month_key][day_str]["initialized"] = True
        
    return st.session_state.planner_data[month_key][day_str]

def update_day_data(year, month, day, new_data):
    month_key = get_month_key(year, month)
    day_str = str(day)
    st.session_state.planner_data[month_key][day_str] = new_data
    save_data(st.session_state.planner_data)


# --- 화면 구성 시작 ---
st.markdown("<div class='apple-title'>✨ 서하의 스마트 플래너 ✨</div>", unsafe_allow_html=True)
st.write("")

# 1. 월 네비게이션 (3칸 강제 배열)
nav_cols = st.columns([1, 2, 1])
with nav_cols[0]:
    if st.button("◀ 이전", use_container_width=True):
        if st.session_state.view_month == 1:
            st.session_state.view_month = 12
            st.session_state.view_year -= 1
        else:
            st.session_state.view_month -= 1
        st.session_state.selected_day = 1
        st.rerun()
with nav_cols[1]:
    st.markdown(f"<h3 style='text-align: center; margin-top:5px;'>{st.session_state.view_year}. {st.session_state.view_month:02d}</h3>", unsafe_allow_html=True)
with nav_cols[2]:
    if st.button("다음 ▶", use_container_width=True):
        if st.session_state.view_month == 12:
            st.session_state.view_month = 1
            st.session_state.view_year += 1
        else:
            st.session_state.view_month += 1
        st.session_state.selected_day = 1
        st.rerun()

st.write("---")

# 2. 요일 헤더 (7칸 강제 배열)
header_cols = st.columns(7)
weekdays = ["일", "월", "화", "수", "목", "금", "토"]
colors = ["#FF3B30", "#86868B", "#86868B", "#86868B", "#86868B", "#86868B", "#007AFF"]
for i, wd in enumerate(weekdays):
    header_cols[i].markdown(f"<div class='weekday-header' style='color:{colors[i]} !important;'>{wd}</div>", unsafe_allow_html=True)

# 3. 달력 출력 (7칸 강제 배열)
cal = calendar.monthcalendar(st.session_state.view_year, st.session_state.view_month)
for week in cal:
    day_cols = st.columns(7)
    for i, day in enumerate(week):
        if day != 0:
            is_today = (st.session_state.view_year == real_today.year and 
                        st.session_state.view_month == real_today.month and 
                        day == real_today.day)
            
            day_data = get_day_data(st.session_state.view_year, st.session_state.view_month, day)
            sticker = day_data.get("sticker", "")
            
            tasks = day_data.get("tasks", [])
            total_t = len(tasks)
            done_t = sum(1 for t in tasks if t["done"])
            
            # 버튼 내용 심플하게 요약 (글자 깨짐 방지)
            prog_str = "✓" if total_t > 0 and done_t == total_t else f"{done_t}/{total_t}" if total_t > 0 else ""
            wd_temp = datetime.date(st.session_state.view_year, st.session_state.view_month, day).weekday()
            day_badge = "🍯" if wd_temp == 0 else "📐" if wd_temp in [1, 3, 5] else "🇺🇸"
            
            btn_text = f"{day}일 {sticker}\n{day_badge} {prog_str}"
            btn_type = "primary" if is_today else "secondary"
            
            if day_cols[i].button(btn_text, key=f"day_{day}", type=btn_type, use_container_width=True):
                st.session_state.selected_day = day
                st.rerun()
        else:
            day_cols[i].markdown("<div style='height:50px; border-radius:12px; border:1px dashed #E2E8F0;'></div>", unsafe_allow_html=True)

st.write("---")

# 4. 상세 미션 영역
s_year = st.session_state.view_year
s_month = st.session_state.view_month
s_day = st.session_state.selected_day
wd_idx = datetime.date(s_year, s_month, s_day).weekday()

day_type = "🇺🇸 영어+탐구 찢기"
if wd_idx == 0: day_type = "🍯 힐링 먼데이"
elif wd_idx in [1, 3, 5]: day_type = "📐 수학+국어 집중"

st.markdown(f"<h3 style='margin:0 0 15px 0; font-size:1.2rem;'>🌸 {s_day}일 일정 : {day_type}</h3>", unsafe_allow_html=True)

day_data = get_day_data(s_year, s_month, s_day)
tasks = day_data.get("tasks", [])

if not tasks:
    st.info("등록된 일정이 없습니다. 아래에서 추가해 보세요!")
else:
    for idx, task in enumerate(tasks):
        # 모바일 강제 1줄 배열
        cb_cols = st.columns([8, 1])
        with cb_cols[0]:
            new_status = st.checkbox(task['text'], value=task['done'], key=f"task_{s_day}_{idx}")
            if new_status != task['done']:
                day_data['tasks'][idx]['done'] = new_status
                update_day_data(s_year, s_month, s_day, day_data)
                st.rerun()
        with cb_cols[1]:
            if st.button("✕", key=f"del_{s_day}_{idx}"):
                day_data['tasks'].pop(idx)
                update_day_data(s_year, s_month, s_day, day_data)
                st.rerun()

st.write("")
with st.form(key=f"add_task_form_{s_day}", clear_on_submit=True):
    form_cols = st.columns([4, 1])
    with form_cols[0]:
        new_task = st.text_input("새 할 일...", label_visibility="collapsed")
    with form_cols[1]:
        if st.form_submit_button("추가") and new_task.strip():
            day_data['tasks'].append({"id": len(tasks)+1, "text": new_task.strip(), "done": False})
            update_day_data(s_year, s_month, s_day, day_data)
            st.rerun()

if st.button("↺ 기본 추천 일정 복원", use_container_width=True):
    day_data['tasks'] = get_default_tasks(s_year, s_month, s_day)
    update_day_data(s_year, s_month, s_day, day_data)
    st.rerun()

# 5. 스티커 영역 (7칸 강제 배열)
st.markdown("<h4 style='margin-top:20px; font-size:1rem;'>🎀 오늘 하루 스티커</h4>", unsafe_allow_html=True)
sticker_cols = st.columns(7)
emojis = ['🌸', '🔥', '🔋', '🫠', '👑', '💖', '❌']
for i, emoji in enumerate(emojis):
    if emoji == '❌':
        if sticker_cols[i].button("✕", key=f"clear_st"):
            day_data['sticker'] = ""
            update_day_data(s_year, s_month, s_day, day_data)
            st.rerun()
    else:
        if sticker_cols[i].button(emoji, key=f"st_{emoji}"):
            day_data['sticker'] = emoji
            update_day_data(s_year, s_month, s_day, day_data)
            st.rerun()

# 6. 오늘의 편지 (가장 완벽한 애플 스타일 카드)
st.markdown(f"""
<div class="letter-box">
    <div style="font-size: 12px; font-weight: 800; margin-bottom: 8px;">
        💌 오늘 도착한 편지 ({real_today.month}/{real_today.day})
    </div>
    <div style="font-size: 16px; font-weight: 700; line-height: 1.5;">
        "{today_letter}"
    </div>
</div>
""", unsafe_allow_html=True)
