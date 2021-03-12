# Simple guide to get started with the CLI on your (linux) PC

## Requirements:
* `pip3` installed
* `python3` installed

## Instructions
After cloning this repo and going into the `cli` directory, you can run the following commands to get this cli running.

1. First, run the django server, that exists on the backend folder of this repo (since the CLI communicates with the backend API)

2. On a new terminal (different than the previous that runs the Django server), cd into the cli/ directory, create a virtual environment to run the CLI, by executing:
```
python3 -m venv ./venv
# and activate the venv
source venv/bin/activate
```

2. Install all the requirements for the CLI by running (into the cli/ directory):
```
pip3 install requirements.txt 
# or pip3 install -r requirements.txt
```

3. Then, run the following, in order to set up the CLI (into the cli/ directory):
```
python3 
```

4. The CLI is ready, you can run the following to see the available commands:
```
ev_group23 --help
```

## Notes:
In order to be able to run the `ev_group23` directly, you need to have activated the virtual environment (since the ev_group23 bash script is in the venv/bin directory and it needs to be in the $PATH ).
