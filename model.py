import requests
import numpy as np
import operator
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
# from flask import session

def scrape_model():
    URL = "https://pomber.github.io/covid19/timeseries.json"
    r = requests.get(URL)
    data = r.json()
    india = data["India"]
    india_data = [d.get("confirmed") for d in india]
    x = []
    for i in range(0, len(india_data)):
        x.append(i)
        if i>0:
            india_data[i]=india_data[i]-india_data[i-1]
    z = len(india_data)

    #print(x)
    #print(india_data)
    x = np.array(x).reshape(-1, 1)
    y = np.array(india_data)


    polynomial_features = PolynomialFeatures(degree=5)
    x_poly = polynomial_features.fit_transform(x)
    model = LinearRegression()
    model.fit(x_poly, y)
    # print(z)
    x = np.array(z).reshape(-1, 1)
    x_poly = polynomial_features.fit_transform(x)
    predicted = round(model.predict(x_poly)[0],0)
    print(int(predicted))
    # session['predicted'] = int(predicted)
    return int(predicted)
scrape_model()