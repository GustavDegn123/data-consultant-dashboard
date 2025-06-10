import plotly.express as px

def plot_weight_vs_volume(df):
    fig = px.scatter(
        df,
        x="volume_cm3",
        y="product_weight_g",
        hover_data=["product_id"],
        title="Sammenhæng mellem produkters vægt og volumen",
        labels={"volume_cm3": "Volumen (cm³)", "product_weight_g": "Vægt (g)"},
    )
    fig.update_layout(xaxis_title="Volumen (cm³)", yaxis_title="Vægt (g)")
    return fig
