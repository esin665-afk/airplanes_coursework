from src.load_data import load_all_data
from src.db_manager import DBManager


def main():
    """Главная функция проекта."""
    print("🚀 ЗАПУСК ПРОЕКТА: Мониторинг самолетов")
    print("=" * 50)

    # 1. Загрузка данных (если нужно обновить)
    # Раскомментируй строку ниже, если хочешь обновить данные при запуске
    # load_all_data()

    # 2. Работа с полученными данными через DBManager
    db = DBManager()

    print("\n📊 РЕЗУЛЬТАТЫ РАБОТЫ DBManager:")
    print("=" * 50)

    # 1. Страны и количество самолетов
    print("\n1. Количество самолетов по странам (Топ-5):")
    countries = db.get_countries_and_aeroplanes_count()
    for name, count in countries[:5]:
        print(f"   ✈️ {name}: {count} самолетов")

    # 2. Все самолеты
    all_planes = db.get_all_aeroplanes()
    print(f"\n2. Всего самолетов в базе: {len(all_planes)}")

    # 3. Средняя скорость
    avg_speed = db.get_avg_speed()
    print(f"\n3. Средняя скорость всех самолетов: {avg_speed:.2f} м/с")

    # 4. Самолеты выше средней скорости
    fast_planes = db.get_aeroplanes_with_higher_speed()
    print(f"\n4. Самолеты со скоростью выше средней (Топ-3):")
    for plane in fast_planes[:3]:
        print(f"   ⚡ {plane[1]} (Скорость: {plane[3]} м/с)")

    # 5. Поиск по ключевому слову
    keyword = "ACA"
    keyword_planes = db.get_aeroplanes_with_keyword(keyword)
    print(f"\n5. Самолеты с позывным '{keyword}' (Air Canada):")
    if keyword_planes:
        for plane in keyword_planes[:3]:
            print(f"   🍁 {plane[1]}")
    else:
        print("   Не найдено.")

    print("\n" + "=" * 50)
    print("✅ РАБОТА ЗАВЕРШЕНА УСПЕШНО!")


if __name__ == "__main__":
    main()
