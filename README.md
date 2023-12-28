# Retirement Calculator
Author: Ari Bernstein

Retirement calculator microservice written in Python.

## Running locally with Docker
1. Install [Docker](https://www.docker.com/products/docker-desktop/)
1. Run `docker compose up`

## Running locally (with suggested virtual environemnt)
```
cd src/
python -m venv venv
. venv/bin/activate
pip3 install -r requirements.txt
uvicorn main:app --reload
```
## Testing with Swagger docs
Navigate to http://localhost:8000/docs