import streamlit as st
import sqlite3
import pandas as pd
import random
import time
import hashlib
from datetime import datetime, date, timedelta

# ==============================================================================
# 1. SETUP & CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="صحصح يا نشمي | التطبيق الرسمي",
    page_icon="🇯🇴",
    layout="wide",
    initial_sidebar_state="collapsed" # نبدأ مغلقين للتركيز على الدخول
)

# ==============================================================================
# 2. DATABASE MANAGEMENT (The Backend)
# ==============================================================================
# لضمان أن التطبيق "Production Ready"، نستخدم SQLite
# هذه الدوال تدير الاتصال وقراءة/كتابة البيانات

def init_db():
    """إنشاء الجداول إذا لم تكن موجودة"""
    conn = sqlite3.connect('nashmi.db')
    c = conn.cursor()
    
    # جدول المستخدمين
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT, join_date TEXT)''')
    
    # جدول السجلات اليومية
    c.execute('''CREATE TABLE IF NOT EXISTS daily_logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  username TEXT, date TEXT, water INTEGER, sleep INTEGER, 
                  steps INTEGER, mood TEXT, xp_gained INTEGER)''')
    
    # جدول تقدم المستخدم (Gamification)
    c.execute('''CREATE TABLE IF NOT EXISTS user_stats
                 (username TEXT PRIMARY KEY, total_xp INTEGER, level TEXT, streak INTEGER, last_active TEXT)''')
    
    conn.commit()
    conn.close()

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

def add_user(username, password):
    conn = sqlite3.connect('nashmi.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username =?', (username,))
    if c.fetchone():
        conn.close()
        return False # User exists
    
    c.execute('INSERT INTO users(username, password, join_date) VALUES (?,?,?)', 
              (username, make_hashes(password), str(date.today())))
    c.execute('INSERT INTO user_stats(username, total_xp, level, streak, last_active) VALUES (?,?,?,?,?)', 
              (username, 0, "نشمي مبتدئ 👶", 0, str(date.today())))
    conn.commit()
    conn.close()
    return True

def login_user(username, password):
    conn = sqlite3.connect('nashmi.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username =? AND password =?', (username, make_hashes(password)))
    data = c.fetchall()
    conn.close()
    return data

def save_log(username, water, sleep, steps, mood, xp):
    conn = sqlite3.connect('nashmi.db')
    c = conn.cursor()
    today = str(date.today())
    
    # Check if already logged today
    c.execute('SELECT * FROM daily_logs WHERE username =? AND date =?', (username, today))
    if c.fetchone():
        conn.close()
        return False # Already logged
        
    c.execute('INSERT INTO daily_logs(username, date, water, sleep, steps, mood, xp_gained) VALUES (?,?,?,?,?,?,?)',
              (username, today, water, sleep, steps, mood, xp))
    
    # Update Stats
    c.execute('SELECT total_xp, streak, last_active FROM user_stats WHERE username=?', (username,))
    stats = c.fetchone()
    current_xp = stats[0] + xp
    last_active = datetime.strptime(stats[2], "%Y-%m-%d").date()
    current_streak = stats[1]
    
    # Streak Logic
    if last_active == date.today() - timedelta(days=1):
        current_streak += 1
    elif last_active < date.today() - timedelta(days=1):
        current_streak = 1 # Reset if missed a day
        
    # Level Logic
    new_level = get_level_title(current_xp)
    
    c.execute('UPDATE user_stats SET total_xp=?, level=?, streak=?, last_active=? WHERE username=?', 
              (current_xp, new_level, current_streak, today, username))
    
    conn.commit()
    conn.close()
    return True

def get_user_data(username):
    conn = sqlite3.connect('nashmi.db')
    c = conn.cursor()
    c.execute('SELECT * FROM user_stats WHERE username=?', (username,))
    stats = c.fetchone()
    
    c.execute('SELECT water, sleep FROM daily_logs WHERE username=? ORDER BY date DESC LIMIT 7', (username,))
    logs = c.fetchall()
    conn.close()
    return stats, logs

def get_leaderboard():
    conn = sqlite3.connect('nashmi.db')
    df = pd.read_sql_query("SELECT username, total_xp, level, streak FROM user_stats ORDER BY total_xp DESC LIMIT 5", conn)
    conn.close()
    return df

# ==============================================================================
# 3. HELPER FUNCTIONS & CONTENT
# ==============================================================================

def get_level_title(xp):
    if xp >= 1000: return "نشمي أسطورة 👑"
    if xp >= 600: return "نشمي محترف 🔥"
    if xp >= 300: return "نشمي متوازن ⚖️"
    if xp >= 100: return "نشمي نشيط 🏃‍♂️"
    return "نشمي مبتدئ 👶"

def get_personality_msg(water, sleep):
    if water < 4 or sleep < 5:
        return "random_scold", "وضعك ما بيبشر.. الجسم ناشف والنوم قليل! 🌵"
    elif water >= 8 and sleep >= 7:
        return "random_praise", "يا هيك النشاط يا بلاش! استمر 💪"
    else:
        return "random_neutral", "بداية جيدة، بس لسا في مجال للتحسن 👌"

# تهيئة قاعدة البيانات عند بدء التشغيل
init_db()

# ==============================================================================
# 4. CUSTOM CSS (PRODUCTION UI)
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;500;800&display=swap');

body, .stApp {
    background-color: #F8F9FA;
    font-family: 'Tajawal', sans-serif !important;
}

/* Hide Streamlit Branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Custom Cards */
.css-card {
    background: #FFFFFF;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    margin-bottom: 15px;
    border: 1px solid #EAEAEA;
}

/* Metric Boxes */
.metric-box {
    text-align: center;
    padding: 10px;
    background: linear-gradient(45deg, #0B6E4F, #2ecc71);
    color: white;
    border-radius: 12px;
}

/* Custom Input Fields */
div[data-baseweb="input"] > div {
    border-radius: 10px;
    background-color: #FFFFFF;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 50px;
    font-weight: bold;
    background-color: #CE1126;
    color: white;
    border: none;
}
.stButton > button:hover {
    background-color: #a80e1f;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 5. APPLICATION FLOW
# ==============================================================================

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ''

# --- AUTHENTICATION PAGE ---
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<div style='text-align: center; margin-top: 50px;'>", unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/2620/2620499.png", width=100)
        st.title("صحصح يا نشمي 🇯🇴")
        st.write("سجل دخولك عشان نحفظ تقدمك وما يضيع تعبك")
        st.markdown("</div>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["تسجيل دخول", "حساب جديد"])
        
        with tab1:
            username = st.text_input("اسم المستخدم")
            password = st.text_input("كلمة السر", type='password')
            if st.button("دخول"):
                if login_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("اسم المستخدم أو كلمة السر غلط")

        with tab2:
            new_user = st.text_input("اختر اسم مستخدم")
            new_pass = st.text_input("اختر كلمة سر", type='password')
            if st.button("إنشاء حساب"):
                if add_user(new_user, new_pass):
                    st.success("تم إنشاء الحساب! هلا بيك.. سجل دخولك هسا")
                else:
                    st.warning("اسم المستخدم هذا محجوز لواحد ثاني")

# --- MAIN DASHBOARD (AFTER LOGIN) ---
else:
    # Fetch Data
    stats, logs = get_user_data(st.session_state.username)
    current_xp = stats[1]
    level_title = stats[2]
    streak = stats[3]
    
    # Sidebar
    with st.sidebar:
        st.title(f"هلا, {st.session_state.username}")
        st.write(f"Level: **{level_title}**")
        st.progress(min((current_xp % 1000) / 1000, 1.0))
        st.write(f"مجموع النقاط: {current_xp}")
        
        st.markdown("---")
        if st.button("تسجيل خروج"):
            st.session_state.logged_in = False
            st.rerun()

    # Main Area
    st.markdown(f"## ☀️ لوحة التحكم اليومية")
    
    col_main, col_stats = st.columns([2, 1])
    
    with col_main:
        # 1. Daily Input Section
        st.markdown("<div class='css-card'>", unsafe_allow_html=True)
        st.subheader("📝 سجل يومك")
        
        with st.form("daily_form"):
            c1, c2 = st.columns(2)
            water = c1.slider("💧 كاسات مي", 0, 15, 5)
            sleep = c2.slider("😴 ساعات نوم", 0, 12, 7)
            steps = st.number_input("👣 خطوات اليوم", 0, 30000, 3000, step=500)
            mood = st.select_slider("كيف النفسية؟", ["تعبان", "ماشي الحال", "ممتازة"])
            
            submit = st.form_submit_button("اعتمد اليوم ✅")
            
            if submit:
                # Calculate XP
                xp_gain = 10 + (20 if water>=8 else 0) + (20 if sleep>=7 else 0) + (10 if steps>5000 else 0)
                
                if save_log(st.session_state.username, water, sleep, steps, mood, xp_gain):
                    st.balloons()
                    st.success(f"كفو! تم الحفظ وكسبت {xp_gain} نقطة")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.warning("سبق وسجلت دخولك لليوم.. ارجع بكرة يا بطل!")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 2. Charts
        if logs:
            st.markdown("<div class='css-card'>", unsafe_allow_html=True)
            st.subheader("📈 أدائك آخر أسبوع")
            chart_data = pd.DataFrame(logs, columns=['Water', 'Sleep'])
            st.area_chart(chart_data)
            st.markdown("</div>", unsafe_allow_html=True)

    with col_stats:
        # 1. Leaderboard (Social/Gamification)
        st.markdown("<div class='css-card'>", unsafe_allow_html=True)
        st.subheader("🏆 كبارية البلد (المتصدرين)")
        leaderboard = get_leaderboard()
        for index, row in leaderboard.iterrows():
            st.write(f"**{index+1}. {row['username']}** - {row['level']}")
            st.caption(f"XP: {row['total_xp']} | Streak: {row['streak']}🔥")
            st.markdown("---")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 2. Daily Tip
        st.info("💡 نصيحة: الجو بالأردن بقلب فجأة، لا تطلع خفيف بالليل حتى لو الصبح شوب!")

    # Footer Logic
    st.markdown("<br><hr><center style='color:gray'>صحصح يا نشمي v3.0 | Production Release</center>", unsafe_allow_html=True)
