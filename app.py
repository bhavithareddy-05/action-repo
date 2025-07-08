from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

@app.route('/webhook', methods=['POST'])
def github_webhook():
    data = request.json
    action_type = "UNKNOWN"
    payload = {}

    if 'commits' in data:
        action_type = "PUSH"
        commit = data['commits'][-1]
        payload = {
            "_id": commit['id'],
            "author": commit['author']['name'],
            "action": action_type,
            "from_branch": "",
            "to_branch": data['ref'].split('/')[-1],
            "timestamp": datetime.utcnow().isoformat()
        }

    elif 'pull_request' in data and data['action'] == "opened":
        action_type = "PULL_REQUEST"
        pr = data['pull_request']
        payload = {
            "_id": str(pr['id']),
            "author": pr['user']['login'],
            "action": action_type,
            "from_branch": pr['head']['ref'],
            "to_branch": pr['base']['ref'],
            "timestamp": datetime.utcnow().isoformat()
        }

    elif 'pull_request' in data and data['action'] == "closed" and data['pull_request']['merged']:
        action_type = "MERGE"
        pr = data['pull_request']
        payload = {
            "_id": str(pr['id']),
            "author": pr['user']['login'],
            "action": action_type,
            "from_branch": pr['head']['ref'],
            "to_branch": pr['base']['ref'],
            "timestamp": datetime.utcnow().isoformat()
        }
    else:
        return jsonify({"message": "Ignored event"}), 400

    mongo.db.events.insert_one(payload)
    return jsonify({"message": "Event recorded"}), 200

@app.route('/events', methods=['GET'])
def get_events():
    events = list(mongo.db.events.find().sort("timestamp", -1))
    for e in events:
        e["_id"] = str(e["_id"])
    return jsonify(events)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
