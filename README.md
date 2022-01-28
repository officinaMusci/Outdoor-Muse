# Outdoor Muse

Outdoor Muse is a web service that allows you to discover new outdoor places, know how to get there, how to come back and what the weather will be.

**Note:** It requires a Google API and an OpenWeather API accounts.

## .env file

To configure the project, create a .env file (gitignored) in the project root :

```
LANGUAGE='fr'
DATETIME_FORMAT='%Y-%m-%d %H:%M:%S.%f'

SECRET_KEY='...'
JWT_SECRET_KEY='...'

GOOGLE_KEY='...'
OPENWEATHER_KEY='...'

FLASK_ENV='development'

DB_ENGINE='...'
```

## Install:

```shell
sh PROJECT_PATH/install.sh
```

It automatically generates HTML doc and runs a test after the installing process.

## Test:

```shell
sh PROJECT_PATH/api/test.sh
```

## Run in development mode:

```shell
sh PROJECT_PATH/api/run.sh
```