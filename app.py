import streamlit as st

pages = {
    "Reports": [
        st.Page("andrii.py", title="Andrii's report"),
        st.Page("artyom.py", title="Artyom's report"),
        st.Page("edgars.py", title="Edgars' report"),
        st.Page("georgy.py", title="Georgy's report")
    ]
}

pg = st.navigation(pages)
pg.run()