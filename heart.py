import pandas as pd
import numpy as np
import joblib
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from sklearn.linear_model import LogisticRegression
#warnings.filterwarnings("ignore", category=DeprecationWarning) 
from sklearn.preprocessing import StandardScaler
import random
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import cross_validate
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV

data = pd.read_csv("heart.csv")
data["trestbps"]=np.log(data["trestbps"])

data=data.drop(["fbs"],axis=1)
data=data.drop(["ca"],axis=1)
data["chol"]=np.log(data["chol"])
target=data["target"]

np.random.shuffle(data.values)
data=data.drop(["target"],axis=1)
print(data.columns)
sc= StandardScaler()
data=sc.fit_transform(data)

random_classifier = RandomForestClassifier()

# Define the hyperparameter grid to search over
param_grid = {'n_estimators': [10, 50, 100, 200],
              'max_depth': [3, 5, 7, None],
              'max_features': ['sqrt', 'log2', None],
              'min_samples_split': [2, 4, 6],
              'min_samples_leaf': [1, 2, 4]}

# Create GridSearchCV object
grid_search = GridSearchCV(estimator=random_classifier,
                           param_grid=param_grid,
                           cv=5)

# Fit the GridSearchCV object on the data
grid_search.fit(data, target)

# Print the best hyperparameters and the corresponding mean cross-validated score
print("Best Hyperparameters: ", grid_search.best_params_)
print("Best Score: ", grid_search.best_score_)
