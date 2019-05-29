test:
	pipenv run pytest --cov

.DEFAULT_GOAL := test
