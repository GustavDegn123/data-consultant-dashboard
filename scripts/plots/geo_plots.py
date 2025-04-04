import pandas as pd
import plotly.express as px
import plotly.io as pio

def plot_country_sales(sales_by_country, save_path=None):
    if isinstance(sales_by_country, pd.Series):
        sales_by_country = sales_by_country.reset_index()
        sales_by_country.columns = ["Land", "USD"]

    # Konverter til string hvis nødvendigt
    if pd.api.types.is_period_dtype(sales_by_country["Land"]):
        sales_by_country["Land"] = sales_by_country["Land"].astype(str)

    fig = px.bar(sales_by_country, x="Land", y="USD", title="Salg pr. land")
    fig.update_layout(template="plotly_white", xaxis_title="Land", yaxis_title="USD")

    if save_path:
        pio.write_image(fig, save_path, width=1000, height=600)

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
