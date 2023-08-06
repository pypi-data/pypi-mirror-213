from feature_engine.datetime import DatetimeFeatures

from regression_model.config.core import config


def preprocess_dataframe(dataframe, config=config):
    # Drop rows with missing values in the target column
    dataframe.dropna(subset=[config.model_config.target], axis=0, inplace=True)
    # dataframe.drop(dataframe.loc[dataframe[config.model_config.target].isnull()].index,
    #                axis = 0, inplace = True)
    # Drop specified columns
    dataframe.drop(config.model_config.drop_features_pp, axis=1, inplace=True)

    # Drop duplicates, keeping the first occurrence
    dataframe.drop_duplicates(keep='first', inplace=True)

    # Extract datetime features
    date_time_features = DatetimeFeatures(
        variables=config.model_config.date_features,
        features_to_extract=['year'],
        drop_original=True,
        missing_values='ignore'
    )
    dataframe = date_time_features.fit_transform(dataframe)

    return dataframe
