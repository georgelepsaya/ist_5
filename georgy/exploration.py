import streamlit as st
import pandas as pd

st.title("Interactive Dataset Exploration")

if 'housing' in st.session_state:
    df = st.session_state.housing

    postcode_avg = (
        df.groupby("geo_plz")
        .agg(avg_totalRent=("totalRent", "mean"),
             color=("color", "first"))
        .reset_index()
    )

    geo_df = pd.read_csv("data/georgy/de.csv", delimiter=",")
    geo_df["latitude"] = pd.to_numeric(geo_df["latitude"])
    geo_df["longitude"] = pd.to_numeric(geo_df["longitude"])

    merged_df = pd.merge(postcode_avg, geo_df, left_on="geo_plz", right_on="postcode", how="inner")
    merged_df = merged_df.dropna()
    if merged_df.empty:
        st.error(
            "Bad merge")
        st.stop()

    min_rent = merged_df["avg_totalRent"].min()
    max_rent = merged_df["avg_totalRent"].max()

    st.map(merged_df.rename(columns={"lng": "lon", "lat": "lat"}),
           color='color')
else:
    st.write("Visit 'Dataset' section first")




