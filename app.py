import streamlit as st
import joblib
import numpy as np

# โหลดโมเดลและ StandardScaler
model = joblib.load('insurance_0218.pkl')
scaler = joblib.load('scaler.pkl')

# ตั้งค่าหน้าหลักของแอป
st.set_page_config(
    page_title="แอปคำนวณค่าใช้จ่ายประกันสุขภาพ",
    page_icon="💰",
)

# CSS Styling เพื่อปรับแต่ง UI
st.markdown("""
    <style>
        body { background-color: #f7f7f7; }
        .title {
            font-size: 36px;
            color: #2c3e50;
            font-weight: bold;
            text-align: center;
        }
        .subtitle {
            font-size: 18px;
            color: #7f8c8d;
            text-align: center;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# ส่วนหัวของแอป
st.title("💰 แอปคำนวณค่าใช้จ่ายประกันสุขภาพ")
st.subheader("🔍 ทำนายค่าใช้จ่ายทางการแพทย์จากข้อมูลส่วนบุคคลของคุณ")


st.markdown("""
    ℹ️ **คำแนะนำ**  
    - กรอกข้อมูลของคุณด้านล่าง แล้วกดปุ่ม **คำนวณ**  
    - ค่าที่ทำนายออกมาจะเป็นค่าใช้จ่ายประกันสุขภาพที่คุณต้องจ่าย **โดยมีหน่วยเป็นดอลลาร์สหรัฐ**
""")

# ข้อมูลประสิทธิภาพของโมเดล
with st.expander("📊 **ประสิทธิภาพของโมเดล (กดเพื่อดูข้อมูลเพิ่มเติม)**"):
    st.write("""
    - **R² Score:** 0.7811 *(โมเดลสามารถอธิบายความแปรปรวนของข้อมูลได้ 78.11%)*  
    - **MLR ดีกว่า SLR** *(ค่าความคลาดเคลื่อนต่ำกว่ามาก ทำให้คาดการณ์แม่นยำขึ้น)*  
    """)

st.write("### 📋 ป้อนข้อมูลของคุณ")

# ช่องกรอกข้อมูล (จัดเรียงให้สวยงาม)
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

age = col1.number_input("📅 อายุ:", min_value=18, max_value=100, value=30, step=1, format="%d")
bmi = col2.number_input("⚖️ ค่า BMI:", min_value=15.0, max_value=50.0, value=25.0, step=0.1, format="%.1f")
children = st.slider("👶 จำนวนบุตรที่อยู่ในความคุ้มครอง:", min_value=0, max_value=5, value=1)

smoker = col4.selectbox("🚬 คุณสูบบุหรี่หรือไม่?", ["ไม่สูบ", "สูบ"])
gender = col3.selectbox("⚥ เพศของคุณ:", ["ชาย", "หญิง"])

# แปลงค่าข้อมูลให้เป็นตัวเลข
smoker = 1 if smoker == "สูบ" else 0
gender = 1 if gender == "ชาย" else 0

# ปุ่มคำนวณค่าใช้จ่าย
if st.button("🔮 คำนวณค่าใช้จ่าย"):
    try:
        # ปรับค่าข้อมูลให้ตรงกับที่ใช้เทรนโมเดล
        features = np.array([[age, gender, bmi, children, smoker]])
        features_scaled = scaler.transform(features)  # สำคัญ! ต้องทำ Scaling ก่อนนำไปทำนาย

        
        prediction = model.predict(features_scaled)
        st.success(f"🎉 ค่าประมาณของค่าใช้จ่ายประกันสุขภาพ : **${prediction[0]:,.2f}**")
    except Exception as e:
        st.error(f"⚠️ เกิดข้อผิดพลาด: {str(e)}")

# ส่วนท้ายของแอป
st.markdown("""
---
💡 *สร้างด้วย Streamlit* | 📊 *MLR (Multiple Linear Regression)* | 🏥 *คำนวณค่าใช้จ่ายสุขภาพของคุณได้ง่าย ๆ*
""")
