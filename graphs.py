import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

print('hello')
import pg8000


connection = pg8000.connect(database = 'bootcamp',
                              user = 'postgres',
                              password = '3443',
                              host='localhost',
                              port='5433')

cursor = connection.cursor()

# create_table_query = f'''CREATE TABLE session (
#                         id SERIAL PRIMARY KEY,
#                         username VARCHAR(100) NOT NULL,
#                         day VARCHAR(100) NOT NULL,
#                         done boolean)
#                         '''
def graph_rep():
    db_url = 'postgresql+pg8000://postgres:3443@localhost:5433/bootcamp'
    engine = create_engine(db_url)

    query = '''SELECT 
        CASE WHEN attendency IS TRUE THEN 'Completed' ELSE 'Not completed' END AS status,
        COUNT(*) AS count
    FROM attendance
    GROUP BY status'''
    
    df = pd.read_sql(query, engine)

    print("DataFrame preview:")
    print(df)
    print("Columns:", df.columns)

    engine.dispose()

    plt.figure(figsize=(10, 6))
    
    if 'count' in df.columns and 'status' in df.columns:
        statuses = df['status']
        counts = df['count']
        plt.figure(figsize=(8, 8))
        plt.pie(counts, labels=statuses, autopct='%1.1f%%', startangle=90, colors=['lightblue', 'lightcoral'])
        plt.title('Proportion of Attendencies (Completed vs Not completed)', fontsize=16)
        plt.show()

    else:
        print("Column 'session_count' not found. Check your SQL query or DataFrame.")
graph_rep()