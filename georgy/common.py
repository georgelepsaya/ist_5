import streamlit as st
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
# min_val = data.min()
# max_val = data.max()
# return (data - min_val) / (max_val - min_val)

def save_to_cache(df) -> None:
    st.session_state.housing = df

def load_from_cache() -> pd.DataFrame:
    return st.session_state.housing

def read_dataset() -> pd.DataFrame:
    return pd.read_csv("data/georgy/germany_housing.csv")


def preprocess_dataset(df: pd.DataFrame) -> pd.DataFrame:

    df.drop([
        "heatingType",
        "telekomTvOffer",
        "telekomHybridUploadSpeed",
        "pricetrend",
        "scoutId",
        "geo_bln",
        "street",
        "energyEfficiencyClass",
        "lastRefurbish",
        "electricityBasePrice",
        "electricityKwhPrice",
        "date"
    ], axis=1, inplace=True)

    df["baseRent"].dropna()

    df["rent_transf"] = np.log(df["baseRent"] + 1)

    perc25 = df["rent_transf"].quantile(0.25)
    perc75 = df["rent_transf"].quantile(0.75)

    # Interquartile range
    iqr = perc75 - perc25

    lower = perc25 - 1.5 * iqr
    upper = perc75 + 1.5 * iqr

    df['rent_transf'] = df['rent_transf'].clip(lower=lower, upper=upper)

    rent_transf = np.array(df['rent_transf']).reshape(-1, 1)
    scaler = MinMaxScaler().fit(rent_transf)
    df["rent_transf"] = scaler.transform(rent_transf)

    df['color'] = df['rent_transf'].apply(lambda x: (int(x * 255), 45, 128, 170))

    df.rename(columns={"totalRent": "Total rent"}, inplace=True)
    df.rename(columns={"baseRent": "Base rent"}, inplace=True)
    
    save_to_cache(df)
    return df