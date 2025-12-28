import streamlit as st

# تأكد أن هذا السطر هو أول سطر في الكود
st.set_page_config(page_title="التوأم الصحي", page_icon="🍎")

st.title("🍎 مستشارك الصحي الذكي")

tab1, tab2 = st.tabs(["نصيحة اليوم", "حاسبة الصحة"])

with tab1:
    st.header("نصيحة طبية سريعة")
    st.info("احرص على شرب الماء بانتظام، فالجفاف يؤثر على تركيزك.")

with tab2:
    weight = st.number_input("الوزن (kg)", value=70)
    height = st.number_input("الطول (cm)", value=170)
    if st.button("احسب"):
        bmi = weight / ((height/100)**2)
        st.write(f"مؤشر كتلة جسمك هو: {bmi:.2f}")
