try:
    import backtrader
    import ccxt
    import pandas as pd
    import numpy as np
    import dotenv
    import requests
    print("pl")
except ImportError as e:
    print("fali",e)