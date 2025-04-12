import streamlit as st

st.title("Dataset overview and preparation")


st.header("Main information")
st.markdown(
    """
    This report explores the U.S. Border Crossing Entry Data from the Bureau of Transportation Statistics.
    It includes monthly data from January 1996 to February 2025 on crossings at the U.S.-Canada and U.S.-Mexico borders.
    The dataset tracks various types of crossings, including vehicles, pedestrians, and trains.
    Raw data is available on this website:

    https://catalog.data.gov/dataset/border-crossing-entry-data-683ae
    """
)


st.header("Data processing")
st.markdown(
    """
    The data processing and visualization were performed using Python along with three libraries: Streamlit, Pandas, and Plotly Express.

    - Streamlit was used to build an interactive and user-friendly web application for exploring the data and presenting the results in real-time. It also allows running the application locally.

    - Pandas handled the data extraction, cleaning, transformation, and aggregation manipulations on the dataset.

    - Plotly Express was used to create dynamic charts, such as line and bar charts, which helped visualize the processed data.

    """
)
st.subheader("Data extract")
st.markdown(
    """
    The data is downloaded from the website in .csv format.
    
    The extract file contains ten columns, and the report contains data on US border crossings for each month from January 1996 to February 2025 for each border’s ports:
    
    - Port Name – Name of the border port.
    - State – the State where the Port is located.
    - Port Code – a codified key of the Port.
    - Border – the border to which the port belongs.
    - Date – month of the report.
    - Measure – type of the border crossing (e.g. pedestrian, passenger vehicle).
    - Value - the number of crossings by the measure per specified month.
    - Latitude – the latitude location of the port.
    - Longitude – the longitude location of the port.
    - Point – the point on the map that consists of longitude and latitude.
    """
)


st.subheader("Pre-processing")
st.markdown(
    """
    1. The Date column is converted to the date format and split into 2 different columns:
        - Month – the month of the report.
        - Year – corresponding year of the report.
    2. The last three columns (Latitude, Longitude, and Point) are out of scope of the current research, so they were excluded.
    
    The extraction function code is visible here:
    
    ```python
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
    ```
    
    """
)

st.subheader("Dynamic data filtering")
st.markdown(
    """
    The user can adjust dynamically the selection criteria of data with Pickers and a Slider:
    - A picker to choose border crossing type.
    - A picker to choose the border.
    - A slider to choose year range.
    
    ```python
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
    ```
    """
)
st.image("edgars/Pictures/selection_criteria.jpg", caption="Data filters displayed in UI.")

st.subheader("Charts")
st.markdown(
    """
    The application creates 2 charts:
    1. Chart for the border crossing over time:
    This chart shows total border crossings over time, based on monthly data from the U.S.–Canada and U.S.–Mexico borders.
    
    ```python
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
    ```
    
    """
)
st.image("edgars/Pictures/chart_ex_1.jpg", caption="Crossings over time - Chart in UI.")
st.markdown(
    """
    2. Top 10 ports by total crossings:
    This chart displays the Top 10 U.S. ports by total border crossings, based on data from the U.S.–Canada and U.S.–Mexico borders.
    
    
    ```python
    # CHART FOR MOST POPULAR CROSSED PORTS
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
    ```
    
    """
)
st.image("edgars/Pictures/chart_ex_2.jpg", caption="Top 10 ports by total crossings - Chart in UI.")


st.header("Data analysis")
st.subheader("Sharp Decline in Border Crossings in Early 2020")
st.image("edgars/Pictures/chart_1.jpg")
st.markdown(
    """
    In February 2020, there is a sharp decline in the number of border crossings at both the US - Mexico and US – Canada borders.
    This dramatic drop aligns with the start of the COVID-19 pandemic and the related travel restrictions implemented by the countries.
    The data shows a gradual recovery beginning in late 2021, with border crossing volumes returning to pre-pandemic levels by July 2022.
    """
)


st.subheader("Long-Term Decline in Peak Border Activity")
st.image("edgars/Pictures/chart_2.jpg")
st.markdown(
    """
    Border crossings peaks have decreased by around 42% since their peak in July 2000.
    This could be attributed to changes in trade patterns, stricter border policies, and evolving technologies that
    reduced the need for physical border crossings.
    """
)


st.subheader("Top 7 Ports by Human Crossings Located at the US - Mexico Border")
st.image("edgars/Pictures/chart_3.jpg")
st.markdown(
    """
    The busiest U.S. border crossings are on the U.S.-Mexico border because of high trade volume, large cities near the
    border, a lot of tourism, and significant immigration.
    
    People cross daily for work, shopping, vacations, or to visit
    family, which increases traffic. The U.S.-Mexico border also has better infrastructure to handle all this activity.
    """
)