# recipe-app-api
django rest api

## Running the app
`docker-compose up`

## Running the tests
`docker-compose run --rm app sh -c "python manage.py test"`

## Linting
`docker-compose run --rm app sh -c "flake8"`

## Create migrations based on model changes
`docker-compose run --rm app sh -c "python manage.py makemigrations"`

## Run migrations
`docker-compose run --rm app sh -c "python manage.py wait_for_db && python manage.py migrate"`

## Making new apps
`docker-compose run --rm app sh -c "python manage.py startapp recipe"`

## Create a superuser
`docker-compose run --rm app sh -c "python manage.py createsuperuser"`
