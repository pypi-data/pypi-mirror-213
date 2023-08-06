import os
import pandas as pd
from . import factor_model
from . import optimization_config as oc
from pypfopt import risk_models
from pandas.tseries.offsets import DateOffset
import tiafork.bbg.datamgr as dm


def get_fund_expense_percent():
    """
    Returns a pandas Series of fund expense percentages for each ETF in the universe.

    :return: (pd.Series) Fund expense percentages for each ETF in the universe.
    """
    return pd.read_csv('../data/factor_data.csv', index_col=0)['Fund Expense Fee%'] / 100


def get_variable_insurance_charges(base_contract_fee=0.0160, optional_benefits_fee=0.0095):
    """
    Returns the variable insurance charges for each subaccount.

    :param base_contract_fee: (float) Base contract fee for each subaccount. Defaults to 0.0160.
    :param optional_benefits_fee: (float) Optional benefits fee for each subaccount. Defaults to 0.0095.
    :return: (pd.Series) Variable insurance charges for each subaccount.
    """
    return round(base_contract_fee + optional_benefits_fee, 4)


def load_classification_schema():
    """
    Returns the classification schema for the universe.

    :return: (pd.DataFrame) Classification schema for the universe.
    """
    return pd.read_csv(os.path.join(oc.ROOT_DIR, 'data', 'classification_schema.csv'), index_col=0)


def load_views():
    """
    Returns the views for the universe.

    :return: (pd.DataFrame) Views for the universe.
    """
    equity_etp_views = pd.read_csv(
        oc.EQUITY_ETP_VIEWS_PATH, index_col='TICKER'
    ).rename(columns={'FWD_RETURN_FORECAST': 'VIEWS'})
    bond_etp_views = pd.read_csv(
        oc.BOND_ETP_VIEWS_PATH, index_col='TICKER'
    ).rename(columns={'ACF_YIELD': 'VIEWS'})
    views = pd.concat([equity_etp_views[['NAME', 'VIEWS']], bond_etp_views[['NAME', 'VIEWS']]]).reset_index()
    return views


def load_proxies():
    """
    Returns the proxies for the universe.

    :return: (pd.DataFrame) Proxies for the universe.
    """
    return pd.read_excel(
        oc.SUBACCOUNTS_XLSX_PATH, engine='openpyxl', sheet_name='proxy'
    ).set_index('SUBACCOUNT').dropna()


def load_subaccount_returns_and_prices():
    """
    Returns the subaccount returns and prices for the universe.

    :return: (tuple) Subaccount returns and prices for the universe.
    """
    subaccount_returns = pd.read_csv(oc.RETURNS_CLASS_A_PATH, index_col=0).dropna(axis=1)
    subaccount_returns.index = pd.to_datetime(subaccount_returns.index, format='%Y')
    subaccount_returns.index = subaccount_returns.index.to_period('Y').to_timestamp('Y')

    if oc.INCLUDE_FEES:
        subaccount_returns = subaccount_returns.subtract(get_variable_insurance_charges(), axis=1)

    subaccount_prices = oc.INITIAL_VALUE * (1 + subaccount_returns).cumprod()
    start_date = subaccount_prices.index.min() - DateOffset(years=1)
    df_initial = pd.DataFrame(oc.INITIAL_VALUE, index=[start_date], columns=subaccount_prices.columns)
    subaccount_prices = pd.concat([df_initial, subaccount_prices]).round(4)
    return subaccount_returns, subaccount_prices


def load_total_net_assets():
    """
    Returns the total net assets for the universe.

    :return: (pd.Series) Total net assets for the universe.
    """
    return pd.read_csv(oc.TOTAL_NET_ASSETS_PATH, index_col=0)['Total Net Assets ($mil)']


def load_tickers():
    """
    Returns the tickers for the universe.

    :return: (pd.Series) Tickers for the universe.
    """
    return load_views()['TICKER'].unique() + ' US Equity'


def load_etf_prices_and_returns(download=False):
    """
    Returns the ETF prices and returns for the universe.

    :param download: (bool) Whether to download the ETF prices and returns from Bloomberg. Defaults to False.
    :return: (tuple) ETF prices and returns for the universe.
    """
    if download:
        mgr = dm.BbgDataManager()
        tickers = load_tickers()
        raw_etf_prices = mgr[tickers].get_historical(
            'PX_LAST', oc.START_DATE, oc.END_DATE, oc.PERIODICITY
        ).fillna(method='ffill')
        raw_etf_prices.columns = [ticker.replace(' US Equity', '') for ticker in raw_etf_prices.columns]
        etf_prices = raw_etf_prices.dropna(axis=1)
    else:
        etf_prices = pd.read_csv(os.path.join(oc.ROOT_DIR, 'data', 'etf_prices.csv'), index_col=0)
    etf_returns = etf_prices.pct_change().dropna().round(4)
    etf_returns.index = etf_returns.index.to_period('Y').to_timestamp('Y')
    etf_prices.index = etf_prices.index.to_period('Y').to_timestamp('Y')
    etf_prices = round(etf_prices / etf_prices.iloc[0], 4)
    pd.to_csv(os.path.join(oc.ROOT_DIR, 'data', 'etf_prices.csv'))
    pd.to_csv(os.path.join(oc.ROOT_DIR, 'data', 'etf_returns.csv'))
    return etf_prices, etf_returns


def load_factor_data():
    """
    Returns the factor data for the universe.

    :return: (pd.DataFrame) Factor data for the universe.
    """
    factor_data = pd.read_csv(os.path.join(oc.ROOT_DIR, 'data', 'factor_data.csv'), index_col=0)
    return factor_data


def load_risk_free_rate(ticker='USGG10YR', prints=False):
    """
    Returns the risk-free rate for the universe.

    :param ticker: (str) Risk-free rate ticker. Defaults to 'USGG10YR'.
    :param prints: (bool) Whether to print the risk-free rate. Defaults to False.
    :return: (float) Risk-free rate for the universe.
    """
    mgr = dm.BbgDataManager()
    rf = mgr[ticker + ' Index'].get_historical(
        'PX_LAST', oc.START_DATE, oc.END_DATE, oc.PERIODICITY
    ).fillna(method='ffill')
    if prints:
        print('Risk-free Rate: {}%'.format(round(rf * 100, 2)))
    return round(rf.squeeze().mean() / 100, 4)


def compute_top_ranked_subaccounts(min_rank=0.70, display_heatmap=False):
    """
    Computes the top ranked subaccounts for the universe.

    :param min_rank: (float) Minimum rank for the top ranked subaccounts. Defaults to 0.70.
    :param display_heatmap: (bool) Whether to display the heatmap. Defaults to False.
    :return: (pd.DataFrame) Top ranked subaccounts for the universe.
    """
    subaccount_prices = load_subaccount_returns_and_prices()[1]
    factor_data = load_factor_data()
    top_ranked_subaccounts = factor_model.analyze_factor_model(
        factor_data, min_rank=min_rank, display_heatmap=display_heatmap
    )
    top_ranked_subaccounts = top_ranked_subaccounts[top_ranked_subaccounts.index.isin(subaccount_prices.columns)]
    return top_ranked_subaccounts


def get_subaccount_prices():
    """
    Returns the subaccount prices for the universe.

    :return: (pd.DataFrame) Subaccount prices for the universe.
    """
    subaccount_prices = load_subaccount_returns_and_prices()[1]
    top_ranked_subaccounts = compute_top_ranked_subaccounts()
    start_date = subaccount_prices.index.min() - DateOffset(years=1)
    df_initial = pd.DataFrame(oc.INITIAL_VALUE, index=[start_date], columns=subaccount_prices.columns)
    subaccount_prices = pd.concat([df_initial, subaccount_prices]).round(4)[top_ranked_subaccounts.index]
    return subaccount_prices


def get_subaccount_returns():
    """
    Returns the subaccount returns for the universe.

    :return: (pd.DataFrame) Subaccount returns for the universe.
    """
    return get_subaccount_prices().pct_change().dropna()


def compute_covariance_matrix():
    """
    Computes the covariance matrix for the universe.

    :return: (pd.DataFrame) Covariance matrix for the universe.
    """
    subaccount_prices = get_subaccount_prices()
    covariance_matrix = risk_models.fix_nonpositive_semidefinite(
        risk_models.risk_matrix(subaccount_prices, 'oracle_approximating', frequency=1)
    )
    return covariance_matrix
