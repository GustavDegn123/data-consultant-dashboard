import matplotlib.pyplot as plt

def plot_series(series, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(10, 5))
    series.plot(kind="bar", ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.tight_layout()
    return fig
