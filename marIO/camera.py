from collector import *

class camera:

    pos_x = 0.0
    pos_y = 0.0

    length = 0.0
    width = 0.0
    screen = None

    garbage_collector = collector(50.0, 480.0, (100.0, 100.0, 100.0))

    def update( obj_lists):
        camera.pos_x = camera.player.ph.pos_x - camera.length / 2 + camera.player.ph.height / 2
        camera.pos_y = 0.0#camera.player.ph.pos_y - camera.width / 2 + camera.player.ph.width / 2
        camera.garbage_collector.update( camera.screen, obj_lists, (camera.pos_x, camera.pos_y))