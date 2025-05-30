import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(page_title="منصة رطوبة - تحليل التربة", layout="centered")

st.title("🌱 منصة رطوبة لتحليل التربة بالذكاء الاصطناعي")

uploaded_file = st.file_uploader("📷 ارفع صورة للتربة", type=["jpg", "jpeg", "png"])

humidity = st.slider("💧 نسبة الرطوبة", 0, 100, 50)
temperature = st.slider("🌡️ درجة الحرارة (°C)", 0, 60, 30)
region = st.text_input("📍 المنطقة", "الرياض")

if uploaded_file and st.button("🔍 تحليل الآن"):

    with st.spinner("جاري تحليل الصورة..."):
        files = {'file': uploaded_file.getvalue()}
        image = Image.open(io.BytesIO(uploaded_file.getvalue()))
        st.image(image, caption="📸 صورة التربة", use_column_width=True)

        try:
            soil_res = requests.post("http://localhost:8000/analyze_image", files={"file": uploaded_file})
            soil_type = soil_res.json().get("soil_type", "غير معروف")

            predict_res = requests.post("http://localhost:8000/predict", json={
                "soil_type": soil_type,
                "humidity": humidity,
                "temperature": temperature,
                "region": region
            })

            result = predict_res.json()

            st.success("✅ تم التحليل بنجاح!")
            st.write(f"**نوع التربة:** {soil_type}")
            st.write(f"**التوصية:** {result.get('recommendation', '-')}")
            st.write(f"**الدقة:** {result.get('confidence', '-')}")
            st.write(f"**ملاحظات:** {result.get('notes', '-')}")

        except Exception as e:
            st.error("حدث خطأ أثناء الاتصال بالخادم. تأكد أن FastAPI يعمل.")

st.markdown("---")
st.caption("منصة رطوبة © 2025")
