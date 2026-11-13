import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


# Функция для подключения к базе
def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dbname=os.getenv("DB_NAME")
    )


# Функция для создания таблиц
def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    # Таблица стран
    cur.execute("""
        CREATE TABLE IF NOT EXISTS countries (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL,
            min_lat FLOAT,
            max_lat FLOAT,
            min_lon FLOAT,
            max_lon FLOAT
        );
    """)

    # Таблица самолетов
    cur.execute("""
        CREATE TABLE IF NOT EXISTS aeroplanes (
            id SERIAL PRIMARY KEY,
            icao24 VARCHAR(10),
            callsign VARCHAR(50),
            origin_country VARCHAR(100),
            velocity FLOAT,
            baro_altitude FLOAT,
            on_ground BOOLEAN,
            country_id INT REFERENCES countries(id) ON DELETE CASCADE
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Таблицы countries и aeroplanes успешно созданы!")


if __name__ == "__main__":
    create_tables()
