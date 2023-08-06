import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

class TitanicClassifier:
    def __init__(self):
        self.pipeline = None

    def fit(self, X, y):
        # Imputar los valores faltantes en la columna 'Age' con la media
        imputer = SimpleImputer(strategy='mean')
        X['age'] = imputer.fit_transform(X[['age']])

        # Dividir los datos en conjuntos de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Definir las columnas numéricas y categóricas
        numeric_features = ['age', 'fare']
        categorical_features = ['sex', 'pclass', 'embarked']

        # Crear transformers para escalado y codificación one-hot
        numeric_transformer = StandardScaler()
        categorical_transformer = OneHotEncoder()

        # Combinar transformers en un ColumnTransformer
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)])

        # Crear el clasificador
        classifier = RandomForestClassifier()

        # Crear el pipeline
        self.pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                        ('classifier', classifier)])

        # Entrenar el pipeline
        self.pipeline.fit(X_train, y_train)

    def predict(self, X):
        # Utilizar el pipeline entrenado para hacer predicciones
        return self.pipeline.predict(X)
