from collections import defaultdict
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import SelectKBest, f_regression, VarianceThreshold
from sklearn.model_selection import GridSearchCV
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import RFECV
from sklearn.linear_model import LinearRegression

class LabelEncoderWrapper:
    def __init__(self):
        self.encoder_dict = defaultdict(LabelEncoder)

    def fit_transform(self, X):
        # Применение LabelEncoder к каждому объектному столбцу
        X_transformed = X.apply(lambda x: self.encoder_dict[x.name].fit_transform(x.astype(str)))
        return X_transformed


class DataFramePreprocessor:
    def __init__(self, object_columns, scaler=StandardScaler(), imputer=SimpleImputer()):
        self.object_columns = object_columns
        self.scaler = scaler
        self.imputer = imputer

    def process(self, data, target):
        data = self.correct_text(data)
        data = self.drop_duplicates(data)
        data = self.apply_label_encoder(data)
        
        X_train, X_test, y_train, y_test = self.split_data(data, target)
        # Заполнение отсутствующих значений
        X_train_imputed, X_test_imputed = self.impute_missing_values(X_train, X_test, y_train)
        
        # Сохраняем имена столбцов
        self.columns = X_train_imputed.columns
        # Преобразуем numpy.ndarray обратно в DataFrame с сохранением имен столбцов
        X_train_imputed = pd.DataFrame(X_train_imputed, columns=self.columns)
        X_test_imputed = pd.DataFrame(X_test_imputed, columns=self.columns)
        
        # Масштабирование данных
        X_train_scaled, X_test_scaled = self.scale_features(X_train_imputed, X_test_imputed)
        # Выбор признаков
        X_train_selected, X_test_selected = self.select_features(X_train_scaled, y_train, X_test_scaled)
        
        return X_train_selected, X_test_selected, y_train, y_test

    @staticmethod
    def correct_text(data):
        return data.apply(lambda x: x.str.strip().lower() if x.dtype == "object" else x)
    
    # Приводим текстовые столбцы к нижнему регистру и удаляем начальные и конечные пробелы
    @staticmethod
    def drop_duplicates(data):
        return data.drop_duplicates(inplace=False)

    def apply_label_encoder(self, data):
        lew = LabelEncoderWrapper()
        data[self.object_columns] = lew.fit_transform(data[self.object_columns])
        return data

    @staticmethod
    def split_data(data, target):
        return train_test_split(data.drop([target], axis=1), data[target], test_size=0.2, random_state=42)

    # Находим оптимальный метод заполнения пропущенных значений с помощью GridSearchCV
    def impute_missing_values(self, X_train, X_test, y_train):
        param_grid_imputer = {'strategy': ['mean', 'median', 'most_frequent', 'constant']}
        grid_search_imputer = GridSearchCV(self.imputer, param_grid=param_grid_imputer, cv=5, scoring='r2')
        grid_search_imputer.fit(X_train, y_train)
        best_imputer = grid_search_imputer.best_estimator_
        X_train_imputed = best_imputer.transform(X_train)
        X_test_imputed = best_imputer.transform(X_test)
        
        # Обратно в DataFrame с сохранением имен столбцов
        X_train_imputed = pd.DataFrame(X_train_imputed, columns=X_train.columns)
        X_test_imputed = pd.DataFrame(X_test_imputed, columns=X_test.columns)
        
        return X_train_imputed, X_test_imputed

    # Масштабирование данных
    def scale_features(self, X_train_imputed, X_test_imputed):
        self.scaler.fit(X_train_imputed)

        X_train_scaled = pd.DataFrame(self.scaler.transform(X_train_imputed), columns=X_train_imputed.columns)
        X_test_scaled = pd.DataFrame(self.scaler.transform(X_test_imputed), columns=X_train_imputed.columns)
        
        return X_train_scaled, X_test_scaled

    # Выбор признаков
    def select_features(self, X_train, y_train, X_test):
        # выбираем k наиболее значимых признаков
        selector = SelectKBest(f_regression, k=X_train.shape[1])
        selector.fit(X_train, y_train)
        k_best = selector.k

        # определяем пороговое значение для отбора признаков с помощью метода VarianceThreshold
        selector = VarianceThreshold()
        selector.fit(X_train)
        threshold = np.percentile(selector.variances_, 100 - (100 / X_train.shape[1]) * k_best)
    
        # удаляем признаки с низкой дисперсией
        sel = VarianceThreshold(threshold=threshold)
        X_train = sel.fit_transform(X_train)
        X_test = sel.transform(X_test)
    
        # удаляем признаки с высокой корреляцией для предотвращения мультиколлинеарности
        corr_matrix = pd.DataFrame(X_train).corr().abs() # получаем матрицу корреляции
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool)) # выбираем верхний треугольник матрицы корреляции
        to_drop = [column for column in upper.columns if any(upper[column] > threshold)] # находим индексы столбцов с корреляцией больше порога
        X_train = np.delete(X_train, to_drop, axis=1) # удаляем коррелирующие признаки
        X_test = np.delete(X_test, to_drop, axis=1)

        # отбор признаков с помощью метода RFE
        lr = LinearRegression()

        # определяем объект с кросс-валидацией
        rfecv = RFECV(estimator=lr, step=1, cv=5, scoring='neg_mean_squared_error')
        rfecv.fit(X_train, y_train)

        # выполняем отбор признаков
        X_train_rfecv = rfecv.transform(X_train)
        X_test_rfecv = rfecv.transform(X_test)
        
        return X_train_rfecv, X_test_rfecv