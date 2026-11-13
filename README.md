# Курсовая работа: Мониторинг самолетов (OpenSky API)

## Описание проекта
Данный проект представляет собой интеграцию с открытым API [OpenSky Network](https://opensky-network.org/) и [Nominatim](https://nominatim.openstreetmap.org/) для сбора данных о самолетах, находящихся в воздушном пространстве заданных стран. 
Полученные данные сохраняются в реляционную базу данных PostgreSQL для дальнейшей аналитики.

## 🛠 Технологии
*   **Python 3.12+**
*   **PostgreSQL** (хранение данных)
*   **psycopg2-binary** (подключение к БД)
*   **requests** (работа с API)
*   **python-dotenv** (безопасное хранение паролей)

## 📁 Структура проекта
```text
airplanes_coursework/
├── src/
│   ├── api.py           # Класс для работы с API (Nominatim, Opensky)
│   ├── config.py        # Список стран для мониторинга
│   ├── database.py      # Функции подключения и создания таблиц
│   ├── db_manager.py    # Класс DBManager для выборки и аналитики
│   └── load_data.py     # Скрипт для загрузки данных в БД
├── main.py              # Точка входа в программу
├── .env                 # Переменные окружения (не в Git)
├── .gitignore
├── pyproject.toml       # Зависимости
└── README.md
## 🚀 Установка и запуск

### 1. Клонирование репозитория и установка зависимостей

```bash
git clone https://github.com/esin665-afk/airplanes_coursework
cd airplanes_coursework
poetry install
```
### 2. Настройка базы данных

Создайте базу данных `airplanes_db` в PostgreSQL.
Создайте файл `.env` в корне проекта и добавьте туда ваши данные:

```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=ваш_пароль
DB_NAME=airplanes_db
```
### 3. Инициализация таблиц и загрузка данных

```bash
# Создание таблиц
python src/database.py

# Загрузка данных по 10 странам (может занять около минуты)
python -m src.load_data
```
### 4. Запуск аналитики

```bash
python main.py
```
## 📊 Реализованный функционал (Класс `DBManager`)

В рамках работы реализован класс `DBManager`, который содержит следующие методы:

*   `get_countries_and_aeroplanes_count()` — выводит страны и количество самолетов над ними (с использованием `LEFT JOIN`).
*   `get_all_aeroplanes()` — список всех самолетов в базе.
*   `get_avg_speed()` — средняя скорость всех судов.
*   `get_aeroplanes_with_higher_speed()` — самолеты со скоростью выше средней (подзапрос).
*   `get_aeroplanes_with_keyword(keyword)` — поиск по позывному (например, 'ACA').

## 👨‍💻 Автор
Василий
