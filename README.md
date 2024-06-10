# project-orbit-streamlit
 

# Pharmacy Market Share in Australia

This project is a Streamlit application that visualizes the market share of pharmacies in Australia. The application allows users to select different metro boundary definitions and view pre- and post-merger store distributions for major pharmacy banners and all pharmacies.

## Features

- Load and filter pharmacy data based on selected metro boundary definitions.
- Visualize pharmacy locations on an interactive map using Plotly.
- Display market share data for pre- and post-merger scenarios.
- Customize visualizations with different metro boundary definitions.

## Installation

### Prerequisites

- Python 3.6 or higher
- Required Python packages listed in `requirements.txt`

### Install Required Packages

```sh
pip install -r requirements.txt
```

### Install Additional Packages

If not included in `requirements.txt`, make sure you have the following installed:

```sh
pip install pandas plotly geopandas shapely streamlit
```

## Running the Application

To run the application, execute the following command in your terminal:

```sh
streamlit run app.py
```

Replace `app.py` with the name of your Python script if it's different.

## Usage

1. Open your web browser and navigate to the URL displayed in the terminal (typically `http://localhost:8501`).
2. Use the sidebar to select the metro boundary definition:
   - `OECD Functional Urban Areas Core Commuting`
   - `ASGS Significant Urban Area`
3. View the visualizations for "Major Banners Only" and "All Pharmacies" in the respective tabs.

## File Structure

- `pharmacy_market_share_app`: Main application file containing the Streamlit app code.
- `Mapping Data/`: Directory containing the shapefiles and cleaned pharmacy data CSV. You will need to download the shape files yourself, as they are too large for this repository.
- `assets/`: Directory containing images and other assets used in the app.

## Code Overview

### `load_data(shape_file_option)`

Loads pharmacy data and filters metro areas based on the selected shapefile option.

- **Parameters**:
  - `shape_file_option` (str): The selected option for metro area boundaries.

- **Returns**:
  - `gdf` (GeoDataFrame): Geospatial DataFrame of pharmacies with metro area classification.
  - `filtered_metro_areas_json` (dict): GeoJSON of filtered metro areas.

### `create_views(gdf, corporate_col, filtered_metro_areas_json)`

Creates visualizations and market share data for pharmacies by corporate group.

- **Parameters**:
  - `gdf` (GeoDataFrame): Geospatial DataFrame of pharmacies.
  - `corporate_col` (str): The column name for corporate group classification.
  - `filtered_metro_areas_json` (dict): GeoJSON of filtered metro areas.

- **Returns**:
  - `fig` (Figure): Plotly map figure.
  - `market_share` (DataFrame): DataFrame of market share by metro area and corporate group.

### `main()`

Main function to run the Streamlit app.

## Custom Styling

Custom CSS styles are applied to enhance the visual appearance of the app, including:
- Sidebar background color
- Main area background color
- Tab and heading styles



## Acknowledgements

- Data sourced from various public and private (Core List Australia) datasets.
- Built using [Streamlit](https://streamlit.io/), [Pandas](https://pandas.pydata.org/), [Plotly](https://plotly.com/python/), and [Geopandas](https://geopandas.org/).


