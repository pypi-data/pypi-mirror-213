import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def analyze_factor_model(factor_data, min_rank=0.7, prints=False, display_heatmap=True, figsize=(15, 6)):
    """
    Analyze factor model for subaccount selection.

    :param factor_data: (pd.DataFrame) DataFrame of factor data.
    :param min_rank: (float) Minimum rank for subaccount selection. Defaults to 0.7.
    :param prints: (bool) Print statements for analysis. Defaults to False.
    :param display_heatmap: (bool) Display heatmap of factor correlations. Defaults to True.
    :param figsize: (tuple) Figure size for heatmap. Defaults to (15, 6).
    :return: (pd.DataFrame) DataFrame of factor scores.
    """
    # Remove rows with missing values
    factor_data = factor_data[factor_data.notna().any(axis=1)]

    # Compute z-scores
    zscore = lambda x: (x - x.mean()) / x.std(ddof=1)
    zscores = factor_data.copy().dropna()
    zscores = zscores.iloc[:, 1:].transform(zscore).clip(-3, 3).fillna(0).round(4)

    # Expense factor
    expense = zscores.copy()[['Fund Expense Fee%']]
    expense = pd.DataFrame(
        expense.mean(axis=1) * -1, columns=['Expense']
    ).round(4)

    # Tenure factor
    tenure = zscores.copy()[['Manager Tenure (Years)']]
    tenure = pd.DataFrame(
        tenure.mean(axis=1), columns=['Tenure']
    ).round(4)

    # Turnover factor
    turnover = zscores.copy()[['Portfolio Turnover%']]
    turnover = pd.DataFrame(
        turnover.mean(axis=1) * -1, columns=['Turnover']
    ).round(4)

    # Factor scores
    factor_scores = pd.concat([
        factor_data['Morningstar Category'], expense, tenure, turnover
    ], axis=1)
    factor_scores['Average'] = factor_scores.iloc[:, 1:].mean(axis=1).round(4)
    factor_scores['Rank'] = factor_scores['Average'].rank(pct=True).round(4)

    # Top ranked subaccounts
    top_ranked = factor_scores[factor_scores.Rank >= min_rank].sort_index()
    if prints:
        print('Number of Top Ranked Sub-Accounts: {}'.format(len(top_ranked.index)))
    top_ranked = top_ranked.sort_values(by='Rank', ascending=False)

    # Factor correlation
    corr = factor_scores.iloc[:, 1:4].corr()

    # Display heatmap
    if display_heatmap:
        plt.figure(figsize=figsize)
        mask = np.triu(np.ones(corr.shape)).astype('bool')
        sns.heatmap(corr, mask=mask, cmap='coolwarm', annot=True)
        plt.title('Cross-Sectional Factor Correlation')

    return top_ranked
