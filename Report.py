import quantstats as qs
import pandas as pd
import os
from collections import OrderedDict

def generate_reports(results, ticker_name, model_name, strategy_name):
    """
    Generate performance HTML reports using QuantStats. Report is salved in `/reports/` directory.

    Parameters
    ----------
    - results: List of Backtrader Cerebro run results containing analyzers.
    - ticker_name: String representing the stock ticker symbol.
    - strategy_name: String representing the name of the trading strategy.
    """


    print("\n--- Generating Performance Reports ---")
    pyfolio_results = results[0].analyzers.getbyname('pyfolio').get_analysis()

    returns_data = pyfolio_results['returns']

    if isinstance(returns_data, (OrderedDict, dict)):
        returns = pd.Series(
            list(returns_data.values()), 
            index=pd.to_datetime(list(returns_data.keys()))
        )
    elif isinstance(returns_data, pd.Series):
        returns = returns_data
    else:
        returns = pd.Series(returns_data)
        
    returns = returns.astype(float)
    returns.index = pd.to_datetime(returns.index)


    # QuantStats Report Generation
    try:
        report_dir = f"./reports/{ticker_name}"
        os.makedirs(report_dir, exist_ok=True)

        quantstats_report_filename = f"{report_dir}/{ticker_name}_{model_name}_{strategy_name}.html"

        qs.reports.html(
            returns, 
            output=quantstats_report_filename, 
            title=f"QuantStats Backtest Report - {ticker_name} - {model_name} - {strategy_name}"
        )
        print(f"Generated QuantStats Report at {quantstats_report_filename}")
        
    except Exception as e:
        print(f"Could not generate QuantStats report: {e}")