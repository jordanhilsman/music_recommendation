import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler



music_df = pd.read_csv('spotify_album_data.csv')
print(music_df.columns)
X = music_df.drop(columns=['name', 'year', 'album_id', 'artist'], inplace=False)


scaler = StandardScaler()
scaler.fit(X)
X_scaled = scaler.transform(X)

pca = PCA(n_components=2)

pca.fit(X_scaled)
X_pca = pca.transform(X_scaled)

kmeans = KMeans(n_clusters=4)
kmeans.fit(X_scaled)

plt.scatter(X_pca[:,0], X_pca[:,1], c=kmeans.labels_, cmap='seismic')
plt.xlabel('PCA Comp 1')
plt.ylabel('PCA Comp 2')
plt.title('K-Means Clustering')
plt.colorbar(label='Cluster Label')


plt.show()

print("PCA Components:")
for i, component in enumerate(pca.components_):
    print(f"PC{i+1}: {', '.join(f'{feat}: {weight:.3f}' for feat, weight in zip(X.columns, component))}")