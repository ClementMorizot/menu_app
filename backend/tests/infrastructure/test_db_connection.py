import psycopg


def test_connection():
    conn = psycopg.connect(
        host="localhost",
        port=5432,
        dbname="menu_app_dev",
        user="menu_user",
        password="ton_mot_de_passe",
    )

    with conn.cursor() as cur:
        cur.execute("SELECT 1;")
        result = cur.fetchone()

    conn.close()

    print("Connexion OK :", result)


if __name__ == "__main__":
    test_connection()