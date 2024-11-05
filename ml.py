import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
from demo.config import engine

query = "SELECT gender, age, fare, pclass FROM users"

users_df = pd.read_sql_query(query, engine)

with open("lr.pkl", "rb") as file:
    titanic_ml = pickle.load(file)

features = ['gender', 'age', 'fare', 'pclass']

lab_en = LabelEncoder()
users_df['gender'] = users_df['gender'].str.lower().replace({'m': 'male', 'f': 'female'})
users_df['gender_encoded'] = lab_en.fit_transform(users_df['gender'])



def predict_survival(pclass, gender, age, fare):
    if gender.lower() in ['m', 'male']:
        gender = 'male'
    elif gender.lower() in ['f', 'female']:
        gender = 'female'
    
    sex_encoded = lab_en.transform([gender])[0]

    input_data = pd.DataFrame([[pclass, sex_encoded, age, fare]], columns=['Pclass', 'Sex', 'Age', 'Fare'])

    prediction = titanic_ml.predict(input_data)

    return "Survived" if prediction[0] == 1 else "Did not survive"

results = predict_survival(3, 'm', 22, 7)
print(results)