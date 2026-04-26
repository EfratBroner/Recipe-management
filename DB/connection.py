import pyodbc

def get_connection():
    connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=Recipes;"
        "Trusted_Connection=yes;"
    )
    return pyodbc.connect(connection_string)



def get_cursor():
    conn = get_connection()
    return conn.cursor(), conn




