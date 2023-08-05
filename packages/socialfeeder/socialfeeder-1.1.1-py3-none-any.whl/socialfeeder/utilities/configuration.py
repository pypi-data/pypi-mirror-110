import bs4
from lxml import etree
import os
from socialfeeder.utilities.common import ObjectView, save_to_json_file
from socialfeeder.utilities.constants import *

def parse(path:str, save:bool=False):
    '''
    Parse xml document to dict object
    '''
    # Load xml
    print(f'INFO: XML file at: {path}')
    lxml_content = open(file=path,mode="r",encoding="utf8").read()
    soup = bs4.BeautifulSoup(lxml_content, "lxml")
    
    # Load xml schema - xsd to validate
    xsd_path = f'{os.path.dirname(os.path.realpath(__file__))}/configuration.xsd'
    # valid, message = _validate(xml_path=path, xsd_path=xsd_path)
    # if not valid:
    #     print(f'ERROR: Failed at validation with message: {message}')
    #     return None
    
    results = []
    pages = soup.findAll("page")
    for page in pages:
        # result - base
        result = {
            "config_at": os.path.abspath(path),
            "actions": _parse_actions(page.find("actions"))
        }

        results.append(ObjectView(result))
        
    if save:
        save_to_json_file(results[0].origin, path.replace('.xml', '.json'))
    return results


def _parse_actions(soup):
    '''
    Function to parse "action" nodes
    '''
    actions = []
    for a in soup.find_all("action", recursive=False):
        default_value = ''
        action_type = a.get("type")
        if action_type == ACTION_TYPE_CLICK:
            default_value = '1' # click max 1 element
        elif action_type == ACTION_TYPE_WAIT:
            default_value = '3' # click max 1 element

        actions.append({
            "name": a.get("name") or f'{a.get("type")} to {(a.get("xpath-to") or "")[0:10]}',
            "url": a.get("url") or '',
            "type": action_type,
            "value": a.get("value") or default_value,
            "bypass_error": True if (a.get("bypass-error") or 'false').lower() in ['true', '1'] else False,
            "xpath_to": a.get("xpath-to") or ''
        })
    
    return actions

def _validate(xml_path:str, xsd_path:str) -> bool:
    '''
    Validate xml schema of the config file
    '''
    # xmlschema_doc = etree.parse(xsd_path)
    # xmlschema = etree.XMLSchema(xmlschema_doc)

    # xml_doc = etree.parse(xml_path)
    # result = xmlschema.validate(xml_doc)

    pass #return (result, xmlschema.error_log)