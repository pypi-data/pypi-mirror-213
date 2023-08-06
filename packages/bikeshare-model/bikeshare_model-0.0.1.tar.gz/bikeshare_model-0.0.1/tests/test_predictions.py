import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import numpy as np
from sklearn.metrics import mean_squared_error, r2_score

from bikeshare_model.predict import make_prediction
from bikeshare_model.config.core import config

from bikeshare_model.predict import make_prediction

def test_make_prediction(sample_input_data):
    
    # Separate target and prediction features
    X = sample_input_data.drop(config.model_config.target, axis=1)
    y = sample_input_data[config.model_config.target]
    
    # Given
    expected_no_predictions = 3476

    # When
    result = make_prediction(input_data=X)
    
    # Then
    predictions = result.get("predictions")
    assert isinstance(predictions, np.ndarray)
    
    print(type(predictions[0]), type(np.int64))
    assert isinstance(predictions[0], np.float64)
    assert result.get("errors") is None
    assert len(predictions) == expected_no_predictions
    _predictions = list(predictions)
    y_true = sample_input_data["cnt"]
    #accuracy = accuracy_score(_predictions, y_true)
    accuracy = r2_score(y_true, _predictions)
    assert accuracy > 0.6