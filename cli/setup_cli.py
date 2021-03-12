import pathlib
import in_place
import os

if __name__ == '__main__':
    path = pathlib.Path(__file__).parent.absolute()
    with open(os.path.expanduser('~/.bashrc'), 'a') as file:
        file.write("alias ev_group23='"+str(path)+"/ev_group23'\n")
    with in_place.InPlace(str(path)+"/ev_group23") as file:
        for line in file:
            if 'python3' in line:
                line = '    python3 '+ str(path)+ '/cli_side.py ${args}\n'
            file.write(line)