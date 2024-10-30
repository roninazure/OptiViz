import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from scipy.interpolate import griddata

def get_stock_symbol():
    """Prompt the user to enter a stock symbol and return it in uppercase."""
    return input("Enter the stock symbol (e.g., SPY): ").strip().upper()

def fetch_options_data(ticker_symbol):
    """
    Fetch options data for the given ticker symbol.
    Returns a tuple (strike_prices, times_to_expiration, implied_volatilities).
    """
    stock = yf.Ticker(ticker_symbol)
    try:
        expiration_dates = stock.options
        print(f"Found {len(expiration_dates)} expiration dates for {ticker_symbol}.")
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")
        return [], [], []

    # Initialize lists for data collection
    strike_prices = []
    times_to_expiration = []
    implied_volatilities = []

    # Fetch options data for each expiration date
    for expiration in expiration_dates[:15]:  # Limit to 15 dates for simplicity
        try:
            options_chain = stock.option_chain(expiration)
        except Exception as e:
            print(f"Error fetching options for {expiration}: {e}")
            continue

        # Calculate time to expiration in months
        time_to_expiration = round((pd.to_datetime(expiration) - pd.Timestamp.now()).days / 30)

        # Gather data from both call and put options
        for option_type in [options_chain.calls, options_chain.puts]:
            for _, row in option_type.iterrows():
                if not np.isnan(row['impliedVolatility']) and row['impliedVolatility'] <= 1:  # Limit to 100%
                    strike_prices.append(row['strike'])
                    times_to_expiration.append(time_to_expiration)
                    implied_volatilities.append(row['impliedVolatility'] * 100)  # Convert to percentage

    return strike_prices, times_to_expiration, implied_volatilities

def create_volatility_surface(ticker_symbol, strike_prices, times_to_expiration, implied_volatilities):
    """
    Generate and display a 3D surface plot of the implied volatility for a given ticker symbol.
    """
    # Convert data to a DataFrame for easier manipulation
    df = pd.DataFrame({
        'Strike Price': strike_prices,
        'Time to Expiration (months)': times_to_expiration,
        'Implied Volatility (%)': implied_volatilities
    })

    # Find and display the maximum time to expiration
    max_months = df['Time to Expiration (months)'].max()
    max_weeks = max_months * 4  # Approximate conversion from months to weeks
    print(f"The chart goes out to approximately {max_months:.1f} months ({max_weeks:.1f} weeks) in the future.")

    # Define custom y-axis range for Strike Price (450 to 750)
    y_min, y_max = 450, 750

    # Interpolate missing values in a grid format
    strike_grid = np.linspace(y_min, y_max, 30)
    time_grid = np.round(np.linspace(df['Time to Expiration (months)'].min(), 
                                     df['Time to Expiration (months)'].max(), 10), 0)
    X, Y = np.meshgrid(time_grid, strike_grid)

    Z = griddata(
        (df['Time to Expiration (months)'], df['Strike Price']),
        df['Implied Volatility (%)'],
        (X, Y),
        method='linear'
    )

    # Custom color scale for higher volatility in red
    custom_colorscale = [
        [0, "blue"],      # Low volatility (0%) - blue
        [0.25, "green"],  # Intermediate low
        [0.5, "yellow"],  # Mid-range volatility (50%) - yellow
        [0.75, "orange"], # Higher
        [1, "red"]        # High volatility (100%) - red
    ]

    # Plot the interpolated surface
    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale=custom_colorscale, opacity=0.8),
                          go.Contour(z=Z, x=X, y=Y, contours=dict(showlabels=True), showscale=False)])

    # Customize layout to show axis values and titles for all axes
    fig.update_layout(
        title=f'Implied Volatility Surface for {ticker_symbol} Options',
        scene=dict(
            xaxis=dict(
                title='Time to Expiration (months)',
                tickvals=np.arange(df['Time to Expiration (months)'].min(), 
                                   df['Time to Expiration (months)'].max() + 1, 3),  # Display every 3 months
                tickformat='.0f',  # Display whole numbers
                showticklabels=True
            ),
            yaxis=dict(
                title='Strike Price ($)',
                range=[y_min, y_max],
                tickvals=np.arange(y_min, y_max + 50, 50),  # Tick every $50
                tickformat='.0f',
                showticklabels=True
            ),
            zaxis=dict(
                title='Implied Volatility (%)',
                nticks=10,
                range=[0, 100],
                tickformat='.0f',
                showticklabels=True
            ),
            aspectratio=dict(x=1, y=1, z=0.5)
        ),
        autosize=True
    )

    fig.show()

def main():
    """Main function to drive the implied volatility surface plot generation."""
    # Step 1: Get stock symbol from the user
    ticker_symbol = get_stock_symbol()

    # Step 2: Fetch options data
    strike_prices, times_to_expiration, implied_volatilities = fetch_options_data(ticker_symbol)
    
    # Check if data was successfully retrieved
    if not strike_prices:
        print("No data found. Please check the symbol and try again.")
        return

    # Step 3: Create and display the volatility surface plot
    create_volatility_surface(ticker_symbol, strike_prices, times_to_expiration, implied_volatilities)

# Run the main function
if __name__ == "__main__":
    main()
