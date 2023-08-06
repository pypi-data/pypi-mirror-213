import pandas as pd
from pypfopt import black_litterman
from . import optimization_data as od


# Constants
RISK_FREE_RATE = od.load_risk_free_rate()
SUBACCOUNT_PRICES = od.get_subaccount_prices()
TOTAL_NET_ASSETS = od.load_total_net_assets()
COVARIANCE_MATRIX = od.compute_covariance_matrix()


def get_views():
    """
    Returns a DataFrame of views for the Black-Litterman model.

    :return: (pd.DataFrame) DataFrame of views for the Black-Litterman model.
    """
    proxies = od.load_proxies()
    views = od.load_views()
    subaccounts = proxies.dropna(subset=['TICKER']).reset_index()
    views = pd.merge(subaccounts, views, left_on='TICKER', right_on='TICKER', how='inner')
    views = views[['SUBACCOUNT', 'TICKER', 'NAME', 'VIEWS']].set_index('SUBACCOUNT')
    views = views[views.index.isin(COVARIANCE_MATRIX.index)]
    return views


def get_views_dict():
    """
    Returns a dictionary of views for the Black-Litterman model.

    :return: (dict) Dictionary of views for the Black-Litterman model.
    """
    return get_views().to_dict()['VIEWS']


def compute_risk_aversion():
    """
    Function to compute risk aversion.

    :return: (float) Risk aversion.
    """
    return round(black_litterman.market_implied_risk_aversion(
        SUBACCOUNT_PRICES, frequency=1, risk_free_rate=RISK_FREE_RATE
    ), 4)


def compute_prior_returns():
    """
    Function to compute prior returns.

    :return: (pd.Series) Prior returns.
    """
    risk_aversion = compute_risk_aversion()
    prior_returns = black_litterman.market_implied_prior_returns(
        TOTAL_NET_ASSETS.loc[COVARIANCE_MATRIX.index], risk_aversion, COVARIANCE_MATRIX, risk_free_rate=RISK_FREE_RATE
    ).round(4)
    return prior_returns


def compute_posterior_returns():
    """
    Function to compute posterior returns.

    :return: (pd.Series) Posterior returns.
    """
    views_dict = get_views_dict()
    bl = black_litterman.BlackLittermanModel(
        cov_matrix=COVARIANCE_MATRIX,
        absolute_views=views_dict,
        pi='market',
        market_caps=TOTAL_NET_ASSETS.loc[COVARIANCE_MATRIX.index]
    )
    return round(bl.bl_returns(), 4)


def compute_expected_returns(method='posterior', fees=True):
    """
    Function to compute expected returns.

    :param method: (str) Method to use to compute expected returns. Options are 'prior' or 'posterior'.
    :param fees: (bool) Whether to include fees in the expected returns.
    :return: (pd.Series) Expected returns.
    """
    if method == 'prior':
        if fees:
            result = (compute_prior_returns() - od.get_variable_insurance_charges()).dropna()
        else:
            result = compute_prior_returns().dropna()
    elif method == 'posterior':
        if fees:
            result = (compute_posterior_returns() - od.get_variable_insurance_charges()).dropna()
        else:
            result = compute_posterior_returns().dropna()
    else:
        raise ValueError(f"Method {method} not recognized. Use 'prior' or 'posterior'.")

    return result.map('{:.4f}'.format).astype(float)


def category_constraints(file_path='../data/subaccounts.xlsx', sheet_name='categories'):
    """
    Function to create a dictionary of category constraints.

    :param file_path: (str) Path to the file containing the category constraints.
    :param sheet_name: (str) Name of the sheet containing the category constraints.
    :return: (dict) Dictionary of category constraints.
    """
    try:
        # Load data
        df = pd.read_excel(file_path, sheet_name=sheet_name)

        # Create sector_constraints dictionary
        sector_constraints = {row['Morningstar Category']: (row['Minimum'], row['Maximum']) for _, row in df.iterrows()}

        expected_returns = compute_expected_returns()
        morningstar_category_mapper = od.load_classification_schema()['Morningstar Category'].loc[
            expected_returns.index].to_dict()

        # Create lower and upper constraint dictionaries
        morningstar_category_lower = {category: sector_constraints[category][0] for category in
                                      sector_constraints.keys()}
        morningstar_category_upper = {category: sector_constraints[category][1] for category in
                                      sector_constraints.keys()}

        # Create a dictionary to return results
        result = {
            'mapper': morningstar_category_mapper,
            'lower': morningstar_category_lower,
            'upper': morningstar_category_upper
        }

        return result

    except FileNotFoundError:
        print(f'File {file_path} not found.')
    except KeyError as e:
        print(f'Key error: {e}')
    except Exception as e:
        print(f'An error occurred: {e}')
