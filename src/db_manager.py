from typing import List, Tuple, Optional, Any
from src.database import get_connection


class DBManager:
    """
    Класс для управления данными в базе данных PostgreSQL.
    Выполняет выборку, фильтрацию и агрегацию данных о самолетах.
    """

    def __init__(self):
        """Инициализация класса. Подключение происходит при вызове методов."""
        pass

    def get_countries_and_aeroplanes_count(self) -> List[Tuple[str, int]]:
        """
        Получает список всех стран и количество самолетов в их воздушных пространствах.
        Использует LEFT JOIN для вывода всех стран, даже если над ними нет самолетов.

        Returns:
            List[Tuple[str, int]]: Список кортежей (название страны, количество самолетов).
        """
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT c.name, COUNT(a.id) as aeroplanes_count
            FROM countries c
            LEFT JOIN aeroplanes a ON c.id = a.country_id
            GROUP BY c.name
            ORDER BY aeroplanes_count DESC;
        """)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

    def get_all_aeroplanes(self) -> List[Tuple[Any, ...]]:
        """
        Получает список всех воздушных судов.

        Returns:
            List[Tuple]: Список кортежей с данными о самолетах (icao24, callsign, страна, скорость, высота).
        """
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT icao24, callsign, origin_country, velocity, baro_altitude, on_ground
            FROM aeroplanes;
        """)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

    def get_avg_speed(self) -> float:
        """
        Получает среднюю скорость по всем самолетам.

        Returns:
            float: Средняя скорость. Если самолетов нет, возвращает 0.0.
        """
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT AVG(velocity) FROM aeroplanes;")
        result = cur.fetchone()[0]
        cur.close()
        conn.close()
        return float(result) if result is not None else 0.0

    def get_aeroplanes_with_higher_speed(self) -> List[Tuple[Any, ...]]:
        """
        Получает список всех самолетов, у которых скорость выше средней.
        Использует подзапрос для вычисления средней скорости.

        Returns:
            List[Tuple]: Список кортежей с данными о самолетах.
        """
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT icao24, callsign, origin_country, velocity, baro_altitude
            FROM aeroplanes
            WHERE velocity > (SELECT AVG(velocity) FROM aeroplanes)
            ORDER BY velocity DESC;
        """)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

    def get_aeroplanes_with_keyword(self, keyword: str) -> List[Tuple[Any, ...]]:
        """
        Получает список всех самолетов, в позывном которых содержатся переданные символы.

        Args:
            keyword (str): Искомая часть позывного (например, 'ACA').

        Returns:
            List[Tuple]: Список кортежей с данными о найденных самолетах.
        """
        conn = get_connection()
        cur = conn.cursor()
        # Используем ILIKE для поиска без учета регистра и % для поиска подстроки
        search_pattern = f"%{keyword}%"
        cur.execute("""
            SELECT icao24, callsign, origin_country, velocity, baro_altitude
            FROM aeroplanes
            WHERE callsign ILIKE %s;
        """, (search_pattern,))
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result
