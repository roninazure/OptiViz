OptiViz - README
================

Overview
--------
OptiViz is a Python-based visualization tool that fetches and analyzes options data for any publicly
traded stock using the Yahoo Finance API. It plots a detailed 3D Implied Volatility Surface, giving
traders and analysts a visual edge in identifying pricing anomalies and trading opportunities.

Features
--------
- 3D visualization of implied volatility by strike price and expiration.
- Supports multiple expiration dates (up to 15).
- Built with Python using yfinance, pandas, plotly, and scipy.
- Focused on intuitive analysis for options traders and quantitative researchers.
- Modular design ready for web/mobile integration.

Installation
------------
1. Clone the repo:
   git clone https://github.com/roninazure/OptiViz.git
   cd OptiViz

2. Create a virtual environment (recommended):
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

Usage
-----
Run the main script and input a valid stock ticker symbol when prompted:

   python main.py

Example input:
   Enter the stock symbol (e.g., SPY): AAPL

Project Structure
-----------------
- main.py - Entry point
- data_fetcher.py - Fetches and processes options data
- plotter.py - Plots implied volatility surfaces
- utils.py - (Coming soon) logging, config, helpers
- requirements.txt - Python dependencies
- README.md - Project documentation

Built With
----------
- yfinance - https://pypi.org/project/yfinance/
- pandas - https://pandas.pydata.org/
- numpy - https://numpy.org/
- scipy - https://scipy.org/
- plotly - https://plotly.com/python/

Coming Soon
-----------
- REST API (Flask/FastAPI)
- Web interface (Dash or React)
- Android/iOS apps
- Strategy backtesting
- Alert systems

License
-------
This project is licensed under the MIT License - see the LICENSE file for details.

Contributing
------------
Contributions are welcome! Please fork the repo and open a pull request. For major changes, please open
an issue first to discuss.

Contact
-------
Created by @roninazure – feel free to reach out or suggest features!
