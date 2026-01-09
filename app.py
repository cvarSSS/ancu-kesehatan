import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import cv2
import mediapipe as mp
import numpy as np
from PIL import Image

# ================= config =================
st.set_page_config(page_title="Ancu Kesehatan", layout="centered")

# ================= header =================
st.markdown("""
<h1 style="text-align:center;">Ancu Kesehatan</h1>
<p style="text-align:center; color:gray;">
Analisis BMI & Estimasi Postur Tubuh Berbasis AI
</p>
<hr>
""", unsafe_allow_html=True)

st.markdown("""
Aplikasi ini menyediakan analisis BMI berbasis data tubuh  
serta estimasi postur visual berbasis AI sebagai pendukung edukasi kesehatan.
""")

st.warning(
    "Estimasi AI berbasis gambar bersifat edukatif dan bukan diagnosis medis."
)

# ================= input BMI =================
st.subheader("1. Analisis BMI (Data Tubuh)")

berat = st.slider("Berat Badan (kg)", 30, 150, 55)
tinggi = st.slider("Tinggi Badan (cm)", 100, 200, 160)

tinggi_m = tinggi / 100
bmi = berat / (tinggi_m ** 2)

# ================= logiv BMI =================
if bmi < 18.5:
    kategori_bmi = "Kurus"
    risiko_bmi = "Kekurangan gizi dan daya tahan tubuh rendah."
    saran_bmi = (
        "Tingkatkan asupan kalori dan protein dari sumber bergizi. "
        "Makan teratur dan pertimbangkan konsultasi ahli gizi."
    )
elif bmi < 25:
    kategori_bmi = "Normal"
    risiko_bmi = "Risiko penyakit rendah jika pola hidup sehat dijaga."
    saran_bmi = (
        "Pertahankan pola makan seimbang, olahraga rutin, tidur cukup, "
        "dan kelola stres."
    )
elif bmi < 30:
    kategori_bmi = "Gemuk"
    risiko_bmi = "Risiko diabetes tipe 2 dan hipertensi meningkat."
    saran_bmi = (
        "Batasi gula dan lemak jenuh, perbanyak aktivitas fisik "
        "minimal 30 menit per hari."
    )
else:
    kategori_bmi = "Obesitas"
    risiko_bmi = "Risiko tinggi penyakit kronis dan gangguan metabolik."
    saran_bmi = (
        "Disarankan perubahan gaya hidup signifikan dan "
        "konsultasi dengan tenaga medis."
    )

# ================= output BMI =================
st.markdown(f"""
**Nilai BMI:** {bmi:.1f}  
**Kategori:** {kategori_bmi}

**Risiko:**  
{risiko_bmi}

**Saran:**  
{saran_bmi}
""")

# ================= grafik BMI =================
st.subheader("Visualisasi Zona BMI")

fig, ax = plt.subplots(figsize=(8, 2))
ax.axvspan(0, 18.5, color="#5DADE2", alpha=0.5, label="Kurus")
ax.axvspan(18.5, 24.9, color="#27AE60", alpha=0.5, label="Normal")
ax.axvspan(25, 29.9, color="#F4D03F", alpha=0.5, label="Gemuk")
ax.axvspan(30, 40, color="#E74C3C", alpha=0.5, label="Obesitas")
ax.axvline(bmi, color="black", linestyle="--", linewidth=2)
ax.set_xlabel("Nilai BMI")
ax.set_yticks([])
ax.legend(loc="upper right")
st.pyplot(fig)

# ================= AI  =================
st.markdown("---")
st.subheader("2. Estimasi Postur Tubuh Berbasis AI (Opsional)")

uploaded = st.file_uploader(
    "Upload foto tubuh tampak depan",
    type=["jpg", "jpeg", "png"]
)

if uploaded:
    image = Image.open(uploaded)
    img = np.array(image)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=True)
    results = pose.process(img_rgb)

    if not results.pose_landmarks:
        st.error("Tubuh tidak terdeteksi. Gunakan foto tampak depan.")
    else:
        lm = results.pose_landmarks.landmark
        ls, rs = lm[11], lm[12]
        lh, rh = lm[23], lm[24]

        shoulder = abs(ls.x - rs.x)
        hip = abs(lh.x - rh.x)
        ratio = shoulder / hip

        if ratio > 1.25:
            kategori_ai = "Kurus (Estimasi Visual)"
        elif ratio > 1.05:
            kategori_ai = "Normal (Estimasi Visual)"
        elif ratio > 0.9:
            kategori_ai = "Gemuk (Estimasi Visual)"
        else:
            kategori_ai = "Obesitas (Estimasi Visual)"

        st.markdown(f"""
        **Hasil Estimasi AI:** {kategori_ai}

        Estimasi ini digunakan sebagai **pendukung visual**  
        dan **tidak menggantikan hasil BMI**.
        """)

        st.image(image, caption="Foto yang dianalisis", use_column_width=True)

# ================= edukasi umum =================
st.markdown("---")
with st.expander("Edukasi BMI, Risiko, dan Saran Umum"):
    df = pd.DataFrame({
        "Kategori BMI": ["Kurus", "Normal", "Gemuk", "Obesitas"],
        "Rentang BMI": ["< 18.5", "18.5 – 24.9", "25 – 29.9", "≥ 30"],
        "Risiko": [
            "Kekurangan gizi",
            "Risiko rendah",
            "Diabetes & hipertensi",
            "Penyakit kronis"
        ],
        "Saran Umum": [
            "Tambah asupan nutrisi",
            "Jaga pola hidup sehat",
            "Batasi gula & lemak",
            "Pendampingan medis"
        ]
    })
    st.table(df)

# ================= FOOTER =================
st.markdown(
    "<hr><p style='text-align:center; color:gray;'>Ancu Kesehatan © 2026</p>",
    unsafe_allow_html=True
)
