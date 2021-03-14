# MHMelectric data_insertion

This is a way to fill your database with some dummy data.

## Installation

### Requirements:
* `python3` installed
* electric_vehicles_data.json
* poi.json
* caltech_acndata_sessions_12month.json

These json files are free and were provided to us through the following [link](https://courses.pclab.ece.ntua.gr/mod/url/view.php?id=337).

### Instructions
After creating a new file named used_data.json by pasting into it the first 150 lines of the file poi.json, you can run the following commands to fill the database by being in the directory `MHMelectric/backend/MHMelectric`.

1. Fill the file `data_insertion/file_paths.json` (all except "json_to_csv", "json_to_csv_to_be_created") with the paths of the corresponding files mentioned above. In particular the correspondence is:
    * dummy_data: dummy_data.json (provided by us) 
    * helper_parse_charging_point: used_data.json 
    * charging_points:  an empty json file (the converted data from used_data.json will be inserted here)
    * electric_vehicles: electric_vehicles_data.json 
    * session: caltech_acndata_sessions_12month.json

2. Convert used_data.json into an appropriate form by running:
```
python3 manage.py shell < data_insertion/helper_parse_charging_point.py
```

3. Run the following commands to fill the database with data:
```
python3 manage.py shell < data_insertion/insert_dummy.py
```
```
python3 manage.py shell < data_insertion/electric_vehicles.py
```
```
python3 manage.py shell < data_insertion/charging_points.py
```
```
python3 manage.py shell < data_insertion/session.py
```


### Preparing some extra data for `admin/system/sessionsupd` API endpoint
1. Fill the file values "json_to_csv" and "json_to_csv_to_be_created" in `data_insertion/file_paths.json`, with your desired paths to files. Specifically:
    * json_to_csv: caltech_acndata_sessions_12month.json 
    * json_to_csv_to_be_created: caltech_acndata_sessions_12month.csv (the new file that will be created)

2. Run the following command to prepare the csv file:
```
python3 manage.py shell < data_insertion/json_to_csv.py
```

3. Now you can use the endpoint `admin/system/sessionsupd` as per specifications, and provide the new csv file on the request body. 


