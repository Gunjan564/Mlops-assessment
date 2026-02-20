import pandas as pd
import numpy as np
from datetime import datetime, timedelta

num_rows = 10000
timestamps = [datetime.now() - timedelta(minutes=x) for x in range(num_rows)]
np.random.seed(42)
close_prices = np.cumsum(np.random.randn(num_rows)) + 50000

df = pd.DataFrame({
    'timestamp': timestamps,
    'open': close_prices + np.random.randn(num_rows),
    'high': close_prices + np.random.uniform(0, 10, num_rows),
    'low': close_prices - np.random.uniform(0, 10, num_rows),
    'close': close_prices,
    'volume_btc': np.random.uniform(0.1, 10, num_rows),
    'volume_usd': np.random.uniform(1000, 100000, num_rows)
})
df.to_csv('data.csv', index=False)
