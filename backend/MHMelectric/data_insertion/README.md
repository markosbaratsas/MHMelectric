# MHMelectric data_insertion

This is a way to fill your database with some dummy data.

## Installation

### Requirements:
* `python3` installed
* electric_vehicles_data.json
* poi.json
* caltech_acndata_sessions_12month.json

### Instructions
After creating a new file named used_data.json by pasting into it the first 150 lines of the file poi.json, you can run the following commands to fill the database by being in the directory MHMelectric/backend/MHMelectric.

1. You need to set up your database by running the following commands:
```
python3 manage.py makemigrations
```
```
python3 manage.py migrate
```

2. Fill the file data_insertion/file_paths.json (all except "json_to_csv") with the paths of the corresponding files mentioned above. In particular the correspondence is:
* dummy_data: dummy_data.json (provided by us) 
* helper_parse_charging_point: used_data.json 
* charging_points:  an empty json file (the converted data from used_data.json will be inserted here)
* electric_vehicles: electric_vehicles_data.json 
* session: caltech_acndata_sessions_12month.json

3. Convert used_data.json into an appropriate form by running:
```
python3 manage.py shell < data_insertion/helper_parse_charging_point.py
```

4. Run the following commands to fill the database with data:
```
python3 manage.py shell < data_insertion/insert_dummy.py
```
```
python3 manage.py shell < data_insertion/electric_vehicles.py
```
```
python3 manage.py shell < data_insertion/session.py
```
```
python3 manage.py shell < data_insertion/charging_points.py
```


