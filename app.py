import streamlit as st
from supabase import create_client

# Judul
st.title("📦 ELS ID - STOK HARIAN")

# Koneksi ke Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# Form Input
with st.form("input_stok"):
    kode = st.text_input("Kode Barang")
    nama = st.text_input("Nama Barang")
    qty = st.number_input("Jumlah Fisik", min_value=0)
    submitted = st.form_submit_button("SIMPAN DATA")
    
    if submitted:
        data = {"kode_barang": kode, "nama_barang": nama, "fisik": qty}
        response = supabase.table("stok_harian_pwt").insert(data).execute()
        st.success("Data Berhasil Disimpan!")
