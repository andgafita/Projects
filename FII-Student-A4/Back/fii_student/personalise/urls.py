from django.urls import path

from .views import *

urlpatterns = [
    path(r'', show_personalise, name='personalise_show'),
    path('boards/', show_join_board, name='join_board_show'),
    path('boards/<id>/', BoardDetail.as_view(), name='board-detail'),
    path('add_board/', add_board, name='add_board'),
    path('boards/add_pref_board/<int:uid>/<int:bid>', add_pref_board, name='add_pref_board'),
    path('boards/remove_pref_board/<int:uid>/<int:bid>', remove_pref_board, name='remove_pref_board'),
    path('boards/check_joined_board/<int:uid>/<int:bid>', check_joined_board, name='check_joined_board'),
    path('boards/check_joined_boards/<int:uid>', check_joined_boards, name='check_joined_boards'),
    path('orar/', show_orar, name='show_orar'),
    path('orar/add_rand/<int:uid>/<int:rid>', add_rand, name='add_rand'),
    path('orar/remove_rand/<int:uid>/<int:rid>', remove_rand, name='remove_rand'),
    path('orar/check_rands/<int:uid>', check_rands, name='check_rands'),
    path('orar/orar_personalised/', show_orar_personalised, name='show_orar_personalised'),
    path('orar/orar_personalised/reset_orar/', reset_orar, name='reset_orar'),
    path('notificari/', show_notificari, name='show_notificari'),
    path('notificari/remove_notification/<int:id>', remove_notification, name='remove_notification'),

    # REST API for cards
    # path('cards/<int:uid>/<string:type>/<int:x>/<int:y>/<>')
    # path('cards/', get_cards, name='get_cards'),
    path('cards/add_card', add_card, name='add_card'),
    path('cards/update_card/<int:cid>', update_card, name='update_card'),
    path('cards/remove_card/<int:cid>', remove_card, name='remove_card')
]
