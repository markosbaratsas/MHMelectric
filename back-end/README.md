# MHMelectric backend

[Django Framework](https://www.djangoproject.com/) and [Django REST Framework](https://www.django-rest-framework.org/) were used for the development of the backend system. The MHMelectric Django project consists of 2 different Django apps, one for consumption of the CLI and REST API calls, and another for user management and backend-frontend communication.

## Installation

### Requirements:
* `pip3` installed
* `python3` installed

### Instructions
After cloning this repo and going into the `backend` directory, you can run the following commands to get this django project ready on your pc.

1. Cd into the `back-end/` directory and create a virtual environment:
```
cd back-end/
python3 -m venv ./venv
```

2. Activate the virtual environment:
```
source venv/bin/activate
```

3. Install all the requirements for this project by running:
```
pip3 install -r requirements.txt
```

4. Go into the `back-end/MHMelectric/` directory, makemigrations and migrate:
```
python3 manage.py makemigrations
python3 manage.py migrate
```

5. Now, you can start the project by running:
```
python3 manage.py runserver 127.0.0.1:8765
```
This command will start the Django development server at localhost on port 8765.
