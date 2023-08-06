import os
import pandas as pd
import numpy as np
from tqdm import tqdm
from bs4 import BeautifulSoup


def morningstar_category(str_list, sub_acct):
    """
    Returns the Morningstar Category for a given subaccount.

    :param str_list: (list) List of strings from the Morningstar page.
    :param sub_acct: (str) Sub-account name.
    :return: (pd.DataFrame) DataFrame of Morningstar Category.
    """
    category_label = 'Morningstar Category'
    morningstar_category_index = [str_list.index(s) for s in [i for i in str_list if category_label in i]][0]

    return pd.DataFrame(
        str_list[morningstar_category_index + 1].split('>')[1].split('<')[0],
        index=[sub_acct],
        columns=[category_label]
    )


def total_net_assets(str_list, sub_acct):
    """
    Returns the Total Net Assets for a given subaccount.

    :param str_list: (list) List of strings from the Morningstar page.
    :param sub_acct: (str) Sub-account name.
    :return: (pd.DataFrame) DataFrame of Total Net Assets.
    """
    total_net_assets_label = 'Total Net Assets ($mil)'
    total_net_assets_index = [str_list.index(s) for s in [i for i in str_list if total_net_assets_label in i]][0]
    try:
        total_net_assets_ = float(
            str_list[total_net_assets_index].split('<label>')[1].split('</label>')[1].split('<')[0].replace(
                '$', '').replace(',', ''))
    except IndexError:
        total_net_assets_ = float(
            str_list[total_net_assets_index:total_net_assets_index + 2][1].split('>')[1].split('<')[0].replace(
                '$', '').replace(',', ''))

    return pd.DataFrame(
        total_net_assets_,
        index=[sub_acct],
        columns=[total_net_assets_label]
    )


def top_sectors(str_list, sub_acct):
    """
    Returns the Top Sectors for a given subaccount.

    :param str_list: (list) List of strings from the Morningstar page.
    :param sub_acct: (str) Sub-account name.
    :return: (pd.DataFrame) DataFrame of Top Sectors.
    """
    keywords = [
        'Cyclical', 'Sensitive', 'Defensive', 'Basic Materials', 'Consumer Cyclical', 'Financial Services',
        'Real Estate',
        'Communication Services', 'Energy', 'Industrials', 'Technology', 'Consumer Defensive', 'Healthcare', 'Utilities'
    ]
    try:
        top_sectors_index = [str_list.index(s) for s in [i for i in str_list if 'Top Sectors' in i]][0]
        top_sectors_ = str_list[top_sectors_index].split('<td>')
        top_sectors_dict = {}
        for keyword in keywords:
            try:
                top_sectors_dict[keyword] = round(float(
                    [x for x in top_sectors_ if keyword in x][0].split(keyword)[-1].split('<')[2].split('>')[1].replace(
                        '%', '')) / 100, 4)
            except IndexError:
                sector_index = top_sectors_.index([x for x in top_sectors_ if keyword in x][0])
                try:
                    top_sectors_dict[keyword] = round(
                        float(top_sectors_[sector_index:sector_index + 3][1].split('<')[0].replace('%', '')) / 100, 4)
                except ValueError:
                    top_sectors_dict[keyword] = 0

        return pd.DataFrame.from_dict(top_sectors_dict, orient='index', columns=[sub_acct]).T
    except IndexError:
        return pd.DataFrame(data=[0] * len(keywords), index=keywords).T


def asset_allocation(str_list, sub_acct):
    """
    Returns the Asset Allocation for a given subaccount.

    :param str_list: (list) List of strings from the Morningstar page.
    :param sub_acct: (str) Sub-account name.
    :return: (pd.DataFrame) DataFrame of Asset Allocation.
    """
    asset_allocation_label = 'Asset Allocation'
    asset_allocation_index = str_list.index([i for i in str_list if asset_allocation_label in i][0])
    asset_allocation_string = str_list[asset_allocation_index:asset_allocation_index + 3][2]
    try:
        us_stocks = round(
            float(asset_allocation_string.split('US Stocks:')[1].split('<')[0].replace(' ', '').replace('%', '')) / 100,
            4)
        non_us_stocks = round(float(
            asset_allocation_string.split('Non US Stocks:')[1].split('<')[0].replace(' ', '').replace('%', '')) / 100,
                              4)
    except IndexError:
        us_stocks = round(
            float(asset_allocation_string.split('Stocks:')[1].split('<')[0].replace(' ', '').replace('%', '')) / 100, 4)
        non_us_stocks = 0
    bonds = round(
        float(asset_allocation_string.split('Bonds:')[1].split('<')[0].replace(' ', '').replace('%', '')) / 100, 4)
    cash = round(float(asset_allocation_string.split('Cash:')[1].split('<')[0].replace(' ', '').replace('%', '')) / 100,
                 4)
    other = round(
        float(asset_allocation_string.split('Other:')[1].split('<')[0].replace(' ', '').replace('%', '')) / 100, 4)
    try:
        asset_allocation_dict = {'US Stocks': us_stocks, 'Non US Stocks': non_us_stocks, 'Bonds': bonds, 'Cash': cash,
                                 'Other': other}
    except UnboundLocalError:
        asset_allocation_dict = {'US Stocks': us_stocks, 'Non US Stocks': non_us_stocks, 'Bonds': bonds, 'Cash': cash,
                                 'Other': other}

    return pd.DataFrame.from_dict(asset_allocation_dict, orient='index', columns=[sub_acct]).T


def ytd_return(str_list, sub_acct):
    """
    Returns the YTD Return for a given subaccount.

    :param str_list: (list) List of strings from the Morningstar page.
    :param sub_acct: (str) Sub-account name.
    :return: (pd.DataFrame) DataFrame of YTD Return.
    """
    total_returns_label = 'Total Returns'
    sec_yield_label = '7-Day SEC Yield'
    try:
        total_returns_index = str_list.index([i for i in str_list if total_returns_label in i][0])
    except IndexError:
        total_returns_index = str_list.index([i for i in str_list if sec_yield_label in i][0])
    total_returns_strings = str_list[total_returns_index:total_returns_index + 20]
    total_returns_strings = total_returns_strings[3]
    try:
        ytd_return_ = round(float(total_returns_strings.split('>')[3].split('<')[0].replace('%', '')), 4)
    except IndexError:
        try:
            ytd_return_ = round(float(total_returns_strings.split('>')[1].split('<')[0].replace('%', '')), 4)
        except ValueError:
            total_returns_strings = str_list[total_returns_index:total_returns_index + 20]
            total_returns_strings = total_returns_strings[1]
            ytd_return_ = round(float(total_returns_strings.split('>')[1].split('<')[0].replace('%', '')), 4)
    except ValueError:
        ytd_return_ = np.nan

    return pd.DataFrame(
        ytd_return_,
        index=[sub_acct],
        columns=['YTD Return%']
    ) / 100


def market_cap(str_list, sub_acct):
    """
    Returns the Market Cap for a given subaccount.

    :param str_list: (list) List of strings from the Morningstar page.
    :param sub_acct: (str) Sub-account name.
    """
    market_cap_label = 'Market Cap'
    market_cap_key = ['Giant', 'Large', 'Medium', 'Small', 'Micro']
    try:
        market_cap_index = str_list.index([i for i in str_list if market_cap_label in i][0])
        market_cap_strings = str_list[market_cap_index:market_cap_index + 2][1].split('</td>')
        market_cap_values = []
        for key in market_cap_key:
            for string in market_cap_strings:
                if key in string:
                    try:
                        market_cap_values.append(float(
                            market_cap_strings[market_cap_strings.index(string) + 1].split('>')[-1].replace(
                                '%', '')) / 100)
                    except ValueError:
                        market_cap_values.append(0)
    except IndexError:
        market_cap_values = [0, 0, 0, 0, 0]

    return pd.DataFrame(market_cap_values, columns=[sub_acct], index=market_cap_key).T


def bond_style(str_list, sub_acct):
    """
    Returns the Bond Style for a given subaccount.

    :param str_list: (list) List of strings from the Morningstar page.
    :param sub_acct: (str) Sub-account name.
    :return: (pd.DataFrame) DataFrame of Bond Style.
    """
    bond_style_label = 'Morningstar Style Box'
    bond_style_key = ['Effective Duration', 'Effective Maturity', 'Average Coupon', 'Average Price']
    try:
        bond_style_index = str_list.index([i for i in str_list if bond_style_label in i][0])
        bond_style_strings = str_list[bond_style_index:bond_style_index + 2][1].split('</td>')
        bond_style_values = []
        for key in bond_style_key:
            for string in bond_style_strings:
                if key in string:
                    try:
                        bond_style_values.append(float(
                            bond_style_strings[bond_style_strings.index(string) + 1].split('>')[-1].replace('%', '')))
                    except ValueError:
                        bond_style_values.append(0)
    except IndexError:
        bond_style_values = [0, 0, 0, 100]

    return pd.DataFrame(bond_style_values, columns=[sub_acct], index=bond_style_key).T


def classification_schema():
    """
    Returns the classification schema for all subaccounts.

    :return: (pd.DataFrame) DataFrame of classification schema.
    """
    filepath = '../data/page_contents/'
    filenames = os.listdir(filepath)
    classification_schema_dict = {}
    for filename in tqdm(filenames):
        with open('{}{}'.format(filepath, filename), encoding='utf8') as fp:
            soup = BeautifulSoup(fp, 'html.parser')
            sub_acct = filename.replace('.html', '')
            str_list = str(soup.find_all('div')).split('div')
            df = pd.concat([
                morningstar_category(str_list, sub_acct),
                total_net_assets(str_list, sub_acct),
                ytd_return(str_list, sub_acct),
                asset_allocation(str_list, sub_acct),
                top_sectors(str_list, sub_acct),
                market_cap(str_list, sub_acct),
            ], axis=1)
            classification_schema_dict[sub_acct] = df
    classification_schema_df = pd.concat(classification_schema_dict.values())
    classification_schema_df = classification_schema_df.loc[classification_schema_df.index != 0].fillna(0)
    classification_schema_df.index = classification_schema_df.index.str.replace('-', '_')
    classification_schema_df.index.name = 'Subaccount Name'

    # Save to csv
    classification_schema_df.to_csv('../data/classification_schema.csv')

    return classification_schema_df
