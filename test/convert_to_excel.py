import pandas as pd

# Read the cleaned CSV file
df = pd.read_csv('test_statements.csv')

# Save to Excel file
df.to_excel('test_statements.xlsx', index=False)

print("CSV file has been successfully converted to Excel format!") 