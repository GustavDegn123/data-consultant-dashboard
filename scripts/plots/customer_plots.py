import plotly.express as px
import plotly.io as pio
import pandas as pd

def plot_bar(data, title, xlabel, ylabel, save_path=None):
    # Hvis data er en Series, konverter til DataFrame
    if isinstance(data, pd.Series):
        data = data.reset_index()
        data.columns = [xlabel, ylabel]

    # Konverter Period til string hvis nødvendigt
    if pd.api.types.is_period_dtype(data[xlabel]):
        data[xlabel] = data[xlabel].astype(str)

    fig = px.bar(data, x=xlabel, y=ylabel, title=title)
    fig.update_layout(template="plotly_white", xaxis_title=xlabel, yaxis_title=ylabel)

    if save_path:
        pio.write_image(fig, save_path, width=1000, height=600)

    return fig

def plot_line(data, title, xlabel, ylabel, save_path=None):
    # Hvis data er en Series, konverter til DataFrame
    if isinstance(data, pd.Series):
        data = data.reset_index()
        data.columns = [xlabel, ylabel]

    # Konverter Period til string hvis nødvendigt
    if pd.api.types.is_period_dtype(data[xlabel]):
        data[xlabel] = data[xlabel].astype(str)

    fig = px.line(data, x=xlabel, y=ylabel, title=title)
    fig.update_layout(template="plotly_white", xaxis_title=xlabel, yaxis_title=ylabel)

    if save_path:
        pio.write_image(fig, save_path, width=1000, height=600)

    return fig
