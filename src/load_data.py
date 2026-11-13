import time
import psycopg2
from src.database import get_connection
from src.api import AeroplanesAPI
from src.config import COUNTRIES


def load_all_data():
    """Загружает данные по всем странам из списка и сохраняет в БД."""
    api = AeroplanesAPI()
    conn = get_connection()
    cur = conn.cursor()

    for country_name in COUNTRIES:
        print(f"\n🌍 Обработка страны: {country_name}...")

        # 1. Получаем координаты (boundingbox)
        bbox = api.get_country_coordinates(country_name)
        if not bbox:
            print(f"Пропускаем {country_name} (нет координат).")
            continue

        # Сохраняем страну в БД (используем RETURNING id, чтобы потом привязать самолеты)
        # bbox = [south, north, west, east]
        cur.execute("""
            INSERT INTO countries (name, min_lat, max_lat, min_lon, max_lon)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (name) DO NOTHING
            RETURNING id;
        """, (country_name, bbox[0], bbox[1], bbox[2], bbox[3]))

        row = cur.fetchone()
        if row:
            country_id = row[0]
        else:
            # Если страна уже была в базе, достаем её ID
            cur.execute("SELECT id FROM countries WHERE name = %s", (country_name,))
            country_id = cur.fetchone()[0]

        conn.commit()
        print(f"✅ Страна {country_name} сохранена (ID: {country_id})")

        # 2. Получаем самолеты над этой страной
        aeroplanes = api.get_aeroplanes(bbox)
        print(f"✈️ Найдено самолетов: {len(aeroplanes)}")

        # 3. Сохраняем самолеты в БД
        saved_count = 0
        for plane in aeroplanes:
            # Индексы данных из API opensky:
            # 0: icao24, 1: callsign, 2: origin_country, 7: baro_altitude, 8: on_ground, 9: velocity
            try:
                icao24 = plane[0]
                callsign = plane[1].strip() if plane[1] else "Unknown"
                origin_country = plane[2]
                baro_altitude = plane[7]
                on_ground = plane[8]
                velocity = plane[9]

                # Пропускаем самолеты без скорости или высоты (чтобы не было Null в БД, хотя можно и Null)
                if velocity is None or baro_altitude is None:
                    continue

                cur.execute("""
                    INSERT INTO aeroplanes (icao24, callsign, origin_country, velocity, baro_altitude, on_ground, country_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                """, (icao24, callsign, origin_country, velocity, baro_altitude, on_ground, country_id))
                saved_count += 1
            except Exception as e:
                print(f"Ошибка при сохранении самолета {plane[1]}: {e}")

        conn.commit()
        print(f"💾 Сохранено {saved_count} самолетов для {country_name}.")

        # Делаем паузу, чтобы API не заблокировало нас за частые запросы
        time.sleep(2)

    cur.close()
    conn.close()
    print("\n🎉 ВСЕ ДАННЫЕ УСПЕШНО ЗАГРУЖЕНЫ В БД!")


if __name__ == "__main__":
    load_all_data()
