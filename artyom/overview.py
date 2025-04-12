import streamlit as st

st.title("Dataset overview and preparation")

st.header("Dataset overview")
st.text("Determinants of Airbnb prices in European cities")

st.subheader("Main information")
st.markdown("""
The `preprocess_dataset` function is responsible for cleaning up the dataset by removing unnecessary columns. 

1. Column Removal: The function uses the DataFrame.drop method to remove the following columns from the dataset:

### Preprocessing in `visualize_dataset`
#### Room Type Filtering

The function allows users to filter the dataset by room_type using a dropdown (`st.selectbox`).
If a specific room type is selected (other than "All"), the dataset is filtered to include only rows where the room_type matches the selected value:
```python
if room_type_filter and room_type_filter != "All":
    df = df[df["room_type"] == room_type_filter]
```

#### Color Metric Calculation:

A new column, `color_metric`, is added to the dataset. 

This column is calculated based on the selected `color_metric_col` (e.g., `realSum` or `guest_satisfaction_overall`).
The color_metric column is created by applying a lambda function to scale the values of the selected column into RGBA color values:
```python
df["color_metric"] = df[color_metric_col].apply(
    lambda x: (
        int(255 / df[color_metric_col].max() * x),  # Red
        100,                                        # Green
        150,                                        # Blue
        255                                         # Transparency
    )
)
```

#### Renaming Columns for Mapping:
The dataset's longitude (lng) and latitude (lat) columns are renamed to lon and lat, respectively, to match the requirements of `st.map`:
```python
df.rename(columns={"lng": "lon", "lat": "lat"})
```

""")


st.header("Data pre-processing")
st.markdown("""
1. Drop the columns that are not needed for the analysis.
2. Drop the rows with missing values.
3. Construct color metric rows for map visualization.""")