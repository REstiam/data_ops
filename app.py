import streamlit as st
import pandas as pd
import plotly.express as px
from src.fetch_data import load_data_from_lag_to_today
from src.process_data import col_date, col_donnees, main_process, fic_export_data, calculer_consommation_totale_semaine
import logging
import os
import glob

logging.basicConfig(level=logging.INFO)

LAG_N_DAYS: int = 7

os.makedirs("data/raw/", exist_ok=True)
os.makedirs("data/interim/", exist_ok=True)

for file_path in glob.glob("data/raw/*json"):
    try:
        os.remove(file_path)
    except FileNotFoundError as e:
        logging.warning(e)

st.title("Data Visualization App")

@st.cache_data(ttl=15 * 60)
def load_data(lag_days: int):
    load_data_from_lag_to_today(lag_days)
    main_process()
    data = pd.read_csv(fic_export_data, parse_dates=[col_date])
    return data

df = load_data(LAG_N_DAYS)

st.subheader("Line Chart of Numerical Data Over Time")

numerical_column = col_donnees

fig = px.line(df, x=col_date, y=col_donnees, title="Consommation totale de la semaine")
st.plotly_chart(fig)

# Calculer la consommation totale sur la dernière semaine de chaque mois
df_last_week_monthly = calculer_consommation_totale_semaine(df, "date", "consommation")

# Afficher le titre
st.title("Consommation totale sur la dernière semaine de chaque mois")

# Afficher les données dans la ligne en dessous avec une taille de police plus grande
st.markdown("**Consommation totale sur la dernière semaine de chaque mois :**")
st.markdown(f"<h1>{df_last_week_monthly}</h1>", unsafe_allow_html=True)


