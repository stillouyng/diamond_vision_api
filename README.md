# Diamond Vision API


### Spam Checker
Spam checker weren't available, so i've created a little one. :)

For best practices it should be as middleware,
but I thought that's overkill for this little project.

You can find it right in the endpoint code [here](./src/api/routers/complaints.py),
it saves in memory when you last made a request.

`One request should be made not faster than 10 seconds.`

### How It Works

Currently, the site is available and located at [Render](https://diamond-vision-api.onrender.com),
but there is no homepage :)

About n8n, there is a problem. You can find n8n settings in [this folder](./pictures)
And yes, there is a bug in n8n logic. You can see that lines from both of conditions are going to
**one http-request**, but in that request logic is using only params from **If Category Is Technical**.

But I can explain :)

Unfortunately, there is no way to use Google credentials in the n8n trial-version.

Of course, I've created that ones. 
I've should use local n8n, but I forgot about that condition, that's my mistake.



### IP Info by API
I'm fetching data from [ip-api](https://ip-api.com),
but honestly I'm not even sure why.
Right now it just prints to console and logs to `LOG_FILE`.


### Environment file

Create your `.env` file using the template from [here](./src/.env.example)


### Quickstart

1. Create an `.env` file.
2. Create a database. Default location is: `./instance/database.sqlite`.
3. Install requirements: 
```bash 
  poetry install
```
4. Run the server.
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

### AI to classify the category

I used [Open Router](https://openrouter.ai) with Mistral-7B-v0.3 model for free.

### Request example

There are two ways to use server:
```text
    local_base_url = "http://127.0.0.1:8000/api/v1/complaints"
    router_base_url = "https://diamond-vision-api.onrender.com/api/v1/complaints"
```
- Add new complaint
```bash
    curl -X POST {{ base_url }} /add \
         -H "Content-Type: application/json" \
         -d '{"text": "Complaint"}'
         -o response.json
```
- Update complaint
```bash
    curl -X PATCH {{ base_url }} /update_complaint \
         -H "Content-Type: application/json" \
         -d '{"id": 1, *filters}'
         -o response_update.json
```
- Get New Complaints
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