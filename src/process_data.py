import pandas as pd
from typing import List
import os
import glob
from pathlib import Path
import json

col_date: str = "date_heure"
col_donnees: str = "consommation"
cols: List[str] = [col_date, col_donnees]
fic_export_data: str = "data/interim/data.csv"


def load_data():
    list_fic: list[str] = [Path(e) for e in glob.glob("data/raw/*json")]
    list_df: list[pd.DataFrame] = []
    for p in list_fic:
        # list_df.append(pd.read_json(p))
        with open(p, "r") as f:
            dict_data: dict = json.load(f)
            df: pd.DataFrame = pd.DataFrame.from_dict(dict_data.get("results"))
            list_df.append(df)

    df: pd.DataFrame = pd.concat(list_df, ignore_index=True)
    return df


def format_data(df: pd.DataFrame):
    # typage
    df[col_date] = pd.to_datetime(df[col_date])
    # ordre
    df = df.sort_values(col_date)
    # filtrage colonnes
    df = df[cols]
    # dédoublonnage
    df = df.drop_duplicates()
    return df


def export_data(df: pd.DataFrame):
    os.makedirs("data/interim/", exist_ok=True)
    df.to_csv(fic_export_data, index=False)

def calculer_consommation_totale_semaine(df: pd.DataFrame, col_date: str, col_donnees: str) -> pd.DataFrame:
    # Assurez-vous que la colonne de dates est au format datetime
    df[col_date] = pd.to_datetime(df[col_date])
    # Grouper les données par semaine et calculer la somme pour chaque semaine
    df_weekly_total = df.groupby(df[col_date].dt.to_period('W'))[col_donnees].sum().reset_index()
    # Supprimer la colonne de dates avant de réinitialiser l'index
    del df_weekly_total[col_date]
    # Réinitialiser l'index
    df_weekly_total = df_weekly_total.groupby(df_weekly_total.index // 4).sum().reset_index()
    return df_weekly_total

def main_process():
    df: pd.DataFrame = load_data()
    df = format_data(df)
    export_data(df)
    df_weekly_total = calculer_consommation_totale_semaine(df, col_date, col_donnees)


if __name__ == "__main__":

    # data_file: str = "data/raw/eco2mix-regional-tr.csv"
    main_process()
