import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
from datetime import datetime

# --- إعدادات الصفحة المتقدمة ---
st.set_page_config(
    page_title="الموسوعة الذكية للمعلوماتية الصحية",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- نظام التصميم (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; }
    .main-header { background: linear-gradient(90deg, #073b4c, #118ab2); padding: 20px; border-radius: 15px; color: white; text-align: center; margin-bottom: 25px; }
    .info-card { background-color: #f8f9fa; border-right: 5px solid #06d6a0; padding: 20px; border-radius: 10px; margin: 10px 0; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .ai-box { background-color: #000; color: #39ff14; padding: 15px; border-radius: 10px; font-family: 'Courier New', monospace; border: 1px solid #39ff14; }
    .stProgress > div > div > div > div { background-color: #06d6a0; }
    </style>
    """, unsafe_allow_html=True)

# --- القائمة الجانبية للتنقل ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3304/3304567.png", width=100)
    st.title("البوابة الصحية الذكية")
    menu = st.radio(
        "انتقل بين المحطات:",
        ["🏠 الشاشة الرئيسية", "📊 مختبر البيانات (Data Lab)", "🤖 مدرسة الـ AI الطبي", "🏥 السجلات الإلكترونية (EHR)", "🔮 مستقبل الطب", "🏁 اختبر معلوماتك"]
    )
    st.divider()
    st.info("💡 **نصيحة نشمي:** المعلوماتية الصحية مش بس تكنولوجيا، هي " + "أمانة ومسؤولية للحفاظ على أرواح الناس.")

# --- المحطة 1: الشاشة الرئيسية ---
if menu == "🏠 الشاشة الرئيسية":
    st.markdown("<div class='main-header'><h1>المركز الأردني لعلوم المعلوماتية الصحية والذكاء الاصطناعي</h1></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("مرحباً بك يا نشمي في رحلة المستقبل!")
        st.write("""
        هاد التطبيق هو دليلك الشامل عشان تفهم كيف بنحول "الأرقام والبيانات" لـ "أرواح بتتعافى". 
        المعلوماتية الصحية (Health Informatics) هي المحرك اللي بخلي المستشفيات تشتغل بذكاء مش بس بجهد.
        """)
        st.image("https://images.unsplash.com/photo-1576091160550-2173dba999ef?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80", use_container_width=True)
    
    with col2:
        st.markdown("### 🧬 ركائز التخصص")
        st.success("1. النظم الخبيرة")
        st.success("2. تحليل البيانات الضخمة")
        st.success("3. أمن المعلومات الطبية")
        st.success("4. واجهات التفاعل البشرية")
        st.metric(label="دقة التشخيص بالـ AI", value="94%", delta="12% زيادة")

# --- المحطة 2: مختبر البيانات ---
elif menu == "📊 مختبر البيانات (Data Lab)":
    st.title("🧪 مختبر معالجة البيانات الصحية")
    st.write("تعال نشوف كيف الـ Data بتفرق معانا بالتشخيص.")
    
    # محاكاة لبيانات ضغط الدم
    st.subheader("محاكي بيانات المرضى (Real-time Stream)")
    data_points = st.slider("حدد حجم العينة لتحليلها:", 50, 500, 100)
    
    import numpy as np
    chart_data = pd.DataFrame({
        'نبض القلب': np.random.normal(75, 10, data_points),
        'مستوى السكر': np.random.normal(120, 20, data_points),
        'العمر': np.random.randint(20, 80, data_points)
    })
    
    fig = px.scatter(chart_data, x="نبض القلب", y="مستوى السكر", color="العمر", 
                     title="العلاقة بين النبض والسكر حسب الفئة العمرية",
                     color_continuous_scale=px.colors.sequential.Viridis)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<div class='info-card'><b>تحليل المحقق:</b> لما نربط هاي البيانات ببعض، بنقدر نتوقع 'الجلطات' قبل ما تصير بـ 48 ساعة! هاد هو جوهر الهيلث انفورماتكس.</div>", unsafe_allow_html=True)

# --- المحطة 3: مدرسة الـ AI الطبي ---
elif menu == "🤖 مدرسة الـ AI الطبي":
    st.title("🧠 كيف بيفكر الذكاء الاصطناعي في المستشفى؟")
    
    st.write("الـ AI مش سحر، هو عبارة عن خوارزميات بتتعلم من الماضي.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("1. الرؤية الحاسوبية (Computer Vision)")
        st.write("القدرة على تحليل صور الأشعة بدقة خرافية.")
        if st.button("شغل محاكي الأشعة"):
            bar = st.progress(0)
            for i in range(101):
                time.sleep(0.01)
                bar.progress(i)
            st.image("https://upload.wikimedia.org/wikipedia/commons/b/b2/Normal_posteroanterior_chest_X-ray.jpg", width=300)
            st.code("RESULT: NORMAL - Accuracy: 99.2%", language="python")

    with col_b:
        st.subheader("2. معالجة اللغات (NLP)")
        st.write("كيف الجهاز بفهم كلام الدكتور المكتوب بخط إيد مش مفهوم!")
        text_input = st.text_area("انسخ ملاحظات طبية هنا:", "Patient suffers from acute headaches and mild fever...")
        if st.button("تحليل النص"):
            st.write("🔍 **الكلمات المفتاحية المستخرجة:** الصداع، الحرارة.")
            st.write("🎯 **التصنيف:** حالة التهابية.")

# --- المحطة 4: السجلات الإلكترونية (EHR) ---
elif menu == "🏥 السجلات الإلكترونية (EHR)":
    st.title("📂 نظام السجلات الصحية الموحد")
    
    st.markdown("""
    في الأردن، عنا نظام 'حكيم'. الهيلث انفورماتكس هي اللي بتخلي ملفك الطبي متاح في عمان وإربد والعقبة بنفس اللحظة.
    """)
    
    with st.expander("🔐 أمن البيانات (Blockchain in Health)"):
        st.write("البيانات مشفرة ومحمية بسلاسل الكتل لضمان عدم التلاعب.")
        st.json({"block_id": 1024, "hash": "8f3e2...9a", "status": "Secure"})

    # تجربة إضافة مريض
    with st.form("Patient Entry"):
        st.subheader("إضافة مريض جديد للنظام")
        p_name = st.text_input("اسم المريض")
        p_blood = st.selectbox("زمرة الدم", ["A+", "B+", "O+", "AB+", "A-", "B-", "O-", "AB-"])
        p_history = st.multiselect("تاريخ أمراض", ["سكري", "ضغط", "حساسية بنسلين", "ربو"])
        if st.form_submit_button("حفظ في قاعدة البيانات"):
            st.success(f"تم تسجيل {p_name} بنجاح وتوزيع البيانات على الشبكة.")

# --- المحطة 5: مستقبل الطب ---
elif menu == "🔮 مستقبل الطب":
    st.title("🚀 لوين رايحين؟")
    
    feat_col1, feat_col2, feat_col3 = st.columns(3)
    
    with feat_col1:
        st.markdown("### الجراحة عن بُعد")
        st.write("طبيب في أمريكا بجري عملية لمريض بالمدينة الطبية عن طريق الروبوت.")
        st.image("https://cdn-icons-png.flaticon.com/512/387/387561.png", width=100)
        
    with feat_col2:
        st.markdown("### النانو تكنولوجي")
        st.write("روبوتات مجهرية بتدخل بالدم وبتحارب الخلايا السرطانية حبة حبة.")
        st.image("https://cdn-icons-png.flaticon.com/512/2540/2540413.png", width=100)
        
    with feat_col3:
        st.markdown("### الطباعة ثلاثية الأبعاد")
        st.write("طباعة أعضاء بشرية (قلب، كلية) باستخدام خلايا المريض نفسه.")
        st.image("https://cdn-icons-png.flaticon.com/512/2833/2833315.png", width=100)

# --- المحطة 6: الاختبار ---
elif menu == "🏁 اختبر معلوماتك":
    st.title("📝 تحدي النشامى في المعلوماتية")
    st.write("خلينا نشوف شو تعلمت اليوم!")
    
    q1 = st.radio("1. شو الهدف الأساسي من الهيلث انفورماتكس؟", ["توفير الحبر والورق", "تحسين جودة الرعاية بالبيانات", "تصليح أجهزة المستشفى"])
    if st.button("تأكد من إجابتي"):
        if q1 == "تحسين جودة الرعاية بالبيانات":
            st.balloons()
            st.success("وحش! إجابة صحيحة.")
        else:
            st.error("للأسف غلط، ركز يا نشمي!")

# --- التذييل (Footer) ---
st.divider()
footer_col1, footer_col2 = st.columns(2)
with footer_col1:
    st.write("© 2025 - جميع الحقوق محفوظة لمحبي الهيلث انفورماتكس")
with footer_col2:
    st.write("تم التطوير باستخدام Streamlit & AI 🇯🇴")
