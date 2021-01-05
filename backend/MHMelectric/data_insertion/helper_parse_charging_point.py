# In order to insert the given data I copied first 150 lines of `poi.json` into `used_data.json`.
# Then I run the following script to get a json that can be loaded...


path_to_file = "/mnt/c/Users/markg/Downloads/OneDrive_1_05-01-2021/charging_points_europe_json/used_data.json"
fw = open("/mnt/c/Users/markg/Downloads/OneDrive_1_05-01-2021/charging_points_europe_json/ready_data.json", "w+")
fw.write('{ "data": [')
with open(path_to_file) as f:
    data = f.read()
    hello = data.split("\n")
    for i in hello:
        fw.write(i + ",\n")

fw.write("]}")
fw.close()