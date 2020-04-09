import os
from time import sleep


FREQUENCY = 12*60*60


def autorun():

    current_path=os.getcwd()
    print(current_path)
    while(1):
        os.system("python manage.py loaddata ./orar/fixtures/orar_full.json")
        os.chdir(os.path.join(current_path, "resources/db"))
        os.system("python db_utils.py")
        os.chdir(current_path)
        os.chdir(os.path.join(current_path, "news/db"))
        os.system("python db_utils2.py")
        sleep(FREQUENCY)

try:
  autorun()
except NameError:
  print('well, it WASN\'T defined after all!')