import pandas as pd
import datetime

df = pd.DataFrame(columns=['date', 'price'])
df = df.append({'date': datetime.datetime.now(), 'price': 20}, ignore_index=True)
print(df)