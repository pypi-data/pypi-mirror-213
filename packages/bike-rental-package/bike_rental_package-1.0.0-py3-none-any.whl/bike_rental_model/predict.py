import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from typing import Union
import pandas as pd
import numpy as np

from bike_rental_model import __version__ as _version
from bike_rental_model.config.core import config
from bike_rental_model.pipeline import bike_rental_pipe
from bike_rental_model.processing.data_manager import load_pipeline
from bike_rental_model.processing.data_manager import pre_pipeline_preparation
from bike_rental_model.processing.validation import validate_inputs
from bike_rental_model.processing.data_manager import load_dataset
from sklearn.model_selection import train_test_split


pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
bike_share_pipe= load_pipeline(file_name=pipeline_file_name)



def make_prediction(*,input_data:Union[pd.DataFrame, dict]) -> dict:
    """Make a prediction using a saved model """

    #validated_data, errors = validate_inputs(input_df=pd.DataFrame(input_data))
    
    #print(validated_data)
    #results = {"predictions": None, "version": _version, "errors": errors}
    
    
    #if not errors:

    predictions = bike_share_pipe.predict(input_data)
    results = {"predictions": predictions,"version": _version}
    print(results)

    return results

if __name__ == "__main__":

   data = load_dataset(file_name=config.app_config.training_data_file)
   X_train, X_test, y_train, y_test = train_test_split(
        data[config.model_config.features],  # predictors
        data[config.model_config.target],
        test_size=config.model_config.test_size,
        # we are setting the random seed here
        # for reproducibility
        random_state=config.model_config.random_state,
    ) 
   make_prediction(input_data=X_test)
