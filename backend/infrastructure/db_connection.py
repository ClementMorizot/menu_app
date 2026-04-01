from psycopg import connect
from psycopg.connection import Connection

def get_connection() -> Connection : 
    return connect(
        dbname = "menu_app_dev",
        user = "menu_user",
        password = "ton_mot_de_passe",
        host = "localhost",
        port=5432
    )