import streamlit as st
import pandas as pd
import plotly.express as px
import os
from tracker import get_product_price, save_price_data

st.set_page_config("📚 Book Tracker", layout="wide")
st.title("📚 Book Price Tracker - Multi prodotto")
st.markdown("Inserisci un link da [books.toscrape.com](https://books.toscrape.com) per monitorare i prezzi.")

# Ingresso URL
url = st.text_input("📘 Inserisci l'URL del libro")

if url:
    with st.spinner("Recupero dati..."):
        data = get_product_price(url)
        if "error" in data:
            st.error(f"Errore: {data['error']}")
        else:
            filename = save_price_data(data)
            st.success(f"📥 Dato salvato: {data['title']} - £{data['price']}")

# Lista file disponibili
st.subheader("📂 Storici disponibili")

data_folder = "data"
if os.path.exists(data_folder):
    csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]
    if csv_files:
        file_selected = st.selectbox("📖 Seleziona un libro per vedere lo storico:", csv_files)
        df = pd.read_csv(os.path.join(data_folder, file_selected))
        st.dataframe(df.tail(5), use_container_width=True)
        fig = px.line(df, x="date", y="price", title=f"Andamento prezzo - {file_selected.replace('_', ' ').replace('.csv','')}")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Nessun storico ancora presente.")
else:
    st.info("Nessun file CSV trovato.")
