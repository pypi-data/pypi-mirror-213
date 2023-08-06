import datetime
import re
import pandas as pd
import numpy as np


def extract_tenures(sublists):
    """
    Extracts the portfolio manager names, start dates, and titles from the sublists.

    :param sublists: (list) List of sublists from the Jackson Holdings website.
    :return: (dict) Dictionary of portfolio manager names, start dates, and titles.
    """
    avg_tenures = {}
    for sublist in sublists:
        # Extract the subaccount name from the sublist
        subaccount_name = sublist[0]  # Update this depending on where the name is in your sublist

        # Check if 'Portfolio Manager' or 'Portfolio Managers' is in the sublist
        if not any(s in sublist for s in ['Portfolio Manager: ', 'Portfolio Managers: ']):
            print(f"No 'Portfolio Manager' section found in subaccount: {subaccount_name}")
            avg_tenures[subaccount_name] = None
            continue

        # Default values
        start_index = None
        end_index = None

        # Find the indices of 'Portfolio Managers: ' or 'Portfolio Manager: ' and 'Purchase and Redemption of Fund
        # Shares  '
        try:
            if 'Portfolio Managers: ' in sublist:
                start_index = sublist.index('Portfolio Managers: ') + 1
            else:
                start_index = sublist.index('Portfolio Manager: ') + 1
            end_index = sublist.index('Purchase and Redemption of Fund Shares  ')
        except ValueError:
            print("Couldn't find the start or end of the table.")

        # Get the lines that form the table, joining lines that end with a comma
        raw_table_lines = sublist[start_index:end_index]
        table_lines = []
        for line in raw_table_lines:
            if table_lines and line.endswith(','):
                table_lines[-1] += ' ' + line
            else:
                table_lines.append(line)

        # Initialize empty lists to store the data
        names = []
        joined_dates = []
        titles = []

        # Initialize a regex pattern for matching
        pattern = r"(?P<name>[\w\s\.]+)\s*(?P<date>[A-Za-z]*\s*\d{4}\*?)\s+(?P<title>.+)"

        for line in table_lines:
            match = re.search(pattern, line.strip())
            if match:
                full_name = match.group('name').strip()
                if full_name:  # Only proceed if full_name is not empty
                    date_str = match.group('date').strip().replace('*', '')  # Remove '*' character
                    title = match.group('title').strip()

                    # Check if a month is present in the name field
                    name_parts = full_name.split()
                    if name_parts[-1] in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                                          'September', 'October', 'November', 'December']:
                        # If the last part of the name is a month, join it with the date
                        date_str = name_parts[-1] + ' ' + date_str
                        name = ' '.join(name_parts[:-1])  # Remove the month from the name
                    else:
                        name = full_name

                    # Check if a month is present in the date string
                    if len(date_str.split()) > 1:  # If there's a month and a year
                        joined_dates.append(datetime.datetime.strptime(date_str, '%B %Y'))
                    else:  # If only year is present
                        joined_dates.append(datetime.datetime.strptime('July ' + date_str, '%B %Y'))

                    names.append(name)
                    titles.append(title)

        # Create a dataframe from the data
        df = pd.DataFrame({
            'Name': names,
            'Joined Fund Management Team In': joined_dates,
            'Title': titles
        })

        # Calculate the tenure in years including partial years and get the average
        today = datetime.datetime.now()
        df['Tenure'] = (today - df['Joined Fund Management Team In']).dt.days / 365.25
        avg_tenure = df['Tenure'].mean()

        # Store the average tenure in the dictionary
        avg_tenures[subaccount_name] = avg_tenure

    # Convert the dictionary into a DataFrame
    tenure_df = pd.DataFrame.from_dict(avg_tenures, orient='index', columns=['Manager Tenure (Years)'])

    # Replace None values with NaN
    tenure_df.replace({np.nan: tenure_df.squeeze().mean()}, inplace=True)

    tenure_df.index = tenure_df.index.map(lambda x: x[:-5] if x.endswith(" Fund") else x)
    tenure_df.index = tenure_df.index.str.replace(
        '/', '_', regex=False).str.replace(
        '®', '', regex=False).str.replace(
        '.', '', regex=False).str.replace(
        ' ', '_', regex=False).str.replace(
        '-', '_', regex=False)

    tenure_df.index.name = 'Subaccount Name'

    tenure_df = round(tenure_df, 2)

    # Save the dataframe to a CSV file
    tenure_df.to_csv('../data/manager_tenures.csv')

    return tenure_df
