import os
import pandas as pd
import plotly.express as px
import geopandas as gpd
from shapely.geometry import Point
import json
import streamlit as st

def load_data(shape_file_option):
    os.environ["SHAPE_RESTORE_SHX"] = "YES"

    df = pd.read_csv("Mapping Data/All pharmacies aus cleaned.csv")

    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df = df.dropna(subset=["latitude", "longitude"])

    if shape_file_option == "OECD Functional Urban Areas Core Commuting":
        old_metro_areas = gpd.read_file(
            "Mapping Data/SUA_2021_AUST_GDA2020_SHP/SUA_2021_AUST_GDA2020.shp"
        )
        print("Columns in old_metro_areas:", old_metro_areas.columns)
        capital_cities = [
            "Sydney",
            "Melbourne",
            "Brisbane",
            "Perth",
            "Adelaide",
            "Hobart",
            "Canberra",
            "Darwin",
        ]
        filtered_old_metro_areas = old_metro_areas[
            old_metro_areas["SUA_NAME21"].isin(capital_cities)
        ]
        new_metro_areas = gpd.read_file(
            "Mapping Data/OECD Functional Urban Area/AUS_core_commuting.shp"
        )

        if new_metro_areas.crs is None:
            new_metro_areas.set_crs("EPSG:7844", inplace=True)

        if old_metro_areas.crs != "EPSG:4326":
            old_metro_areas = old_metro_areas.to_crs("EPSG:4326")
        if new_metro_areas.crs != "EPSG:4326":
            new_metro_areas = new_metro_areas.to_crs("EPSG:4326")

        filtered_new_metro_areas = gpd.sjoin(
            new_metro_areas,
            filtered_old_metro_areas,
            how="inner",
            predicate="intersects",
        )
        filtered_metro_areas_json = json.loads(filtered_new_metro_areas.to_json())
        filtered_metro_areas = filtered_new_metro_areas
    else:
        old_metro_areas = gpd.read_file(
            "Mapping Data/SUA_2021_AUST_GDA2020_SHP/SUA_2021_AUST_GDA2020.shp"
        )
        print("Columns in old_metro_areas:", old_metro_areas.columns)
        capital_cities = [
            "Sydney",
            "Melbourne",
            "Brisbane",
            "Perth",
            "Adelaide",
            "Hobart",
            "Canberra",
            "Darwin",
        ]
        filtered_metro_areas = old_metro_areas[
            old_metro_areas["SUA_NAME21"].isin(capital_cities)
        ]

        if old_metro_areas.crs != "EPSG:4326":
            old_metro_areas = old_metro_areas.to_crs("EPSG:4326")

        filtered_metro_areas_json = json.loads(filtered_metro_areas.to_json())

    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.longitude, df.latitude), crs="EPSG:4326"
    )

    gdf["metro_area"] = gdf.geometry.apply(
        lambda x: next(
            (
                name
                for name, geom in zip(
                    filtered_metro_areas["SUA_NAME21"], filtered_metro_areas.geometry
                )
                if geom.contains(x)
            ),
            "Outside Metro",
        )
    )

    return gdf, filtered_metro_areas_json

def create_views(gdf, corporate_col, filtered_metro_areas_json):
    gdf_filtered = gdf.copy()

    store_count = (
        gdf_filtered[gdf_filtered["metro_area"] != "Outside Metro"]
        .groupby(["metro_area", corporate_col])
        .size()
        .unstack(fill_value=0)
    )
    market_share = store_count.div(store_count.sum(axis=1), axis=0) * 100
    market_share = market_share.round(1)

    color_mapping = {
        "SIG": "#7a002b",
        "CWG": "#a2003a",
        "Mergeco": "#7a002b",
        "EBO": "#ff1668",
        "API": "#ffa3c4",
        "RHC": "#9d4141",
        "Nat Pharm": "#e3bbbb",
        "Blooms": "#491e1e",
        "Independents & Minors": "#c5bbbb",
    }

    fig = px.scatter_mapbox(
        gdf_filtered,
        lat="latitude",
        lon="longitude",
        color=corporate_col,
        hover_name="Name",
        hover_data={
            "Categories": True,
            "Address": True,
            "City": True,
            "State": True,
            "Postcode": True,
        },
        zoom=4,
        height=800,
        width=1200,
        mapbox_style="carto-positron",
        color_discrete_map=color_mapping,
    )

    fig.update_layout(
        paper_bgcolor="#ece1d9",
        plot_bgcolor="#ece1d9",
        margin=dict(t=0, b=0, l=0, r=0),
        mapbox=dict(
            center=dict(lat=-25.2744, lon=133.7751),
            zoom=4,
            layers=[
                {
                    "source": filtered_metro_areas_json,
                    "type": "fill",
                    "color": "rgba(128, 177, 211, 0.6)",
                    "below": "traces",
                },
                {
                    "source": filtered_metro_areas_json,
                    "type": "line",
                    "color": "rgba(69, 117, 180, 1.0)",
                    "below": "traces",
                },
            ],
        ),
        showlegend=False,
    )

    return fig, market_share

def main():
    st.set_page_config(page_title="Pharmacy Market Share", layout="wide")

    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            background-color: #e7c5c5;
        }
        .main {
            background-color: #ece1d9;
        }
        .css-18e3th9 {
            padding-top: 3rem;
        }
        .css-1d391kg {
            padding-top: 2rem;
        }
        h1, h2, h3 {
            color: #7a002b;
        }
        .stTabs [role="tablist"] .stTabs [role="tab"] {
            color: #7a002b;
        }
        .stTabs [role="tablist"] .stTabs [role="tab"]:focus {
            color: #ff1668;
            background-color: rgba(255, 22, 104, 0.2);
        }
        .stTabs [role="tablist"] .stTabs [role="tab"][aria-selected="true"] {
            color: #ff1668;
            border-bottom: 2px solid #ff1668;
        }
        .css-1d391kg .element-container .markdown-text-container * {
            color: #423838 !important;
        }
        .stTabs [role="tablist"] .stTabs [role="tab"] {
            color: #423838;
        }
        .map-title {
            background-color: #7a002b;
            color: #ece1d9;
            text-align: center;
            line-height: 2.5;
            font-size: 1.5rem;
            width: 1200px;
            margin-bottom: 0px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.image("assets/wh_logo.png", use_column_width=True)

    st.title("Pharmacy Market Share in Australia")

    shape_file_option = st.sidebar.selectbox(
        "Select Metro Boundary Definition",
        ("OECD Functional Urban Areas Core Commuting", "ASGS Significant Urban Area"),
    )

    with st.spinner("Loading data and generating visualizations..."):
        gdf, filtered_metro_areas_json = load_data(shape_file_option)

        tab1, tab2 = st.tabs(["Major Banners Only", "All Pharmacies"])

        with tab1:
            st.markdown(
                "<div class='map-title'>Pre-Merger Stores in Australia by Corporate</div>",
                unsafe_allow_html=True,
            )
            pre_merge_fig, pre_market_share_majors = create_views(
                gdf[gdf["Corporate"] != "Independents & Minors"],
                "Corporate",
                filtered_metro_areas_json,
            )
            st.plotly_chart(pre_merge_fig)

            st.markdown(
                "<div class='map-title'>Post-Merger Stores in Australia by Corporate 2</div>",
                unsafe_allow_html=True,
            )
            post_merge_fig, post_market_share_majors = create_views(
                gdf[gdf["Corporate 2"] != "Independents & Minors"],
                "Corporate 2",
                filtered_metro_areas_json,
            )
            st.plotly_chart(post_merge_fig)

        with tab2:
            st.markdown(
                "<div class='map-title'>Pre-Merger Stores in Australia by Corporate</div>",
                unsafe_allow_html=True,
            )
            pre_merge_fig, pre_market_share_all = create_views(
                gdf, "Corporate", filtered_metro_areas_json
            )
            st.plotly_chart(pre_merge_fig)

            st.markdown(
                "<div class='map-title'>Post-Merger Stores in Australia by Corporate 2</div>",
                unsafe_allow_html=True,
            )
            post_merge_fig, post_market_share_all = create_views(
                gdf, "Corporate 2", filtered_metro_areas_json
            )
            st.plotly_chart(post_merge_fig)

if __name__ == "__main__":
    main()
