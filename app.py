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

# Calculer la consommation totale de la semaine
df_weekly_total = calculer_consommation_totale_semaine(df, col_date, col_donnees)

st.write("Consommation totale de la semaine:")
st.write(df_weekly_monthly)

# Créer la charte graphique en cercle
fig = px.pie(df_last_week_monthly, values='consommation', names='date', title='Consommation totale sur la dernière semaine de chaque mois')
st.plotly_chart(fig, use_container_width=True)
