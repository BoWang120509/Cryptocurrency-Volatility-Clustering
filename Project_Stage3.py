import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

#-----------------------------------------
# Step 3. Clustering analysis using KMean
#-----------------------------------------

FEATURE_FILE = "features_by_month.csv"
OUTPUT_FILE = "features_with_clusters.csv"

# ============ LOAD DATA ============
df = pd.read_csv(FEATURE_FILE)

# Features that are used for clustering
features = df.drop(columns=["symbol", "month", "extreme_flag"])

# Standrize. Some features was log but the distributions are not complied with mean = 0 and variance = 1.
# For example, the jump frequency and the buy ratio. 
# Also, the kmean results can be disturbed by some features with large numerical scales, the centre will be dominated by those features.
scaler = StandardScaler()
X_scaled = scaler.fit_transform(features)

# ============ Clustering + silhouette ============
# The minimum k should be 3 since 2 will devide the currencies into only 2 groups.
# Based on the articles and GPT, k>6 situation is hard to be explained and each cluster is unstable.
# Large k will devide the pool into more clusters, each will only contain dozen of samples, some of them might be isolated.
k_range = range(3, 7)
sil_scores = []
all_labels = {}

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=50, n_init=20)
    labels = kmeans.fit_predict(X_scaled)
    score = silhouette_score(X_scaled, labels)
    sil_scores.append(score)
    all_labels[k] = labels
    print(f"k = {k}, silhouette score = {score:.4f}")

best_k = k_range[np.argmax(sil_scores)]
print(f"\nThe best number of clustering: k = {best_k}, silhouette = {max(sil_scores):.4f}")
df["cluster_id"] = all_labels[best_k]

df.to_csv(OUTPUT_FILE, index=False)
print("Saved the clustering file", OUTPUT_FILE)

# ============ Figures ============
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

df["pca1"] = X_pca[:, 0]
df["pca2"] = X_pca[:, 1]

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="pca1", y="pca2", hue="cluster_id", style="extreme_flag",
                palette="tab10", s=50, alpha=0.8)
plt.title(f"PCA 2D Scatter Plot (k = {best_k})")
plt.legend(title="Cluster")
plt.tight_layout()
plt.savefig("cluster_scatter_pca.png")





# ======== Additional Figures for Cluster Analysis ========

# 1. Silhouette Score vs K
plt.figure(figsize=(8, 5))
plt.plot(list(k_range), sil_scores, marker='o')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Score vs K')
plt.grid(True)
plt.tight_layout()
plt.savefig("silhouette_score_vs_k.png")
print("✅ Saved silhouette score curve")

# 2. Cluster Feature Radar Plot
from sklearn.preprocessing import StandardScaler

cluster_means = df.groupby('cluster_id')[features.columns].mean()

scaler = StandardScaler()
cluster_means_scaled = pd.DataFrame(
    scaler.fit_transform(cluster_means),
    index=cluster_means.index,
    columns=cluster_means.columns
)

# Scaled Radar Plot
labels = features.columns.tolist()
num_vars = len(labels)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]

plt.figure(figsize=(8, 8))
ax = plt.subplot(polar=True)

for cluster_id, row in cluster_means_scaled.iterrows():
    values = row.tolist()
    values += values[:1]
    ax.plot(angles, values, label=f'Cluster {cluster_id}')
    ax.fill(angles, values, alpha=0.2)

ax.set_thetagrids(np.degrees(angles[:-1]), labels)
plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
plt.title("Cluster Feature Radar Plot (Standardized)")
plt.tight_layout()
plt.savefig("cluster_radar_plot_standardized.png")
print("✅ Saved radar plot")


# 3. Barplot of Extreme Flag Distribution per Cluster
plt.figure(figsize=(8, 5))
extreme_counts = df[df['extreme_flag'] == 1]['cluster_id'].value_counts().sort_index()
sns.barplot(x=extreme_counts.index, y=extreme_counts.values)
plt.xlabel("Cluster ID")
plt.ylabel("Number of Extreme Coins")
plt.title("Distribution of Extreme Coins across Clusters")
plt.tight_layout()
plt.savefig("extreme_coins_distribution.png")
print("✅ Saved extreme coins distribution barplot")
