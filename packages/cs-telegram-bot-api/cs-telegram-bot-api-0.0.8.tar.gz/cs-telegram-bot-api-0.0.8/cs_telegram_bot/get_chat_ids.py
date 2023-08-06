import psycopg2
from urllib.parse import urlparse

def get_chat_ids(db_url):
    # Parse the database URL
    result = urlparse(db_url)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port

    # Connect to the database
    conn = psycopg2.connect(
        dbname=database,
        user=username,
        password=password,
        host=hostname,
        port=port
    )

    # Execute the SQL query
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM telegram_chat_ids")
    
    # Fetch all results
    results = cursor.fetchall()

    # Close the connection
    conn.close()

    # Unpack chat IDs from results (which are tuples)
    chat_ids = {chat[0]:chat[1] for chat in results}
    
    return chat_ids

