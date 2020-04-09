import os
import django
import json
import random

nr = 50

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fii_student.settings")
django.setup()
from personalise.models import Board, Personalise

GRUPE = ['-', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7',
         'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7',
         'X1', 'X2', 'X3', 'alta grupa']


def add_boards_and_get_ids(file_name):
    # load info from json
    b_list = []
    with open(file_name, 'r', encoding='utf8') as ff:
        boards = json.load(ff)
        for board in boards:
            b = Board(
                      year=board['year'],
                      subject=board['subject'],
                      teacher=board['teacher'],
                      description=board['description']
            )
            b.save()
            b_list.append(b)
    return b_list


def insert_values():

    # clear db
    Board.objects.all().delete()

    b_list = add_boards_and_get_ids('boards.json')
    return
    years = [1, 2, 3]
    #  populate db
    for _ in range(nr):
        if _ > len(list_names) - 1 or _ > len(list_surnames) - 1:
            break
        s = Student(name=list_names[_], surname=list_surnames[_], year=random.randrange(1, 4), semian=GRUPE[random.randrange(0, len(GRUPE)-1)])
        s.save()
        p = Personalise(user=s)
        p.save()
        board1 = b_list[random.randrange(0, len(b_list))]
        board2 = b_list[random.randrange(0, len(b_list))]
        p.boards.add(board1)
        # p.remove_board(board1)  # test remove
        p.boards.add(board2)
        p.save()
        p.init_orar()
        p.save()
        pass


def main():
    insert_values()


if __name__ == '__main__':
    main()
