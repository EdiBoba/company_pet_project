# Company project

# Environment

* Python 3.8+

Install dependencies:
```shell
pip install -r requirements.txt
pip install -r requirements.migrations.txt
```

Run database:
```shell
docker compose up -d
```

Apply migrations:
```shell
alembic upgrade head
```

# Tear down environment

Downgrade migrations:
```shell
alembic downgrade base
```

Stop docker compose:
```shell
docker compose down
```
