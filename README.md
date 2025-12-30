# SimpBackTest
This project is a backtesting pipeline that allows users to test simple algorithmic trading strategies with ease. It contains all necessary steps for backtesting, including data fetching, feature generation, model selection, signal creation, and report generation. The project is highly modularized and compatible with sklearn and pandas, so users can modify or import strategies without overhead.

Trading signals are saved and loaded to Backtrader for backtesting, and quantStats is responsible for generating an HTML report that contains all testing metrics and graphs like the one below. There is also an automated Action workflow that generates a [**static webpage**](https://aaron3963.github.io/SimpBackTest/) which contains all the reports generated.

<img width="1738" height="1109" alt="image" src="https://github.com/user-attachments/assets/cae97f3c-6d0c-47d9-9dd4-1334f1c261ff" />




## Environment Setup
This project used Python 3.12, with the following packages installed:

| Package | Version |
|---------|---------|
| yfinance | 0.2.66 |
| pandas | 2.3.3 |
| numpy | 1.26.4 |
| sklearn | 1.7.2 |
| backtrader | 1.9.78.123 |
| quantstats | 0.0.77 |

## How to Run
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required packages as listed in the [Environment Setup](#environment-setup) section.
4. Run the main script or Jupyter notebook to start the analysis.

## Project Structure
`main.ipynb`: The main Jupyter notebook containing the analysis and model implementation.

`CustomCSVData.py`: Custom data feed class for Backtrader.

`Strategies.py`: Contains the trading strategies implemented.

`Report.py`: Generates performance reports and visualizations.

## File Structures
`./data/`: Contains raw and processed data files.

`./data/predictions/`: Stores prediction results for different models.

`./reports/`: Contains generated strategy performance reports and prediction metrics for each ticker.
