import pandas as pd

df = pd.DataFrame({'A': ['foo', 'bar', 'foo', 'bar'], 'B': [1, 2, 3, 4]})
print(df)
result = df.groupby('A')['B'].transform('mean')
print(result)