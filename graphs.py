import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

print('hello')
import pg8000


connection = pg8000.connect(database = 'xxx',
                              user = 'postgres',
                              password = 'xxxx',
                              host='localhost',
                              port='5433')

cursor = connection.cursor()

# create_table_query = f'''CREATE TABLE session (
#                         id SERIAL PRIMARY KEY,
#                         username VARCHAR(100) NOT NULL,
#                         day VARCHAR(100) NOT NULL,
#                         done boolean)
#                         '''
db_url = 'postgresql+pg8000://postgres:3443@localhost:5433/bootcamp'
engine = create_engine(db_url)

query = '''SELECT username, COUNT(done) as session_count FROM session WHERE done is TRUE
            GROUP BY username'''


df = pd.read_sql(query, engine)

print("DataFrame preview:")
print(df)
print("Columns:", df.columns)

engine.dispose()

plt.figure(figsize=(10, 6))
if 'session_count' in df.columns:
    plt.bar(df['username'], df['session_count'], color='skyblue')
    plt.title('Number of Sessions per User', fontsize=16)
    plt.xlabel('Username', fontsize=14)
    plt.ylabel('Session Count', fontsize=14)
    plt.grid(axis='y', linestyle='-.', alpha=0.7)
    plt.xticks(rotation=45, fontsize=10)
    plt.tight_layout()
    plt.show()
else:
    print("Column 'session_count' not found. Check your SQL query or DataFrame.")