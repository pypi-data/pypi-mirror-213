import re
import pandas as pd


def extract_returns(sublists, subaccount_names):
    """
    Extracts returns from subaccount sublists.

    :param sublists: (list) List of subaccount sublists.
    :param subaccount_names: (list) List of subaccount names.
    :return: (pd.DataFrame) DataFrame of returns.
    """
    dfs_A = []
    dfs_I = []

    for sublist in sublists:
        subaccount_pattern = r"JNL\/?[a-zA-Z0-9\s®\-\&\.]+"
        match = re.search(subaccount_pattern, sublist[0], re.DOTALL)
        subaccount = match.group().strip() if match else 'No Subaccount Found'

        indices = [i for i, s in enumerate(sublist) if 'Best Quarter' in s]

        if len(indices) == 2:
            class_A_list = sublist[sublist.index('Annual Total Returns as of December 31 '):indices[0]]
            class_I_list = sublist[indices[0]:indices[1]]
        elif len(indices) == 1:
            class_A_list = []
            class_I_list = sublist[sublist.index('Annual Total Returns as of December 31 '):indices[0]]
        else:
            class_A_list = []
            class_I_list = []

        year_pattern = r"\b20\d{2}\b"
        return_pattern = r"(-?\d+\.\d{2}%)"

        years_A = re.findall(year_pattern, " ".join(class_A_list))
        returns_A = [float(r.strip('%')) for r in re.findall(return_pattern, " ".join(class_A_list))][:len(years_A)]

        class_I_returns_str = " ".join(class_I_list)
        if "Class I" in class_I_returns_str:
            class_I_returns_str = class_I_returns_str.split("Class I")[1]
            years_I = re.findall(year_pattern, class_I_returns_str)
            returns_I = [float(r.strip('%')) for r in re.findall(return_pattern, class_I_returns_str)[:len(years_I)]]
        else:
            continue

        if not years_A and not years_I:
            continue

        if years_A and returns_A:
            df_A = pd.DataFrame({
                'Year': years_A,
                subaccount + ' Class A Returns': returns_A,
            })
            df_A.set_index('Year', inplace=True)
            dfs_A.append(df_A)

        if years_I and returns_I:
            df_I = pd.DataFrame({
                'Year': years_I,
                subaccount + ' Class I Returns': returns_I,
            })
            df_I.set_index('Year', inplace=True)
            dfs_I.append(df_I)

    final_df_A = pd.concat(dfs_A, axis=1)
    final_df_I = pd.concat(dfs_I, axis=1)

    final_df_A.columns = final_df_A.columns.str.replace(r' Class A Returns| Class I Returns', '', regex=True)
    final_df_I.columns = final_df_I.columns.str.replace(r' Class A Returns| Class I Returns', '', regex=True)

    subaccounts_in_A = set(final_df_A.columns.str.replace(r' Class A Returns| Class I Returns', '', regex=True))
    subaccounts_in_I = set(final_df_I.columns.str.replace(r' Class A Returns| Class I Returns', '', regex=True))

    missing_subaccounts_A = set(subaccount_names) - subaccounts_in_A
    missing_subaccounts_I = set(subaccount_names) - subaccounts_in_I

    print("Subaccounts missing from Class A dataframe:", missing_subaccounts_A)
    print("Subaccounts missing from Class I dataframe:", missing_subaccounts_I)

    # Rename the final dataframes
    returns_class_a = final_df_A
    returns_class_i = final_df_I

    # Convert the dataframe values to float, divide by 100 and round to 4 decimals
    returns_class_a = returns_class_a.applymap(lambda x: round(float(x)/100, 4))
    returns_class_i = returns_class_i.applymap(lambda x: round(float(x)/100, 4))

    returns_class_a.columns = returns_class_a.columns.map(lambda x: x[:-5] if x.endswith(" Fund") else x)
    returns_class_i.columns = returns_class_i.columns.map(lambda x: x[:-5] if x.endswith(" Fund") else x)

    returns_class_a.columns = returns_class_a.columns.str.replace(
        '/', '_', regex=False).str.replace(
        '®', '', regex=False).str.replace(
        '.', '', regex=False).str.replace(
        ' ', '_', regex=False).str.replace(
        '-', '_', regex=False)
    returns_class_i.columns = returns_class_i.columns.str.replace(
        '/', '_', regex=False).str.replace(
        '®', '', regex=False).str.replace(
        '.', '', regex=False).str.replace(
        ' ', '_', regex=False).str.replace(
        '-', '_', regex=False)

    returns_class_a.columns = returns_class_a.columns.map(lambda x: x[:-5] if x.endswith(" Fund") else x)
    returns_class_i.columns = returns_class_i.columns.map(lambda x: x[:-5] if x.endswith(" Fund") else x)

    # Save to csv file
    returns_class_a.to_csv('../data/returns_class_a.csv')
    returns_class_i.to_csv('../data/returns_class_i.csv')

    return returns_class_a, returns_class_i
