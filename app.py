import streamlit as st
from g4f.client import Client

# إعدادات واجهة التطبيق
st.set_page_config(page_title="تطبيق عافية AI", page_icon="🩺", layout="centered")

st.markdown("""
    <style>
    body, .stApp { direction: rtl; text-align: right; }
    .stTextArea textarea, .stTextInput input { font-size: 18px !important; direction: rtl; text-align: right; }
    h1, h2, h3 { color: #0070f3; text-align: right; }
    div.stButton > button:first-child { background-color: #0070f3; color: white; font-size: 20px; font-weight: bold; width: 100%; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🩺 تطبيق عافية AI")
st.subheader("مساعدك الذكي لتخفيف الألم وتجهيز تقارير الأطباء")
st.divider()

medical_history = st.text_input("📝 التاريخ الطبي (سكري، ضغط، إلخ):", placeholder="اكتب حالتك هنا...")
patient_complaint = st.text_area("💬 وش تحس فيه حالياً؟ (اكتب بالعامية):", placeholder="مثال: أحس بصداع قوي من بعد الغداء...")

if st.button("🚀 حلل حالتي وجهز التقرير"):
    if not patient_complaint:
        st.warning("الرجاء كتابة ما تشعر به أولاً.")
    else:
        with st.spinner("جاري تحليل حالتك..."):
            try:
                client = Client()
                prompt = f"""
                أنت مساعد طبي ذكي محترف. تم تزويدك بحالة مريض يتحدث بالعامية.
                التاريخ الطبي للمريض: {medical_history if medical_history else 'لا يوجد'}
                شكوى المريض الحالية: {patient_complaint}
                
                بناءً على ذلك، قم بتقديم رد باللغة العربية الفصحى يحتوي على قسمين واضحة:
                1) نصائح وتوجيهات أولية ومباشرة للمريض لتخفيف ألمه وطمأنته.
                2) تقرير طبي مختصر ومجهز ومصاغ بأسلوب احترافي لتقديمه للطبيب عند زيارته.
                """
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}]
                )
                
                result_text = response.choices[0].message.content
                st.success("✨ تم التحليل بنجاح!")
                st.info(result_text)
            except Exception as e:
                st.error("عذراً، يرجى المحاولة مرة أخرى.")
