from setuptools import setup

setup(
    name='titanic_ml',
    version='1.0',
    author='Álvaro',
    author_email='alvaro.maestre@edu.uah.es',
    description='Un clasificador de RandomForest para el dataset Titanic',
    packages=['titanic_ml'],
    install_requires=['pandas', 'scikit-learn'],
)