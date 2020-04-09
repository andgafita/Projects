import os
import json
import datetime

insert_command = "INSERT INTO resources(title, timestamp, url, content, type) VALUES("


def get_real_data():
    commands = []
    # log_id = -1
    for f in os.listdir(os.path.join(os.getcwd(), 'jsons')):
        # log_id += 1
        fpath = os.path.join(os.getcwd(), 'jsons', f)
        with open(fpath, 'rb') as fin:
            json_file = json.loads(fin.read().decode('utf-8'))
            if 'site' in json_file :
                new_command = insert_command + '\'' + json_file['title'] + '\',' + 'null' + ',\'' + json_file['site'] + '\',' + 'null,\'' + json_file['type'] + '\')'
            elif 'content' in json_file :
                new_command = insert_command + '\'' + json_file['title'] + '\',' + 'null' + ', null' + ',\'' + json_file['content'] + '\',\'' + json_file['type'] + '\')'
            # print(new_command)
            commands.append(new_command)
            # return commands
    return commands


if __name__ == "__main__":
    get_real_data()
