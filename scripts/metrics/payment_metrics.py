import pandas as pd

def compute_payment_sums(df):
    return df.groupby("payment_type")["payment_value"].sum().reset_index()

# I scripts/metrics/payment_metrics.py
def compute_avg_installments(df):
    df_grouped = df.groupby("payment_type")["payment_installments"].mean().reset_index()
    df_grouped.rename(columns={"payment_installments": "avg_installments"}, inplace=True)
    return df_grouped



