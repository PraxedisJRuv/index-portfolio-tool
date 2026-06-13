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
├── Important notes/
│   ├── Some errors.txt     # Common issues and troubleshooting notes
│   └── to do.txt           # Current work in progress
├── modular/
│   ├── modules/
│   │   ├── benchmarks.py                 # Benchmark-related helpers and index logic
│   │   ├── dashboard_mix_clusters.py     # Mixed-cluster dashboard utilities
│   │   ├── dashboard_utils.py            # Dashboard processing helpers
│   │   ├── extraction.py                 # Data extraction utilities
│   │   ├── Inputs.py                     # Ticker lists and inputs
│   │   ├── portfolio.py                  # Portfolio construction logic
│   │   └── optimization/
│   │       ├── algorithm_pseudocode.md   # Description of the bi-objective clustering
│   │       ├── cluster_search.py         # Bi-objective cluster algorithm
│   │       ├── cluster_search_utils.py   # Pipeline integration of cluster search
│   │       ├── estimate.py               # Estimation helpers (returns)
│   │       ├── Clustering/
│   │       │   ├── medoids.cpp           # C++ clustering implementation
│   │       │   ├── multi_objective.py    # Multi-objective clustering logic
│   │       │   ├── cluster/
│   │       │   │   ├── cluster_assignations.cpp   # C++ cluster centroid assignment
│   │       │   │   ├── kmedoids.py
│   │       │   │   ├── setup.py
│   │       │   │   └── test.py
│   │       │   └── medoids/
│   │       │       ├── kmedoids.cpp      # C++ k-medoids implementation
│   │       │       ├── kmedoids.py
│   │       │       ├── setup.py
│   │       │       └── test.py
│   │       └── Markowitz/
│   │           ├── restricted/
│   │           │   ├── markowitz.cpp
│   │           │   ├── markowitz.py
│   │           │   ├── setup.py
│   │           │   └── test.py
│   │           └── usual/
│   │               ├── markowitz.cpp
│   │               ├── markowitz.py
│   │               ├── setup.py
│   │               └── test.py
│   └── testing/
│       ├── main_testing.py               # Backend/testing pipeline
│       ├── manual_dashboard.py           # Local dashboard testing helpers
│       ├── regression.py                 # Regression testing
│       ├── regression2.py                # Additional regression tests
│       └── test_extraction.py            # Data extraction tests
├── resources/
│   ├── index_t.csv                       # Sample index dataset
│   ├── temporal.csv                      # Sample temporal stock data
│   └── Usable.csv                        # Additional sample dataset
│ 
├── dash.py                               # Streamlit dashboard entry point
├── mixed_cluster_dash.py                 # Alternate mixed-cluster dashboard script
├── LICENSE
├── README.md
└── requirements.txt
```

## Methodology
The currently clustering is made with the distance induced by making the correlations a norm,
wich is (2(1-Pij))^1/2 where Pij is the correlation of stock i and stock j.
The current algorithm for this minimizes the distance, which is the traditional clustering focus.
This was made with speed in mind

The Markowitz optimization is made via a gradient descent algorithm, and it's focused to solve the 
usual markowitz problem for reduced tracking error (w-wb)T Sigma(w_wb), but with a vector of expected return added. That's why there is a lambda option,
to choose the priority in which the tracking error or excess revanue is made.

The bi-objetcive clustering option works misxing two clusterization results and returning 
among the three the clusters in between them at the midle of their change to one into the other. It chooses the one which optemizes a certain metric, in this case minimizing the distance to any of the options was chosen for a quicker result, but the ideal would be minmizing the tracking error. THe details on how the algorithm works can be found at algortihm_pseudocode.md file 

Important (work in progress): the covariance matrix is calculated as usual, which is certainly not the best way since it ends up having noise, solving this is a work in progress. 
