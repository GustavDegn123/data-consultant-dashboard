import plotly.express as px

def plot_delivery_time_by_month(df):
    fig = px.line(
        df,
        x="month",
        y="delivery_time_days",
        title="📦 Gennemsnitlig leveringstid pr. måned",
        labels={"month": "Måned", "delivery_time_days": "Leveringstid (dage)"}
    )
    fig.update_layout(xaxis_title="Måned", yaxis_title="Gns. leveringstid (dage)")
    return fig

import plotly.express as px

def plot_geo_map(df):
    fig = px.scatter_mapbox(
        df,
        lat="geolocation_lat",
        lon="geolocation_lng",
        color="type",
        zoom=3,
        mapbox_style="carto-positron",
        title="Geografisk fordeling af kunder og sælgere",
        height=600
    )
    return fig
