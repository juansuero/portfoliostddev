# Portfolio Standard Deviation Calculator

This Streamlit application allows users to calculate the standard deviation of their portfolio. Users can input their holding tickers and the number of shares they own for each. The application fetches historical stock data, calculates the daily standard deviation for the holdings, creates a correlation matrix to show how well diversified the portfolio is, and displays the standard deviation of the portfolio.

## Features

- Input holding tickers and number of shares.
- Select the period for historical data.
- Calculate daily standard deviation of the portfolio.
- Display a correlation matrix as a heatmap.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```

2. Install the required libraries:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the Streamlit app:
    ```sh
    streamlit run stddev.py
    ```

2. Open your web browser and go to `http://localhost:8501`.

3. Enter your holding tickers (comma separated) and the number of shares for each ticker (comma separated).

4. Select the period for historical data.

5. Click the "Calculate" button to see the daily standard deviation of your portfolio and the correlation matrix.

## Dependencies

- streamlit
- yfinance
- pandas
- numpy
- seaborn
- matplotlib

## License

This project is licensed under the MIT License.