# Cryptocurrency-Volatility-Clustering

# Project Overview
This project focuses on analyzing the volatility patterns of over 1000 cryptocurrency pairs using minute-level trading data.
The goal is to cluster different cryptocurrencies based on their volatility, extreme behavior, and trading activity,
thereby identifying distinct market behavior groups within the crypto ecosystem.
The full pipeline includes:
1. Data extraction and cleaning from raw zipped parquet files
2. Feature engineering on volatility, jump frequency, skewness, kurtosis, and trading volume dynamics
3. Extreme coin labeling based on statistical behavior
4. Dimensionality reduction (PCA) and clustering analysis (KMeans)
5. 5.Multiple visualization outputs for cluster behavior interpretation
6. Demonstration of Bash command simulation and Spark RDD/DataFrame processing
7. All code is executed inside a Docker environment for full reproducibility

