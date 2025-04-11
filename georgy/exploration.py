import streamlit as st
import pandas as pd
import pydeck as pdk


st.title("Interactive Dataset Exploration")

if 'german_housing_df' in st.session_state:
    df = st.session_state.german_housing_df

    postcode_avg = (
        df.groupby("geo_plz")
        .agg(avg_totalRent=("totalRent", "mean"))
        .reset_index()
    )

    geo_df = pd.read_csv("data/georgy/de.csv", delimiter=",")
    geo_df["latitude"] = pd.to_numeric(geo_df["latitude"])
    geo_df["longitude"] = pd.to_numeric(geo_df["longitude"])

    merged_df = pd.merge(postcode_avg, geo_df, left_on="geo_plz", right_on="postcode", how="inner")
    merged_df = merged_df.dropna()
    st.dataframe(merged_df)
    if merged_df.empty:
        st.error(
            "Bad merge")
        st.stop()

    min_rent = merged_df["avg_totalRent"].min()
    max_rent = merged_df["avg_totalRent"].max()

    if max_rent - min_rent == 0:
        merged_df["alpha"] = 255
    else:
        merged_df["alpha"] = merged_df["avg_totalRent"].apply(
            lambda x: int(50 + (x - min_rent) / (max_rent - min_rent) * 205)
        )

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=merged_df,
        pickable=True,
        opacity=1,
        radiusScale=0.2,
        get_position='[longitude, latitude]',
        get_radius=20000,
        get_fill_color='[0, 0, 255, alpha]',
    )

    view_state = pdk.ViewState(
        longitude=10.4515,
        latitude=51.1657,
        zoom=6,
        pitch=0,
    )

    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={
            "html": "<b>Post Code:</b> {geo_plz} <br/>"
                    "<b>Avg Rent:</b> {avg_totalRent}",
            "style": {"color": "white"},
        }
    )

    st.title("Germany Rent Price map by ZIP Code")
    st.write("Each post code area is highlighted with a circle where the opacity reflects the average rent price.")
    st.pydeck_chart(r)

else:
    st.write("Visit 'Dataset' section first")





