# ============================================
# 📊 STREAMLIT APP: Top 10 Kripto Harga Tertinggi
# Sumber data: CoinGecko API (Realtime)
# ============================================

import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

# -------------------------------
# 🧭 Judul dan Deskripsi
# -------------------------------
st.set_page_config(page_title="Data Kripto Realtime", page_icon="💰", layout="wide")

st.title("💰 Data Realtime Cryptocurrency (CoinGecko API)")
st.markdown("""
Aplikasi ini menampilkan **seluruh data koin kripto** dan **visualisasi 10 koin dengan harga tertinggi**
berdasarkan data realtime dari [CoinGecko API](https://www.coingecko.com/en/api).  
Data diperbarui setiap kali halaman dimuat ulang.
""")

# -------------------------------
# 🔄 Ambil Data dari API
# -------------------------------
@st.cache_data(ttl=300)  # cache 5 menit agar efisien
def load_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 250,
        "page": 1,
        "sparkline": False
    }
    all_data = []
    for page in range(1, 5):  # Ambil hingga 1000 coin
        params["page"] = page
        response = requests.get(url, params=params)
        data = response.json()
        if not data:
            break
        all_data.extend(data)
    df = pd.DataFrame(all_data)
    return df

df = load_data()

# -------------------------------
# 📋 Ringkas Data
# -------------------------------
df_summary = df[['name', 'symbol', 'current_price', 'market_cap', 'price_change_percentage_24h']]
df_summary.columns = ['Nama', 'Simbol', 'Harga (USD)', 'Market Cap', 'Perubahan 24h (%)']

# -------------------------------
# 📄 Tampilkan Seluruh Dataframe
# -------------------------------
st.subheader("📋 Seluruh Data Cryptocurrency (Realtime)")
st.dataframe(df_summary, use_container_width=True)

# -------------------------------
# 📊 Visualisasi Top 10 Harga Tertinggi
# -------------------------------
st.subheader("🔝 Top 10 Kripto dengan Harga Tertinggi (USD)")

# Ambil 10 koin dengan harga tertinggi
top10 = df_summary.nlargest(10, 'Harga (USD)')

# Tampilkan tabel top 10
st.dataframe(top10, use_container_width=True)

# Buat visualisasi
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(top10['Nama'], top10['Harga (USD)'], color='orange')
ax.set_title("Top 10 Kripto dengan Harga Tertinggi", fontsize=14)
ax.set_xlabel("Nama Koin")
ax.set_ylabel("Harga (USD)")
plt.xticks(rotation=45, ha='right')

# Tambahkan label harga di atas bar
for bar in bars:
    ax.text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height(),
        f"{bar.get_height():,.0f}",
        ha='center', va='bottom', fontsize=8
    )

st.pyplot(fig)

# -------------------------------
# 💾 Unduh Data (seluruh data)
# -------------------------------
st.download_button(
    label="⬇️ Unduh Seluruh Data CSV",
    data=df_summary.to_csv(index=False).encode('utf-8'),
    file_name='data_kripto_realtime.csv',
    mime='text/csv'
)

st.success("✅ Data berhasil dimuat dan divisualisasikan!")
