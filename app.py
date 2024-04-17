import streamlit as st
import pandas as pd
import plotly.express as px
from src.fetch_data import load_data_from_lag_to_today
from src.process_data import col_date, col_donnees, main_process, fic_export_data
import logging
import os
import glob

import requests
from dotenv import load_dotenv
 
load_dotenv()

from schedule import every, repeat
import schedule
import time


logging.basicConfig(level=logging.INFO)

LAG_N_DAYS: int = 7
LENGTH_DATA: int = 0

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
    
def remove_data(df: pd.DataFrame, last_n_samples: int = 4*3):
    # df: pd.DataFrame = pd.read_csv(fic_export_data)
    return df.iloc[:-last_n_samples]
    # df.to_csv(fic_export_data, index=False)
df = load_data(LAG_N_DAYS)

df, removed_data = remove_data(df, last_n_samples=4*24)

def display_removed_data(remove_data: pd.DataFrame):
    st.write("Données supprimées :")
    st.write(remove_data)
    
st.subheader("Line Chart of Numerical Data Over Time")

numerical_column = col_donnees

while True:
    schedule.run_pending()
    df: pd.DataFrame = pd.read_csv(fic_export_data, parse_dates=[col_date])
    if len(df) > LENGTH_DATA:
        LENGTH_DATA = len(df)
        logging.info(f"Nb points de mesure: {LENGTH_DATA}")
        st.toast("Nouvelles données disponibles", icon="🎉")
    requests.post(
        os.environ["BLOWERIO_URL"] + "/messages",
        data={"to": "+33783112476", "message": "Test du SMS"},
    )

    time.sleep(60)
