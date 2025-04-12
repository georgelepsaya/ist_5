import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pydeck as pdk

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

def visualize_data(df: pd.DataFrame) -> None:
    st.subheader("Content Type Distribution")
    st.bar_chart(df['type'].value_counts())

    st.subheader("Top 10 Countries by Number of Titles")
    top_countries = df['country'].value_counts().head(10)
    st.bar_chart(top_countries)

    st.subheader("Releases Over the Years")
    release_trend = df['release_year'].value_counts().sort_index()
    st.line_chart(release_trend)

    st.subheader("🌍 Titles Produced by Country (Map View)")

    country_coords = {
        "United States": (37.0902, -95.7129),
        "India": (20.5937, 78.9629),
        "United Kingdom": (55.3781, -3.4360),
        "Canada": (56.1304, -106.3468),
        "France": (46.2276, 2.2137),
        "Germany": (51.1657, 10.4515),
        "Japan": (36.2048, 138.2529),
        "South Korea": (35.9078, 127.7669),
        "Australia": (-25.2744, 133.7751),
        "Mexico": (23.6345, -102.5528),
        "Spain": (40.4637, -3.7492),
        "Brazil": (-14.2350, -51.9253),
        "Italy": (41.8719, 12.5674),
        "Turkey": (38.9637, 35.2433),
        "Unknown": (0, 0)
    }

    # Count titles per country
    country_counts = df['country'].dropna().str.split(', ')
    country_exploded = country_counts.explode().str.strip()
    country_freq = country_exploded.value_counts().reset_index()
    country_freq.columns = ['country', 'count']

    country_freq['lat'] = country_freq['country'].apply(lambda x: country_coords.get(x, (0, 0))[0])
    country_freq['lon'] = country_freq['country'].apply(lambda x: country_coords.get(x, (0, 0))[1])

    country_freq = country_freq[(country_freq['lat'] != 0) & (country_freq['lon'] != 0)]

    max_count = country_freq['count'].max()
    country_freq['size'] = country_freq['count'] / max_count * 500000  # scale size

    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=pdk.ViewState(
            latitude=20,
            longitude=0,
            zoom=1,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=country_freq,
                get_position='[lon, lat]',
                get_radius='size',
                get_fill_color='[200, 30, 0, 160]',
                pickable=True,
            )
        ],
        tooltip={
            "html": "<b>{country}</b><br/>Titles: {count}",
            "style": {"color": "white", "backgroundColor": "black"}
        }
    ))

df = load_data()
try:
    df = preprocess_data(df)
    visualize_data(df)
except Exception as e:
    st.error(f"Error during preprocessing: {e}")
