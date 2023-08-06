import pandas as pd
import matplotlib.pyplot as plt
from . import optimization_config as oc
from . import optimization_data as od

# Constants
CLASSIFICATION_SCHEMA = pd.read_csv('../data/classification_schema.csv', index_col=0)
INITIAL_VALUE = oc.INITIAL_VALUE


def get_benchmark_portfolio():
    """
    Returns the benchmark portfolio for the JNL Mellon model.

    :return: (pd.DataFrame) Benchmark portfolio.
    """
    US_EQUITY_BENCHMARK = 'JNL_Mellon_S&P_500_Index'
    INTERNATIONAL_EQUITY_BENCHMARK = 'JNL_Mellon_International_Index'
    FIXED_INCOME_BENCHMARK = 'JNL_Mellon_Bond_Index'

    benchmark_portfolio = pd.DataFrame({
        US_EQUITY_BENCHMARK: [0.6269],
        INTERNATIONAL_EQUITY_BENCHMARK: [0.1240],
        FIXED_INCOME_BENCHMARK: [0.2494]
    }).T
    benchmark_portfolio.columns = ['Weighting%']
    benchmark_portfolio = round(benchmark_portfolio / benchmark_portfolio.sum(), 4)
    return benchmark_portfolio


def get_market_portfolio_prices_and_returns():
    """
    Returns the market portfolio prices and returns for the JNL Mellon model.

    :return: (tuple) Market portfolio prices and returns.
    """
    benchmark_portfolio = get_benchmark_portfolio()
    subaccount_prices = od.get_subaccount_prices()
    market_portfolio_prices = pd.DataFrame(index=subaccount_prices.index)
    market_portfolio_prices['Market_Portfolio_Price'] = subaccount_prices.mul(
        benchmark_portfolio['Weighting%']
    ).sum(axis=1)
    market_portfolio_prices = round((market_portfolio_prices / market_portfolio_prices.iloc[0])*100, 4)
    market_portfolio_returns = round(market_portfolio_prices.pct_change().dropna(), 4)
    return market_portfolio_prices, market_portfolio_returns


def display_benchmark_portfolio():
    """
    Displays the benchmark portfolio for the JNL Mellon model.

    :return: None.
    """
    portfolio = get_benchmark_portfolio().copy().squeeze()
    portfolio = portfolio[portfolio != 0].sort_values(ascending=False)

    portfolio_asset_classes = CLASSIFICATION_SCHEMA[[
        'US Stocks', 'Non US Stocks', 'Bonds', 'Cash', 'Other'
    ]].loc[portfolio.index].mul(portfolio, axis=0).sum()
    portfolio_asset_classes.index.name = 'Asset Class'

    portfolio_sectors = CLASSIFICATION_SCHEMA[[
        'Basic Materials', 'Consumer Cyclical', 'Financial Services', 'Real Estate', 'Communication Services',
        'Energy', 'Industrials', 'Technology', 'Consumer Defensive', 'Healthcare', 'Utilities'
    ]].loc[portfolio.index].mul(portfolio, axis=0).sum()
    portfolio_sectors.index.name = 'Sectors'

    print('\n')
    print(portfolio)
    print('\n')
    print(portfolio_asset_classes.round(4).sort_values(ascending=False))
    print('\n')
    print(portfolio_sectors.round(4).sort_values(ascending=False))
    print('\n')
    print(portfolio.groupby(CLASSIFICATION_SCHEMA['Morningstar Category']).sum().sort_values(ascending=False))
    print('\n')

    subaccount_prices = od.get_subaccount_prices()
    market_portfolio_prices, _ = get_market_portfolio_prices_and_returns()
    pd.concat([
        market_portfolio_prices, subaccount_prices['JNL_Mellon_S&P_500_Index']
    ], axis=1).plot(figsize=(10, 6), colormap='jet')
    plt.show()
