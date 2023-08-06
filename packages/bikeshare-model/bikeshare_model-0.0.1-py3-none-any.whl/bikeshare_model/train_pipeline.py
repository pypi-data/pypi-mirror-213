import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.utils import check_X_y
from sklearn.metrics import mean_squared_error, r2_score

from bikeshare_model.config.core import config
from bikeshare_model.pipeline import bikeshare_pipe
from bikeshare_model.processing.data_manager import load_dataset, save_pipeline

def run_training() -> None:
    
    """
    Train the model.
    """

    # read training data
    data = load_dataset(file_name=config.app_config.training_data_file)
    #print("loading preprocess dataset",data.head)

    # divide train and test
    X_train, X_test, y_train, y_test = train_test_split(
        data[config.model_config.features],  # predictors
        data[config.model_config.target],
        test_size=config.model_config.test_size,
        # we are setting the random seed here
        # for reproducibility
        random_state=config.model_config.random_state,
    )
    
    #print("Train data ",X_train.head)

    # Pipeline fitting
    #X,y =  check_X_y(X_train,y_train)
    bikeshare_pipe.fit(X_train,y_train)  #
    y_pred = bikeshare_pipe.predict(X_test)
    #print("Accuracy(in %):", accuracy_score(y_test, y_pred)*100)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print("R2 Score :", r2)
    print("Mean Square Error",mse)

    # persist trained model
    save_pipeline(pipeline_to_persist= bikeshare_pipe)
    # printing the score
    
if __name__ == "__main__":
    run_training()