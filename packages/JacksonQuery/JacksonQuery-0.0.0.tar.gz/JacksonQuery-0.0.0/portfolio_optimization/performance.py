import warnings
import ffn
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm
from patsy import dmatrices


def performance_stats(
        backtest_timeseries, risk_free_rate=0.02, freq=252):
    """
    Computes the cumulative performance statistics based on data from the backtest_timeseries.

    :param backtest_timeseries: (pd.DataFrame) Timeseries performance of efficient frontier portfolios.
    :param risk_free_rate: (float) Optional, annualized risk-free rate, defaults to 0.02.
    :param freq: (str) Data frequency used for display purposes. Refer to pandas docs for valid freq strings.
    :return: (pd.DataFrame) DataFrame of cumulative performance statistics for all efficient frontier portfolios.
    """
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    benchmark_ticker = backtest_timeseries.columns[-1]
    perf = ffn.core.GroupStats(backtest_timeseries)
    perf.set_riskfree_rate(float(risk_free_rate))
    portfolios = backtest_timeseries.columns
    start_date = backtest_timeseries.index[0].strftime('%m-%d-%Y')
    end_date = backtest_timeseries.index[-1].strftime('%m-%d-%Y')

    cagr = None
    vol = None
    capm_b = None
    beta_b = None
    jensen_alpha_b = None
    sharpe_b = None
    treynor_b = None
    sortino_b = None
    drawdown_b = None
    ulcer_b = None
    m2_b = None
    m2_alpha_b = None
    capture_ratio_b = None

    cagrs = {}
    vols = {}
    capms = {}
    betas = {}
    jensen_alphas = {}
    appraisal_ratios = {}
    sharpes = {}
    treynors = {}
    information_ratios = {}
    sortinos = {}
    capture_ratios = {}
    drawdowns = {}
    ulcers = {}
    m2s = {}
    m2_alphas = {}

    for portfolio in portfolios[:-1]:
        p = backtest_timeseries.copy()[[portfolio, benchmark_ticker]]
        r = p.pct_change().dropna()
        p.name, r.name = portfolio, benchmark_ticker
        # return
        cagr = (1 + r).prod() ** (freq / (freq if r.shape[0] < freq else r.shape[0])) - 1
        # risk
        vol = r.std() * (freq if r.shape[0] > freq else r.shape[0]) ** 0.5
        # client regression model
        y, x = r[portfolio], r[benchmark_ticker]
        yx = pd.concat([y, x], axis=1)
        y, X = dmatrices(
            'y ~ x',
            data=yx,
            return_type='dataframe'
        )
        mod = sm.OLS(y, X)
        res = mod.fit()
        # benchmark regression model
        y_b, x_b = r[benchmark_ticker], r[benchmark_ticker]
        yx_b = pd.concat([y_b, x_b], axis=1)
        y_b, X_b = dmatrices(
            'y_b ~ x_b',
            data=yx_b,
            return_type='dataframe'
        )
        mod_b = sm.OLS(y_b, X_b)
        res_b = mod_b.fit()
        # capm
        capm = risk_free_rate + res.params.values[1] * (cagr[benchmark_ticker] - risk_free_rate)
        beta = res.params.values[1]
        capm_b = risk_free_rate + res_b.params.values[1] * (cagr[benchmark_ticker] - risk_free_rate)
        beta_b = res_b.params.values[1]
        # jensen's alpha
        non_systematic_risk = (
                vol[portfolio] ** 2
                - res.params.values[1] ** 2
                * vol[benchmark_ticker] ** 2
        )
        non_systematic_risk_b = (
                vol[benchmark_ticker] ** 2
                - res_b.params.values[1] ** 2
                * vol[benchmark_ticker] ** 2
        )
        jensen_alpha = float(cagr[portfolio] - capm)
        jensen_alpha_b = float(cagr[benchmark_ticker] - capm_b)
        # appraisal ratio
        appraisal_ratio = jensen_alpha / (non_systematic_risk ** 0.5)
        appraisal_ratio_b = jensen_alpha_b / (non_systematic_risk_b ** 0.5)
        # sharpe ratio
        sharpe = (cagr[portfolio] - risk_free_rate) / vol[portfolio]
        sharpe_b = (cagr[benchmark_ticker] - risk_free_rate) / vol[benchmark_ticker]
        # treynor ratio
        treynor = cagr[portfolio] / beta
        treynor_b = cagr[benchmark_ticker] / 1.
        # information ratio
        yx1 = yx.copy()
        yx1['Active_Return'] = yx1[portfolio] - yx1[benchmark_ticker]
        information_ratio = yx1['Active_Return'].mean() / yx1['Active_Return'].std()
        # sortino ratio
        downside_returns = (yx1[yx1[portfolio] < 0])[portfolio].values
        downside_deviation = downside_returns.std() * (freq if r.shape[0] > freq else r.shape[0]) ** 0.5
        sortino = cagr[portfolio] / downside_deviation
        downside_returns_b = (yx1[yx1[benchmark_ticker] < 0])[[benchmark_ticker]].values
        downside_deviation_b = downside_returns_b.std() * (freq if r.shape[0] > freq else r.shape[0]) ** 0.5
        sortino_b = cagr[benchmark_ticker] / downside_deviation_b
        # capture ratio
        up_returns = yx[yx[portfolio] >= 0].round(4)
        try:
            up_geo_avg = (1 + up_returns[portfolio]).prod() ** (1 / len(up_returns.index)) - 1
            up_geo_avg_b = (1 + up_returns[benchmark_ticker]).prod() ** (1 / len(up_returns.index)) - 1
            down_returns = yx[yx[portfolio] < 0].round(4)
            down_geo_avg = (1 + down_returns[portfolio]).prod() ** (1 / len(down_returns.index)) - 1
            down_geo_avg_b = (1 + down_returns[benchmark_ticker]).prod() ** (1 / len(down_returns.index)) - 1
            up_capture = up_geo_avg / up_geo_avg_b
            down_capture = down_geo_avg / down_geo_avg_b
            capture_ratio = up_capture / down_capture
            capture_ratio_b = 1.
        except ZeroDivisionError:
            capture_ratio = np.nan
            capture_ratio_b = 1.
        # drawdown
        lowest_return = yx[portfolio].min()
        drawdown = p.copy()[[portfolio]]
        drawdown = drawdown.fillna(method='ffill')
        drawdown[np.isnan(drawdown)] = -np.Inf
        roll_max = np.maximum.accumulate(drawdown)
        drawdown = drawdown / roll_max - 1.
        drawdown = drawdown.round(4)
        drawdown = drawdown.iloc[-1:, :].squeeze()
        lowest_return_b = yx[benchmark_ticker].min()
        drawdown_b = p.copy()[[benchmark_ticker]]
        drawdown_b = drawdown_b.fillna(method='ffill')
        drawdown_b[np.isnan(drawdown_b)] = -np.Inf
        roll_max_b = np.maximum.accumulate(drawdown_b)
        drawdown_b = drawdown_b / roll_max_b - 1.
        drawdown_b = drawdown_b.round(4)
        drawdown_b = drawdown_b.iloc[-1:, :].squeeze()
        # ulcer performance index
        ulcer = \
            ffn.core.to_ulcer_performance_index(
                p[[portfolio]], risk_free_rate, nperiods=freq).to_frame('ulcer_index').values[0].squeeze()
        ulcer_b = ffn.core.to_ulcer_performance_index(
            p[[benchmark_ticker]], risk_free_rate, nperiods=freq).to_frame('ulcer_index').values[0].squeeze()
        # M^2 alpha
        m2 = float(sharpe * vol[benchmark_ticker] + risk_free_rate)
        m2_b = float(sharpe_b * vol[benchmark_ticker] + risk_free_rate)
        m2_alpha = m2 - cagr[benchmark_ticker]
        m2_alpha_b = m2_b - cagr[benchmark_ticker]
        # record results
        cagrs[portfolio] = cagr[portfolio]
        vols[portfolio] = vol[portfolio]
        capms[portfolio] = capm
        betas[portfolio] = beta
        jensen_alphas[portfolio] = jensen_alpha
        appraisal_ratios[portfolio] = appraisal_ratio
        sharpes[portfolio] = sharpe
        treynors[portfolio] = treynor
        information_ratios[portfolio] = information_ratio
        sortinos[portfolio] = sortino
        capture_ratios[portfolio] = capture_ratio
        drawdowns[portfolio] = drawdown
        ulcers[portfolio] = ulcer.round(4)
        m2s[portfolio] = m2
        m2_alphas[portfolio] = m2_alpha
    cagrs[benchmark_ticker] = cagr[benchmark_ticker]
    vols[benchmark_ticker] = vol[benchmark_ticker]
    capms[benchmark_ticker] = capm_b
    betas[benchmark_ticker] = beta_b
    jensen_alphas[benchmark_ticker] = jensen_alpha_b
    appraisal_ratios[benchmark_ticker] = 0
    sharpes[benchmark_ticker] = sharpe_b
    treynors[benchmark_ticker] = treynor_b
    information_ratios[benchmark_ticker] = 0
    sortinos[benchmark_ticker] = sortino_b
    capture_ratios[benchmark_ticker] = capture_ratio_b
    drawdowns[benchmark_ticker] = drawdown_b
    ulcers[benchmark_ticker] = ulcer_b.round(4)
    m2s[benchmark_ticker] = m2_b
    m2_alphas[benchmark_ticker] = m2_alpha_b

    cols = [
        'vol',
        'beta',
        'cagr',
        'drawdown',
        'capm',
        'jensen_alpha',
        'm2',
        'm2_alpha',
        'sharpe',
        'treynor',
        'sortino',
        'info_ratio',
        'capture_ratio',
        'appraisal_ratio',
        'ulcer',
    ]

    dicts = [
        vols,
        betas,
        cagrs,
        drawdowns,
        capms,
        jensen_alphas,
        m2s,
        m2_alphas,
        sharpes,
        treynors,
        sortinos,
        information_ratios,
        capture_ratios,
        appraisal_ratios,
        ulcers,
    ]

    performance_data = pd.DataFrame(index=list(cagrs.keys()), columns=cols).reset_index()
    for col, d in zip(cols, dicts):
        performance_data[col] = performance_data['index'].map(d)
    performance_data = performance_data.set_index('index')
    performance_data.index.name = start_date + ' - ' + end_date
    return performance_data.round(4)


def plot_portfolios(backtest_timeseries):
    """
    Plot the backtest timeseries

    :param backtest_timeseries: pd.DataFrame
    :return: None
    """
    # Converting the index to datetime
    backtest_timeseries.index = pd.to_datetime(backtest_timeseries.index)

    # Create a colormap
    cmap = cm.jet  # use the colormap directly

    plt.figure(figsize=(12, 6))

    special_cols = ['Portfolio_Benchmark', 'Portfolio_Current', 'Portfolio_JNL_Mellon_S&P_500_Index']
    special_colors = ['darkred', 'black', 'purple']
    special_dict = dict(zip(special_cols, special_colors))

    for i, column in enumerate(backtest_timeseries.columns):
        if column in special_cols:
            color = special_dict[column]
        else:
            color = cmap(i / len(backtest_timeseries.columns))

        plt.plot(
            backtest_timeseries.index,
            backtest_timeseries[column],
            label=column,
            color=color
        )

    # Formatting the x-axis
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title('Portfolios over time')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.show()
