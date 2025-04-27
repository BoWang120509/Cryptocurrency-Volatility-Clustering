# Cryptocurrency-Volatility-Clustering

Project Overview
This project focuses on analyzing the volatility patterns of over 1000 cryptocurrency pairs using minute-level trading data.

Link to the creator for the dataset (!!! Important !!!) ---- https://www.kaggle.com/datasets/jorijnsmit/binance-full-history/data?select=1INCH-BUSD.parquet

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

Technologies Used
1. Python 3.10
2. pandas, numpy, pyarrow, scikit-learn, matplotlib, seaborn, tqdm
3. Apache Spark 3.4.1 (for RDD/DataFrame demonstration)
4. Docker Desktop (containerized environment)
5. Bash commands simulation (zip file scanning)

Key Outputs
1. "coin_metadata_usdt.csv": Filtered list of major USDT pairs
2. "features_by_month.csv": Engineered feature dataset per month
3. "features_with_clusters.csv": Cluster assignments for all samples
4. "cluster_scatter_pca.png": PCA 2D scatter plot with cluster coloring
5. "silhouette_score_vs_k.png": Silhouette scores for k=3-6
6. "cluster_radar_plot_standardized.png": Radar charts comparing cluster features
7. "extreme_coins_distribution.png": Barplot showing extreme coins across clusters

Project Highlights
1. Big Data Handling: Direct processing of minute-level data for over 1000 crypto pairs
2. Tidy Data Practice: Restructured datasets to fit tidy data principles
3. MapReduce & Spark Usage: Demonstrated both concepts in the workflow
4. Clustering Validation: Silhouette score optimization
5. Comprehensive Visual Analysis: PCA, boxplots, radar charts, and barplots
6. Fully Reproducible: Complete environment documented and executed within Docker
