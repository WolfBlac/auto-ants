
from curses import raw
import os
import logging
import pygetwindow
import pyautogui
import time
import re
from curses.ascii import isalpha
from colorama import Fore

MAP_SIZE = 1200
# possibly Retina correction, not sure - but it's required
RETINA_KOEF = 2
KEY_PRESS_INTERVAL = 0.2
PROGRAM_NAME = 'The Ants'
LANGDATA = os.path.dirname(os.path.realpath(__file__)) + "/tessdata"
# Page segmentation modes:
#   0    Orientation and script detection (OSD) only.
#   1    Automatic page segmentation with OSD.
#   2    Automatic page segmentation, but no OSD, or OCR.
#   3    Fully automatic page segmentation, but no OSD. (Default)
#   4    Assume a single column of text of variable sizes.
#   5    Assume a single uniform block of vertically aligned text.
#   6    Assume a single uniform block of text.
#   7    Treat the image as a single text line.
#   8    Treat the image as a single word.
#   9    Treat the image as a single word in a circle.
#  10    Treat the image as a single character.
#  11    Sparse text. Find as much text as possible in no particular order.
#  12    Sparse text with OSD.
#  13    Raw line. Treat the image as a single text line,
#                         bypassing hacks that are Tesseract-specific.

# OCR Engine modes:
# 0 Legacy engine only.
# 1 Neural nets LSTM engine only.
# 2 Legacy + LSTM engines.
# 3 Default, based on what is available.
CUSTOM_CONFIG = '--oem 3 --psm {} --tessdata-dir {}'.format(11, LANGDATA)

LANGUAGES = ['eng', 'rus', 'chi_sim']

xLocBox = None
yLocBox = None
fLocBox = None
fBox = None

#---------------------------------------------------------#

def print_rsp(param, inhex=False):

    # define colors
    GREEN = Fore.GREEN
    RED   = Fore.RED
    RESET = Fore.RESET

    # data = str(data)
    data = bytearray(param, encoding="raw_unicode_escape")
    # print(data.hex('_', 4))
    data = data.decode('unicode_escape').encode('raw_unicode_escape')
    # data = data.encode('raw_unicode_escape')
    # return
    # data = param.replace(r'\\x', r',\x')
    # data = data.replace(b'\\\\x',b',\\x')
    # data = data.split(',')

    # print(data)
    # for chunk in data:
        # chunk_bytes = bytearray(chunk, encoding="raw_unicode_escape")
        # print(chunk_bytes)
    # print(chunk)
    for i in data:
        if isalpha(i):
            print(' {}{}{}'.format(RED, chr(i), RESET), end="")
        else:
            print(' {}'.format(hex(i)[2:] if inhex else int(hex(i), 16)), end="")
            # print(' {}'.format(), end="")
        # print()

    print()
    print()

#---------------------------------------------------------#

def findWindowBbox(cropUI=False):
    logging.info('getting window bbox with{} UI'.format('out' if cropUI else ''))
    geometry = None
    if '{} {}'.format(PROGRAM_NAME, PROGRAM_NAME) not in pygetwindow.getAllTitles():
        logging.warning(
            'it seems {} are not launched, waiting...'.format(PROGRAM_NAME))
    while not geometry:
        geometry = pygetwindow.getWindowGeometry(PROGRAM_NAME)
        time.sleep(1)
        logging.debug(pygetwindow.getAllTitles())

    # title + resource bar
    titleCorrection = (25 + 60) if cropUI else 0
    chatCorrection = -100 if cropUI else 0

    return (
        geometry[0] * RETINA_KOEF,
        (geometry[1] + titleCorrection) * RETINA_KOEF,
        (geometry[2] + geometry[0]) * RETINA_KOEF,
        (geometry[3] + geometry[1] + chatCorrection) * RETINA_KOEF
    )


def get_window_screen(wbox):
    return pyautogui.screenshot().crop(wbox)


def to_coord(x, y, wbox):
    return ((wbox[0] + x) / RETINA_KOEF, (wbox[1] + y) / RETINA_KOEF)


def find_picture(picture, path, confidence=0.9, throw=True):
    box = pyautogui.locate(path, picture, confidence=confidence)

    if not box:
        if throw:
            raise RuntimeError("%s not found" % path)
        else:
            logging.debug('{} not found'.format(path))
            return None

    return (box.left, box.top, box.left + box.width, box.top + box.height)

#---------------------------------------------------------#

def exit_to_map(wbox):
    logging.info('exiting to map')
    backBox = True
    while backBox is not None:
        screen = get_window_screen(wbox)
        backBox = find_picture(screen, 'resources/back.png', throw=False)
        if backBox:
            pyautogui.click(to_coord(backBox[0] + 20, backBox[1] + 20, wbox))
            time.sleep(0.5)

    outBox = find_picture(screen, 'resources/nestout.png', throw=False)
    if outBox:
        pyautogui.click(to_coord(outBox[0] + 50, outBox[1] + 50, wbox))

    while not find_picture(screen, 'resources/search.png', throw=False):
        time.sleep(0.5)
        screen = get_window_screen(wbox)


def press_done(wbox):
    pyautogui.click(to_coord(50, wbox[3] - 100, wbox))

# TODO
def scan_current_coord(wbox):
    pass
    # screen = get_window_screen()
    # sbox = find_picture(screen, 'resources/server.png')
    # lbox = find_picture(screen, 'resources/location.png', 0.5)
    # current_coord = screen.crop((
    #     sbox[2] + 10,
    #     sbox[1],
    #     lbox[0],
    #     sbox[3]
    # ))

    # coord_config = '{} -c tessedit_char_whitelist=0123456789XY:'.format(CUSTOM_CONFIG)
    # coord = pytesseract.image_to_string(
    #     current_coord,
    #     config=coord_config
    # ).strip()


def go_to_position(x, y, wbox, screen=None, changeX=True):
    logging.debug('Going to [%s:%s]' % (x, y))

    if not screen:
        screen = get_window_screen(wbox)

    sbox = find_picture(screen, 'resources/search.png')
    pyautogui.click(to_coord(sbox[0] + 20, sbox[1] + 20, wbox), button=pyautogui.LEFT)
    time.sleep(1)
    screen = get_window_screen(wbox)

    global fBox
    if not fBox:
        fBox = find_picture(screen, 'resources/locateinactive.png', 0.9, False)
        if fBox:
            pyautogui.click(to_coord(fBox[0] + 20, fBox[1] + 20, wbox))
            screen = get_window_screen(wbox)

    fBox = find_picture(screen, 'resources/locateactive.png', 0.9)

    if changeX:
        global xLocBox
        if not xLocBox:
            xLocBox = find_picture(screen, 'resources/locx.png')
        pyautogui.click(to_coord(xLocBox[0] + 100, xLocBox[1] + 10, wbox))
        # TODO: meh
        pyautogui.keyDown('backspace')
        pyautogui.keyDown('backspace')
        pyautogui.keyDown('backspace')
        pyautogui.keyDown('backspace')

        pyautogui.typewrite(str(x), interval=KEY_PRESS_INTERVAL)
        press_done(wbox)

    global yLocBox
    if not yLocBox:
        yLocBox = find_picture(screen, 'resources/locy.png')
    pyautogui.click(to_coord(yLocBox[0] + 100, yLocBox[1] + 20, wbox))
    # TODO: meh
    pyautogui.keyDown('backspace')
    pyautogui.keyDown('backspace')
    pyautogui.keyDown('backspace')
    pyautogui.keyDown('backspace')

    pyautogui.typewrite(str(y), interval=KEY_PRESS_INTERVAL)
    press_done(wbox)

    global fLocBox
    if not fLocBox:
        fLocBox = find_picture(screen, 'resources/find.png', 0.9)
    pyautogui.click(to_coord(fLocBox[0] + 40, fLocBox[1] + 40, wbox))

    time.sleep(1)

#---------------------------------------------------------#
