import math

import numpy as np

from my_model.predict import make_prediction


def test_make_prediction(sample_input_data):
    # Given
    expected_first_prediction_value = 0
    expected_number_predictions = 62

    # When
    result = make_prediction(input_data=sample_input_data)

    # Then
    predictions = result.get("predictions")
    assert isinstance(predictions[0], np.float64)
    assert result.get("errors") is None
    assert len(predictions) == expected_number_predictions
    assert math.isclose(predictions[0], expected_first_prediction_value, abs_tol=1)
