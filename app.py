from datetime import datetime
import random
import re

import streamlit as st

st.set_page_config(
    page_title="Lost & Found HWP",
    page_icon="🔎",
    layout="centered",
    initial_sidebar_state="collapsed",
)

EMAIL_PATTERN = r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$"
CLASS_OPTIONS = [f"ม.{grade}/{room}" for grade in range(1, 7) for room in range(1, 15)]
LOCATIONS = [
    "ทั้งหมด",
    "อาคาร 1",
    "อาคาร 2",
    "อาคาร 3",
    "อาคาร 4",
    "อาคาร 5",
    "โรงอาหาร",
    "หน้าเสาธง",
    "โดม",
    "อื่นๆ",
]
FIND_CATEGORIES = ["อุปกรณ์การเรียน", "กระเป๋า/กระเป๋าสตางค์", "อุปกรณ์อิเล็กทรอนิกส์", "เสื้อผ้า", "ขวดน้ำ", "อื่นๆ"]
CATEGORIES = FIND_CATEGORIES
STUDENTS = {
    "65001": {"name": "กมลชนก ใจดี", "class": "ม.5/1", "score": 82, "email": "student1@gmail.com"},
    "65002": {"name": "ธนกฤต แสงทอง", "class": "ม.4/3", "score": 64, "email": "thanakrit@hotmail.com"},
    "65003": {"name": "พิมพ์ชนก รุ่งเรือง", "class": "ม.6/2", "score": 95, "email": "pimchanok@outlook.com"},
}


def is_valid_email(email):
    if not isinstance(email, str):
        return False
    normalized = email.strip().lower()
    if not normalized or "@" not in normalized:
        return False
    if normalized.count("@") != 1:
        return False
    local_part, domain = normalized.rsplit("@", 1)
    if not local_part or not domain or "." not in domain:
        return False
    return bool(re.fullmatch(EMAIL_PATTERN, normalized))


def find_student_by_email(email):
    normalized = (email or "").strip().lower()
    for student_id, student in STUDENTS.items():
        for field in ("email", "personal_email", "school_email"):
            if student.get(field, "").strip().lower() == normalized:
                return student_id
    return None


def generate_otp():
    return f"{random.randint(0, 999999):06d}"


def logout_user():
    st.session_state.logged_in = False
    st.session_state.student_id = ""
    st.session_state.auth_email = ""
    st.session_state.auth_step = "email"
    st.session_state.otp_code = ""
    st.session_state.login_email = ""
    st.session_state.login_otp = ""
    st.session_state.pending_link_email = ""
    st.session_state.pending_student_id = ""
    st.session_state.pending_class = ""
    st.session_state.active_page = "find"
    st.session_state.find_open = True
    st.rerun()


if "reports" not in st.session_state:
    st.session_state.reports = [
        {
            "item": "กระเป๋าสตางค์สีดำ",
            "category": "กระเป๋า/กระเป๋าสตางค์",
            "location": "โรงอาหาร",
            "found_at": "03/09/2026 07:45",
            "description": "พบใต้โต๊ะใกล้ประตูทางออก มีบัตรนักเรียนอยู่ด้านใน",
            "reporter": "65003",
            "status": "นำส่งห้องปกครองแล้ว",
        },
        {
            "item": "เสื้อพละไซซ์ M",
            "category": "เสื้อผ้า",
            "location": "โดม",
            "found_at": "02/09/2026 16:20",
            "description": "เสื้อพละสีฟ้า ปักชื่อย่อที่หน้าอกด้านซ้าย",
            "reporter": "65001",
            "status": "นำส่งห้องปกครองแล้ว",
        },
        {
            "item": "ปากกาสไตลัส",
            "category": "อุปกรณ์การเรียน",
            "location": "อาคาร 3",
            "found_at": "02/09/2026 12:10",
            "description": "สีขาว พร้อมปลอกแม่เหล็กสีเทา",
            "reporter": "65002",
            "status": "นำส่งห้องปกครองแล้ว",
        },
    ]
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "student_id" not in st.session_state:
    st.session_state.student_id = ""
if "auth_email" not in st.session_state:
    st.session_state.auth_email = ""
if "auth_step" not in st.session_state:
    st.session_state.auth_step = "email"
if "otp_code" not in st.session_state:
    st.session_state.otp_code = ""
if "login_email" not in st.session_state:
    st.session_state.login_email = ""
if "login_otp" not in st.session_state:
    st.session_state.login_otp = ""
if "pending_link_email" not in st.session_state:
    st.session_state.pending_link_email = ""
if "pending_student_id" not in st.session_state:
    st.session_state.pending_student_id = ""
if "pending_class" not in st.session_state:
    st.session_state.pending_class = ""

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@400;500;600;700&family=Noto+Sans+Thai:wght@400;500;600;700&display=swap');
    :root { --orange:#FF9D00; --brown:#7B542F; --soft:#FFAD60; --ink:#222222; --cream:#FFF9F2; --white:#FFFFFF; --muted:#67594c; }
    * { box-sizing: border-box; }
    html, body, [class*="css"] { font-family: 'Noto Sans Thai', sans-serif; color: var(--ink); font-size: 15px; }
    html, body { margin: 0; padding: 0; background: var(--cream); }
    body { overscroll-behavior-y: none; }
    .stApp { background: linear-gradient(180deg, #f5efe7 0%, #fffaf3 100%); }
    .stApp::before, .stApp::after { content: ""; position: fixed; pointer-events: none; z-index: 0; opacity: .08; }
    .stApp::before { width: 28rem; height: 28rem; top: 8rem; left: -14rem; border: 4rem solid var(--orange); border-radius: 50%; transform: rotate(18deg); }
    .stApp::after { width: 20rem; height: 20rem; right: -8rem; bottom: 4rem; border: 3rem solid var(--soft); transform: rotate(32deg); clip-path: polygon(50% 0, 100% 50%, 50% 100%, 0 50%); }
    .main { width: 100%; }
    .main .block-container { position: relative; z-index: 1; max-width: 430px; width: 100%; margin: 0 auto; padding: 12px 12px 48px; }
    .block-container::after { content: ""; position: fixed; width: 16rem; height: 16rem; top: 42%; right: -7rem; pointer-events: none; z-index: -1; opacity: .06; background: var(--brown); transform: rotate(45deg); clip-path: polygon(50% 0, 100% 100%, 0 100%); }
    [data-testid="stAppViewContainer"] { overflow-x: hidden; }
    [data-testid="stHeader"] { background: transparent; }
    h1, h2, h3 { font-family: 'Kanit', sans-serif; letter-spacing: 0; }
    h1 { font-size: clamp(2rem, 8vw, 3.5rem); line-height: 1.05; }
    h2 { font-size: 1.5rem; }
    p { line-height: 1.6; }
    .mobile-shell { max-width: 430px; width: 100%; margin: 0 auto; }
    .brand { background: var(--brown); color: white; padding: 1.1rem 1.15rem; border-radius: 0 0 16px 16px; margin: -12px -12px 1rem; }
    .brand-kicker { color: var(--soft); font-size: .75rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
    .brand h1 { margin: .15rem 0 .35rem; }
    .brand p { margin: 0; color: #fff8ef; }
    .auth-card { background: var(--brown); color: var(--white); border-radius: 16px; padding: 1.1rem 1rem; margin-bottom: 1rem; }
    .auth-card .auth-header { font-family: 'Kanit', sans-serif; font-size: 1.2rem; font-weight: 600; color: var(--white); margin-bottom: .35rem; }
    .auth-card .auth-subtitle { color: #f7eedf; font-size: .84rem; }
    .nav-drawer { background: var(--brown); border-radius: 16px; padding: .7rem; margin: 0 0 1.2rem; }
    .nav-title { color: #fff8ef; font-family: Kanit, sans-serif; font-size: 1rem; padding: .3rem .6rem .65rem; }
    .nav-drawer div.stButton > button { background: transparent; color: white; text-align: left; border: 1px solid transparent; box-shadow: none; padding: .7rem .8rem; margin: .12rem 0; min-height: 44px; }
    .nav-drawer div.stButton > button:hover { background: rgba(255,255,255,.12); color: white; }
    .nav-drawer .active-nav div.stButton > button { background: var(--orange); color: var(--ink); }
    .nav-drawer .active-nav div.stButton > button:hover { background: var(--orange); color: var(--ink); }
    .nav-drawer .logout-nav > button { background: rgba(255,255,255,.12); color: white; border: 1px solid rgba(255,255,255,.2); }
    .modal-kicker { color: var(--brown); font-size: .8rem; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; }
    [data-testid="stDialog"] > div[role="dialog"] { animation: modal-rise .22s ease-out; border-radius: 16px; max-width: min(430px, calc(100vw - 16px)); width: min(430px, calc(100vw - 16px)); margin: 0 auto; }
    [data-testid="stDialog"] div[data-testid="stVerticalBlock"] { gap: .55rem; }
    @keyframes modal-rise { from { opacity: 0; transform: translateY(18px); } to { opacity: 1; transform: translateY(0); } }
    .profile { background: white; border: 1px solid #eadbc9; border-left: 5px solid var(--orange); padding: .8rem 1rem; border-radius: 12px; margin-bottom: 1.1rem; }
    .profile strong { display: block; font-family: Kanit, sans-serif; font-size: 1.05rem; }
    .profile-meta { color: #67594c; font-size: .85rem; display:flex; gap: .9rem; flex-wrap:wrap; }
    .score { color: var(--brown); font-weight: 700; }
    .profile-dashboard { display:grid; grid-template-columns: minmax(0, 1.45fr) minmax(170px, .85fr); gap: 1rem; margin: 1.2rem 0; }
    .score-card { background: var(--brown); color: white; border-radius: 16px; padding: 1.25rem; min-height: 16rem; display:flex; flex-direction:column; justify-content:space-between; }
    .score-heading { display:flex; justify-content:space-between; align-items:center; color:#fff8ef; font-size:.78rem; font-weight:700; letter-spacing:.08em; }
    .score-icon { color:var(--soft); font-size:1.35rem; }
    .score-number { font-family: Kanit, sans-serif; font-size:4.25rem; line-height:1; font-weight:600; margin:.6rem 0 .1rem; }
    .score-subtext { color:#fff8ef; font-size:.86rem; }
    .progress-labels { display:flex; justify-content:space-between; gap:.5rem; color:#fff8ef; font-size:.76rem; margin-top: .7rem; }
    .progress-track { background:rgba(255,255,255,.25); border-radius:99px; height:.55rem; overflow:hidden; margin-top:.35rem; }
    .progress-fill { background:var(--orange); height:100%; border-radius:inherit; }
    .target-copy { color:#fff8ef; font-size:.78rem; margin:.8rem 0 0; }
    .stat-stack { display:flex; flex-direction:column; gap:1rem; }
    .stat-card { background:white; border:1px solid #eadbc9; border-radius:16px; padding:1rem; flex:1; }
    .stat-card-label { color:#67594c; font-size:.8rem; }
    .stat-card-icon { color:var(--orange); font-size:1.3rem; float:right; }
    .stat-card-value { color:var(--brown); font-family:Kanit, sans-serif; font-size:1.65rem; font-weight:600; margin-top:.55rem; }
    .motivation-banner { background:var(--soft); border-radius:14px; padding:1rem 1.15rem; color:var(--ink); margin-bottom:1.2rem; }
    .motivation-banner strong { display:block; color:var(--brown); font-family:Kanit, sans-serif; font-size:1.15rem; }
    .motivation-banner p { font-size:.86rem; margin:.2rem 0 0; }
    .section-label { color: var(--brown); font-family: Kanit, sans-serif; font-size: 1.35rem; font-weight: 600; margin: 1.5rem 0 .55rem; }
    .hint { color:#67594c; font-size:.88rem; margin-top:-.35rem; }
    .feed-card { background: white; border: 1px solid #eadbc9; border-radius: 12px; padding: 1rem; margin: .75rem 0; box-shadow: 0 3px 12px rgba(123,84,47,.06); }
    .feed-card h3 { margin: 0; color: var(--ink); font-size: 1.15rem; }
    .tag { display:inline-block; background:#fff0df; color:var(--brown); font-size:.75rem; font-weight:600; padding:.2rem .5rem; border-radius:5px; margin:.45rem .35rem .45rem 0; }
    .feed-meta { color:#67594c; font-size:.83rem; }
    .status { color:#437343; font-weight:600; font-size:.82rem; margin-top:.65rem; }
    .threshold { background: #fff0df; border: 1px solid var(--soft); padding:.8rem 1rem; border-radius:10px; color:var(--brown); font-weight:600; margin: .8rem 0; }
    .instruction-card { background: #fff0df; border: 1px solid var(--soft); border-radius: 12px; color: var(--brown); font-weight: 600; padding: 1rem; margin-top: .8rem; }
    div.stButton > button, div[data-testid="stFormSubmitButton"] button { width:100%; min-height: 44px; border-radius:9px; font-weight:700; border:0; background:var(--orange); color:var(--ink); }
    div.stButton > button:hover, div[data-testid="stFormSubmitButton"] button:hover { background:#e88900; color:var(--ink); }
    div.stButton > button:focus, div[data-testid="stFormSubmitButton"] button:focus { outline: 2px solid rgba(123,84,47,.35); outline-offset: 2px; }
    div[role="listbox"], div[data-baseweb="menu"] { max-width: 100% !important; }
    div[role="option"], div[data-baseweb="menu"] li { min-height: 44px; font-size: 15px; }
    input, textarea, select, [data-baseweb="select"] > div { min-height: 44px; width: 100%; max-width: 100%; font-size: 16px; }
    [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea, [data-testid="stSelectbox"] div, [data-testid="stDateInput"] input, [data-testid="stTimeInput"] input { width: 100% !important; max-width: 100% !important; }
    .stAlert, .stWarning, .stSuccess, .stError, .stInfo { max-width: 100%; }
    .stMarkdownContainer, .stForm, .element-container, .stWidget { max-width: 100%; }
    @media (max-width: 639px) { .profile-dashboard { grid-template-columns: 1fr; } .score-card { min-height: 15rem; } }
    @media (min-width: 640px) { .main .block-container { padding-top: 16px; } .brand { margin-left:0; margin-right:0; border-radius:16px; } .stApp { padding: 0; } }
    @media (min-width: 768px) { .stApp { display: flex; justify-content: center; padding: 20px 0; } .mobile-shell { width: 100%; } }
    </style>
    """,
    unsafe_allow_html=True,
)


def show_login():
    st.markdown('<div class="brand"><div class="brand-kicker">Horwang Pathumthani School</div><h1>Lost & Found HWP</h1><p>พื้นที่กลางสำหรับของหายและของที่เก็บได้ในโรงเรียน</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">เข้าสู่ระบบด้วยอีเมลส่วนตัว</div>', unsafe_allow_html=True)
    st.caption("เข้าสู่ระบบด้วยอีเมลส่วนตัวและยืนยัน OTP เพื่อเชื่อมต่อกับข้อมูลนักเรียน")

    if st.session_state.auth_step == "otp" and st.session_state.auth_email:
        st.markdown(
            f'<div class="auth-card"><div class="auth-header">ยืนยันตัวตน / Identity Verify</div><div class="auth-subtitle">ส่งรหัส OTP ไปยัง {st.session_state.auth_email}</div></div>',
            unsafe_allow_html=True,
        )
        st.info(f"รหัส OTP ชั่วคราว: {st.session_state.otp_code} (สำหรับการทดสอบในเครื่องนี้)")

    if st.session_state.auth_step == "profile_link":
        st.markdown(
            '<div class="instruction-card">อีเมลของคุณยังไม่ได้เชื่อมกับข้อมูลนักเรียน กรุณากรอกรหัสนักเรียนและชั้นเรียนเพื่อเริ่มใช้งาน</div>',
            unsafe_allow_html=True,
        )

    with st.form("login_form"):
        if st.session_state.auth_step == "email":
            email = st.text_input(
                "อีเมลส่วนตัว / Personal Email",
                placeholder="เช่น student1@gmail.com",
                max_chars=80,
                key="login_email",
            )
            submitted = st.form_submit_button("ส่งรหัส OTP / Send OTP", use_container_width=True)
        elif st.session_state.auth_step == "otp":
            st.text_input(
                "อีเมลที่ลงทะเบียน",
                value=st.session_state.auth_email,
                disabled=True,
                key="registered_email_display",
            )
            otp_input = st.text_input(
                "OTP 6 หลัก / Verification Code",
                placeholder="กรอก 6 หลัก",
                max_chars=6,
                key="login_otp",
            )
            submitted = st.form_submit_button("ยืนยันตัวตน / Verify", use_container_width=True)
        else:
            st.text_input(
                "อีเมลที่เชื่อมต่อ",
                value=st.session_state.auth_email,
                disabled=True,
                key="link_email_display",
            )
            student_id = st.text_input(
                "รหัสนักเรียน / Student ID",
                placeholder="เช่น 65001",
                max_chars=10,
                key="pending_student_id",
            )
            student_class = st.selectbox(
                "ชั้นเรียน / Class",
                options=["เลือกชั้นเรียน / Select Class", *CLASS_OPTIONS],
                index=0,
                key="pending_class",
            )
            submitted = st.form_submit_button("เชื่อมข้อมูลนักเรียน / Link profile", use_container_width=True)

    if submitted:
        if st.session_state.auth_step == "email":
            email = st.session_state.login_email.strip()
            if not is_valid_email(email):
                st.error("อีเมลไม่ถูกต้อง กรุณากรอกอีเมลที่ถูกต้อง เช่น student1@gmail.com")
                return
            st.session_state.auth_email = email.lower()
            st.session_state.auth_step = "otp"
            st.session_state.otp_code = generate_otp()
            st.success("ส่งรหัสยืนยันไปแล้ว กรุณากรอกรหัส OTP ด้านล่าง")
            st.rerun()
        elif st.session_state.auth_step == "otp":
            entered_otp = st.session_state.login_otp.strip()
            if entered_otp != st.session_state.otp_code:
                st.error("รหัส OTP ไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง")
                return
            student_id = find_student_by_email(st.session_state.auth_email)
            if student_id is None:
                st.session_state.auth_step = "profile_link"
                st.session_state.pending_link_email = st.session_state.auth_email
                st.success("ยืนยันอีเมลสำเร็จ กรุณาเชื่อมต่อข้อมูลนักเรียนก่อนใช้งาน")
                st.rerun()
                return
            st.session_state.logged_in = True
            st.session_state.student_id = student_id
            st.session_state.active_page = "find"
            st.session_state.find_open = True
            st.session_state.auth_step = "email"
            st.session_state.otp_code = ""
            st.session_state.login_otp = ""
            st.rerun()
        else:
            student_id = st.session_state.pending_student_id.strip()
            student_class = st.session_state.pending_class
            if not student_id or not student_class or student_class == "เลือกชั้นเรียน / Select Class":
                st.error("กรุณากรอกรหัสนักเรียนและเลือกชั้นเรียนให้ครบถ้วน")
                return
            if student_id not in STUDENTS:
                st.error("รหัสนักเรียนไม่ถูกต้อง กรุณาตรวจสอบอีกครั้ง")
                return
            student = STUDENTS[student_id]
            student["email"] = st.session_state.auth_email.lower()
            student["class"] = student_class
            st.session_state.logged_in = True
            st.session_state.student_id = student_id
            st.session_state.active_page = "find"
            st.session_state.find_open = True
            st.session_state.auth_step = "email"
            st.session_state.otp_code = ""
            st.session_state.login_otp = ""
            st.rerun()


def show_profile(student_id):
    student = STUDENTS[student_id]
    returned = sum(report["reporter"] == student_id for report in st.session_state.reports)
    st.markdown('<div class="brand"><div class="brand-kicker">Lost & Found HWP</div><h1>ของหาย ได้คืน</h1><p>ช่วยกันดูแลของทุกชิ้นในรั้วโรงเรียน</p></div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="profile"><strong>{student["name"]}</strong><div class="profile-meta"><span>อีเมล: {student["email"]}</span><span>รหัสนักเรียน: {student_id}</span><span>ชั้น: {student["class"]}</span><span class="score">คะแนนพฤติกรรม: {min(student["score"], 100)} / 100</span></div></div>',
        unsafe_allow_html=True,
    )
    if 5 <= returned <= 7:
        st.markdown('<div class="threshold">ผ่านเกณฑ์เสนอขอเพิ่มคะแนนพฤติกรรม</div>', unsafe_allow_html=True)
    st.caption(f"คุณช่วยนำส่งของแล้ว {returned} รายการ")


def report_form(student_id):
    """Render the report workflow inside a touch-friendly modal dialog."""
    st.markdown('<div class="modal-kicker">Report found</div>', unsafe_allow_html=True)
    st.subheader("แจ้งของที่พบ / Report found")
    _, close_col = st.columns([4, 1])
    with close_col:
        if st.button("× ปิด", key="close_report"):
            st.rerun()
    st.markdown('<div class="hint">กรอกข้อมูลให้ครบถ้วน เพื่อให้เจ้าของตามหาได้ง่ายขึ้น</div>', unsafe_allow_html=True)
    with st.form("report_modal_form", clear_on_submit=True):
        item = st.text_input("ชื่อสิ่งของ *", placeholder="เช่น กระเป๋าสตางค์สีดำ")
        category = st.selectbox("หมวดหมู่ *", CATEGORIES)
        location = st.selectbox("สถานที่พบ *", LOCATIONS[1:])
        found_date = st.date_input("วันที่พบ *", value=datetime.now().date(), format="DD/MM/YYYY")
        found_time = st.time_input("เวลาที่พบ *", value=datetime.now().replace(second=0, microsecond=0).time(), step=300, format="24h")
        description = st.text_area("รายละเอียดเพิ่มเติม", placeholder="สี ลักษณะ จุดสังเกต หรือข้อมูลที่ช่วยยืนยันเจ้าของ", height=100)
        submitted = st.form_submit_button("บันทึกการแจ้งเก็บของ", use_container_width=True)
    if submitted:
        if not item.strip():
            st.error("กรุณาระบุชื่อสิ่งของ")
            return
        st.session_state.reports.insert(0, {"item": item.strip(), "category": category, "location": location, "found_at": f"{found_date.strftime('%d/%m/%Y')} {found_time.strftime('%H:%M')}", "description": description.strip() or "ไม่มีรายละเอียดเพิ่มเติม", "reporter": student_id, "status": "นำส่งห้องปกครองแล้ว"})
        st.success("บันทึกเรียบร้อย ขอบคุณที่ช่วยดูแลของในโรงเรียน")
        st.rerun()


@st.dialog("แจ้งของที่พบ / Report found")
def report_dialog(student_id):
    report_form(student_id)


@st.dialog("ตามหาของหาย / Find an item")
def find_dialog():
    st.markdown('<div class="modal-kicker">Find an item</div>', unsafe_allow_html=True)
    st.subheader("ตามหาของหาย / Find an item")
    _, close_col = st.columns([4, 1])
    with close_col:
        if st.button("× ปิด", key="close_find"):
            st.session_state.find_open = False
            st.rerun()
    with st.form("find_modal_form"):
        filter_col1, filter_col2 = st.columns(2)
        with filter_col1:
            location_filter = st.selectbox("สถานที่ / Location", ["เลือกสถานที่"] + LOCATIONS[1:])
        with filter_col2:
            category_filter = st.selectbox("ประเภท / Category", ["เลือกประเภท"] + FIND_CATEGORIES)
        search = st.text_input("คำค้นหา / Keyword", placeholder="ค้นหาชื่อสิ่งของหรือรายละเอียด")
        submitted = st.form_submit_button("ค้นหา / Search", use_container_width=True)
    if not submitted:
        st.markdown('<div class="instruction-card">กรุณาเลือกสถานที่และประเภทสิ่งของที่ต้องการค้นหา<br><small>Please select a location and item category to search.</small></div>', unsafe_allow_html=True)
        return
    if location_filter == "เลือกสถานที่" or category_filter == "เลือกประเภท":
        st.warning("กรุณาเลือกสถานที่และประเภทก่อนค้นหา")
        return
    query = search.strip().lower()
    matches = [report for report in st.session_state.reports if (not query or query in f"{report['item']} {report['description']}".lower()) and report["location"] == location_filter and report["category"] == category_filter]
    if not matches:
        st.info("ไม่พบสิ่งของในสถานที่และประเภทที่คุณเลือก")
        return
    for report in matches:
        st.markdown(f'<article class="feed-card"><h3>{report["item"]}</h3><span class="tag">{report["category"]}</span><span class="tag">{report["location"]}</span><div class="feed-meta">พบเมื่อ {report["found_at"]}</div><p>{report["description"]}</p><div class="status">● {report["status"]}</div></article>', unsafe_allow_html=True)


def navigation(student_id):
    if "active_page" not in st.session_state:
        st.session_state.active_page = "find"
    if "find_open" not in st.session_state:
        st.session_state.find_open = True
    st.markdown('<div class="nav-drawer"><div class="nav-title">เมนูหลัก / Main menu</div>', unsafe_allow_html=True)
    nav_items = [
        ("report", "＋  แจ้งของที่พบ / Report found", ""),
        ("find", "🔍  ตามหาของหาย / Find an item", ""),
        ("activity", "🎖️  ประวัติผู้ใช้ / User Profile", ""),
    ]
    for page, label, indicator in nav_items:
        wrapper = "active-nav" if st.session_state.active_page == page else ""
        st.markdown(f'<div class="{wrapper}">', unsafe_allow_html=True)
        if st.button(f"{label} {indicator}", key=f"nav_{page}", use_container_width=True):
            st.session_state.active_page = page
            if page == "report":
                report_dialog(student_id)
            elif page == "find":
                st.session_state.find_open = True
                st.rerun()
            elif page == "activity":
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="logout-nav">', unsafe_allow_html=True)
    if st.button("ออกจากระบบ / Logout", key="nav_logout", use_container_width=True):
        logout_user()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def profile_dashboard(student_id):
    student = STUDENTS[student_id]
    mine = [report for report in st.session_state.reports if report["reporter"] == student_id]
    returned = len(mine)
    progress = min(returned / 5, 1)
    remaining = max(5 - returned, 0)
    target_copy = "ผ่านเกณฑ์เสนอขอเพิ่มคะแนนพฤติกรรม" if 5 <= returned <= 7 else f"อีก {remaining} ครั้ง จะผ่านเกณฑ์เสนอขอเพิ่มคะแนนพฤติกรรม"
    st.markdown('<div class="section-label">ประวัติผู้ใช้ / User Profile</div>', unsafe_allow_html=True)
    if st.button("ออกจากระบบ / Logout", key="profile_logout", use_container_width=True):
        logout_user()
    st.markdown(
        f'''<div class="profile-dashboard">
        <section class="score-card"><div><div class="score-heading"><span>BEHAVIOR SCORE</span><span class="score-icon">✦</span></div><div class="score-number">{min(student["score"], 100)}</div><div class="score-subtext">คะแนนพฤติกรรม: {min(student["score"], 100)} / 100</div></div><div><div class="progress-labels"><span>ส่งคืนของแล้ว {returned} ครั้ง</span><span>เป้าหมาย 5 ครั้ง</span></div><div class="progress-track"><div class="progress-fill" style="width:{progress * 100:.0f}%"></div></div><div class="target-copy">{target_copy}</div></div></section>
        <div class="stat-stack"><section class="stat-card"><span class="stat-card-icon">↗</span><div class="stat-card-label">รายการที่ส่งต่อ</div><div class="stat-card-value">{returned} รายการ</div></section><section class="stat-card"><span class="stat-card-icon">✓</span><div class="stat-card-label">สถานะเริ่มต้น</div><div class="stat-card-value">Sent</div><div class="feed-meta">นำส่งห้องปกครองแล้ว</div></section></div>
        </div>
        <div class="motivation-banner"><strong>คุณกำลังสร้างความเปลี่ยนแปลง</strong><p>ทุกครั้งที่แจ้งของที่พบ คุณจะได้รับ 10 คะแนนพฤติกรรม และช่วยให้เจ้าของได้ของคืนเร็วขึ้น</p></div>''',
        unsafe_allow_html=True,
    )
    if not mine:
        st.info("ยังไม่มีกิจกรรมของคุณ")
    for report in mine:
        st.markdown(f'<article class="feed-card"><h3>{report["item"]}</h3><div class="feed-meta">{report["location"]} · {report["found_at"]}</div><div class="status">● {report["status"]}</div></article>', unsafe_allow_html=True)


st.markdown('<div class="mobile-shell">', unsafe_allow_html=True)
if not st.session_state.logged_in:
    show_login()
else:
    show_profile(st.session_state.student_id)
    navigation(st.session_state.student_id)
    if st.session_state.active_page == "find" and st.session_state.find_open:
        find_dialog()
    elif st.session_state.active_page == "activity":
        profile_dashboard(st.session_state.student_id)
st.markdown('</div>', unsafe_allow_html=True)

