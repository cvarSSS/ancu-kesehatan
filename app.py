import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PIL import Image

# ===== safe import mediapipe =====
try:
    import mediapipe as mp
except Exception:
    mp = None

# ================= config =================
st.set_page_config(
    page_title="Ancu Kesehatan",
    layout="centered"
)

# ================= header =================
st.markdown("""
<h1 style="text-align:center;">Ancu Kesehatan</h1>
<p style="text-align:center; color:gray;">
Analisis BMI & Estimasi Postur Tubuh Berbasis AI
</p>
<hr>
""", unsafe_allow_html=True)

st.markdown(
    "Aplikasi edukasi kesehatan berbasis data tubuh dan analisis visual AI."
)

st.warning(
    "Hasil AI bersifat edukatif dan bukan diagnosis medis."
)

# ================= BMI INPUT =================
st.subheader("1. Analisis BMI (Data Tubuh)")

berat = st.slider("Berat Badan (kg)", 30, 150, 55)
tinggi = st.slider("Tinggi Badan (cm)", 100, 200, 160)

tinggi_m = tinggi / 100
bmi = berat / (tinggi_m ** 2)

# ================= BMI LOGIC =================
if bmi < 18.5:
    kategori = "Kurus"
    risiko = "Kekurangan gizi dan daya tahan tubuh rendah."
    saran = (
        "Tingkatkan asupan kalori dan protein, makan teratur, "
        "serta pertimbangkan konsultasi ahli gizi."
    )
elif bmi < 25:
    kategori = "Normal"
    risiko = "Risiko penyakit rendah jika pola hidup sehat dijaga."
    saran = (
        "Pertahankan pola makan seimbang, olahraga rutin, "
        "tidur cukup, dan kelola stres."
    )
elif bmi < 30:
    kategori = "Gemuk"
    risiko = "Risiko diabetes tipe 2 dan hipertensi meningkat."
    saran = (
        "Batasi konsumsi gula dan lemak, perbanyak aktivitas fisik "
        "minimal 30 menit per hari."
    )
else:
    kategori = "Obesitas"
    risiko = "Risiko tinggi penyakit kronis dan gangguan metabolik."
    saran = (
        "Disarankan perubahan gaya hidup signifikan dan "
        "konsultasi dengan tenaga medis."
    )

# ================= BMI OUTPUT =================
st.markdown(f"""
**Nilai BMI:** {bmi:.1f}  
**Kategori:** {kategori}

**Risiko:**  
{risiko}

**Saran:**  
{saran}
""")

# ================= BMI VISUAL =================
st.subheader("Visualisasi Zona BMI")

fig, ax = plt.subplots(figsize=(8, 2))
ax.axvspan(0, 18.5, alpha=0.4)
ax.axvspan(18.5, 24.9, alpha=0.4)
ax.axvspan(25, 29.9, alpha=0.4)
ax.axvspan(30, 40, alpha=0.4)
ax.axvline(bmi, linestyle="--", linewidth=2)
ax.set_xlabel("Nilai BMI")
ax.set_yticks([])
st.pyplot(fig)

# ================= AI SECTION =================
st.markdown("---")
st.subheader("2. Estimasi Postur Tubuh Berbasis AI (Opsional)")

if mp is None:
    st.info("Fitur AI tidak tersedia di environment ini.")
else:
    uploaded = st.file_uploader(
        "Upload foto tubuh tampak depan",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded:
        image = Image.open(uploaded).convert("RGB")
        img = np.array(image)

        mp_pose = mp.solutions.pose

        with mp_pose.Pose(
            static_image_mode=True,
            model_complexity=1,
            min_detection_confidence=0.5
        ) as pose:
            results = pose.process(img)

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

            Estimasi ini hanya sebagai pendukung visual
            dan tidak menggantikan hasil BMI.
            """)

            st.image(
                image,
                caption="Foto yang dianalisis",
                use_column_width=True
            )

# ================= EDUKASI =================
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
            "Batasi gula & lemak, aktif bergerak",
            "Pendampingan medis"
        ]
    })
    st.table(df)

# ================= FOOTER =================
st.markdown(
    "<hr><p style='text-align:center; color:gray;'>Ancu Kesehatan © 2026</p>",
    unsafe_allow_html=True
)
