import streamlit as st
import pandas as pd
import numpy as np

from georgy.common import preprocess_dataset, read_dataset
# from sklearn.preprocessing import MinMaxScaler

st.title("Dataset overview and preparation")

st.header("Dataset overview")

st.subheader("ℹ️ Main information")

st.markdown(
    """
    **🏠 Apartment rental offers in Germany** dataset from Kaggle: 
    https://www.kaggle.com/datasets/corrieaar/apartment-rental-offers-in-germany

    The dataset contains rental offers scraped from Germany's biggest real estate online platform - 
    Immoscout24. This dataset only contains offers for rental properties. While it was created from 2018 
    to 2019, it is still relevant and gives a good idea of the housing situation in different parts of Germany.
    """
)

st.subheader("📄 Format and structure")

st.markdown(
    """
    The `.csv` dataset contains columns for most of the important properties, such as:

    - Bundesland, City, District, ZIP code, etc.
    - Service fee, base and total rent
    - Year of construction, condition, information about amenities, etc.
    - Living space in m²

    And many more. There are missing values in this dataset for some variables, which is why data pre-processing
    is done in the next step. Below is a snippet of the initial state of the dataset:
    """
)

df = read_dataset()
st.dataframe(df.head())

st.header("Data pre-processing")

st.subheader("⚙️ Pre-processing strategy")

st.markdown(
    """
    The strategy for preprocessing is the following:

    1. If a variable contains a lot of missing values:
        - We remove it if it doesn't have much relevance for this analysis
        - We keep it to display if it is relevant at any point
        - Rows with missing values for baseRent are dropped.
        - log2 transformation is applied in a new column for the color scheme
        - MinMax scaling is applied for the color column
        - Using IQR we clip outliers, equating them to the lower and upper bounds
    2. Remove irrelevant variables:
        - Some of the variables are out of the scope of this analysis
        - "Description" and "Facilities" columns have already been dropped to lower the size of the dataset
    3. Remove duplicate variables
        - There are variables with a different name, which contains the same data in the same or worse format.
        These columns should be dropped.
    """
)

st.subheader("☑ Dataset after pre-processing")

df = preprocess_dataset(df)
st.dataframe(df.head())

