# Описание
В репозитории представлен небольшой учебный проект на FastAPI, написанный в ходе прохождения курса от компании Y_LAB.
# Установка
## Зависимости
+ ### Redis
+ ### Postgresql
+ ### Python 3.10

# Порядок установки
## Создание базы данных в Postgresql
Необходимо создать новую БД в Postgresql
## Создание и активация локального окружения
```bash
python -m venv venv
venv\Scripts\activate
```
## Установка библиотек
```bash
pip install -r requirements.txt
```
## Создание файла переменных окружения
Нужно создать файл .env на уровне main.py по примеру из файла .env.example (можно просто скопировать)

## Применение миграции
```bash
alembic upgrade head
```
## Запуск
```bash
uvicorn main:app --reload
```

## Сборка образа docker-compose
```bash
docker compose build
```
## Запуск образа
```bash
docker compose up -d
```
После запуска образа сразу будет запущен контейнер с тестами, но его можно запустить повторно командой
```bash
docker start tests_app -a
```
