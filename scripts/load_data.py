import pandas as pd
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_PATH = os.path.join(BASE_DIR, 'data')

def load_accounts():
    return pd.read_csv(os.path.join(DATA_PATH, "Accounts.csv"))

def load_plant_hierarchy():
    return pd.read_csv(os.path.join(DATA_PATH, "Plant Hierarchy.csv"))

def load_sales_data():
    return pd.read_csv(os.path.join(DATA_PATH, "Plant_DTS.csv"))
