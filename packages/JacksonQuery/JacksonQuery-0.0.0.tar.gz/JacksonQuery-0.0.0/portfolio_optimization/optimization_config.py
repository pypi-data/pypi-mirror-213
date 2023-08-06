import os
import pandas as pd

# Backtest parameters
INITIAL_VALUE = 100
START_DATE = '12/31/2012'
END_DATE = '12/31/2022'
PERIODICITY = 'YEARLY'

# Optimization parameters
BOUNDS = (0, 0.10)
GAMMA = 0
MIN_WEIGHT = 0.02
INCLUDE_FEES = True

# Data paths
ROOT_DIR = os.path.abspath("..")
CLASSIFICATION_SCHEMA = pd.read_csv('../data/classification_schema.csv', index_col=0)
EQUITY_ETP_VIEWS_PATH = 'https://raw.githubusercontent.com/nathanramoscfa/cape/main/data/etf_cape_return_forecast.csv'
BOND_ETP_VIEWS_PATH = 'https://raw.githubusercontent.com/nathanramoscfa/cape/main/data/acf_yield.csv'
SUBACCOUNTS_XLSX_PATH = os.path.join(ROOT_DIR, 'data', 'subaccounts.xlsx')
TOTAL_NET_ASSETS_PATH = os.path.join(ROOT_DIR, 'data', 'total_net_assets.csv')
RETURNS_CLASS_A_PATH = os.path.join(ROOT_DIR, 'data', 'returns_class_a.csv')

# Current holdings
CURRENT_PORTFOLIO = pd.Series({
        'JNL_Mellon_Bond_Index': 0.1579,
        'JNL_Mellon_Consumer_Discretionary_Sector': 0.1579,
        'JNL_Mellon_Nasdaq_100_Index': 0.1579,
        'JNL_T_Rowe_Price_Short_Term_Bond': 0.1579,
        'JNL_WMC_Government_Money_Market': 0.1579,
        'JNL_Invesco_Small_Cap_Growth': 0.1053,
        'JNL_JPMorgan_MidCap_Growth': 0.1053
    }, index=[
        'JNL_Mellon_Bond_Index',
        'JNL_Mellon_Consumer_Discretionary_Sector',
        'JNL_Mellon_Nasdaq_100_Index',
        'JNL_T_Rowe_Price_Short_Term_Bond',
        'JNL_WMC_Government_Money_Market',
        'JNL_Invesco_Small_Cap_Growth',
        'JNL_JPMorgan_MidCap_Growth'
    ])
