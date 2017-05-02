#!/bin/env python3
"""
CurseMeta

Use output of https://github.com/NikkyAI/alpacka-meta to make static metadata 
used by CurseModpackDownloader v1.x to get all modfiles.

Copyright 2017 Dries007

Licensed under the EUPL, Version 1.1 only (the "Licence");
You may not use this work except in compliance with the Licence.
You may obtain a copy of the Licence at:

https://joinup.ec.europa.eu/software/page/eupl5

Unless required by applicable law or agreed to in writing, software
distributed under the Licence is distributed on an "AS IS" basis,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the Licence for the specific language governing
permissions and limitations under the Licence.
"""
import calendar
import sys
import getopt
import json
import time

from pathlib import Path


def parse_top_level_files(file):
    ids = set()

    with open(file) as f:
        data = json.load(f)["Data"]

    for project in data:
        ids.add(project["Id"])

    return ids


def parse_addon_folder(addon_folder, output_folder, **kwargs):
    for i, project in enumerate(addon_folder.iterdir()):
        project_in = Path(addon_folder, project.name)
        project_files = Path(project_in, 'files')
        project_out = Path(output_folder, project.name)
        project_id = int(project.name)

        project_out.mkdir(parents=True, exist_ok=True)
        types = []
        for name, ids in kwargs.items():
            if project_id in ids:
                types.append(name)
        project_type = ','.join(types) if len(types) != 0 else "UNKNOWN"

        print("Parsing project nr", i, "id:", project_id, "type:", project_type)

        # make out/<projectid>.json
        with open(Path(project_in, 'index.json')) as f:
            data = json.load(f)
        with open(Path(output_folder, project.name).with_suffix('.json'), 'w') as f:
            json.dump(data, f)

        ids = set()
        # make out/<projectid>/files.json
        with open(Path(project_files, 'index.json')) as f:
            data = json.load(f)
        for file in data:
            ids.add(file['Id'])
        with open(Path(project_out, 'files.json'), 'w') as f:
            json.dump(data, f)

        # make out/<projectid>/index.json
        with open(Path(project_out, 'index.json'), 'w') as f:
            json.dump({'type': project_type, 'ids': sorted(ids)}, f)

        # make out/<projectid>/<fileid>.json
        for j, file in enumerate(project_files.iterdir()):
            if file.name == "index.json":
                continue
            with open(file) as f:
                data = json.load(f)
            with open(Path(project_out, file.name), 'w') as f:
                json.dump(data, f)


def run(input_folder, output_folder):
    if not input_folder.is_dir():
        raise IOError("Input not a folder.")
    output_folder.mkdir(parents=True, exist_ok=True)
    if not output_folder.is_dir():
        raise IOError("Input not a folder.")

    print("Parsing mods.json ...")
    mods = parse_top_level_files(Path(input_folder, "mods.json"))
    print("Parsing modpacks.json ...")
    modpacks = parse_top_level_files(Path(input_folder, "modpacks.json"))
    print("Parsing complete.json ...")
    complete = parse_top_level_files(Path(input_folder, "complete.json"))
    print("Parsing addons ...")
    parse_addon_folder(Path(input_folder, "addon"), output_folder, mod=mods, modpack=modpacks)

    with open(Path(output_folder, 'index.json'), 'w') as f:
        json.dump({
            'timestamp': calendar.timegm(time.gmtime()),
            'timestamp_human': time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime()),
            'mods': sorted(mods),
            'modpacks': sorted(modpacks),
            'ids': sorted(complete),
        }, f)


def main(argv):
    input_folder = 'in'
    output_folder = 'out'
    try:
        opts, args = getopt.getopt(argv, 'hi:o:', ['help', 'input=', 'output='])
    except getopt.GetoptError:
        print('test.py -i <input_folder> -o <output_folder>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('test.py -i <input_folder> -o <output_folder>')
            sys.exit()
        elif opt in ('-i', '--input'):
            input_folder = arg
        elif opt in ('-o', '--output'):
            output_folder = arg
    print('Input folder is:', input_folder)
    print('Output folder is:', output_folder)

    run(Path(input_folder).resolve(), Path(output_folder).resolve())


if __name__ == '__main__':
    main(sys.argv[1:])
