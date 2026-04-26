# Index Portfolio Tool
Tool that allows you to comfortarbly extract real data to robustly build index portfolios and compare different metrics while having some visual aid, in a fast an intuitive manner.
## Features
- Has an interactive dashboard in which can adjust parameters and extract real information regarding 100 companies of the Nasdaq 100, and the Nasdaq 100, SP500 and IPC indexes.
- Build portfolios based in benchmarks. Currently: volatility and equally weighted. 
- Build a clusterized version of the portfolio. Currently: clustering via correlation. (C++ via pybind11)
- Optimize the clusterized portfolio. Currently: Markowitz Optimization with a lamba parameter to determine priority. (C++ via pybind11)
- Display each portfolio metrics. Currently: tracking error, information ratio, sharpe ratio and volatility 
- Display a graph to visualize the tracking error.

<img width="556" height="304" alt="Adobe Express - ScreenRecording_03-22-2026 14-02-39_1" src="https://github.com/user-attachments/assets/467b342f-9d7f-439c-bc53-542e89f177de" />

## Tech Stack
| Layer        | Technology              |
|-------------|--------------------------|
| Language     | Python 3.10+, C++17     |
| Optimization | pybind11, NumPy         |
| Data         | Pandas, Pandas_datareader|
| Visualization| Streamlit, plotly   |

## Installation

1. Clone the repository
   git clone https://github.com/PraxedisJRuv/index-portfolio-tool.git

2. Create a virtual environment
   python -m venv venv
   venv\Scripts\activate

3. Install dependencies
   pip install -r requirements.txt

4. Build C++ extension (requires pybind11)
   cd cpp && python setup.py build_ext --inplace

5. There might be errors, but inside /Important notes Some errors.txt has 
many specific instructions in how to solve many issues, specially regarding 
C++ binding with python and the Eigen library used for Markowitz optimization.

## Usage
streamlit run dash.py

## Project Structure

```text
index-portfolio-tool/
├── .vscode/                # Configuration for VS Code (C++ settings)
├── Important notes/
│   ├── some_errors.txt     # Details about common errors and solutions
│   └── to_do.txt           # List of work in progress
├── Modular/
│   ├── optimization/ 
│   │   ├── Clustering/
│   │   │   └── medoids/
│   │   │       ├── kmedoids.cpp      # Clustering algorithm (C++)
│   │   │       ├── kmedoids.py       # Python wrapper for C++ functions
│   │   │       └── setup.py          # pybind11 build configuration
│   │   └── Markowitz/
│   │       ├── restricted/           # Optimization with turnover penalty
│   │       └── usual/                # Standard optimization
│   ├── benchmarks.py       # Functions regarding benchmarks and indices
│   ├── dashboard_utils.py  # Functions for recursive dashboard processing
│   ├── extraction.py       # Data extraction methods for Stooq
│   ├── inputs.py           # Stooq ticker lists for stocks and indices
│   ├── main_testing.py     # Backend pipeline testing
│   ├── manual_dashboard.py # Local data extraction for dashboard testing
│   └── portfolio.py        # Portfolio construction logic
├── dash.py                 # Streamlit dashboard entry point
├── .gitignore
├── index_t.csv             # Index data for testing 
├── License
├── README.md
├── requirements.txt
└── temporal.csv            # Stock data for testing
```

## Methodology
The currently clustering is made with the distance induced by making the correlations a norm,
wich is (2(1-Pij))^1/2 where Pij is the correlation of stock i and stock j.
The current algorithm for this minimizes the distance, which is the traditional clustering focus.
This was made with speed in mind

The Markowitz optimization is made via a gradient descent algorithm, and it's focused to solve the 
usual markowitz problem for reduced tracking error (w-wb)T Sigma(w_wb), but with a vector of expected return added. That's why there is a lambda option,
to choose the priority in which the tracking error or excess revanue is made.

Important (work in progress): the covariance matrix is calculated as usual, which is certainly not the best way since it ends up having noise, solving this is a work in progress. Current expected return vector is random between certain values, a linear regression with sickit learn was implemented, but ended removes since it could be slow and better methods are known.
