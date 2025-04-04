import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd

def plot_bar_series(data, title, xlabel, ylabel, save_path=None):
    # Konverter Series til DataFrame hvis nødvendigt
    if isinstance(data, pd.Series):
        data = data.reset_index()
        data.columns = [xlabel, ylabel]

    # Konverter evt. Period-type til string
    if pd.api.types.is_period_dtype(data[xlabel]):
        data[xlabel] = data[xlabel].astype(str)

    fig = px.bar(data, x=xlabel, y=ylabel, title=title)
    fig.update_layout(template="plotly_white", xaxis_title=xlabel, yaxis_title=ylabel)

    if save_path:
        pio.write_image(fig, save_path, width=1000, height=600)

    return fig

def plot_trend(data, title, xlabel, ylabel, save_path=None):
    fig = go.Figure()

    # Sørg for at Month er str (Plotly + Kaleido kræver det)
    if pd.api.types.is_period_dtype(data["Month"]):
        data["Month"] = data["Month"].astype(str)

    for name, group in data.groupby("Product_Name"):
        fig.add_trace(go.Scatter(
            x=group["Month"],
            y=group["Sales_USD"],
            mode="lines+markers",
            name=name
        ))

    fig.update_layout(
        title=title,
        template="plotly_white",
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        legend_title="Produkt"
    )

    if save_path:
        pio.write_image(fig, save_path, width=1000, height=600)

    return fig
