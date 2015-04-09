# coding: utf8
from datetime import datetime
import itertools
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import PolynomialFeatures, Imputer
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import Ridge, BayesianRidge
from utils import *

data_accidents = load_data_from_csv('data/parsered1.csv', False)
data_weather = load_data_from_csv('data/weather_utf8.csv',False)

'''
Because of the fact that we don't have particular time (only dates) for accidents and do have time for weather
measurements, let's choose one time for all accident, e.g. 15:00.
'''

for i in data_accidents.index:
    #converting date to standard datetime representation, adding particular time
    data_accidents.ix[i,'date'] = str(datetime.strptime(str(data_accidents.ix[i,'date']) + ' 15:00:00', '%Y-%m-%d %H:%M:%S'))

for i in data_weather.index:
    data_weather.ix[i,'date'] = str(datetime.strptime(str(data_weather.ix[i,'date']),'%d.%m.%Y %H:%M'))

#merging two datasets on date
data = data_accidents.merge(data_weather, on='date')

#casting to numpy array
array = np.array(data[['num_dtp','T']].values, dtype=np.float64)

#preprocessing, completing missing values
imp = Imputer(missing_values='NaN', strategy='median', axis=1)
new_data = imp.fit_transform(array)

#sorting data by 'T', for better plotting
new_data = new_data[new_data[:, 1].argsort()]

x = new_data[:,1]
y = new_data[:,0]

x_plot = x

X = x[:,np.newaxis]
X_plot = x_plot[:,np.newaxis]

plt.scatter(x, y, s = 30, label="training points")

#algos = itertools.cycle([Ridge(), BayesianRidge()])

for degree in [1, 3, 5, 7]:
    model = make_pipeline(PolynomialFeatures(degree), Ridge())
    model.fit(X, y)
    y_plot = model.predict(X_plot)
    plt.plot(x_plot, y_plot, label="degree %d" % degree)

plt.legend(loc='lower left')
plt.show()
