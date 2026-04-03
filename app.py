import streamlit as st
from supabase import create_client
import datetime

# 1. Konfigurasi Halaman & CSS untuk Warna Tombol
st.set_page_config(page_title="EL'S ID - STOK", layout="wide")

st.markdown("""
    <style>
    /* Mengubah warna tombol (Hack CSS) */
    div.stButton > button:first-child { height: 3em; font-weight: bold; }
    /* Tombol MENU (Biru) */
    .st-emotion-cache-10trblm { background-color: #4A90E2; color: white; }
    /* Header Tabel Oranye */
    .header-tabel {
        background-color: #FF8C00;
        padding: 10px;
        border-radius: 5px;
        color: white;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Koneksi Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# 3. Logo & Tombol Navigasi Atas (Mirip Foto 2)
st.image("https://els.id/wp-content/uploads/2021/03/Logo-Els-Computer-1.png", width=150) # Opsional: ganti URL logo kamu
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.button("🟦 MENU", use_container_width=True)
with col_m2:
    st.button("🟧 EDIT", use_container_width=True)
with col_m3:
    st.button("🟥 LOGOUT", use_container_width=True)

st.divider()

# 4. Form Input (Sejajar seperti Foto 2)
with st.form("input_stok_harian"):
    c1, c2 = st.columns(2)
    kode_brg = c1.text_input("KODE BARANG:")
    nama_brg = c2.text_input("NAMA BARANG:")
    
    c3, c4 = st.columns([3, 1])
    filter_brg = c3.text_input("Filter barang...")
    qty_input = c4.number_input("Qty", min_value=0)
    
    # Tombol Simpan Oranye
    submit = st.form_submit_button("💾 SIMPAN DATA 👆", use_container_width=True)

    if submit:
        data_baru = {
            "kode_barang": kode_brg,
            "nama_barang": nama_brg,
            "fisik": qty_input,
            "tanggal": str(datetime.date.today()),
            "username": "ADMIN-PWT" # Bisa disesuaikan nanti
        }
        try:
            supabase.table("stok_harian_pwt").insert(data_baru).execute()
            st.success("✅ Data Berhasil Disimpan ke Supabase!")
            st.rerun()
        except Exception as e:
            st.error(f"Gagal: {e}")

# 5. Tabel Riwayat dengan Header Oranye (Foto 2)
st.markdown('<div class="header-tabel">NAMA BARANG <span style="float:right">KODE BARANG</span></div>', unsafe_allow_html=True)

# Ambil data terbaru untuk ditampilkan di bawah
try:
    res = supabase.table("stok_harian_pwt").select("*").order("created_at", desc=True).limit(10).execute()
    if res.data:
        # Menampilkan data dalam bentuk list yang rapi
        for item in res.data:
            with st.expander(f"{item['nama_barang']} - ({item['kode_barang']})"):
                st.write(f"Jumlah Fisik: {item['fisik']}")
                st.write(f"Tanggal: {item['tanggal']}")
    else:
        st.info("Belum ada riwayat input hari ini.")
except:
    st.warning("Gagal memuat data riwayat.")
