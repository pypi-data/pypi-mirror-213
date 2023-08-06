import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from bike_rental_model.config.core import config
from bike_rental_model.pipeline import bike_rental_pipe
from bike_rental_model.processing.data_manager import load_dataset, save_pipeline,_load_raw_dataset

def run_training() -> None:
    
    """
    Train the model.
    """

    # read training data
    data = load_dataset(file_name=config.app_config.training_data_file)
    
    # divide train and test
    X_train, X_test, y_train, y_test = train_test_split(
        data[config.model_config.features],  # predictors
        data[config.model_config.target],
        test_size=config.model_config.test_size,
        # we are setting the random seed here
        # for reproducibility
        random_state=config.model_config.random_state,
    )

    # Pipeline fitting
    bike_rental_pipe.fit(X_train,y_train)  #
    #y_pred = titanic_pipe.predict(X_test)
    #print("Accuracy(in %):", accuracy_score(y_test, y_pred)*100)

    # persist trained model
    save_pipeline(pipeline_to_persist= bike_rental_pipe)
    # printing the score
    
if __name__ == "__main__":
    run_training()