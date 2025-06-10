# scripts/plots/product_plots.py
import plotly.express as px

def top_product_categories(df, top_n=10):
    df = df.dropna(subset=["product_category_name_danish"])
    top = df["product_category_name_danish"].value_counts().nlargest(top_n)

    fig = px.bar(
        top,
        title=f"Top {top_n} mest solgte produktkategorier",
        labels={"value": "Antal solgte", "index": "Kategori"},
    )
    fig.update_layout(xaxis_title="Kategori", yaxis_title="Antal solgte")
    return fig

# scripts/plots/product_plots.py
def plot_avg_price_freight(df_avg):
    fig = px.bar(
        df_avg.melt(id_vars="product_category_name_danish", value_vars=["price", "freight_value"]),
        x="product_category_name_danish",
        y="value",
        color="variable",
        barmode="group",
        title="Gennemsnitspris og fragt pr. produktkategori",
        labels={"product_category_name_danish": "Kategori", "value": "Beløb (R$)", "variable": "Type"}
    )
    fig.update_layout(xaxis_tickangle=45)
    return fig

