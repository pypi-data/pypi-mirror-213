import math

import numpy as np

from regression_model.predict import make_prediction


def test_make_prediction(sample_input_data):
    # Given
    expected_first_prediction_value = 125
    expected_no_predictions = len(sample_input_data)
    # #print("Sample input data: ", sample_input_data)
    # print("Length of sample input data: ", len(sample_input_data))

    # When
    result = make_prediction(input_data=sample_input_data)

    # Then
    predictions = result.get("predictions")
    # print("Length of predictions: ", len(predictions))
    # print("Predictions: ",predictions)
    assert isinstance(predictions, list)
    assert isinstance(predictions[0], np.float64)
    assert result.get("errors") is None
    assert len(predictions) == expected_no_predictions
    assert math.isclose(predictions[0], expected_first_prediction_value, abs_tol=100)
