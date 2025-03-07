import pandas as pd
import numpy as np
import joblib
import xgboost as xgb
from datetime import datetime
from sklearn.model_selection import train_test_split
from typing import Tuple, Union, List

class DelayModel:
    def __init__(self):
        self._model = None  # Aquí se guardará el modelo entrenado

    def preprocess(self, data: pd.DataFrame, target_column: str = None) -> Union[Tuple[pd.DataFrame, pd.Series], pd.DataFrame]:
        """
        Prepara los datos crudos para entrenamiento o predicción.
        """

        # Asegurar que la columna 'min_diff' exista
        if "min_diff" not in data.columns:
            data["min_diff"] = self.get_min_diff(data)

        # Generar variables adicionales
        data["high_season"] = ((data["MES"].isin([1, 2, 7, 12])) | (data["DIA"].between(15, 31))).astype(int)
        data["delay"] = (data["min_diff"] > 15).astype(int)

        # Generar features para el modelo
        features = pd.concat([
            pd.get_dummies(data['OPERA'], prefix='OPERA'),
            pd.get_dummies(data['TIPOVUELO'], prefix='TIPOVUELO'),
            pd.get_dummies(data['MES'], prefix='MES')
        ], axis=1)

        if target_column:
            return features, data[target_column]
        return features

    @staticmethod
    def get_min_diff(data):
        """
        Calcula la diferencia en minutos entre 'Fecha-O' y 'Fecha-I'.
        """
        fecha_o = pd.to_datetime(data['Fecha-O'], errors='coerce')
        fecha_i = pd.to_datetime(data['Fecha-I'], errors='coerce')
        return (fecha_o - fecha_i).dt.total_seconds() / 60

    def fit(self, features: pd.DataFrame, target: pd.Series) -> None:
        """
        Entrena el modelo con los datos preprocesados.
        """
        print("Entrenando modelo...")

        # Balanceo de clases
        n_y0 = len(target[target == 0])
        n_y1 = len(target[target == 1])
        scale = n_y0 / n_y1

        # Entrenar XGBoost con balanceo
        self._model = xgb.XGBClassifier(random_state=1, learning_rate=0.01, scale_pos_weight=scale)
        self._model.fit(features, target)

        # Guardar el modelo
        joblib.dump(self._model, "challenge/model.pkl")
        print("✅ Modelo guardado en challenge/model.pkl")

    def predict(self, features: pd.DataFrame) -> List[int]:
        """
        Predice retrasos en nuevos vuelos.
        """
        if self._model is None:
            self._model = joblib.load("/app/challenge/model.pkl")

        return self._model.predict(features).tolist()

if __name__ == "__main__":
    # Cargar datos y asegurarse de que 'min_diff' esté presente
    df = pd.read_csv("data/data.csv", low_memory=False)
    
    if "min_diff" not in df.columns:
        df["min_diff"] = DelayModel.get_min_diff(df)
        df.to_csv("data/data.csv", index=False)  # Guardar cambios

    model = DelayModel()
    X, y = model.preprocess(df, target_column="delay")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    model.fit(X_train, y_train)

    sample = X_test.iloc[:5]
    print("Predicciones:", model.predict(sample))
