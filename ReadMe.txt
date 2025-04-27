1. Project Introduction
This project studies the volatility patterns of various cryptocurrencies based on minute-level data.
It performs feature engineering (volatility, jump frequency, transaction behavior),
clustering analysis (KMeans), and multiple visualization outputs.
The project is executed fully in a Docker environment, with additional Bash and Spark demonstrations for Data Processing techniques.

2. Environment
Docker Desktop
	version 28.0.4, build b8034c0
	Container Name: dreamy_volhard
	Container ID: dde8e5fa1940626b3c057c5d1326793c48aec34942d3390a7be5efa2d26d86e3
	Image Name: project810
Python 3.10
PySpark
pandas, numpy, matplotlib, seaborn, tqdm, scikit-learn, pyarrow

3. Build Instruction
Open terminal, navigate to project folder, then run: docker build -t project810 .
PS. You can change the name "project810" if you want

4. Run Instruction
After build success, run container: docker run -it -v "(where you saved the folder)" :/workspace project810
Enter bash shell, then run:
python Bash_Scan_Zip.py
python Project_Stage1.py
python Project_Stage2.py
python Project_Stage3.py
python Spark_Sample_Analysis.py

5. Execution Order
Step	Script	                            Purpose
1	Bash_Scan_Zip.py	            Bash command simulation (zipfile scan)
2	Project_Stage1.py	            Cryptocurrency data selection and preparation
3	Project_Stage2.py	            Feature engineering (volatility, jump, transaction)
4	Project_Stage3.py	            Clustering analysis (KMeans + visualizations)
5	Spark_Sample_Analysis.py	    Spark RDD and DataFrame demonstration

6. Output Files
File	                                    Description
coin_metadata_usdt.csv	                    Selected currencies after filtering
features_by_month.csv	                    Feature dataset for clustering
features_with_clusters.csv	            Feature dataset with cluster_id assigned
cluster_scatter_pca.png	                    PCA scatter plot colored by cluster
silhouette_score_vs_k.png	            Silhouette score vs k plot
cluster_radar_plot_standardized.png	    Cluster feature radar chart
boxplot_log_return_std.png	            Boxplot of log return std across clusters
extreme_coins_distribution.png	            Bar plot of extreme coins distribution

7. Environment Dependencies (pip_list.txt)
Full pip environment dependency list can be found in the file pip_list.txt.

8. Notes
Spark_Sample_Analysis.py is for demonstrating Spark RDD/DataFrame capabilities.
The main project data processing and clustering are implemented using pandas and scikit-learn.