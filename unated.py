import pandas as pd
import numpy as np
import csv

links_city = pd.read_csv('A:/Language-processor/links_city.csv')
name_city = pd.read_csv('A:/Language-processor/name_city.csv')

(pd.concat([links_city, name_city], axis=1)
 .to_csv('A:/Language-processor/unated.csv', index=False, encoding='utf-8'))
