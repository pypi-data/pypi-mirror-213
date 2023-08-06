"""
Download the JSON contents of an API endpoint
"""
import json
import shutil
import sys
from pathlib import Path

import requests

SETTINGS_FILE = Path('apidownload.json')


def fetch_endpoint(url: str, file: str, indent: int = 2):
    """
    Download the JSON data at url and save it in file
    """
    print('Updating ', file, sep='')
    try:
        request = requests.get(url, timeout=20)
    except requests.ConnectionError:
        print('\tCouldn\'t connect to', url, file=sys.stderr)
        return
    try:
        data = request.json()
    except requests.JSONDecodeError:
        print('\tInvalid JSON format returned', file=sys.stderr)
        return
    Path(file).write_text(json.dumps(data, indent=indent))
    print('\tDone')


def create_settings_file():
    """
    Copy the example settings.json file into this directory
    """
    shutil.copyfile(
        Path(__file__).parent / 'apidownload.json',
        SETTINGS_FILE
    )
    print('Created', SETTINGS_FILE.absolute())


def check_endpoint(endpoint: dict):
    valid = True
    if 'url' not in endpoint:
        print('Missing "url" parameter:', endpoint)
        valid = False
    if 'file' not in endpoint:
        print('Missing "file" parameter:', endpoint)
        valid = False
    return valid

def main():
    """
    Entry-point to program
    """
    if SETTINGS_FILE.exists():
        try:
            settings = json.loads(SETTINGS_FILE.read_text())
        except json.JSONDecodeError:
            print('Invalid JSON format:', SETTINGS_FILE.absolute(), file=sys.stderr)
            return
        for endpoint in settings:
            if isinstance(endpoint, dict):
                if check_endpoint(endpoint):
                    fetch_endpoint(**endpoint)
            else:
                print('Invalid endpoint type:', endpoint, file=sys.stderr)
    else:
        create_settings_file()


if __name__ == '__main__':
    main()
