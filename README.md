# Diamond Vision API


### Spam Checker
Spam checker weren't available, so i've created a little one. :)

For best practices it should be as middleware,
but I thought that's overkill for this little project.

You can find it right in the endpoint code [here](./src/api/routers/complaints.py),
it saves in memory when you last made a request.

`One request should be made not faster than 10 seconds.`

### IP Info by API
I'm fetching data from [ip-api](https://ip-api.com),
but honestly I'm not even sure why.
Right now it just prints to console and logs to `LOG_FILE`.

### Environment file
Create your `.env` file using the template from [here](./src/.env.example)


### Start-up example
1. Create an `.env` file.
2. Install requirements: 
```bash 
  poetry install
```
3. Run the server.
```bash
  poetry run uvicorn src.main:app
```

### ⚠️ Don't Forget!

- **env.py** - Make sure to set your DB URL here:
```python
# Look for this line and change it:
sqlalchemy.url = your_database_url_here
```
- **alembic.ini** - Update this too:
```ini
[alembic]
sqlalchemy.url = your_database_url_here
```

### Request example

```bash
    curl -X POST http://api.example.com/complaints \
         -H "Authorization: Bearer $TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"text": "Complaint"}'
         -o response.json
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
- 429 Too Many Requests:
```json
{
  "message": "Too many requests.",
  "details": "Try again In 6 seconds later."
}
```
- 500 Internal Server Error:
```json
{
  "message": "<Error Type>",
  "details": "<Error Description>"
}
```