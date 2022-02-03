from typing import NoReturn
from ants_common import *

import coloredlogs
import logging
import pyautogui
# import threading
from PIL import Image
import enlighten
import gc
# import pyheif

STEP_SIZE = 20  # if zoom out, 10 if default zoom
AXIS_SIZE = 2 # int(MAP_SIZE / STEP_SIZE) + 1

#---------------------------------------------------------#


def get_snippet_file(x, y):
    return 'map/{}-{}.png'.format(x, y)


def make_screenshots():
    wbox = findWindowBbox()
    wboxWithoutUI = findWindowBbox(True)
    pyautogui.click(wbox[0] + 100, wbox[1] - 25)
    exit_to_map(wbox)

    manager = enlighten.get_manager()
    pbar = manager.counter(total=AXIS_SIZE * AXIS_SIZE,
                           desc='frames', unit='f')
    for x in range(AXIS_SIZE):
        changeX = True
        for y in range(AXIS_SIZE):
            changeX = changeX or y == 0
            filename = get_snippet_file(x, y)
            if not os.path.exists(filename):
                go_to_position(x * STEP_SIZE, y * STEP_SIZE,
                               wbox, changeX=changeX)
                changeX = False
                screen = get_window_screen(wboxWithoutUI)
                screen.save(filename)
                # threading.Thread(target=screen.save,
                #                  args=[filename]).start()
            else:
                changeX = True
            pbar.update()
        # logging.info('finished {} row'.format(x))

# def zoom_out(wbox):
#     centerx = (wbox[2] - wbox[0]) / 2
#     centery = (wbox[3] - wbox[1]) / 2
#     pyautogui.keyDown('option')
#     pyautogui.mouseDown(centerx, centery)
#     pyautogui.dragRel()

def merge_screenshots():
    snippet = Image.open(get_snippet_file(0, 0))
    logging.info('original snippet: {}'.format(snippet.size))
    sizex, sizey = snippet.size

    size_koef = 1
    temp_size = AXIS_SIZE

    sizex = int(sizex / size_koef)
    sizey = int(sizey / size_koef)

    HOFFSET = 115 / RETINA_KOEF
    VOFFSET = 480 / RETINA_KOEF

    hoffset = int(HOFFSET / size_koef)
    voffset = int(VOFFSET / size_koef)

    result_size = ((sizex - hoffset) * temp_size, (sizey - voffset) * temp_size)
    section_size = (int(sizex / RETINA_KOEF), int(sizey / RETINA_KOEF))

    logging.info('result size: {}'.format(result_size))
    logging.info('section size: {}'.format(section_size))

    result = Image.new(mode="RGB", size=result_size, color=(0, 0, 0))

    for x in range(temp_size):
        for y in range(temp_size):
            filename = get_snippet_file(x, y)
            if not os.path.exists(filename):
                continue
            with Image.open(filename) as section:
                section = section.resize(section_size)
                section_x = (result_size[0] - section_size[0]) / 2 + \
                            (y - x) * (section_size[0] - hoffset)

                section_y = (x + y) * (section_size[1] - voffset)

                section_x = int(section_x)
                section_y = int(section_y)
                result.paste(section, (section_x, section_y))

        logging.info('{} row finished'.format(x))
        gc.collect()

    # logging.info('resizing')
    # result.resize((int(result_size[0] / 2), int(result_size[1] / 2)))
    logging.info('saving')
    result.save('map.png')

#---------------------------------------------------------#


if __name__ == '__main__':
    try:
        coloredlogs.install(
            level='INFO', fmt='%(asctime)s %(levelname)s %(message)s')

        make_screenshots()
        merge_screenshots()
        # Image.MAX_IMAGE_PIXELS = None
        # with Image.open('map.png') as allmap:
        #     # allmap = allmap.resize((65500, 65500))
        #     allmap.save('map2.png', bitmap_format='png', dpi=(240, 240))

        exit(0)
    except pyautogui.FailSafeException as e:
        logging.error(e)
        exit(1)
    except RuntimeError as e:
        logging.error(e)
        exit(1)
    except OSError as e:
        logging.error(e)
        exit(1)
