# Описание

...

# Запуститиь демо контейнер

```bash
docker compose up
```

Взаимодействовать с сервисом можно через [интерактивную документацию API](http://localhost:10008/docs)

## Что происходит во время запуска демо контейнера

...

# Swagger

...

## Полезные команды

### run migrations

```bash
alembic upgrade head
```

### create migration file

```bash
alembic revision --autogenerate -m "init"
```

### run tests

```bash
pytest -vv tests
```
