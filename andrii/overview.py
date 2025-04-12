import streamlit as st

st.title("Dataset overview and preparation")

st.header("Dataset overview")
st.text("Netflix Movies and TV Shows Dataset")

st.subheader("Main information")

st.markdown(
    """
    **🎬 Netflix Movies and TV Shows Dataset** from Kaggle:  
    https://www.kaggle.com/datasets/shivamb/netflix-shows

    This dataset contains detailed information about movies and TV shows available on Netflix until 2021. 
    It includes metadata such as the type of content, title, director, cast, country, date added to Netflix, 
    release year, duration, content rating, genres (listed_in), and a short description.
    """
)
st.subheader("Data Pre-processing")

st.markdown("""
The `preprocess_data` function is responsible for preparing and cleaning the dataset to ensure consistent structure and data quality.

It focuses on preserving essential columns like `show_id`, while filling in missing values for less critical fields.

---

### Preprocessing in `preprocess_data`

#### Important Column Handling
The function ensures every entry has a `show_id`, which is critical as a unique identifier.

```python
df.dropna(subset=['show_id'], inplace=True)
```

#### Missing Value Handling
Less critical fields like `director`, `cast`, and `country` are filled with `"Unknown"` to retain rows without key metadata.

```python
df['director'].fillna("Unknown", inplace=True)
df['cast'].fillna("Unknown", inplace=True)
df['country'].fillna("Unknown", inplace=True)
```

#### Date and Type Handling
The `date_added` column is converted to a proper datetime format, and `release_year` is cast to integer where possible.

```python
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['release_year'] = df['release_year'].astype(int)
```

#### Default Fallbacks for Descriptive Data
Default strings like `"Untitled"` or `"No Description"` are used where appropriate.

```python
df['title'].fillna("Untitled", inplace=True)
df['description'].fillna("No Description", inplace=True)
```
""")