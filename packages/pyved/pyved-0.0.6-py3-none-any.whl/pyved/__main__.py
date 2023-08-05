import argparse
import os
from pathlib import Path
from . import utils


parser = argparse.ArgumentParser(
    prog='pyved',
    description='runs PYVED and opens a new/existing project',
    epilog="pyved (=PY Visual Editor) is a new toolbox for easy game development. For more information, please visit "
           "https://github.com/wktab/gamedev-pyved/"
)
# configuration --
# besoin d'utiliser des sub parsers car on a plusieurs cmd
subparser = parser.add_subparsers(dest='command', required=True)
new = subparser.add_parser('new')
new.add_argument('project', type=str)  # , required=True)
register = subparser.add_parser('open')
register.add_argument('filepath', type=str)  # , required=True)
cmd = subparser.add_parser('version')
# -- fin configuration


# definition implem {{
def create_new_project(pname, tool_ver):
    target_dir = Path(pname)
    if target_dir.exists():
        print(f"ERROR: folder {target_dir} already exists")
    else:
        os.mkdir(target_dir)
        print(f" +Initializing a new project named \"{target_dir}\"...")
        DB_QT = '"'
        with open(os.path.join(target_dir, 'pyved.json'), 'w') as fout:
            fout.write("{\n")
            fout.write(' ' * 4 + '"tag":' + DB_QT + 'pyved' + tool_ver + DB_QT + ",\n")
            fout.write(' ' * 4 + '"project":' + DB_QT + pname + DB_QT + ",\n")
            fout.write("}")

        # main source-code file
        with open(os.path.join(target_dir, 'main.py'), 'w') as fout:
            fout.write("import katagames_engine as kengi")
            fout.write("\n")
            fout.write("kengi.init()")


def open_project(desc_ptr, dirname):
    print('*' * 32)
    print(' Welcome to PYVED')
    print('*' * 32)

    print()
    print(desc_ptr.read())
    print('---')

    print('Listing files:')

    t_dir = Path(dirname)
    has_main = False
    for entry in t_dir.iterdir():
        print(entry.name)
        if 'main.py' == entry.name:
            has_main = True
    if not has_main:
        raise Exception('invalid project format! main.py not found in the project folder')

    # ouverture projet avec format valide ds l'editor
    from . import editor
    editor.target_dir = dirname
    editor.target_file = 'main.py'
    editor.run_editor()


# }} definition implem


# ------
#  main chunk of code
# -----
def main():
    # tool_version = pyved.__version__
    tool_ver = utils.get_version()

    args = parser.parse_args()
    if args.command == 'new':
        create_new_project(args.project, tool_ver)

    elif args.command == 'open':
        filepath = os.path.abspath(args.filepath)
        dirname = os.path.dirname(filepath)
        if not os.path.isfile(os.path.join(dirname, filepath)):
            print(f"ERROR: cannot read the file {filepath}, please provide a valid pyved.json FILE")
        else:
            fptr = open(filepath, 'r')
            open_project(fptr, dirname)
            fptr.close()

    elif args.command == 'version':
        print(f"PYVED - version {tool_ver}")
    else:
        print(f"ERROR: command {args.command} is not a valid command!")


if __name__ == '__main__':
    main()
