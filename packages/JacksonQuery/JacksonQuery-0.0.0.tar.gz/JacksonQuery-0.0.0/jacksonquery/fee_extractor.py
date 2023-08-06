import re
import pandas as pd


def extract_fees(string_list):
    """
    Extracts the management fee from the subaccount list.

    :param string_list: (list) List of strings from the subaccount list.
    :return: (dict) Dictionary of subaccount names and management fees.
    """
    table_dict = {}
    subaccount_name = string_list[0].strip()  # strip the subaccount name as well
    table_dict[subaccount_name] = {}

    class_a_started = False
    class_i_started = False

    for line in string_list[3:]:
        line = line.strip()  # strip the line here
        if 'Class A' in line:
            class_a_started = True
            class_i_started = False
            continue
        elif 'Class I' in line:
            if not class_a_started:
                class_i_started = True
            else:
                break
        if class_a_started or class_i_started:
            if 'Management Fee' in line:
                fee = next((float(s.strip('%')) for s in line.split() if s.endswith('%')), None)
                if fee is not None:
                    table_dict[subaccount_name]['Management Fee'] = fee
            elif 'Distribution and/or Service (12b-1) Fees' in line:
                fee = next((float(s.strip('%')) for s in line.split() if s.endswith('%')), None)
                if fee is not None:
                    table_dict[subaccount_name]['12b-1 Fees'] = fee
            elif 'Other Expenses' in line and 'Administrative Fee' not in line:
                fee = next((float(s.strip('%')) for s in line.split() if s.endswith('%')), None)
                if fee is not None:
                    table_dict[subaccount_name]['Other Expenses'] = fee
            elif 'Total Annual Fund Operating Expenses' in line and 'After Waiver/Reimbursement' not in line:
                fee = next((float(s.strip('%')) for s in line.split() if s.endswith('%')), None)
                if fee is not None:
                    table_dict[subaccount_name]['Total Annual Fund Operating Expenses'] = fee
            elif 'Less Waiver/Reimbursement' in line:
                fee = next((float(s.strip('%')) for s in line.split() if s.endswith('%')), None)
                if fee is not None:
                    table_dict[subaccount_name]['Waiver/Reimbursement'] = fee
            elif 'Acquired Fund Fees and Expenses' in line:
                fee = next((float(s.strip('%')) for s in line.split() if s.endswith('%')), None)
                if fee is not None:
                    table_dict[subaccount_name]['Acquired Fund Fees and Expenses'] = fee
            elif re.search(r'Total Annual Fund Operating Expenses.*After Waiver/Reimbursement', line):
                fee = next((float(s.strip('%')) for s in line.split() if s.endswith('%')), None)
                if fee is not None:
                    table_dict[subaccount_name]['Total Expenses After Waiver/Reimbursement'] = fee

    return table_dict


def extract_management_fee(sublists):
    """
    Extracts the management fee from the subaccount list.

    :param sublists: (list) List of subaccount lists.
    :return: (dict) Dictionary of subaccount names and management fees.
    """

    # Create a dictionary to store the extracted fees
    fee_dict = {}
    for sublist in sublists:
        fee_info = extract_fees(sublist)
        fee_dict.update(fee_info)

    # Create a DataFrame from the dictionary
    management_fees = pd.DataFrame.from_dict(fee_dict, orient='index')

    # After creating the DataFrame, fill the NaN values with specific conditions
    management_fees['Waiver/Reimbursement'] = management_fees['Waiver/Reimbursement'].fillna(0)
    management_fees['Acquired Fund Fees and Expenses'] = management_fees['Acquired Fund Fees and Expenses'].fillna(0)
    management_fees['Total Expenses After Waiver/Reimbursement'] = management_fees['Total Expenses After '
                                                                                   'Waiver/Reimbursement'].fillna(
        management_fees['Total Annual Fund Operating Expenses'])

    # Round the values in the DataFrame to 4 decimal places
    management_fees = management_fees.round(4)

    # Format subaccount names in the index
    management_fees.index = management_fees.index.map(lambda x: x[:-5] if x.endswith(" Fund") else x)
    management_fees.index = management_fees.index.str.replace(
        '/', '_', regex=False).str.replace(
        '®', '', regex=False).str.replace(
        '.', '', regex=False).str.replace(
        ' ', '_', regex=False).str.replace(
        '-', '_', regex=False)

    management_fees.index.name = 'Subaccount Name'

    # Save the management_fees dataframe to csv file
    management_fees.to_csv('../data/management_fees.csv')

    return management_fees
