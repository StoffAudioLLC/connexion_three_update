# Install:

    cd connexion_three_update-master
    Pipenv install --dev
    Pipenv shell

## To run server:

    uvicorn connexion_experiment.uwsgi_config:rate_limit --port=8893

## To test server:

    python ./tests/request_test.py

### Features:

-ASGI Ratelimiting

-Example of Mime type parsing
