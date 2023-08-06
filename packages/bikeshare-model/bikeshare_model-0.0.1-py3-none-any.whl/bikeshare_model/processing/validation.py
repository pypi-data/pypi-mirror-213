import pandas as pd
import numpy as np


def validate_input_data(data):
    # Check for missing values
    if (data==''):
        raise ValueError("Input data contains missing values.")

    
    return True
