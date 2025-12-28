import streamlit as st
import random
from datetime import datetime, date

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="صحصح يا نشمي 🇯🇴",
    page_icon="🇯🇴",
    layout="wide"
)

# ==================================================
# GLOBAL STYLE (COLORS + UI)
# ==================================================
st.markdown("""
<style>
body {
    background-color: #F7F5F2;
}
.stButton>button {
    width: 100%;
    border-radius: 20px;
    background-color: #CE1126;
    color: white;
    font-weight: bold;
    font-size: 16px;
}
.card {
    background-color: white;
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
.title {
    text-align:center;
    color:#0B6E4F;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# SESSION STATE (MEMORY)
# ==================================================
if "profile" not in st.session_state:
    st.session_state.profile = {
        "name": "نشمي",
        "streak": 0,
        "last_visit": None,
        "level": "نشمي مبتدئ"
    }

# ==================================================
# HELPER FUNCTIONS
# ==================================================
def update_streak():
    today = date.today()
    last = st.session_state.profile["last_visit"]

    if last is None:
        st.session_state.profile["streak"] = 1
    else:
        diff = (today - last).days
        if diff == 1:
            st.session_state.profile["streak"] += 1
        elif diff > 1:
            st.session_state.profile["streak"] = 1

    st.session_state.profile["last_visit"] = today


def get_level(streak):
    if streak >= 10:
        return "نشمي أسطورة 💪"
    elif streak >= 5:
        return "نشمي متوازن 👌"
    else:
        return "نشمي على الطريق"


def choose_personality(water, sleep):
    if water < 4 and sleep < 5:
        return "sarcastic"
    elif water >= 8 and sleep >= 7:
        return "supportive"
    else:
        return "normal"


def personality_message(mode):
    messages = {
        "sarcastic": [
            "واضح الجسم عطشان والنوم زعلان 😏",
            "هيك بدنا نصير؟ كاسة مي مش غلط 💧"
        ],
        "supportive": [
            "كفو! جسمك مبسوط منك 👏",
            "هيك النشامى الصح 💪"
        ],
        "normal": [
            "أمورك ماشية، بس في مجال نتحسن 👌"
        ]
    }
    return random.choice(messages[mode])


def daily_surprise():
    return random.choice([
        "👵 وصفة ستّي: بابونج ونام بكير",
        "🔥 تحدي اليوم: اعمل 10 ضغط",
        "💧 اشرب كاسة مي هسا",
        "😏 نصيحة صريحة: صحتك أهم من كل شي"
    ])


def honest_feedback(water, sleep):
    if water < 5:
        return "الصراحة؟ جسمك ناشف اليوم 💧"
    if sleep < 6:
        return "واضح إنك محتاج نوم 😴"
    return "أمورك ممتازة، كمل هيك 👌"


def predict_energy(water, sleep):
    score = water * 6 + sleep * 10
    return min(score, 100)

# ==================================================
# HEADER
# ==================================================
st.markdown("<h1 class='title'>🇯🇴 صحصح يا نشمي</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;'>رفيقك الصحي اليومي.. بحكي معك وبتذكّرك بنفسك</p>",
    unsafe_allow_html=True
)

st.divider()

# ==================================================
# SIDEBAR (USER INPUT)
# ==================================================
with st.sidebar:
    st.header("👤 ملفك")

    name = st.text_input("اسمك", st.session_state.profile["name"])
    water = st.slider("كم كاسة مي شربت؟ 💧", 0, 15, 5)
    sleep = st.slider("كم ساعة نمت؟ 😴", 0, 12, 7)

    st.session_state.profile["name"] = name

# ==================================================
# UPDATE MEMORY
# ==================================================
update_streak()
st.session_state.profile["level"] = get_level(st.session_state.profile["streak"])

# ==================================================
# MAIN CONTENT
# ==================================================
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader(f"👋 أهلاً {name}")

    st.write(f"🏆 مستواك: **{st.session_state.profile['level']}**")
    st.write(f"🔥 أيام متتالية: **{st.session_state.profile['streak']}**")

    personality = choose_personality(water, sleep)
    st.info(personality_message(personality))

    st.markdown("---")
    st.subheader("🎁 مفاجأة اليوم")
    st.success(daily_surprise())
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🗣️ بدك الصراحة؟")
    if st.button("احكيلي الصراحة"):
        st.warning(honest_feedback(water, sleep))
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⚡ طاقتك اليوم")

    energy = predict_energy(water, sleep)
    st.metric("Energy Level", f"{energy}%")

    st.progress(energy / 100)

    st.markdown("---")
    st.subheader("⏱️ تحدي سريع")
    if st.button("🔥 أعطيني تحدي"):
        st.info(random.choice([
            "قوم تمشى دقيقتين 🚶",
            "اشرب مي دفعة وحدة 💧",
            "افرد ظهرك وعدل جلستك 🧍"
        ]))
    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# FOOTER
# ==================================================
st.divider()
st.markdown(
    "<p style='text-align:center;'>دير بالك على صحتك.. النشمي القوي بعرف يهتم بحاله 🇯🇴</p>",
    unsafe_allow_html=True
)
