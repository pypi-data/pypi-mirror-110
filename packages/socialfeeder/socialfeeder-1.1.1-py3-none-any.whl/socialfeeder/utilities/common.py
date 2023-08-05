import json
import datetime

def json_default(o):
    '''
    Json default method
    '''
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
    return o


def save_to_json_file(data:dict,file):
    '''
    Save json object to file
    '''
    with open(file, 'w', encoding='utf8') as outfile: 
        outfile.write(json.dumps(data, indent = 2, default=json_default, ensure_ascii=False))

class ObjectView(object):
    '''
    Convert nested dict to dynamic object
    '''
    def __init__(self, d, nested=True):
        self.origin = d
        for a, b in d.items():
            if nested:
                if isinstance(b, (list, tuple)):
                    setattr(self, a, [ObjectView(x) if isinstance(x, dict) else x for x in b])
                else:
                    setattr(self, a, ObjectView(b) if isinstance(b, dict) else b)
            else:
                setattr(self, a, b)

    def has_field(self, field):
        fields = field.split('.')
        if len(fields) == 0:
            return False

        obj = self.origin
        for f in fields:
            if f not in obj:
                return False
            obj = obj[f]
            
        return True