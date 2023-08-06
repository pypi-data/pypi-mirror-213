import re
import pandas as pd
from fuzzywuzzy import process
from tika import parser as parser


def extract_financial_highlights(filepath):
    """
    Extracts financial highlights from a pdf file.

    :param filepath: (str) Path to pdf file.
    :return: (pd.DataFrame) DataFrame of financial highlights.
    """
    raw = parser.from_file(filepath)
    content = raw.get('content', '')
    lines = content.split('\n')

    str_list = [line for line in lines if line and line != ' ']

    section_name = '    FINANCIAL HIGHLIGHTS '
    end_section_name = '    APPENDIX A '

    try:
        start_index = str_list.index(section_name)
        end_index = str_list.index(end_section_name)
    except ValueError as e:
        print(f"Couldn't find the start or end of the financial highlights section: {e}")
        start_index = end_index = None

    if start_index is not None and end_index is not None:
        str_list_financial_highlights = str_list[start_index:end_index]
    else:
        str_list_financial_highlights = []

    updated_strings = [re.sub(r'\(([0-9.]+)\)', lambda m: '-' + m.group(1), re.sub(r'\([a-z]\)', '', s)) for s in
                       str_list_financial_highlights]

    columns = [
        'Period ended',
        'Net asset value, beginning of period($)',
        'Net investment income (loss)($)',
        'Net realized & unrealized gains (losses)($)',
        'Total from investment operations($)',
        'Net investment income($)',
        'Net realized gains on investment transactions($)',
        'Net asset value, end of period($)',
        'Total return(%)',
        'Net assets,end of period (in thousands)($)',
        'Portfolio turnover(%)',
        'Net expenses to average net assets(%)',
        'Total expenses to average net assets(%)',
        'Net investment income (loss) to average net assets(%)'
    ]

    def process_table(table_lines, table_columns):
        """
        Processes a table of data.

        :param table_lines: (list) List of strings.
        :param table_columns: (list) List of column names.
        :return: (pd.DataFrame) DataFrame of data.
        """
        data = [line.split() for line in table_lines]
        data = [[0 if cell == '—' else cell for cell in row] for row in data]
        table_df = pd.DataFrame(data, columns=table_columns)
        table_df.set_index('Period ended', inplace=True)

        return table_df

    class_A_dfs = {}
    class_I_dfs = {}

    current_subaccount = None
    current_class = None
    current_table = []

    for line in updated_strings:
        if line.startswith('JNL'):
            if current_subaccount is not None and current_table:
                df = process_table(current_table, columns)
                if current_class == 'A':
                    class_A_dfs[current_subaccount] = df
                elif current_class == 'I':
                    class_I_dfs[current_subaccount] = df
            current_table = []
            current_subaccount = line.strip()
        elif line.startswith('Class '):
            if current_subaccount is not None and current_table:
                df = process_table(current_table, columns)
                if current_class == 'A':
                    class_A_dfs[current_subaccount] = df
                elif current_class == 'I':
                    class_I_dfs[current_subaccount] = df
            current_table = []
            current_class = line.split()[1]
        elif line.startswith('12/31/'):
            current_table.append(line)

    if current_subaccount is not None and current_table:
        df = process_table(current_table, columns)
        if current_class == 'A':
            class_A_dfs[current_subaccount] = df
        elif current_class == 'I':
            class_I_dfs[current_subaccount] = df

    return class_A_dfs, class_I_dfs


def extract_avg_turnover(subaccount_names, filepath, class_type='A'):
    """
    Extracts the average turnover for each subaccount.

    :param subaccount_names: (list) List of subaccount names.
    :param filepath: (str) Path to pdf file.
    :param class_type: (str) Class type. Either 'A' or 'I'.
    :return: (pd.DataFrame) DataFrame of average turnover.
    """
    highlights_class_A, highlights_class_I = extract_financial_highlights(filepath)

    if class_type == 'A':
        dfs = highlights_class_A
    elif class_type == 'I':
        dfs = highlights_class_I
    else:
        raise ValueError(f"Invalid class_type: {class_type}. Expected 'A' or 'I'.")

    avg_turnover = {}

    # Update keys
    dfs = update_keys(dfs, subaccount_names)

    for subaccount, df in dfs.items():
        df['Portfolio turnover(%)'] = df['Portfolio turnover(%)'].replace('N/A', 0).astype(float)
        avg_turnover[subaccount] = df['Portfolio turnover(%)'].mean()

    avg_turnover_df = pd.DataFrame(list(avg_turnover.items()), columns=['Subaccount Name', 'Portfolio Turnover%'])
    avg_turnover_df.set_index('Subaccount Name', inplace=True)

    # Transform the values
    avg_turnover_df = avg_turnover_df.applymap(lambda x: round(float(x), 4))

    # Check for subaccount names not appearing in avg_turnover_df
    missing_subaccounts = set(subaccount_names) - set(avg_turnover_df.index)
    if missing_subaccounts:
        print("The following subaccount names do not appear in the avg_turnover_df index:")
        for name in missing_subaccounts:
            print(name)

    avg_turnover_df.index = avg_turnover_df.index.map(lambda x: x[:-5] if x.endswith(" Fund") else x)
    avg_turnover_df.index = avg_turnover_df.index.str.replace(
        '/', '_', regex=False).str.replace(
        '®', '', regex=False).str.replace(
        '.', '', regex=False).str.replace(
        ' ', '_', regex=False).str.replace(
        '-', '_', regex=False)

    avg_turnover_df.index.name = 'Subaccount Name'

    # Save the dataframe to a CSV file
    avg_turnover_df.to_csv('../data/portfolio_turnovers.csv')

    return avg_turnover_df


def find_best_match(name, subaccount_names):
    """
    Finds the best match for a subaccount name.

    :param name: (str) Subaccount name.
    :param subaccount_names: (list) List of subaccount names.
    :return: (str) Best match for subaccount name.
    """
    best_match, _ = process.extractOne(name, subaccount_names)

    return best_match


def update_keys(dfs, subaccount_names):
    """
    Updates the keys of a dictionary of DataFrames.

    :param dfs: (dict) Dictionary of DataFrames.
    :param subaccount_names: (list) List of subaccount names.
    :return: (dict) Dictionary of DataFrames with updated keys.
    """
    new_keys = [find_best_match(key, subaccount_names) for key in dfs.keys()]
    updated_dfs = {new_key: dfs[old_key] for old_key, new_key in zip(dfs.keys(), new_keys)}

    return updated_dfs
