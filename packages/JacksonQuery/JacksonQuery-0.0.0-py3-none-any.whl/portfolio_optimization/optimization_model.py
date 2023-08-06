import bt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from tqdm import tqdm
from pypfopt import efficient_frontier, objective_functions
from . import optimization_config as oc
from . import optimization_inputs as oi
from . import optimization_data as od
from . import benchmark_model as bm

# Constants
EXPECTED_RETURNS = oi.compute_expected_returns(fees=oc.INCLUDE_FEES)
COVARIANCE_MATRIX = oi.COVARIANCE_MATRIX
RISK_FREE_RATE = oi.RISK_FREE_RATE
FUND_EXPENSE_PERCENT = od.get_fund_expense_percent()
VARIABLE_INSURANCE_CHARGES = od.get_variable_insurance_charges()

CATEGORY_MAPPER = oi.category_constraints()['mapper']
CATEGORY_LOWER = oi.category_constraints()['lower']
CATEGORY_UPPER = oi.category_constraints()['upper']

CURRENT_PORTFOLIO = oc.CURRENT_PORTFOLIO


def clean_weights(weightings, cutoff=0.0001, rounding=4):
    """
    Helper function to clean the raw weights output by the optimizer.

    :param weightings: (pd.Series) Raw weights output by the optimizer.
    :param cutoff: (float) Minimum weight to include in the portfolio. Defaults to 0.0001.
    :param rounding: (int) Number of decimal places to round weights. Defaults to 4.
    :return: (pd.Series) Cleaned weights.
    """
    if weightings is None:
        raise AttributeError("Weights not yet computed")
    clean_weights_ = weightings.copy()
    clean_weights_[np.abs(clean_weights_) < cutoff] = 0
    if rounding is not None:
        if not isinstance(rounding, int) or rounding < 1:
            raise ValueError("Rounding must be a positive integer")
        clean_weights_ = np.round(clean_weights_, rounding)
    clean_weights_ = clean_weights_.div(clean_weights_.sum())
    clean_weights_ = clean_weights_[clean_weights_ != 0]
    return clean_weights_


def calculate_minimum_risk():
    """
    Calculates the minimum risk portfolio.

    :return: (float) Minimum risk, (pd.Series) Minimum risk weights, (pd.DataFrame) Minimum risk performance metrics.
    """
    results = pd.DataFrame()
    ef = efficient_frontier.EfficientFrontier(EXPECTED_RETURNS, COVARIANCE_MATRIX, oc.BOUNDS)
    ef.add_objective(objective_functions.L2_reg, gamma=oc.GAMMA)
    ef.add_sector_constraints(CATEGORY_MAPPER, CATEGORY_LOWER, CATEGORY_UPPER)
    ef.min_volatility()

    min_risk_weights = ef.clean_weights(oc.MIN_WEIGHT)
    min_risk_weights = pd.DataFrame.from_dict(min_risk_weights, orient='index', columns=['Min_Risk_Portfolio'])
    min_risk_weights = clean_weights(min_risk_weights, cutoff=oc.MIN_WEIGHT)
    min_risk_weights = min_risk_weights.squeeze().fillna(0)
    min_risk_weights = min_risk_weights[min_risk_weights != 0].sort_values(ascending=False).round(4)
    min_risk_weights.index.name = 'TICKER'

    # Calculate Portfolio Total Expense%
    subaccount_fees = FUND_EXPENSE_PERCENT.loc[min_risk_weights.index] + VARIABLE_INSURANCE_CHARGES
    total_portfolio_expense = (subaccount_fees * min_risk_weights).sum()

    performance = pd.DataFrame(
        ef.portfolio_performance(risk_free_rate=RISK_FREE_RATE),
        columns=['Min_Risk_Portfolio'],
        index=['Expected_Return', 'Volatility', 'Sharpe_Ratio']
    )
    performance.loc['Total_Expense%'] = total_portfolio_expense

    results = pd.concat([results, performance], axis=1)
    results.columns = ['PORTFOLIO']
    results = results.rename(index={0: 'Expected_Return', 1: 'Volatility', 2: 'Sharpe_Ratio', 3: 'Total_Expense%'})
    min_risk = results.loc['Volatility'].squeeze()
    return min_risk, min_risk_weights, results


def calculate_maximum_risk():
    """
    Calculates the maximum risk portfolio.

    :return: (float) Maximum risk, (pd.Series) Maximum risk weights, (pd.DataFrame) Maximum risk performance metrics.
    """
    results = pd.DataFrame()
    ef = efficient_frontier.EfficientFrontier(EXPECTED_RETURNS, COVARIANCE_MATRIX, oc.BOUNDS)
    ef.add_objective(objective_functions.L2_reg, gamma=oc.GAMMA)
    ef.add_sector_constraints(CATEGORY_MAPPER, CATEGORY_LOWER, CATEGORY_UPPER)
    ef.efficient_risk(1.0)

    max_risk_weights = ef.clean_weights(oc.MIN_WEIGHT)
    max_risk_weights = pd.DataFrame.from_dict(max_risk_weights, orient='index', columns=['Max_Risk_Portfolio'])
    max_risk_weights = clean_weights(max_risk_weights, cutoff=oc.MIN_WEIGHT)
    max_risk_weights = max_risk_weights.squeeze().fillna(0)
    max_risk_weights = max_risk_weights[max_risk_weights != 0].sort_values(ascending=False).round(4)
    max_risk_weights.index.name = 'TICKER'

    # Calculate Portfolio Total Expense%
    subaccount_fees = FUND_EXPENSE_PERCENT.loc[max_risk_weights.index] + VARIABLE_INSURANCE_CHARGES
    total_portfolio_expense = (subaccount_fees * max_risk_weights).sum()

    performance = pd.DataFrame(
        ef.portfolio_performance(risk_free_rate=RISK_FREE_RATE),
        columns=['Max_Risk_Portfolio'],
        index=['Expected_Return', 'Volatility', 'Sharpe_Ratio']
    )
    performance.loc['Total_Expense%'] = total_portfolio_expense

    results = pd.concat([results, performance], axis=1).round(4)
    results.columns = ['PORTFOLIO']
    results = results.rename(index={0: 'Expected_Return', 1: 'Volatility', 2: 'Sharpe_Ratio', 3: 'Total_Expense%'})
    max_risk = results.loc['Volatility'].squeeze()
    return max_risk, max_risk_weights, results


def plot_efficient_frontier(weightings, results, figsize=(10, 6)):
    """
    Plots the efficient frontier.

    :param weightings: (pd.Series) Portfolio weights.
    :param results: (pd.DataFrame) Portfolio performance metrics.
    :param figsize: (tuple) Figure size.
    :return: None
    """
    # set the figure size
    plt.figure(figsize=figsize)

    # plot individual holdings as a scatterplot
    for ticker in weightings.index:
        plt.scatter(COVARIANCE_MATRIX.loc[ticker, ticker] ** 0.5, EXPECTED_RETURNS[ticker], marker='o', color='k')

    # get the minimum risk portfolio and maximum sharpe portfolio
    min_risk_portfolio = results.iloc[:, 0]
    max_sharpe_portfolio = results.loc[:, results.loc['Sharpe_Ratio'].idxmax()]
    benchmark_portfolio = results.loc[:, 'Benchmark']
    jnl_sp500_portfolio = results.loc[:, 'JNL_Mellon_S&P_500_Index']
    current_portfolio = results.loc[:, 'Current']

    # plot the efficient frontier
    plt.plot(
        results.loc['Volatility'].iloc[:-3],
        results.loc['Expected_Return'].iloc[:-3],
        'k-', label="Efficient Frontier", zorder=1
    )

    # plot the minimum risk portfolio
    plt.scatter(
        min_risk_portfolio.loc['Volatility'],
        min_risk_portfolio.loc['Expected_Return'],
        marker='*', color='red', s=250, label='Minimum Risk', zorder=2
    )

    # plot the maximum sharpe portfolio
    plt.scatter(
        max_sharpe_portfolio.loc['Volatility'],
        max_sharpe_portfolio.loc['Expected_Return'],
        marker='*', color='green', s=250, label='Maximum Sharpe', zorder=2
    )

    # plot the benchmark portfolio
    plt.scatter(
        benchmark_portfolio.loc['Volatility'],
        benchmark_portfolio.loc['Expected_Return'],
        marker='*', color='blue', s=250, label='Benchmark', zorder=2
    )

    # plot the current portfolio
    plt.scatter(
        current_portfolio.loc['Volatility'],
        current_portfolio.loc['Expected_Return'],
        marker='*', color='magenta', s=250, label='Current', zorder=2
    )

    # plot the JNL Mellon S&P 500 Index portfolio
    plt.scatter(
        jnl_sp500_portfolio.loc['Volatility'],
        jnl_sp500_portfolio.loc['Expected_Return'],
        marker='*', color='purple', s=250, label='JNL_Mellon_S&P_500_Index', zorder=2
    )

    plt.title('Efficient Frontier with Individual Holdings')
    plt.xlabel('Volatility')
    plt.ylabel('Expected Returns')
    plt.legend(loc='best')
    plt.show()


def calculate_efficient_frontier(display_plot=False):
    """
    Calculates the efficient frontier.

    :param display_plot: (bool) Display the efficient frontier plot.
    :return: (pd.DataFrame) Efficient frontier performance metrics.
    """
    min_risk = calculate_minimum_risk()[0]
    max_risk = calculate_maximum_risk()[0]

    weightings = pd.DataFrame()
    results = pd.DataFrame()
    counter = 1
    for risk in tqdm(np.linspace(min_risk + .001, max_risk - .001, 20).round(4)):
        ef = efficient_frontier.EfficientFrontier(EXPECTED_RETURNS, COVARIANCE_MATRIX, oc.BOUNDS)
        ef.add_objective(objective_functions.L2_reg, gamma=oc.GAMMA)
        ef.add_sector_constraints(CATEGORY_MAPPER, CATEGORY_LOWER, CATEGORY_UPPER)
        ef.efficient_risk(risk)
        weights = ef.clean_weights(oc.MIN_WEIGHT)
        weights = pd.DataFrame.from_dict(weights, orient='index', columns=[counter]).round(4)
        weights = clean_weights(weights, cutoff=oc.MIN_WEIGHT)
        weights.index.name = 'TICKER'
        weights = weights.fillna(0)

        # Properly align subaccount_fees and weights before multiplication
        subaccount_fees = FUND_EXPENSE_PERCENT.reindex(weights.index) + VARIABLE_INSURANCE_CHARGES
        total_portfolio_expense = (subaccount_fees * weights[counter]).sum()

        performance = pd.DataFrame(
            ef.portfolio_performance(risk_free_rate=RISK_FREE_RATE),
            columns=[counter],
            index=['Expected_Return', 'Volatility', 'Sharpe_Ratio']
        )
        performance.loc['Total_Expense%'] = total_portfolio_expense
        weightings = pd.concat([weightings, weights], axis=1).round(4)
        results = pd.concat([results, performance], axis=1).round(4)
        counter += 1

    if display_plot:
        print('Efficient Frontier:')
        plot_efficient_frontier(weightings, results)

    weightings['Benchmark'] = bm.get_benchmark_portfolio()
    weightings = weightings.fillna(0)

    # Calculate the expected return, volatility, and Sharpe ratio for the benchmark portfolio
    benchmark_weights = weightings['Benchmark']
    benchmark_returns = EXPECTED_RETURNS.loc[benchmark_weights.index]
    benchmark_exp_return = np.dot(benchmark_weights, benchmark_returns)
    benchmark_cov_matrix = COVARIANCE_MATRIX.loc[benchmark_weights.index, benchmark_weights.index]
    benchmark_volatility = np.sqrt(np.dot(benchmark_weights.T, np.dot(benchmark_cov_matrix, benchmark_weights)))
    benchmark_sharpe_ratio = (benchmark_exp_return - RISK_FREE_RATE) / benchmark_volatility

    subaccount_fees = FUND_EXPENSE_PERCENT.loc[benchmark_weights.index] + VARIABLE_INSURANCE_CHARGES
    benchmark_expense_percent = (subaccount_fees * benchmark_weights).sum()

    # Add the benchmark performance to the results
    results['Benchmark'] = [benchmark_exp_return, benchmark_volatility, benchmark_sharpe_ratio,
                            benchmark_expense_percent]

    # Calculate the expected return, volatility, and Sharpe ratio for the current portfolio
    weightings['Current'] = CURRENT_PORTFOLIO
    weightings = weightings.fillna(0)

    current_returns = EXPECTED_RETURNS.loc[CURRENT_PORTFOLIO.index]
    current_exp_return = np.dot(CURRENT_PORTFOLIO, current_returns)
    current_cov_matrix = COVARIANCE_MATRIX.loc[CURRENT_PORTFOLIO.index, CURRENT_PORTFOLIO.index]
    current_volatility = np.sqrt(np.dot(CURRENT_PORTFOLIO.T, np.dot(current_cov_matrix, CURRENT_PORTFOLIO)))
    current_sharpe_ratio = (current_exp_return - RISK_FREE_RATE) / current_volatility

    subaccount_fees = FUND_EXPENSE_PERCENT.loc[CURRENT_PORTFOLIO.index] + VARIABLE_INSURANCE_CHARGES
    current_expense_percent = (subaccount_fees * CURRENT_PORTFOLIO).sum()

    # Add the current portfolio performance to the results
    results['Current'] = [current_exp_return, current_volatility, current_sharpe_ratio,
                          current_expense_percent]

    # Calculate the expected return, volatility, and Sharpe ratio for 'JNL_Mellon_S&P_500_Index'
    weightings.loc['JNL_Mellon_S&P_500_Index', 'JNL_Mellon_S&P_500_Index'] = 1
    weightings = weightings.fillna(0)
    jnl_sp500_weights = weightings['JNL_Mellon_S&P_500_Index']
    jnl_sp500_returns = EXPECTED_RETURNS.loc[jnl_sp500_weights.index]
    jnl_sp500_exp_return = np.dot(jnl_sp500_weights, jnl_sp500_returns)
    jnl_sp500_cov_matrix = COVARIANCE_MATRIX.loc[jnl_sp500_weights.index, jnl_sp500_weights.index]
    jnl_sp500_volatility = np.sqrt(np.dot(jnl_sp500_weights.T, np.dot(jnl_sp500_cov_matrix, jnl_sp500_weights)))
    jnl_sp500_sharpe_ratio = (jnl_sp500_exp_return - RISK_FREE_RATE) / jnl_sp500_volatility

    subaccount_fees = FUND_EXPENSE_PERCENT.loc[jnl_sp500_weights.index] + VARIABLE_INSURANCE_CHARGES
    jnl_sp500_expense_percent = (subaccount_fees * jnl_sp500_weights).sum()

    # Add the 'JNL_Mellon_S&P_500_Index' performance to the results
    results['JNL_Mellon_S&P_500_Index'] = [
        jnl_sp500_exp_return, jnl_sp500_volatility, jnl_sp500_sharpe_ratio, jnl_sp500_expense_percent
    ]

    return weightings, results


def compute_effective_exposure(weightings, categories):
    """
    Compute the effective exposure of a portfolio to each category.

    :param weightings: (pd.DataFrame) The weightings of the portfolio.
    :param categories: (list) The categories to compute the effective exposure for.
    :return: (pd.DataFrame) The effective exposure of the portfolio to each category.
    """

    # Transpose the weightings dataframe to align with the standard dataframe format where each column represents a
    # feature.
    weightings_ = weightings.copy().T

    # Initialize the effective_exposure dataframe
    effective_exposure = pd.DataFrame(index=weightings_.index, columns=categories)

    for portfolio in weightings_.index:
        for category in categories:
            # Compute the effective exposure of the portfolio for the category
            effective_exposure.loc[portfolio, category] = np.sum(
                weightings_.loc[portfolio] * oc.CLASSIFICATION_SCHEMA.loc[weightings_.columns, category]
            )

    effective_exposure = effective_exposure.T

    return effective_exposure.round(4)


def select_portfolio(portfolio_number, weightings):
    """
    Select the portfolio with the given number from the weightings dataframe.

    :param portfolio_number: (int) The number of the portfolio to select.
    :param weightings: (pd.DataFrame) The weightings of the portfolios.
    :return: (pd.Series) The weightings of the selected portfolio.
    """
    portfolio = weightings[portfolio_number]
    return portfolio[portfolio != 0].sort_values(ascending=False)


def compute_category_exposure(weightings):
    """
    Compute the exposure of the portfolio to each category.

    :param weightings: (pd.DataFrame) The weightings of the portfolio.
    :return: (pd.DataFrame) The exposure of the portfolio to each category.
    """
    category_exposure = weightings.groupby(oc.CLASSIFICATION_SCHEMA['Morningstar Category']).sum()
    category_exposure = category_exposure[category_exposure != 0].dropna(axis=1, how='all').fillna(0).round(4)
    return category_exposure


def plot_holdings_values(portfolio, figsize=(12, 6)):
    """
    Plot the values of the holdings in the portfolio over time.

    :param portfolio: (pd.Series) The weightings of the portfolio.
    :param figsize: (tuple) The size of the figure.
    :return: None
    """
    subaccount_prices = od.get_subaccount_prices()
    df = subaccount_prices[portfolio.index]
    df.index = pd.to_datetime(df.index)

    plt.figure(figsize=figsize)
    for column in df.columns:
        plt.plot(df.index, df[column], label=column)

    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title('Subaccounts over time')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.show()


def display_selected_portfolio(portfolio_number, weightings, results):
    """
    Display the selected portfolio.

    :param portfolio_number: (int) The number of the portfolio to select.
    :param weightings: (pd.DataFrame) The weightings of the portfolios.
    :param results: (pd.DataFrame) The results of the portfolios.
    :return: None
    """
    portfolio = select_portfolio(portfolio_number, weightings)
    asset_class_exposure = compute_effective_exposure(
        weightings,
        ['US Stocks', 'Non US Stocks', 'Bonds', 'Cash', 'Other']
    ).round(4)
    category_exposure = compute_category_exposure(weightings)
    sector_exposure = compute_effective_exposure(weightings, [
        'Basic Materials', 'Consumer Cyclical', 'Financial Services', 'Real Estate',
        'Communication Services', 'Energy', 'Industrials', 'Technology', 'Consumer Defensive',
        'Healthcare', 'Utilities'
    ])
    marketcap_exposure = compute_effective_exposure(weightings, ['Giant', 'Large', 'Medium', 'Small', 'Micro'])
    style_exposure = compute_effective_exposure(weightings, ['Cyclical', 'Sensitive', 'Defensive'])

    print('Portfolio {}:'.format(portfolio_number))
    print('\n')
    print(compute_effective_exposure(weightings, ['YTD Return%'])[portfolio_number])
    print('\n')
    print(portfolio)
    print('\n')
    print(results[portfolio_number])
    print('\n')
    print(asset_class_exposure[portfolio_number].sort_values(ascending=False))
    print('\n')
    print(category_exposure[portfolio_number][category_exposure[portfolio_number] != 0].sort_values(ascending=False))
    print('\n')
    print(sector_exposure[portfolio_number].sort_values(ascending=False))
    print('\n')
    print(marketcap_exposure[portfolio_number].sort_values(ascending=False))
    print('\n')
    print(style_exposure[portfolio_number].sort_values(ascending=False))
    print('\n')
    print()


def optimal_portfolio(results):
    """
    Select the optimal portfolio from the results dataframe.

    :param results: (pd.DataFrame) The results of the portfolios.
    :return: (pd.Series) The weightings of the optimal portfolio.
    """
    print('Optimal Portfolio: ')
    return results.loc[:, results.loc['Sharpe_Ratio'].idxmax()]


def run_backtests(weightings):
    """
    Run backtests for each portfolio.

    :param weightings: (pd.DataFrame) The weightings of the portfolios.
    :return: (bt.backtest.Backtest) The backtest results.
    """
    # Get the subaccount prices
    subaccount_prices = od.get_subaccount_prices()

    # Create a strategy for each portfolio
    strategies = []

    for col in weightings.columns:
        weights = weightings[col]

        # Define the strategy
        strategy = bt.Strategy(f'Portfolio_{col}',
                               [bt.algos.RunOnce(),
                                bt.algos.SelectAll(),
                                bt.algos.WeighSpecified(**weights),
                                bt.algos.Rebalance()])

        # Add to the list of strategies
        strategies.append(bt.Backtest(strategy, subaccount_prices))

    # Run all backtests
    return bt.run(*strategies)


def backtest_timeseries(backtest_results):
    """
    Get the timeseries of the backtest results.

    :param backtest_results: (bt.backtest.Backtest) The backtest results.
    :return: (pd.Series) The timeseries of the backtest results.
    """
    return backtest_results._get_series('y').drop_duplicates()
