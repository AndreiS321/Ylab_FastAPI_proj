# Описание
В репозитории представлен небольшой учебный проект на FastAPI, написанный в ходе прохождения курса от компании Y_LAB.
# Доп. задания
## ДЗ 2
1) ORM запрос в модуле models.py
2) Тестовый сценарий в tests\crud\test_cases.py
## ДЗ 4
1) Обновление данных из google sheets в admin\parsers.py
2) Блюда по акции реализованы там же в admin\parser.py
# Установка
## Зависимости
+ ### Redis
+ ### RabbitMQ
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
# Запуск
## Запуск приложения
```bash
uvicorn main:app --reload
```
# Celery
## Настройка Celery
Для использования нужно Excel файла для управления БД нужно:
1) Создать Excel файл формата одного из форматов .xlsx,.xlsm,.xltx,.xltm
2) Указать название файла в .env (по примеру из .env.example)

Для использования Google sheets вместо файла  Excel нужно:
1) Создать проект в Google Cloud
2) Добавить Google sheets API в проект
3) Создать сервисную почту и сгенерировать json-ключ
4) Скопировать файл в папку проекта admin
5) Прописать название файла в .env (по примеру из .env.example)
6) Прописать id таблицы (https://docs.google.com/spreadsheets/d/id_таблицы/)
## Запуск Celery
### Celery worker
```bash
celery -A admin.tasks:app worker
```
### Celery beat
```bash
celery -A admin.tasks:app beat
```

# Docker
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