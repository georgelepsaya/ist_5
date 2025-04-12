import streamlit as st
import pandas as pd

st.title("Interactive Dataset Exploration")

filepath = "data/andrii/netflix_titles.csv"

def load_data() -> pd.DataFrame:
    df = pd.read_csv(filepath)
    return df

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    df.dropna(subset=['show_id'], inplace=True)

    df['title'].fillna("Untitled", inplace=True)
    df['type'].fillna("Unknown", inplace=True)
    df['director'].fillna("Unknown", inplace=True)
    df['cast'].fillna("Unknown", inplace=True)
    df['country'].fillna("Unknown", inplace=True)
    df['rating'].fillna("Not Rated", inplace=True)
    df['duration'].fillna("Unknown", inplace=True)
    df['listed_in'].fillna("Unknown", inplace=True)
    df['description'].fillna("No Description", inplace=True)

    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

    df = df[df['release_year'].notnull()]
    df['release_year'] = df['release_year'].astype(int)

    return df