from feature_engine.encoding import OrdinalEncoder, RareLabelEncoder
from feature_engine.imputation import (  # noqa
    AddMissingIndicator,
    CategoricalImputer,
    MeanMedianImputer,
)
from feature_engine.selection import DropFeatures
from feature_engine.transformation import LogTransformer
from feature_engine.wrappers import SklearnTransformerWrapper  # noqa
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import Lasso
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Binarizer, MinMaxScaler  # noqa

from regression_model.config.core import config
from regression_model.processing import sklearn_preprocessors as skpp

price_pipe = Pipeline(
    [
        # ===== IMPUTATION =====
        # add missing indicator
        (
            "missing_indicator",
            AddMissingIndicator(variables=config.model_config.numerical_vars_with_na),
        ),
        # impute numerical variables with the mean
        (
            "mean_imputation",
            MeanMedianImputer(
                imputation_method="mean",
                variables=config.model_config.numerical_vars_with_na,
            ),
        ),
        # ===== TEMPORAL VARIABLES =====
        (
            "elapsed_time",
            skpp.ElapsedYearsTransformer(
                vars=config.model_config.temporal_vars,
                # ref_var = config.model_config.ref_var,
            ),
        ),
        # ===== DROP FEATURES =====
        ("drop_features", DropFeatures(features_to_drop=config.model_config.drop_features)),
        # # impute categorical variables with string missing
        # (
        #     "missing_imputation",
        #     CategoricalImputer(
        #         imputation_method="missing",
        #         variables=config.model_config.categorical_vars_with_na_missing,
        #     ),
        # ),
        # # impute categorical variables with string missing
        # (
        #     "frequent_imputation",
        #     CategoricalImputer(
        #         imputation_method="frequent",
        #         variables=config.model_config.categorical_vars_with_na_frequent,
        #     ),
        # ),
        # ==== DATA TYPES CONVERSION =====
        (
            'convert_to_int64',
            skpp.DataTypeConverter(
                vars=config.model_config.float_cols,
                data_type=config.model_config.to_int64
            )
        ),
        # ==== VARIABLE TRANSFORMATION =====
        (
            "log",
            LogTransformer(
                    variables=config.model_config.numericals_log_vars
            )
        ),
        # ('yeojohnson', YeoJohnsonTransformer(variables=config.model_config.numericals_log_vars)),
        # #Binarizer
        # (
        #     "binarizer",
        #     SklearnTransformerWrapper(
        #         transformer=Binarizer(threshold=0),
        #         variables=config.model_config.binarize_vars,
        #     ),
        # ),
        # ==== mappers ====
        (
            "mapper_type_vars",
            skpp.Mapper(
                variables=config.model_config.type_vars,
                mappings=config.model_config.type_vars_mappings,
            ),
        ),
        # ==== CATEGORICAL ENCODING ====
        (
            "rare_label_encoder",
            RareLabelEncoder(
                tol=config.model_config.rare_labels_tolerance, n_categories=1,
                variables=config.model_config.categorical_vars
            ),
        ),
        # encode categorical variables using the target mean
        (
            "categorical_encoder",
            OrdinalEncoder(
                encoding_method="ordered",
                variables=config.model_config.categorical_vars,
            ),
        ),
        # ==== MinMaxScaler ====
        ("scaler", MinMaxScaler()),
        # ==== Model Selection ====
        (
            'selector',
            SelectFromModel(
                Lasso(
                    alpha=config.model_config.alpha,
                    random_state=config.model_config.random_state,
                    )
            )
        ),
        (
            "Lasso",
            Lasso(
                alpha=config.model_config.alpha,
                random_state=config.model_config.random_state,
            ),
        ),
    ]
)

# print(price_pipe[2:])
