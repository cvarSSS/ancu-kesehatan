import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PIL import Image

# ================= config =================
st.set_page_config(
    page_title="Ancu Kesehatan",
    layout="centered"
)

# ================= header =================
st.markdown("""
<h1 style="text-align:center;">Ancu Kesehatan</h1>
<p style="text-align:center; color:gray;">
Analisis BMI & Edukasi Kesehatan
</p>
<hr>
""", unsafe_allow_html=True)

st.markdown(
    "Aplikasi edukasi kesehatan berbasis data tubuh dan pemahaman risiko BMI."
)

st.warning(
    "Aplikasi ini bersifat edukatif dan bukan pengganti diagnosis medis."
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

# ================= EDUKASI VISUAL =================
st.markdown("---")
st.subheader("2. Upload Foto Tubuh (Edukasi Visual)")

uploaded = st.file_uploader(
    "Upload foto tubuh tampak depan",
    type=["jpg", "jpeg", "png"]
)

if uploaded:
    image = Image.open(uploaded).convert("RGB")
    st.image(image, caption="Foto yang diunggah", use_column_width=True)

    st.info(
        "Analisis visual AI belum tersedia di server ini.\n\n"
        "Gunakan hasil BMI sebagai indikator utama kesehatan."
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
