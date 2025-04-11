import streamlit as st
import pandas as pd

st.title("Interactive Dataset Exploration")

currency = "€"

if 'housing' in st.session_state:
    df = st.session_state.housing

    states = ['All', 'Nordrhein_Westfalen', 'Rheinland_Pfalz', 'Sachsen', 'Bremen',
             'Schleswig_Holstein', 'Baden_Württemberg', 'Thüringen', 'Hessen',
             'Niedersachsen', 'Bayern', 'Hamburg', 'Sachsen_Anhalt',
             'Mecklenburg_Vorpommern', 'Berlin', 'Brandenburg', 'Saarland']
    bundesland = st.selectbox("Bundesland", [opt.replace("_", " ") for opt in states])

    rent_price = st.radio(
        "Rent price",
        ["Total rent", "Base rent"],
        captions=[
            "Including service fees",
            "Excluding service fees"
        ],
    )

    if bundesland != 'All':
        df = df[df['regio1'].str.replace("_", " ") == bundesland]

    price_metrics_cols = st.columns(4)
    price_metrics_cols[1].metric("Median", f"{currency}{df[rent_price].median():.2f}")
    price_metrics_cols[3].metric("Max", f"{currency}{df[rent_price].max():.2f}")
    price_metrics_cols[2].metric("Min", f"{currency}{df[rent_price].min():.2f}")
    price_metrics_cols[0].metric("Average", f"{currency}{df[rent_price].mean():.2f}")

    postcode_avg = (
        df.groupby("geo_plz")
        .agg(avg_totalRent=("Total rent", "mean"),
             color=("color", "first"),)
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




