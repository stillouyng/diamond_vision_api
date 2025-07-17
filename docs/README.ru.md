[🇺🇸 English](../README.md) |  [🇷🇺 Русский](README.ru.md)


# Diamond Vision API

[![Workflow](https://github.com/stillouyng/diamond_vision_api/actions/workflows/workflow.yml/badge.svg)](https://github.com/stillouyng/diamond_vision_api/actions/workflows/workflow.yml)

### Stack
Poetry, FastAPI, httpx, SQLAlchemy 2.0, pydantic, Alembic, pytest, Flake8, n8n  


### Spam Checker
Сайт spam-checker не доступен, поэтому я добавил маленькую проверку. 

Для лучшей практики, проверка на спам должна была быть как middleware,
но, я подумал, что это будет чересчур.

Вы можете найти проверку прямо в коде эндпоинта: [здесь](../src/api/routers/complaints.py),
Код сохраняет запросы в памяти с проверкой следующего правила:

`Один запрос не чаще, чем раз в 10 секунд.`

### How It Works

В текущей инстанции, сайт расположен и доступен на сайте [Render](https://diamond-vision-api.onrender.com),
без домашней страницы :)

Так же, прошу учесть, что сайт запускается в течение минуты после первого запроса.

Насчет n8n, есть небольшая проблема. Вы можете найти скриншоты настроек n8n в папке [pictures](../pictures).
Я забыл о том, что онлайн версия n8n не позволяет указывать credentials.json от Google :(

### IP Info by API
Я получаю данные из [ip-api](https://ip-api.com),
но, честно говоря, я не совсем понял зачем.
Прямо сейчас данные выводятся в консоль и сохраняются в `LOG_FILE`.


### Environment file

Создайте ваш `.env` файл, используя шаблон [.env.example](../src/.env.example)


### Quickstart

1. Создайте `.env` файл.
2. Создайте файл базы данных. Стандартный путь: `./instance/database.sqlite`.
3. Установите зависимости: 
```bash 
  poetry install
```
4. Запустите сервер.
```bash
  poetry run uvicorn src.main:app
```

### ⚠️ Don't Forget!

- **env.py** - Удостоверьтесь что вы задали путь к базе данных:
```python
# Look for this line and change it:
sqlalchemy.url = your_database_url_here
```
- **alembic.ini** - Не забудьте обновить этот путь тоже:
```ini
[alembic]
sqlalchemy.url = your_database_url_here
```

### AI to classify the category

Я использую [Open Router](https://openrouter.ai) c ИИ Mistral-7B-v0.3.

### Request example

Существует два возможных пути расположения сервера:
```text
    local_base_url = "http://127.0.0.1:8000/api/v1/complaints"
    router_base_url = "https://diamond-vision-api.onrender.com/api/v1/complaints"
```
- Добавить новую жалобу
```bash
    curl -X POST {{ base_url }} /add \
         -H "Content-Type: application/json" \
         -d '{"text": "Complaint"}'
         -o response.json
```
- Обновить жалобу
```bash
    curl -X PATCH {{ base_url }} /update_complaint \
         -H "Content-Type: application/json" \
         -d '{"id": 1, *filters}'
         -o response_update.json
```
- Получить новые жалобы (С стандартным фильтром "за последний час")
```bash
    curl -X GET {{ base_url }} /get_new_complaints \
         -H "Content-Type: application/json" \
         -o response_list.json
```


### Responses
- 201 Created:
```json
{
  "id": 1,
  "text": "Complaint",
  "status": "open",
  "created_at": "2025-07-13T12:00:00",
  "sentiment": "neutral"
}
```
- 422 Validate Error:
```json
{
  "message": "Validate error.",
  "details": "Validated fields description."
}
```
- 429 Too Many Requests:
```json
{
  "message": "Too many requests.",
  "details": "Try again In <sec_last> seconds later."
}
```
- 500 Internal Server Error:
```json
{
  "message": "<Error Type>",
  "details": "<Error Description>"
}
```