Portfolio Simulator
===================

This is a portfolio simulator that uses historical market data to simulate investment returns and analyze portfolio performance. The program is written in Python and uses the following libraries:

    Pandas
    Numpy
    Matplotlib
    Tkinter

Installation
------------

To install the program, you can download the source code from the GitHub repository and run it using Python. Alternatively, you can use PyInstaller to create an executable file that can be run on any computer without needing to install Python or any additional libraries.

To create an executable file using PyInstaller, navigate to the directory containing the source code and run the following command:

```css
pyinstaller --onefile main.py

This will create a single executable file called "main.exe" in the "dist" directory.

Usage
-----

To use the program, you will need to provide a CSV file containing historical market data for the assets you wish to analyze. The file should have the following columns:

    Date
    Ticker
    Price

Once you have a CSV file with the required data, you can launch the program by running "main.py" or "main.exe". The program will prompt you to select the CSV file you wish to analyze, and then allow you to choose which assets to include in your portfolio.

After selecting your assets, the program will generate a series of statistics and visualizations to help you analyze portfolio performance. These include:

    Cumulative portfolio returns
    Individual asset returns
    Portfolio risk and volatility
    Kurtosis and skewness
    And more!

Contributions
-------------

If you would like to contribute to this project, feel free to submit a pull request on GitHub or contact me directly. Any contributions or feedback are greatly appreciated!
