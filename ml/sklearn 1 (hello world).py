import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.cluster import KMeans

X = np.random.random((10, 5))
y = np.array(['M','F','F','F','F','F','F','M','F','M'])


# Separa 70% dos dados para teste e outros 30% para treino
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

# SVC
svc = SVC(kernel='linear')
svc.fit(X_train, y_train)

# KNN
knn = KNeighborsClassifier(n_neighbors=4)
knn.fit(X_train, y_train)

# NaiveBayes
gnb = GaussianNB()
gnb.fit(X_train, y_train)

# K-Means ( Unsupervised )
k_means = KMeans(n_clusters=4, random_state=0)
k_means.fit(X_train)

print("correto:", y_test)

print("predito SVC:", svc.predict(X_test))
print("predito KNN:", knn.predict(X_test))
print("predito GNB:", gnb.predict(X_test))
print("predito KME:", k_means.predict(X_test))

print("teste pull-push")




