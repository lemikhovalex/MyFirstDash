import pandas as pd
import numpy as np
import os


def generate_circle():
    if not os.path.isfile('circle.csv'):
        n = 100
        x = np.random.random_sample(n) * np.pi * 2
        df = pd.DataFrame()
        df['x'] = np.cos(x)
        df['y'] = np.sin(x)
        df.to_csv('circle.csv')
