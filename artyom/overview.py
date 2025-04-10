import numpy as np
import streamlit as st
import pandas as pd
from glob import glob

currency = "€"


def load_dataset() -> pd.DataFrame:
    dataset_filename = st.selectbox(
        "Dataset", 
        glob("artyom/data/*.csv"),
        format_func=lambda x: x.split("/")[-1].rstrip(".csv").capitalize()
    )
    return pd.read_csv(dataset_filename)


def tab_view(df: pd.DataFrame):
    with st.expander("Table View", expanded=True):
        st.write(df)

def preprocess_dataset(df: pd.DataFrame) -> None:
    df.drop(columns=[
        "Unnamed: 0",
        "room_shared",
        "room_private",
        "person_capacity",
        "host_is_superhost",
        "multi",
        "biz",
        "bedrooms",
        "dist",
        "metro_dist",
        "attr_index",
        "attr_index_norm",
        "rest_index",
        "rest_index_norm",
    ], inplace=True)




def visualize_dataset(df: pd.DataFrame) -> None:
    input_metric_cols = st.columns(2)
    
    size_metric_col_name = input_metric_cols[0].selectbox("Visualize as size", ["realSum", "guest_satisfaction_overall"])
    color_metric_col_name = input_metric_cols[1].selectbox("Visualize as color", ["realSum", "guest_satisfaction_overall"])
    
    room_type_filter = st.selectbox("Filter Room Type", df["room_type"].unique())
    if room_type_filter:
        df = df[df["room_type"] == room_type_filter]
    
    
    df["color_metric"] = df[color_metric_col_name].apply(
        lambda x: (
            int(255 / df[color_metric_col_name].max() * x),
            100,
            150,
            255 # Transparency
        )
    )
    
    price_metrics_cols = st.columns(4)
    
    price_metrics_cols[0].metric("Median", f"{currency}{df['realSum'].median():.2f}")
    price_metrics_cols[1].metric("Max", f"{currency}{df['realSum'].max():.2f}")
    price_metrics_cols[2].metric("Min", f"{currency}{df['realSum'].min():.2f}")
    price_metrics_cols[3].metric("Average", f"{currency}{df['realSum'].mean():.2f}")
    
    st.map(
        df.rename(columns={"lng": "lon", "lat": "lat"}),
        size=size_metric_col_name,
        color="color_metric",
    )
    
    
df = load_dataset()
try:
    preprocess_dataset(df)
    visualize_dataset(df)
except Exception as e:
    raise(e)
finally:
    tab_view(df)