import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd

def plot_country_sales(sales_by_country):
    fig, ax = plt.subplots(figsize=(12, 6))
    sales_by_country.plot(kind="bar", ax=ax, title="Salg pr. land")
    ax.set_ylabel("USD")
    ax.set_xlabel("Land")
    plt.tight_layout()
    return fig

def plot_customer_map(df):
    try:
        import folium
        from streamlit_folium import st_folium
    except ImportError:
        raise ImportError("Installér 'folium' og 'streamlit_folium' for at vise kort")

    map_center = [df["latitude2"].mean(), df["longitude"].mean()]
    m = folium.Map(location=map_center, zoom_start=2)

    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["latitude2"], row["longitude"]],
            radius=4,
            popup=row.name,
            color="blue",
            fill=True,
            fill_opacity=0.6,
        ).add_to(m)

    return m
