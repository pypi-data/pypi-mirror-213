init:
	pip install -r requirements.txt

test:
	PYTHONDONTWRITEBYTECODE=1 py.test tests --cov=pyhip -v # -x --cov-report html

lint:
	pylint --min-similarity-lines=20 src/pyhip
