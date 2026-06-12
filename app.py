import streamlit as st
import pandas as pd
import joblib

# 1. SETTING HALAMAN WEB
st.set_page_config(page_title="Dashboard Efisiensi Energi", layout="wide", initial_sidebar_state="collapsed")

# 2. LOAD MODEL MACHINE LEARNING
rf_model = joblib.load('model_hybrid.pkl')

# =====================================================================
# 3. KUMPULAN FUNGSI LOGIKA FUZZY 
# =====================================================================
def left_shoulder(x, a, b):
    if x <= a: return 1.0
    elif a < x < b: return (b - x) / (b - a)
    else: return 0.0

def triangle(x, a, b, c):
    if x <= a or x >= c: return 0.0
    elif a < x <= b: return (x - a) / (b - a)
    elif b < x < c: return (c - x) / (c - b)
    else: return 0.0

def right_shoulder(x, a, b):
    if x <= a: return 0.0
    elif a < x < b: return (x - a) / (b - a)
    else: return 1.0

def fuzzify_T_out(x): return {"Dingin": left_shoulder(x, 3.6, 6.9), "Sejuk": triangle(x, 3.6, 6.9, 10.4), "Panas": right_shoulder(x, 6.9, 10.4)}
def fuzzify_RH_out(x): return {"Kering": left_shoulder(x, 50, 70), "Normal": triangle(x, 60, 77, 85), "Lembap": right_shoulder(x, 80, 90)}
def fuzzify_Windspeed(x): return {"Tenang": left_shoulder(x, 1.5, 2.5), "Sedang": triangle(x, 1.5, 3.6, 6.0), "Kencang": right_shoulder(x, 5.0, 8.0)}
def fuzzify_T1(x): return {"Rendah": left_shoulder(x, 18.5, 19.5), "Normal": triangle(x, 18.5, 21.6, 22.5), "Tinggi": right_shoulder(x, 22.0, 23.0)}
def fuzzify_RH_1(x): return {"Rendah": left_shoulder(x, 32.0, 35.0), "Normal": triangle(x, 32.0, 39.6, 45.0), "Tinggi": right_shoulder(x, 42.0, 45.0)}
def fuzzify_T2(x): return {"Dingin": left_shoulder(x, 17.5, 18.5), "Nyaman": triangle(x, 17.5, 20.0, 22.5), "Panas": right_shoulder(x, 22.0, 23.0)}

def evaluasi_rules_lengkap(f_T_out, f_RH_out, f_Wind, f_T1, f_RH_1, f_T2):
    out = {"Sangat_Boros": [], "Boros": [], "Normal": [], "Efisien": [], "Sangat_Efisien": []}
    out["Sangat_Boros"].extend([min(f_T_out["Dingin"], f_T2["Panas"]), min(f_T_out["Panas"], f_T2["Dingin"]), min(f_T_out["Panas"], f_Wind["Kencang"], f_T2["Dingin"]), min(f_T_out["Dingin"], f_Wind["Kencang"], f_T2["Panas"]), min(f_RH_out["Lembap"], f_T_out["Panas"], f_T2["Dingin"])])
    out["Boros"].extend([min(f_T1["Rendah"], f_RH_1["Rendah"], f_T2["Panas"]), min(f_T2["Panas"], f_T_out["Sejuk"])])
    out["Efisien"].extend([min(f_T1["Tinggi"], f_RH_1["Tinggi"]), min(f_T1["Normal"], f_RH_1["Tinggi"]), min(f_T1["Tinggi"], f_RH_1["Normal"])])
    out["Sangat_Efisien"].extend([min(f_T1["Tinggi"], f_RH_1["Tinggi"], f_T_out["Dingin"]), min(f_T1["Tinggi"], f_RH_1["Tinggi"], f_T2["Nyaman"]), min(f_T_out["Sejuk"], f_T2["Nyaman"], f_RH_out["Normal"]), min(f_T_out["Sejuk"], f_T1["Normal"], f_Wind["Tenang"]), min(f_T2["Nyaman"], f_T1["Normal"], f_RH_1["Normal"]), min(f_T_out["Dingin"], f_T2["Dingin"]), min(f_T_out["Panas"], f_T2["Panas"]), min(f_Wind["Tenang"], f_RH_out["Normal"], f_T2["Nyaman"])])
    return {kategori: max(nilai) if nilai else 0.0 for kategori, nilai in out.items()}

def defuzzifikasi_sugeno(hasil_agregasi):
    nilai_konstan = {"Sangat_Boros": 10.0, "Boros": 30.0, "Normal": 50.0, "Efisien": 75.0, "Sangat_Efisien": 90.0}
    pembilang = sum(alpha * nilai_konstan[kat] for kat, alpha in hasil_agregasi.items())
    penyebut = sum(hasil_agregasi.values())
    return round(pembilang / penyebut, 2) if penyebut != 0 else 0.0

# =====================================================================
# 4. SUNTIKAN CSS (EFEK GLASSMORPHISM STATIS)
# =====================================================================
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
        html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* Efek Card yang langsung terlihat jelas tanpa harus hover */
        div[data-testid="column"] {
            background: rgba(26, 25, 83, 0.6); /* Background warna lebih pekat */
            backdrop-filter: blur(12px); 
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(47, 47, 228, 0.7); /* Garis tepi biru neon statis */
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 4px 15px 0 rgba(47, 47, 228, 0.15); /* Cahaya glow tipis permanen */
            transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
        }

        /* Hover effect sedikit ditambahkan agar UI tetap terasa interaktif */
        div[data-testid="column"]:hover {
            transform: translateY(-3px);
            border-color: rgba(47, 47, 228, 1.0);
            box-shadow: 0 8px 25px 0 rgba(47, 47, 228, 0.3);
        }

        div[data-testid="metric-container"] {
            background: transparent;
            border: none;
            box-shadow: none;
        }
        
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 5. DESAIN ANTARMUKA WEB (UI) GLASSMORPHISM TANPA EMOJI
# =====================================================================
st.title("Evaluasi Efisiensi Energi Rumah Pintar")
st.markdown("Sistem Hybrid Logika Fuzzy (Sugeno) & Machine Learning (Random Forest)")
st.markdown("<br>", unsafe_allow_html=True)

# --- BARIS 1: INPUT SENSOR LINGKUNGAN LUAR ---
st.subheader("Faktor Lingkungan Eksternal")
col1, col2, col3 = st.columns(3)

with col1:
    T_out = st.slider("Suhu Luar (°C)", -5.0, 30.0, 28.0)
with col2:
    RH_out = st.slider("Kelembapan Luar (%)", 20.0, 100.0, 85.0)
with col3:
    Windspeed = st.slider("Kecepatan Angin (m/s)", 0.0, 15.0, 1.0)

st.markdown("<br>", unsafe_allow_html=True)

# --- BARIS 2: INPUT SENSOR DALAM RUMAH ---
st.subheader("Faktor Kondisi Internal")
col4, col5, col6 = st.columns(3)

with col4:
    T1 = st.slider("Suhu Dapur (°C)", 15.0, 30.0, 24.0)
with col5:
    RH_1 = st.slider("Kelembapan Dapur (%)", 20.0, 70.0, 50.0)
with col6:
    T2 = st.slider("Suhu R. Keluarga (°C)", 15.0, 35.0, 21.0)

st.markdown("<br>", unsafe_allow_html=True)

# --- TOMBOL & HASIL EKSEKUSI ---
_, btn_col, _ = st.columns([1, 2, 1])

with btn_col:
    if st.button("Analisis Efisiensi Sekarang", type="primary", use_container_width=True):
        
        f_T_out, f_RH_out, f_Wind = fuzzify_T_out(T_out), fuzzify_RH_out(RH_out), fuzzify_Windspeed(Windspeed)
        f_T1, f_RH_1, f_T2 = fuzzify_T1(T1), fuzzify_RH_1(RH_1), fuzzify_T2(T2)
        
        hasil_agregasi = evaluasi_rules_lengkap(f_T_out, f_RH_out, f_Wind, f_T1, f_RH_1, f_T2)
        skor_sugeno = defuzzifikasi_sugeno(hasil_agregasi)
        
        input_array = [[T_out, RH_out, Windspeed, T1, RH_1, T2, skor_sugeno]]
        skor_hybrid = rf_model.predict(input_array)[0]
        
        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("Hasil Perbandingan Algoritma")
        
        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            st.info("Prediksi Sistem Pakar (Fuzzy Sugeno)")
            st.metric(label="Tingkat Efisiensi", value=f"{skor_sugeno:.2f}%")
            
        with res_col2:
            st.success("Prediksi Hybrid (Fuzzy + ML Terkoreksi)")
            st.metric(label="Tingkat Efisiensi", value=f"{skor_hybrid:.2f}%", delta=f"{skor_hybrid - skor_sugeno:.2f}%")