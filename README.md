# Report on Datasets and Processing

## Housing Prices in Germany
**🏠 Apartment rental offers in Germany** dataset from Kaggle: 
https://www.kaggle.com/datasets/corrieaar/apartment-rental-offers-in-germany

The dataset contains rental offers scraped from Germany's biggest real estate online platform - 
Immoscout24. This dataset only contains offers for rental properties. While it was created from 2018 
to 2019, it is still relevant and gives a good idea of the housing situation in different parts of Germany. 

The `.csv` dataset contains columns for most of the important properties, such as:

- Bundesland, City, District, ZIP code, etc.
- Service fee, base and total rent
- Year of construction, condition, information about amenities, etc.
- Living space in m²

### Pre-processing
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

#### Calculating color

First we apply log transformation to normalise the distribution.

```python
df["rent_transf"] = np.log(df["baseRent"] + 1)
```

Then we clip outliers, calculated with an interquantile range and set them to lower 
and upper bound values.

```python
perc25 = df["rent_transf"].quantile(0.25)
perc75 = df["rent_transf"].quantile(0.75)
iqr = perc75 - perc25
lower = perc25 - 1.5 * iqr
upper = perc75 + 1.5 * iqr
df['rent_transf'] = df['rent_transf'].clip(lower=lower, upper=upper)
```

Then apply min-max scaling to get values in range from 0 to 1:

```python
rent_transf = np.array(df['rent_transf']).reshape(-1, 1)
min_val = rent_transf.min()
max_val = rent_transf.max()
rent_transf = (rent_transf - min_val) / (max_val - min_val)
df["rent_transf"] = rent_transf
```

Finally, multiply value of red by the calculated values and get the color metric,
which will be displayed on the map:

```python
df['color'] = df['rent_transf'].apply(lambda x: (int(x * 255), 45, 128, 170))
```


## Exploratory Analysis report

### Rent prices

Below is a map with average rent prices for every zip code in Germany. This mapping was achieved by merging the
initial dataset with the one containing coordinates for zip codes.

![Rent in Germany](./images/georgy/rent_germany.png)

It is clear that in Eastern part of Germany prices are generally lower than in Western and Southern part of it. It is
also clear that prices are more expensive around major cities, like Berlin, Hamburg, Munich, etc.

On the web report it's also possible to inspect some states of Germany, e.g. Baden-Württemberg, to see how prices
vary there and see the average and median prices.

![Rent in Germany](./images/georgy/rent_bawu.png)

We can also explore the median prices of total rent prices in every state.

```python
median_prices = df.groupby("regio1")["totalRent"].median().reset_index()
median_prices = median_prices.sort_values(by="totalRent", ascending=False)
plt.figure(figsize=(10, 6))
plt.bar(median_prices["regio1"], median_prices["totalRent"], color="skyblue")
plt.xlabel("Bundesland")
plt.ylabel("Median Housing Price (€)")
plt.title("Median Housing Prices by Bundesland")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
```

![Rent in Germany](./images/georgy/median_prices.png)


## Airbnb rent prices in European cities
This analysis is based on several independent datasets that share the same structure. 

The datasets used are available here:
- https://zenodo.org/records/4446043

For this analysis, only data has been taken for workdays for Barcelona, Amsterdam, Berlin, and Budapest.

The columns are as following:

- `realSum`: the full price of accommodation for two people and two nights in EUR
- `room_type`: the type of the accommodation 
- `room_shared`: dummy variable for shared rooms
- `room_private`: dummy variable for private rooms
- `person_capacity`: the maximum number of guests 
- `host_is_superhost`: dummy variable for superhost status
- `multi`: dummy variable if the listing belongs to hosts with 2-4 offers
- `biz`: dummy variable if the listing belongs to hosts with more than 4 offers
- `cleanliness_rating`: cleanliness rating
- `guest_satisfaction_overall`: overall rating of the listing
- `bedrooms`: number of bedrooms (0 for studios)
- `dist`: distance from city centre in km
- `metro_dist`: distance from nearest metro station in km
- `attr_index`: attraction index of the listing location
- `attr_index_norm`: normalised attraction index (0-100)
- `rest_index`: restaurant index of the listing location
- `attr_index_norm`: normalised restaurant index (0-100)
- `lng`: longitude of the listing location
- `lat`: latitude of the listing location

## Pre-processing & Processing

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

## Examples of Analysis Results
![alt text](images/artyom/example-barcelona.png)
![alt text](images/artyom/example-berlin.png)


# Netflix movies datset

**🎬 Netflix Movies and TV Shows Dataset** from Kaggle:    
- https://www.kaggle.com/datasets/shivamb/netflix-shows

This dataset contains detailed information about movies and TV shows available on Netflix until 2021. 
It includes metadata such as the type of content, title, director, cast, country, date added to Netflix, 
release year, duration, content rating, genres (listed_in), and a short description.


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