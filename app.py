import streamlit as st

st.set_page_config(layout="wide")

pages = {
    "Andrii": [
        st.Page("andrii/overview.py",
                title="Overview",
                url_path="andrii-overview",
                icon="📄"),
        st.Page("andrii/exploration.py",
                title="Explore",
                url_path="andrii-exploration",
                icon="📊"),
    ],
    "Artjoms - Airbnb Flat Prices": [
        st.Page("artyom/overview.py",
                title="Overview",
                url_path="artyom-overview",
                icon="📄"),
        st.Page("artyom/exploration.py",
                title="Explore",
                url_path="artyom-exploration",
                icon="📊"),
    ],
    "Edgars - US Border Crossings": [
        st.Page("edgars/overview.py",
                title="Overview",
                url_path="edgars-overview",
                icon="📄"),
        st.Page("edgars/exploration.py",
                title="Explore",
                icon="📊"),
    ],
    "Georgy - Rental Offers in Germany": [
        st.Page("georgy/overview.py",
                title="Overview",
                url_path="georgy-overview",
                icon="📄"),
        st.Page("georgy/exploration.py",
                title="Explore",
                url_path="georgy-exploration",
                icon="📊"),
    ]
}

pg = st.navigation(pages)
pg.run()