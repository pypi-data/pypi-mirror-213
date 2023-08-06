import pandas as pd


def load_data():
    """
    Loads data from csv files.

    :return: (tuple) Tuple of DataFrames.
    """
    classification_schema = pd.read_csv('../data/classification_schema.csv', index_col=0)
    management_fees = pd.read_csv('../data/management_fees.csv', index_col=0)
    manager_tenures = pd.read_csv('../data/manager_tenures.csv', index_col=0)
    portfolio_turnovers = pd.read_csv('../data/portfolio_turnovers.csv', index_col=0)
    total_net_assets = pd.read_csv('../data/total_net_assets.csv', index_col=0)

    return classification_schema, management_fees, manager_tenures, portfolio_turnovers, total_net_assets


def process_data():
    """
    Processes data for factor analysis.

    :return: (pd.DataFrame) DataFrame of processed data.
    """
    management_fees, manager_tenures, portfolio_turnovers, classification_schema, total_net_assets = load_data()

    factor_data = pd.concat([management_fees, manager_tenures, portfolio_turnovers], axis=1).sort_index()
    factor_data = pd.concat([classification_schema, factor_data], axis=1).dropna()
    factor_data = factor_data.rename(columns={
        'Total Expenses After Waiver/Reimbursement': 'Fund Expense Fee%'
    })

    factor_data = factor_data[[
        'Morningstar Category',
        'Fund Expense Fee%',
        'Manager Tenure (Years)',
        'Portfolio Turnover%'
    ]]

    factor_data.to_csv('../data/factor_data.csv')

    return factor_data
