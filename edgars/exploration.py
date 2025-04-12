import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Interactive Dataset Exploration")

# Load data
@st.cache_data
def load_data():
    # Data from the catalog.data.gov
    # Border Crossing Entry Data
    # https://catalog.data.gov/dataset/border-crossing-entry-data-683ae
    df = pd.read_csv("data/edgars/Border_Crossing_Entry_Data.csv", parse_dates=["Date"]) # Load file and parse the date colum as a date

    # Pre Processing:
    # Split the date column into YEAR and MONTH
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month

    # Drop unwanted columns: LATITUDE, LONGITUDE, POINT
    df = df.drop(columns=["Latitude", "Longitude", "Point"])

    return df

df = load_data()

st.header("U.S. Border Crossings Visualization")
st.markdown(f'Explore inbound crossings at the US-Canada and US-Mexico borders ({int(df["Year"].min())}–{int(df["Year"].max())}).')


# Sidebar with data filters
with st.sidebar:
    st.header("Data Filters")

    # Select type of border crossing e.g. pedestrians, truck, bus
    selected_measure = st.multiselect("Select U.S. border crossing type:", sorted(df["Measure"].unique()), default=["Pedestrians"])

    # Select border (either US-Canada or US-Mexico)
    selected_border = st.multiselect("Select Border:", df["Border"].unique(), default=df["Border"].unique())

    # Choose year range of data selection
    year_range = st.slider("Select Year Range:", int(df["Year"].min()), int(df["Year"].max()), (int(df["Year"].min()), int(df["Year"].max())))

# Apply filters to the data frame
filtered = df[
    (df["Measure"].isin(selected_measure)) & # Selected type of crossing
    (df["Border"].isin(selected_border)) & # Selected border
    (df["Year"] >= year_range[0]) & # Year range from
    (df["Year"] <= year_range[1]) # Year range to
]


# Toggle to show data in a table view
if st.checkbox("Show data table:"):
    st.dataframe(filtered)


# CHART FOR BORDER CROSSINGS OVER TIME
# 1) Prepare the data
# Group the filtered data by date and sum the Value column to get total crossings per date
time_series = (
    filtered.groupby("Date")["Value"]
    .sum()
    .reset_index()  # Converts the grouped object back into a DataFrame
    .sort_values("Date")  # Ensures the data is in chronological order
)

# Create a line chart with plotly showing total crossings over time
fig = px.line(
    time_series,
    x="Date",         # x-axis: Date
    y="Value",        # y-axis: Total number of crossings
    title="Total Crossings Over Time - Chart"
)

# Render the plotly chart in the streamlit app
st.plotly_chart(fig, use_container_width=True)


# CHART FOR MOST POPULAR CROSSED PORTS WITH BORDER PREFIX
# 1) Prepare the data
top_ports = (
    # Group by port name, aggregating sum for the crossings value and capturing the first border value
    filtered.groupby("Port Name")
    .agg({"Value": "sum", "Border": "first"})
    .reset_index()
)

# Create a new column that combines the Border and Port Name.
top_ports["Port Label"] = top_ports["Port Name"] + " | " + top_ports["Border"]

# Sort by value in descending order and pick the top 10 ports
top_ports = top_ports.sort_values("Value", ascending=False).head(10)

# 2) Create a horizontal bar chart using the new Port Label column
fig2 = px.bar(
    top_ports,
    x="Value",           # Bar length = crossing count
    y="Port Label",      # Use the custom label that has the border prefix
    orientation="h",     # Horizontal bars
    title="Top 10 Ports by Total Crossings - Chart"
)

# Render the plotly chart in streamlit
st.plotly_chart(fig2, use_container_width=True)
