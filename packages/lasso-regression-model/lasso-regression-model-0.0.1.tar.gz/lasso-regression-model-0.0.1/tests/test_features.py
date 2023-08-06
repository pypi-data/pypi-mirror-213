import pytest

from regression_model.config.core import config
from regression_model.processing.sklearn_preprocessors import ElapsedYearsTransformer


def test_ElapsedYearsTransformer(sample_input_data):
    # Given
    transformer = ElapsedYearsTransformer(
        vars=config.model_config.temporal_vars,  # Built_in_year_year
        # reference_variable=config.model_config.ref_var,
    )
    assert sample_input_data["Built_in_year_year"].iat[3] == 2020.0

    # When
    subject = transformer.fit_transform(sample_input_data)

    # Then
    assert subject["Built_in_year_year"].iat[3] == 2020.0


def test_ElapsedYearsTransformer_invalid_variable(sample_input_data):
    # Given
    transformer = ElapsedYearsTransformer(
        vars=["InvalidVariable"],  # Invalid variable name
        # reference_variable=config.model_config.ref_var,
    )

    # When/Then
    # An exception should be raised when fitting the transformer
    with pytest.raises(KeyError):
        transformer.fit_transform(sample_input_data)


def test_ElapsedYearsTransformer_missing_variable(sample_input_data):
    # Given
    transformer = ElapsedYearsTransformer(
        vars=["MissingVariable"],  # Variable not present in the dataset
        # reference_variable = config.model_config.ref_var,
    )

    # When/Then
    # An exception should be raised when fitting the transformer
    with pytest.raises(KeyError):
        transformer.fit_transform(sample_input_data)
