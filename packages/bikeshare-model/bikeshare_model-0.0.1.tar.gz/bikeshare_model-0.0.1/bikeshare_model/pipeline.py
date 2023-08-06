import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor

from bikeshare_model.config.core import config
#from bikeshare_model.processing.features import WeathersitImputer
from bikeshare_model.processing.features import Mapper
from bikeshare_model.processing.features import OutlierHandler
from bikeshare_model.processing.features import WeekdayOneHotEncoder
#from bikeshare_model.processing.features import WeekdayImputer
from bikeshare_model.processing.features import bikeshareImputer

bikeshare_pipe = Pipeline([
    ##Imputation##
    ('weekD', bikeshareImputer(variables='weekday')),
    ('weathS', bikeshareImputer(variables='weathersit')),
    ##Mapper##
    #('map_yr',Mapper('yr',{'2011': 0, '2012': 1})),
    ('map_mnth',Mapper('mnth',{'January':1,'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8,'September':9, 'October':10, 'November':11, 'December':12})),
    ('map_season',Mapper('season',{'spring':1, 'summer':2, 'fall':3, 'winter':4})),
    ('map_weathersit',Mapper('weathersit',{'Clear':1,'Mist':2, 'Light Rain':3, 'Heavy Rain':4})),
    ('map_holiday',Mapper('holiday',{'No':0, 'Yes':1})),
    ('map_workingday',Mapper('workingday',{'No':0, 'Yes':1})),
    ('map_hr', Mapper('hr',{'12am':0, '1am':1, '2am':2, '3am':3, '4am':4, '5am':5, '6am':6, '7am':7, '8am':8, '9am':9, '10am':10, '11am':11, '12pm':12, '1pm':13, '2pm':14, '3pm':15, '4pm':16, '5pm':17, '6pm':18, '7pm':19, '8pm':20, '9pm':21, '10pm':22, '11pm':23 })),
    
    #RemoveOutlier#
    ('temp_outl',OutlierHandler('temp')),
    ('atemp_outl',OutlierHandler('atemp')),
    ('hum_outl',OutlierHandler('hum')),
    ('windspeed_outl', OutlierHandler('windspeed')),
    #OneHotEncoder#
    ('weekday_enc',WeekdayOneHotEncoder('weekday')),
    ('model_rf', RandomForestRegressor(n_estimators=150, max_depth=5,random_state=42))
])