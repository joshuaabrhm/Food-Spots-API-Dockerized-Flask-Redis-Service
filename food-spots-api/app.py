import os
import json

import redis
from flask import Flask, jsonify, request

app = Flask(__name__)
r = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True,
)


@app.route("/")
def home():
    return jsonify(message="Food Spots API", visits=r.incr("hits"))


@app.route("/spots", methods=["GET"])
def list_spots():
    return jsonify([json.loads(s) for s in r.lrange("spots", 0, -1)])


@app.route("/spots", methods=["POST"])
def add_spot():
    data = request.get_json(silent=True) or {}
    if not data.get("name") or not data.get("area"):
        return jsonify(error="name and area are required"), 400
    spot = {"name": data["name"], "area": data["area"]}
    r.rpush("spots", json.dumps(spot))
    return jsonify(spot), 201


@app.route("/health")
def health():
    r.ping()
    return jsonify(status="ok")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
