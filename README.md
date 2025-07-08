# action-repo
# GitHub Webhook Listener

## Features
- Listens to GitHub webhooks for PUSH, PULL_REQUEST, MERGE events
- Stores them in MongoDB
- Frontend fetches and displays events every 15 seconds

## Setup Instructions

### Backend
1. `cd backend`
2. Create `.env` file with:
   ```
   MONGO_URI=<your MongoDB URI>
   ```
3. `pip install -r requirements.txt`
4. `python app.py`

### Frontend
Open `frontend/index.html` in browser.

### Ngrok for Webhook Testing
```
ngrok http 5000
```
Use the generated HTTPS URL in GitHub → Settings → Webhooks

Select events: push, pull_request
