# PONER TODOS LOS IMPORTS AQUÍ:
# TODOS LOS IMPORTS
# data manipulation and plotting
# for saving the pipeline
import joblib
import numpy as np
import pandas as pd

# from feature-engine
from feature_engine.imputation import AddMissingIndicator, MeanMedianImputer
from feature_engine.selection import DropFeatures

# to separate training and test
from sklearn.model_selection import train_test_split

# the model
from sklearn.naive_bayes import GaussianNB

# from Scikit-learn
from sklearn.pipeline import Pipeline

from my_model.config.core import config

# PONER PIPELINE AQUÍ
# RECORDAR USO DE VARIABLES PARA COLUMNAS EJEMPLO: features_to_drop=config.model_config.drop_features
genero_pipe = Pipeline(
    [
        # ===== IMPUTATION =====
        (
            "drop_features",
            DropFeatures(features_to_drop=config.model_config.drop_features),
        ),
        #  missing indicator
        (
            "missing_indicator",
            AddMissingIndicator(variables=config.model_config.numerical_vars_with_na),
        ),
        # imputamos variables numericas con la mean
        (
            "mean_imputation",
            MeanMedianImputer(
                imputation_method="mean",
                variables=config.model_config.numerical_vars_with_na,
            ),
        ),
        ("GaussianNB", GaussianNB()),
    ]
)
