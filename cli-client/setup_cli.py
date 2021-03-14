import pathlib
import in_place
import os

if __name__ == '__main__':
    path = str(pathlib.Path(__file__).parent.absolute())
    os.system("chmod +x ev_group23")
    with in_place.InPlace(path+"/ev_group23") as file:
        for line in file:
            if 'python3' in line:
                line = '    python3 '+ path+ '/cli_side.py ${args}\n'
            file.write(line)

    os.system(f"cp {path}/ev_group23 {path}/venv/bin/ev_group23")