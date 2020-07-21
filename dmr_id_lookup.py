from urllib.request import urlopen
from json import load
from os.path import normpath, dirname, realpath
from os import getcwd
from re import search
from shutil import copy2
from datetime import datetime
from sys import exit

def lookup_id(id):
    '''Returns the first name and callsign of the given user ID if it exists.'''

    # More information at: https://www.radioid.net/api
    query = 'https://database.radioid.net/api/dmr/user/?id=' + id
    response = load(urlopen(query))
    if(response['count'] == 0):
        # No records stored for queried ID
        return None
    else:
        # Extract the first name and callsign from the returned result
        result = response['results'][0]
        first_name = result['fname']
        callsign = result['callsign']
        lookup_result = (first_name, callsign)
        return lookup_result

def backup_file(dir, file_name):
    '''Creates a copy of the given file with the time prefixed.'''

    current_time = datetime.now().strftime('%Y%m%d%H%m%S')
    file_path = normpath(dir + '/' + file_name)
    backup_file_path = normpath(dir + '/' + current_time + '_' + file_name)
    copy2(file_path, backup_file_path)

def populate_empty_ids(dsd_folder):
    '''
    Populates empty DMR records in the given 'DSDPlus.radios' file with
    results from the radioid.net API.
    '''

    file_name = 'DSDPlus.radios'
    log_name = 'updated_records.log'
    file_path = normpath(dsd_folder + '/' + file_name)
    log_path = normpath(dsd_folder + '/' + log_name)

    # Read the DSDPlus.radios file into memory
    try:
        with open(file_path, 'r', encoding='UTF-8') as old_file:
            unpopulated_file = old_file.readlines()
    except FileNotFoundError:
        exit('DSDPlus.radios not found! Is the script in the same directory as the DSDPlus folder?')

    # Backup the current DSDPlus.radios file in case something goes wrong
    backup_file(dsd_folder, file_name)

    # Overwrite file with the contents of the old file and
    # populate the radio alias field if it is empty.
    with open(file_path, 'w', encoding='UTF-8') as new_file, open(log_path, 'a', encoding='UTF-8') as log_file:
        for line in unpopulated_file:
            # Check if current line is an empty DMR record
            # by checking if radio alias is literally ""
            if search(r'^DMR.*\"\".*$', line):
                # Get the ID by itself
                id = line.split(',')
                id = id[3].strip()

                lookup_result = lookup_id(id)
                if lookup_result is not None:
                    # Save the alias in the format: "First name (Callsign)"
                    new_alias = '"{} ({})"'.format(lookup_result[0], lookup_result[1])
                else:
                    new_alias = '"No record"'

                info_output = 'Populated ID {} with alias {}'.format(id, new_alias)
                print(info_output)
                log_file.write(info_output + '\n')
                
                # Write updated alias to the new file
                updated_line = line.replace('""', new_alias)
                new_file.write(updated_line)
            else:
                # Otherwise, copy the line verbatim.
                new_file.write(line)
        print('All records populated!')
        log_file.write('All records populated!\n\n')
                

if __name__ == '__main__':
    # Script must be in the DSDPlus folder
    dsd_folder = dirname(realpath(__file__))
    populate_empty_ids(dsd_folder)
    input('Press any key to exit')
    exit(0)
