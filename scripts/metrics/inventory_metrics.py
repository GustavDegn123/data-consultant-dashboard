def compute_weight_volume(df):
    df = df.copy()
    df["volume_cm3"] = (
        df["product_length_cm"] * df["product_height_cm"] * df["product_width_cm"]
    )
    return df[["product_id", "product_weight_g", "volume_cm3"]].dropna()
