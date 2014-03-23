TARGET?=tests

.PHONY: flake8 example test coverage

flake8:
	flake8 federated_login example tests

example:
	DJANGO_SETTINGS_MODULE=example.settings PYTHONPATH=. \
		django-admin.py runserver

test:
	DJANGO_SETTINGS_MODULE=tests.settings PYTHONPATH=. \
		django-admin.py test ${TARGET}

coverage:
	coverage erase
	DJANGO_SETTINGS_MODULE=tests.settings PYTHONPATH=. \
		coverage run --branch --source=federated_login \
		`which django-admin.py` test ${TARGET}
	coverage html
	coverage report
