import matplotlib.pyplot as plt

def plot_bar(data, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(10, 5))
    data.plot(kind="bar", ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    return fig

def plot_line(data, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(10, 5))
    data.plot(kind="line", ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.grid(True)
    plt.tight_layout()
    return fig
