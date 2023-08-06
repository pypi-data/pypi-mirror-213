import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

from bike_rental_model.config.core import config
from bike_rental_model.processing.features import WeathersitImputer,WeekdayImputer,OutlierHandler
from bike_rental_model.processing.features import Mapper as mapper
from bike_rental_model.processing.data_manager import _load_raw_dataset


df = _load_raw_dataset(file_name="bike-sharing-dataset.csv")

def get_year_and_month(dataframe):

    df = dataframe.copy()
    # convert 'dteday' column to Datetime datatype
    df['dteday'] = pd.to_datetime(df['dteday'], format='%Y-%m-%d')
    # Add new features 'yr' and 'mnth
    df['yr'] = df['dteday'].dt.year
    df['mnth'] = df['dteday'].dt.month_name()
    
    return df
df=get_year_and_month(df)

hour_mappings = {
    '12am': 0,
    '1am': 1,
    '2am': 2,
    '3am': 3,
    '4am': 4,
    '5am': 5,
    '6am': 6,
    '7am': 7,
    '8am': 8,
    '9am': 9,
    '10am': 10,
    '11am': 11,
    '12pm': 12,
    '1pm':13,
    '2pm':14,
    '3pm':15,
    '4pm':16,
    '5pm':17,
    '6pm':18,
    '7pm':19,
    '8pm':20,
    '9pm':21,
    '10pm':22,
    '11pm':23,
    '12pm':24
}

month_mappings = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12
}

season_mappings = {  
    'winter': 1,
    'fall': 2,
    'spring': 3,
    'summer': 4
}

weather_mappings = {
    'Mist': 1,
    'Clear': 2,
    'Light Rain': 3,
    'Heavy Rain': 4
}

holiday_mappings = {
    'Yes': 1,
    'No': 0
}

weekday_mappings ={
    'Mon':1,
    'Tue' :2,
    'Wed' : 3,
    'Thu': 4,
    'Fri':5,
    'Sat':6,
    'Sun':7
}

# Instantiate Mapper for features
ordinal_features = ['hr', 'mnth','season','weathersit','holiday','weekday','workingday']

mappings = {
    'hr': hour_mappings,
    'mnth': month_mappings,
    'season': season_mappings,
    'weathersit': weather_mappings,
    'holiday': holiday_mappings,
    'weekday': weekday_mappings,
    'workingday':holiday_mappings
}


mapper = mapper(variables=ordinal_features, mappings=mappings)

df_transformed = mapper.transform(df)
df = pd.DataFrame(df_transformed)

lower_bound = {
    'temp': df_transformed.temp.quantile(0.25),
    'atemp': df_transformed.atemp.quantile(0.25),
    'hum': df_transformed.hum.quantile(0.25),
    'windspeed': df_transformed.windspeed.quantile(0.25)
}

upper_bound = {
    'temp': df_transformed.temp.quantile(0.75),
    'atemp': df_transformed.atemp.quantile(0.75),
    'hum': df_transformed.hum.quantile(0.75),
    'windspeed': df_transformed.windspeed.quantile(0.75)
}
numerical_features=['temp', 'atemp', 'hum', 'windspeed']



bike_rental_pipe = Pipeline([
    ('weekday_imputer', WeekdayImputer()),
    
    ('weather_imputer',WeathersitImputer()),
    ('mapper', mapper),
    ('outlier_handler', OutlierHandler(variables=numerical_features, lower_bound=lower_bound, upper_bound=upper_bound)),
    ('regressor', LinearRegression())
])
