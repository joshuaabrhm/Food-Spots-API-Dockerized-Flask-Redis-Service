# Food Spots API

A small REST API for adding and listing food spots, built with **Flask** and **Redis**, and packaged with **Docker Compose** so the whole thing runs with a single command.

![CI](../../actions/workflows/ci.yml/badge.svg)

## Why I built this

To get hands-on with Docker: writing a Dockerfile, running a multi-container app with Compose, and keeping data alive across restarts with volumes. The structure was inspired by the [docker-curriculum](https://github.com/prakhar1989/docker-curriculum) tutorial.

## Tech stack

Python 3.12, Flask, Redis, Docker, Docker Compose, pytest, GitHub Actions

## Architecture

```
 client (curl / browser)
          |
          v
  +---------------+        +----------------+
  |  web (Flask)  | -----> |  redis         |
  |  port 5000    |        |  volume: data  |
  +---------------+        +----------------+
        docker-compose network (web reaches redis by hostname "redis")
```

## Run it

You need [Docker](https://docs.docker.com/get-docker/) installed.

```bash
git clone <your-repo-url>
cd food-spots-api
docker compose up --build
```

The API is now at `http://localhost:5000`.

## API

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| GET    | `/`      | Welcome message and visit counter |
| GET    | `/spots` | List all food spots |
| POST   | `/spots` | Add a spot (JSON body with `name` and `area`) |
| GET    | `/health`| Health check (pings Redis) |

### Try it

```bash
curl localhost:5000/
curl -X POST localhost:5000/spots \
  -H "Content-Type: application/json" \
  -d '{"name":"CTR","area":"Malleshwaram"}'
curl localhost:5000/spots
curl localhost:5000/health
```

Missing `name` or `area` returns `400`.

## Data persistence

Redis stores data in a named Docker volume (`redis-data`). Stop and restart with `docker compose down` then `docker compose up` and your spots are still there. To wipe everything: `docker compose down -v`.

## Run tests

Tests use `fakeredis`, so no Redis server is needed.

```bash
pip install -r requirements-dev.txt
python -m pytest -v
```

## Project structure

```
food-spots-api/
├── app.py                  # Flask app
├── requirements.txt        # runtime deps
├── requirements-dev.txt    # test deps
├── Dockerfile
├── docker-compose.yml      # web + redis
├── tests/test_app.py
└── .github/workflows/ci.yml  # tests + docker build on every push
```

## What I learned

- Image vs container, and how Dockerfile layer order affects build caching
- Service-name networking in Compose
- Using volumes for persistent data and env vars for config
- Writing tests that don't depend on external services
- Basic CI with GitHub Actions

## License

MIT
