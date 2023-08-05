import numpy as np
import pandas as pd

import yfinance as yf

def getData():
    df=yf.download("BTC-USD",period='7d',interval='1m')
    return df