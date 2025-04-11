import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

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

df = pd.read_csv("data/georgy/germany_housing.csv")

st.dataframe(df.head())

st.header("Data pre-processing")

st.subheader("⚙️ Pre-processing strategy")

st.markdown(
    """
    The strategy for preprocessing is the following:

    1. If a variable contains a lot of missing values:
        - We remove it if it doesn't have much relevance for this analysis
        - We keep it to display if it is relevant at any point
        - There is no need to perform imputation and handle all missing values, since the goal is not to build a 
        model but to conduct a meaningful exploratory analysis of this dataset.
    2. Remove irrelevant variables:
        - Some of the variables are out of the scope of this analysis
        - "Description" and "Facilities" columns have already been dropped to lower the size of the dataset
    3. Remove duplicate variables
        - There are variables with a different name, which contains the same data in the same or worse format.
        These columns should be dropped.
    """
)

df = df.drop([
    "heatingType",
    "telekomTvOffer",
    "telekomHybridUploadSpeed",
    "pricetrend",
    "scoutId",
    "geo_bln",
    "street",
    "energyEfficiencyClass",
    "lastRefurbish",
    "electricityBasePrice",
    "electricityKwhPrice",
    "date"
], axis=1)

df["baseRent"].dropna()

rent_transf = np.log(df["baseRent"] + 1)
df["rent_transf"] = rent_transf

perc25 = df["rent_transf"].quantile(0.25)
perc75 = df["rent_transf"].quantile(0.75)
iqr = perc75 - perc25
lower = perc25 - 1.5 * iqr
upper = perc75 + 1.5 * iqr

df['rent_transf'] = df['rent_transf'].clip(lower=lower, upper=upper)

rent_transf = np.array(df['rent_transf']).reshape(-1, 1)
scaler = MinMaxScaler().fit(rent_transf)
df["rent_transf"] = scaler.transform(rent_transf)

df['color'] = df['rent_transf'].apply(lambda x: (int(x * 255), 45, 128, 128))

st.session_state.housing = df

st.subheader("☑ Dataset after pre-processing")

st.dataframe(df.head())

