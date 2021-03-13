# Testing MHMelectric system

## Backend testing
In order to validate that the API is working as expected, Django testing was used.

Django tests were created for each of the 2 django apps (rest_api, users) and, specifically, 2 different kind of tests for each app (test views and test urls).
To execute the backend tests, first you need to install the backend system (installation steps in directory backend/README.md), and, then you can run:
```
python3 manage.py test
```


## CLI testing
In order to validate that the CLI is working as expected, the module pytest was used.

The purpose of the tests was to test whether by providing specific arguments to CLI the right API call is executed or not.
To execute the tests, first you need to install the cli-client system (installation steps in directory cli-client/README.md), and, then located in the directory cli-client you can run:
```
python3 -m pytest test_cli.py
```
