import plotly.express as px

def plot_review_score_distribution(df):
    fig = px.bar(df, x="score", y="count", title="Fordeling af anmeldelsesscore",
                 labels={"score": "Review score", "count": "Antal anmeldelser"})
    fig.update_layout(xaxis=dict(dtick=1))
    return fig

def plot_reviews_per_category(df):
    fig = px.bar(df.sort_values("review_score", ascending=False), 
                 x="product_category_name_english", y="review_score",
                 title="Gennemsnitlig review-score pr. produktkategori",
                 labels={"product_category_name_english": "Kategori", "review_score": "Review-score"})
    fig.update_layout(xaxis_tickangle=-45)
    return fig
