from ants_common import *

import coloredlogs
import pytesseract

STEP_SIZE = 20  # if zoom out, 10 if default zoom
AXIS_SIZE = int(MAP_SIZE / STEP_SIZE) + 1

def find_in_section(x, y, query):
    filename = 'map/{}-{}.png'.format(x, y)
    result = pytesseract.image_to_string(
        filename,
        lang='+'.join(LANGUAGES),
        config=CUSTOM_CONFIG
    ).splitlines()
    result = ''.join(result)
    result = result.replace(' ', '')
    result = result.lower()
    # logging.info(result)
    if query in result:
        logging.info('found @ {}:{}'.format(x, y))

if __name__ == '__main__':
    try:
        coloredlogs.install(
            level='INFO', fmt='%(asctime)s %(levelname)s %(message)s')

        query = 'введите'
        for x in range(AXIS_SIZE):
            for y in range(AXIS_SIZE):
                find_in_section(x, y, query)
            logging.info('{} row finished'.format(x))
    except RuntimeError as e:
        logging.error(e)