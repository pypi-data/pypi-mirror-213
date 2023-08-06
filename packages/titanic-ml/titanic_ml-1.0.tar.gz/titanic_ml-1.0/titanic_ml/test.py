import pandas as pd
from titanic_classifier import TitanicClassifier


# Cargar el dataset Titanic
df = pd.read_csv('H:\\Mi unidad\\Master\\9. Analítica Escalable\\Bloque 2\\PEC2\\proyecto\\titanic_ml\\titanic_ml\\titanic.csv', sep=";")

# Dividir los datos en características (X) y variable objetivo (y)
X = df.drop('survived', axis=1)
y = df['survived']

# Crear una instancia del clasificador Titanic
classifier = TitanicClassifier()

# Entrenar el clasificador
classifier.fit(X, y)

# Hacer predicciones en nuevos datos
new_data = pd.DataFrame({'age': [30, 40], 'fare': [50, 100], 'sex': ['female', 'male'], 'pclass': [1, 2], 'embarked': ['C', 'S']})
predictions = classifier.predict(new_data)

print("Predicciones:")
print(predictions)