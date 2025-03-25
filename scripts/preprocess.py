import pandas as pd

def convert_date_column(df, column="Date_Time"):
    df[column] = pd.to_datetime(df[column], errors="coerce")
    return df

def join_data(sales_df, accounts_df, products_df):
    # Join på Account_id
    merged = sales_df.merge(accounts_df, on="Account_id", how="left")
    # Join på Product_id (svarende til Product_Name_id)
    merged = merged.merge(products_df, left_on="Product_id", right_on="Product_Name_id", how="left")
    return merged
