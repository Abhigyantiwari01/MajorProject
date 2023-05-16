import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.metrics import accuracy_score
# DATA FOR PRED for diabetes
data=pd.read_csv("diabetes.csv")
#returns first five rows
print(data.head())

#excluding the last column as it is the target column
X=data.iloc[:,:8]
print(X.shape[1])

y=data[["Outcome"]]

X=np.array(X)
y=np.array(y)

# Define the hyperparameters to search over
'''
n_estimators: The number of trees in the random forest ensemble.
max_depth: The maximum depth of each decision tree in the random forest
min_samples_split: minimum number of samples to split for a child nodes
min_samples_leaf: minimun samples at the leaf of a descision tree 
'''
param_grid = {
     'n_estimators': [50, 100, 200],
    'max_depth': [3, 5, 10],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
}

# Create a random forest classifier
random_classifier = RandomForestClassifier()

# Use GridSearchCV to find the best hyperparameters
'''
GridSearchCV: It is performs search over specified parameters
cv: number of folds
'''
grid_search = GridSearchCV(estimator=random_classifier, param_grid=param_grid, cv=5)
grid_search.fit(X, y.reshape(-1,))

# Print the best hyperparameters and the corresponding accuracy score
print("Best hyperparameters:", grid_search.best_params_)
print("Best accuracy:", grid_search.best_score_)
joblib.dump(random_classifier,"modeldia1")
