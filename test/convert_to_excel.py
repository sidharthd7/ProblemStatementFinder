import pandas as pd

df = pd.read_csv('test_statements.csv')

df.to_excel('test_statements.xlsx', index=False)

print("CSV file successfully converted to Excel!") 