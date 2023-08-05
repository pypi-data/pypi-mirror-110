from socialfeeder.engines import core as chrome
from socialfeeder.utilities.constants import *
from datetime import datetime
import time
import random as r

def run(config, debug:bool=True, headless:bool=True):
    
    result = {
        'start_at': datetime.now(),
        'res_stack': []
    }
    
    if debug: print(f'[feeder] Starting feeding...')
    if debug: print(f'[feeder]  Open new driver instance.')
    driver = chrome.get_instance(headless=headless)

    if debug: print(f'[feeder]  Running actions...')
    for action_group in config:
        for action in action_group.actions:
            if action.url:
                driver.get(action.url)

            if action.type == ACTION_TYPE_WAIT:
                code, res = _do_wait(driver, action, debug=debug)
            elif action.type == ACTION_TYPE_BROWSE:
                code, res = _do_browse(driver, action, debug=debug)
            elif action.type == ACTION_TYPE_CLICK:
                code, res = _do_click(driver, action, debug=debug)
            elif action.type == ACTION_TYPE_FILL:
               code, res =  _do_fill(driver, action, debug=debug)
            elif action.type == ACTION_TYPE_SCROLL_DOWN:
               code, res =  _do_scroll_down(driver, action, debug=debug)
            elif action.type == ACTION_TYPE_SAVE_TEXT:
               code, res =  _do_save_text(driver, action, debug=debug)
            else:
                code, res = -1, 'Non-support action'
                if debug: print(f'[feeder]      Non-support action! Please contact ADMIN.')
            
            result['res_stack'].append({'code':code, 'message': res})

    result['end_at'] = datetime.now()
    result['duration_in_s'] = (result['end_at'] - result['start_at']).total_seconds()
    if debug: print(f'[feeder] Finished.')

    return result

    
def _do_save_text(driver, action, debug:bool=False, indent:int=1):
    if debug: print(f'[feeder] {"    "*indent}Doing {action.name}')
    try:
        elements = driver.find_elements_by_xpath(action.xpath_to)
        for element in elements:
            with open(action.value, 'a', encoding='utf8') as file:
                file.write((element.text or "").strip())
                file.write("\n")
    except Exception as e:
        if not action.bypass_error:
            return (-1, f'{action.name} failed with message: {str(e)}')
    return (0, f'{action.name} succeeded')


def _do_wait(driver, action, debug:bool=False, indent:int=1):
    if debug: print(f'[feeder] {"    "*indent}Doing {action.name}')
    try:
        wait_sec = int(action.value)
        if debug: print(f'[feeder] {"    "*(indent+1)}Waiting for ~{wait_sec} second(s)')
        time.sleep(int(r.uniform(1 if wait_sec < 3 else wait_sec-2, wait_sec)))
    except Exception as e:
        if not action.bypass_error:
            return (-1, f'{action.name} failed with message: {str(e)}')
    
    return (0, f'{action.name} succeeded')


def _do_browse(driver, action, debug:bool=False, indent:int=1):
    if debug: print(f'[feeder] {"    "*indent}Doing {action.name}')
    try:
        chrome.scroll_down_bottom(driver)
    except Exception as e:
        if not action.bypass_error:
            return (-1, f'{action.name} failed with message: {str(e)}')

    return (0, f'{action.name} succeeded')


def _do_scroll_down(driver, action, debug:bool=False, indent:int=1):
    if debug: print(f'[feeder] {"    "*indent}Doing {action.name}')
    try:
        chrome.scroll_down(driver, height=int(action.value))
    except Exception as e:
        if not action.bypass_error:
            return (-1, f'{action.name} failed with message: {str(e)}')

    return (0, f'{action.name} succeeded')


def _do_click(driver, action, debug:bool=False, indent:int=1):
    if debug: print(f'[feeder] {"    "*indent}Doing {action.name}')
    try:
        elements = driver.find_elements_by_xpath(action.xpath_to)
        limit = len(elements)
        if debug: print(f'[feeder] {"   "*(indent+1)}Found {limit} element(s)')

        if limit > int(action.value):
            limit = int(action.value)
        elements = elements[0:limit]
        if debug: print(f'[feeder] {"   "*(indent+1)}Will limit for {len(elements)} element(s)')
        for e in elements:
            if debug: print(f'[feeder] {"   "*(indent+1)}Click on {str(e.text[0:100])}')
            try: 
                e.click()
            except:
                chrome.click(driver, e)
    except Exception as e:
        if not action.bypass_error:
            return (-1, f'{action.name} failed with message: {str(e)}')

    return (0, f'{action.name} succeeded')

    
def _do_fill(driver, action, debug:bool=False, indent:int=1):
    if debug: print(f'[feeder] {"    "*indent}Doing {action.name}')
    try:
        elements = driver.find_elements_by_xpath(action.xpath_to)
        for e in elements:
            e.send_keys(action.value)
    except Exception as e:
        if not action.bypass_error:
            return (-1, f'{action.name} failed with message: {str(e)}')
    return (0, f'{action.name} succeeded')

