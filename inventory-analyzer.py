#!/bin/env python3

import time
from tqdm import tqdm
import re
import json
import os
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

sns.set_theme()

cars={}
if os.path.exists('cars.json'):
    f=open('cars.json', 'r')
    cars = json.loads(f.read())
    f.close()
print(f'loaded {len(cars)} existing cars')

cars_df = pd.DataFrame(cars)

#sns.displot(cars_df, x="make")
#
#plt.show()

#########################################################
# MAKES
#########################################################

#makes = {}
#for car in cars:
#    try:
#        makes[car['make']]
#    except KeyError:
#        makes[car['make']] = 0
#    makes[car['make']] += 1
#
#makes2 = [(x, makes[x]) for x in makes]
#makes2.sort(key=lambda make: make[1], reverse=True)
#makes3={}
#makes3['make'] = [x[0] for x in makes2]
#makes3['count'] = [x[1] for x in makes2]
#
#sns.barplot(y="make", x="count", data=makes3, orient='h')
##plt.xticks(rotation=90)
#
#plt.show()

#########################################################
# MAKES & MODELS
#########################################################

models = {}
for car in cars:
    try:
        models[f"{car['year']} {car['make']} {car['model']}"]
    except KeyError:
        models[f"{car['year']} {car['make']} {car['model']}"] = 0
    models[f"{car['year']} {car['make']} {car['model']}"] += 1

models2 = [(x, models[x]) for x in models]
models2.sort(key=lambda model: model[1], reverse=True)
models3={}
models3['model'] = [x[0] for x in models2[:20]]
models3['count'] = [x[1] for x in models2[:20]]

sns.barplot(y='model', x='count', data=models3, orient='h')

plt.show()

