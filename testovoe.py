import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

file_path = "C:/Users/lenovo/Desktop/testovoe/trips_data.xlsx"
data = pd.read_excel(file_path)

if 'Unnamed: 0' in data.columns:
    data = data.drop('Unnamed: 0', axis=1)

data = pd.get_dummies(data, columns=['city', 'vacation_preference', 'transport_preference', 'target'])

target_columns = [col for col in data.columns if col.startswith('target')]
X = data.drop(target_columns, axis=1)
y = data[target_columns]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=49)

model = RandomForestClassifier()
model.fit(X_train, y_train)

salary = 230000
city = "Москва"
age = 62
why_pref = "Пляжный отдых"
transport = "Космический корабль"
family = 1

input_data = pd.DataFrame({
    'salary': [salary],
    'city': [city],
    'age': [age],
    'vacation_preference': [why_pref],
    'transport_preference': [transport],
    'family_members': [family]
})

input_data = pd.get_dummies(input_data, columns=['city', 'vacation_preference', 'transport_preference'])

for column in X.columns:
    if column not in input_data.columns:
        input_data[column] = 0

input_data = input_data[X.columns]

y_pred = model.predict(input_data)
y_pred_test = model.predict(X_test)
target_names = [col.split('_')[1] for col in target_columns]
predicted_city = target_names[np.argmax(y_pred)]

accuracy = accuracy_score(y_test.values.argmax(axis=1), y_pred_test.argmax(axis=1))

print("Предсказание города:", predicted_city)
print(f"Точность модели: {accuracy:.2f}")