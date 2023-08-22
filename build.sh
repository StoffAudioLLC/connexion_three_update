# because AWS Linux doesn't have make by default
# pip freeze>requirements.txt
pipenv run black .
pipenv run ruff .
pipenv run pytest . --doctest-modules
pipenv run coverage run --source=copyright-shared-lambda -m pytest .
pipenv run coverage report
pipenv run coverage html
pipenv run poetry build