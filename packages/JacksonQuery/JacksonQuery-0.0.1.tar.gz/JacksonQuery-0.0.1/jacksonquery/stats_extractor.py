import pandas as pd


CLASSIFICATION_SCHEMA = pd.read_csv('../data/classification_schema.csv', index_col=0)


def total_net_assets():
    """
    Creates csv file of total net assets for each subaccount.

    :return: (csv file) Saves csv file to data folder.
    """
    total_net_assets_df = CLASSIFICATION_SCHEMA[['Total Net Assets ($mil)']].sort_values(
        by='Total Net Assets ($mil)', ascending=False)
    total_net_assets_df['Weighting%'] = round(
        total_net_assets_df['Total Net Assets ($mil)'] / total_net_assets_df['Total Net Assets ($mil)'].sum(), 4)

    total_net_assets_df.index = total_net_assets_df.index.str.replace(
        '/', '_', regex=False).str.replace(
        '®', '', regex=False).str.replace(
        '.', '', regex=False).str.replace(
        ' ', '_', regex=False).str.replace(
        '-', '_', regex=False)
    total_net_assets_df.index.name = 'Subaccount Name'
    total_net_assets_df.to_csv('../data/total_net_assets.csv')

    return total_net_assets_df


def ytd_return():
    """
    Creates csv file of YTD return for each subaccount.

    :return: (csv file) Saves csv file to data folder.
    """
    ytd_return_df = CLASSIFICATION_SCHEMA[['YTD Return%']].sort_values(by='YTD Return%', ascending=False)
    ytd_return_df.index = ytd_return_df.index.str.replace(
        '/', '_', regex=False).str.replace(
        '®', '', regex=False).str.replace(
        '.', '', regex=False).str.replace(
        ' ', '_', regex=False).str.replace(
        '-', '_', regex=False)
    ytd_return_df.index.name = 'Subaccount Name'
    ytd_return_df.to_csv('../data/ytd_return.csv')

    return ytd_return_df


def asset_allocation():
    """
    Creates csv file of asset allocation for each subaccount.

    :return: (csv file) Saves csv file to data folder.
    """
    groupby_asset_class = CLASSIFICATION_SCHEMA[
        ['US Stocks', 'Non US Stocks', 'Bonds', 'Cash', 'Other', 'Total Net Assets ($mil)']].copy()
    groupby_asset_class['Weighting%'] = round(
        groupby_asset_class['Total Net Assets ($mil)'] / groupby_asset_class['Total Net Assets ($mil)'].sum(), 4)
    groupby_asset_class = round(groupby_asset_class[['US Stocks', 'Non US Stocks', 'Bonds', 'Cash', 'Other']].mul(
        groupby_asset_class['Weighting%'], axis=0).sum(), 4)
    groupby_asset_class.to_csv('../data/asset_allocation.csv')

    return groupby_asset_class
