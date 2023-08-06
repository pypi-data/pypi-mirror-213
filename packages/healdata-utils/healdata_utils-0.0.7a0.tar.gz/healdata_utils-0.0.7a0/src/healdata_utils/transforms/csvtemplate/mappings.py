''' 
contains mappings (both lambda functions or column mappings)
''' 

from healdata_utils import schemas
# split array columns
def split_str_array(string,sep='|'):
    if string:
        return [s.strip() for s in string.split(sep)]
    else:
        return None

# if object within array, assign to properties
def map_keys_vals(keys,vals):
    ''' zips two lists of the same size as 
    a dictionary
    ''' 
    return dict(zip(keys,vals))

def split_and_map(string,prop):
    ''' 
    splits nested stringified delimited lists 
    (delimiters being | for outer and = for inner)
    and zips/maps each of the inner lists to a set
    of values (right now keys of a dictionary)
    TODO: rename function split_and_map_to_keys
    TODO: generalize to more than keys


    '''
    if string:
        keys = prop['items']['properties'].keys()
        return [
            map_keys_vals(keys,split_str_array(x,sep='=')) 
            for x in split_str_array(string,sep='|')
        ]
    else:
        return None

def loads_dict(string,item_sep='|',key_val_sep='='):
    if string:
        return dict([split_str_array(s,key_val_sep) 
            for s in split_str_array(string,item_sep)])
def mapval(v,mapping):
    v = str(v)
    if v in mapping:
        return mapping[v]
    else:
        return v

def to_bool(v):
    if v.lower() in true_values:
        return True 
    elif v.lower() in false_values:
        return False 
    else:
        return ""
        
typemap = {
    #from bacpac
    'text':'string',
    'float':'number',
    #from hemo
    'NUM':'number',
    'CHAR':'string'
}

formatmap = {
    'ISO8601':'' # NOTE: this is the default date format for frictionless so not necessary to specify
}

props = schemas.healjsonschema['properties']
    #mappings for array of dicts, arrays, and dicts


true_values = ["true","1","yes","required","y"]
false_values = ["false","0","no","not required","n"]



fieldmap = {
    'constraints.required': lambda v: to_bool(v),
    'constraints.enum': lambda v: split_str_array(v),
    # 'constraints.maximum':int,
    # 'constraints.minimum':int, #TODO:need to add to schema
    # 'constraints.maxLength':int,
    'cde_id': lambda v: split_and_map(v, props['cde_id']),
    'ontology_id': lambda v: split_and_map(v, props['ontology_id']),
    'encoding':lambda v: loads_dict(v),
    'format': lambda v: mapval(v,formatmap),
    'type':lambda v: mapval(v,typemap),
    #'univar_stats.cat_marginals':lambda v: split_and_map(v, prop['univar_stats']['cat_marginals']),
    'missingValues':lambda v: split_str_array(v),
    'trueValues': lambda v: split_str_array(v),
    'falseValues':lambda v: split_str_array(v),
    # TODO: add stats
}
