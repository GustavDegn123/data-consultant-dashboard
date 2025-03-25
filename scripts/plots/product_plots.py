import matplotlib.pyplot as plt

def plot_bar_series(data, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(10, 5))
    data.plot(kind="bar", ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.tight_layout()
    return fig

def plot_trend(data, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(10, 5))
    for name, group in data.groupby("Product_Name"):
        ax.plot(group["Month"].astype(str), group["Sales_USD"], label=name)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0))
    plt.tight_layout()
    return fig
