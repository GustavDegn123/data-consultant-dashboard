import plotly.express as px
import plotly.io as pio
import pandas as pd

def plot_series(series, title, xlabel, ylabel, save_path=None):
    # Konverter Series til DataFrame
    if isinstance(series, pd.Series):
        series = series.reset_index()
        series.columns = [xlabel, ylabel]

    # Konverter Period til str hvis nødvendigt
    if pd.api.types.is_period_dtype(series[xlabel]):
        series[xlabel] = series[xlabel].astype(str)

    fig = px.bar(series, x=xlabel, y=ylabel, title=title)
    fig.update_layout(template="plotly_white", xaxis_title=xlabel, yaxis_title=ylabel)

    if save_path:
        pio.write_image(fig, save_path, width=1000, height=600)

    return fig
