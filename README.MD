# Install:
    Pipenv install --dev
# To run server:

    uvicorn connexion_experiment.uwsgi_config:rate_limit --port=8893

## To test server:

    python ./tests/request_test.py
