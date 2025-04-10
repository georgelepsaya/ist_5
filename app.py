import streamlit as st

st.set_page_config(layout="wide")

pages = {
    "Andrii": [
        st.Page("andrii/overview.py",
                title="Dataset",
                url_path="andrii-overview",
                icon="📄"),
        st.Page("andrii/exploration.py",
                title="Exploration",
                url_path="andrii-exploration",
                icon="📊"),
    ],
    "Artyom": [
        st.Page("artyom/overview.py",
                title="Dataset & Exploration",
                url_path="artyom-overview",
                icon="📊"),
    ],
    "Border Crossings (Edgars)": [
        st.Page("edgars/overview.py",
                title="Dataset",
                url_path="edgars-overview",
                icon="📄"),
        st.Page("edgars/exploration.py",
                title="Border Crossings Explorer",
                icon="📊"),
    ],
    "Georgy": [
        st.Page("georgy/overview.py",
                title="Dataset",
                url_path="georgy-overview",
                icon="📄"),
        st.Page("georgy/exploration.py",
                title="Exploration",
                url_path="georgy-exploration",
                icon="📊"),
    ]
}

pg = st.navigation(pages)
pg.run()