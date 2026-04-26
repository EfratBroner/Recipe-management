from DB.connection import get_connection

def test_connection():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT 1")
    print(cursor.fetchone())

    conn.close()

if __name__ == "__main__":
    test_connection()
