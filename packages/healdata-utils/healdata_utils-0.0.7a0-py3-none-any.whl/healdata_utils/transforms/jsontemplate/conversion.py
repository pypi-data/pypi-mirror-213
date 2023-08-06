from pathlib import Path
import json
# from frictionless import Resource,Package
from collections.abc import MutableMapping
from .mappings import join_prop
from healdata_utils.utils import flatten_except_if
from os import PathLike

def convert_templatejson(
    jsontemplate:str,
    fields_name:str='data_dictionary',
    sep_iter = '|',
    sep_dict = '=',
    **kwargs
    ):
    """
    Converts a JSON file or dictionary conforming to HEAL specifications
    into a HEAL-specified data dictionary in both csv format and json format.

    Converts in-memory data or a path to a data dictionary file.
    
    Parameters
    ----------
    csvtemplate : str or path-like or an object that can be inferred as data by frictionless's Resource class.
        Data or path to data with the data being a tabular HEAL-specified data dictionary.
        This input can be any data object or path-like string excepted by a frictionless Resource object.
    data_dictionary_props : dict
        The HEAL-specified data dictionary properties.
    mappings : dict, optional
        Mappings (which can be a dictionary of either lambda functions or other to-be-mapped objects).
        Default: specified fieldmap.

    Returns
    -------
    dict
        A dictionary with two keys:
            - 'templatejson': the HEAL-specified JSON object.
            - 'templatecsv': the HEAL-specified tabular template.

    """
    if isinstance(jsontemplate,(str,PathLike)):
        data_dictionary_props = json.loads(Path(jsontemplate).read_text())
    elif isinstance(jsontemplate, MutableMapping):
        data_dictionary_props = jsontemplate
    else:
        raise Exception("jsontemplate needs to be either dictionary-like or a path to a json")


    fields_json = data_dictionary_props.pop(fields_name)
    fields_csv = []
    for f in fields_json:
        field_flattened = flatten_except_if(f)
        field_csv = {
            propname:join_prop(propname,prop)
            for propname,prop in field_flattened.items()
        }
        fields_csv.append(field_csv)

    template_json = dict(**data_dictionary_props,data_dictionary=fields_json)
    template_csv = dict(**data_dictionary_props,data_dictionary=fields_csv)

    return {"templatejson":template_json,"templatecsv":template_csv}