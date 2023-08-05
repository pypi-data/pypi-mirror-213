from abc import ABC, abstractmethod
from sklearn.linear_model import LinearRegression, ElasticNet, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV

# абстрактный класс для всех моделей
class BaseModel(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def fit(self, X_train, y_train):
        pass

    @abstractmethod
    def predict(self, X_test):
        pass


class LinearRegressionModel(BaseModel):
    def __init__(self):
        self.model = LinearRegression(fit_intercept=True, normalize=False, copy_X=True)

    def fit(self, X_train, y_train):
        best_params = self.tune_hyperparameters(X_train, y_train)
        self.model = LinearRegression(**best_params)
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        return self.model.predict(X_test)

    def tune_hyperparameters(self, X, y):
        param_grid = {
            "fit_intercept": [True, False],
            "normalize": [True, False],
            "copy_X": [True, False]
        }

        grid_search = GridSearchCV(self.model, param_grid=param_grid)
        grid_search.fit(X, y)

        best_params = grid_search.best_params_

        return best_params


class ElasticNetModel(BaseModel):
    def __init__(self):
        self.model = ElasticNet(random_state=42)

    def fit(self, X_train, y_train):
        best_params = self.tune_hyperparameters(X_train, y_train)
        self.model = ElasticNet(**best_params, random_state=42)
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        return self.model.predict(X_test)

    def tune_hyperparameters(self, X, y):
        param_grid = {
            "alpha": [0.1, 1, 10],
            "l1_ratio": [0, 0.25, 0.5, 0.75, 1],
            "max_iter": [1000, 5000, 10000]
        }

        grid_search = GridSearchCV(self.model, param_grid=param_grid)
        grid_search.fit(X, y)

        best_params = grid_search.best_params_

        return best_params


class RandomForestRegressorModel(BaseModel):
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)

    def fit(self, X_train, y_train):
        best_params = self.tune_hyperparameters(X_train, y_train)
        self.model = RandomForestRegressor(**best_params, random_state=42)
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        return self.model.predict(X_test)

    def tune_hyperparameters(self, X, y):
        param_grid = {
            "n_estimators": [50, 100, 150],
            "max_features": ["sqrt", "log2"],
            "min_samples_split": [2, 3, 4],
            "min_samples_leaf": [1, 2, 3]
        }

        grid_search = GridSearchCV(self.model, param_grid=param_grid)
        grid_search.fit(X, y)

        best_params = grid_search.best_params_

        return best_params


class GradientBoostingRegressorModel(BaseModel):
    def __init__(self):
        self.model = GradientBoostingRegressor(random_state=42)

    def fit(self, X_train, y_train):
        best_params = self.tune_hyperparameters(X_train, y_train)
        self.model = GradientBoostingRegressor(**best_params, random_state=42)
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        return self.model.predict(X_test)

    def tune_hyperparameters(self, X, y):
        param_grid = {
            "n_estimators": [50, 100, 150],
            "learning_rate": [0.01, 0.1, 0.2, 0.3],
            "max_depth": range(1, 11),
            "min_samples_split": [2, 3, 4]
        }

        grid_search = GridSearchCV(self.model, param_grid=param_grid)
        grid_search.fit(X, y)

        best_params = grid_search.best_params_

        return best_params