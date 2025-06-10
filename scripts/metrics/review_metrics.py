def compute_review_score_distribution(df):
    return df["review_score"].value_counts().sort_index().reset_index(name="count").rename(columns={"review_score": "score"})

def compute_reviews_per_category(order_reviews, order_items, products, category_translation):
    merged = (
        order_reviews.merge(order_items, on="order_id")
                     .merge(products, on="product_id")
                     .merge(category_translation, on="product_category_name", how="left")
    )
    return merged.groupby("product_category_name_english")["review_score"].mean().reset_index()
