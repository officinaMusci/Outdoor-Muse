# Outdoor Muse

Outdoor Muse is a web service that allows you to discover new outdoor places, know how to get there, how to come back and what the weather will be.

**Note:** It requires a Google API and an OpenWeather API accounts.

## .env file

To configure the project, create a .env file (gitignored) in  the project root :

```
LANGUAGE='en'
DATETIME_FORMAT='%Y-%m-%d %H:%M:%S.%f'

DB_ENGINE='sqlite:///outdoor_muse.db'

GOOGLE_KEY='...'
OPENWEATHER_KEY='...'

FLASK_ENV='development'
```

## Install:

```shell
sh PROJECT_PATH/install.sh
```

It automatically runs a test after the installing process.

## Test:

```shell
sh PROJECT_PATH/test.sh
```

## Run in development mode:

```shell
sh PROJECT_PATH/dev.sh
```