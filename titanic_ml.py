import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pickle

# Load and inspect the data
df = pd.read_csv('Titanic-Dataset.csv')
df.isnull().sum()

# Drop rows with missing values and duplicates
newdf = df.dropna().drop_duplicates()


# Label encode the 'Sex' column
lab_en = LabelEncoder()
newdf['Sex'] = lab_en.fit_transform(newdf['Sex'])

# Define features and target
features = ['Pclass', 'Sex', 'Age', 'Fare']
X = newdf[features]
y = newdf.Survived

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train the logistic regression model
lr = LogisticRegression()
lr.fit(X_train, y_train)

# Predict on the test set
y_pred = lr.predict(X_test)

# Confusion matrix
cm = metrics.confusion_matrix(y_test, y_pred)



with open("lr.pkl", "wb") as file:
    pickle.dump(lr, file)