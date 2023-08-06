''' 
takes the filled out variable level metadata template
and converts to json, validates, and saves json template to file
based on an explicit set of mapping functions

goes the other way (from json to csv as well)

see convert_templatecsv_to_json and convert_json_to_templatecsv
''' 
import petl as etl
from pathlib import Path
# from frictionless import Resource,Package
from healdata_utils.utils import convert_rec_to_json
from healdata_utils.io import read_table
from .mappings import fieldmap
from os import PathLike

def convert_templatecsv(
    csvtemplate: str,
    data_dictionary_props: dict,
    mappings: dict = fieldmap,
) -> dict:
    """
    Converts a CSV conforming to HEAL specifications (but see 2 additional notes below) 
    into a HEAL-specified data dictionary in both csv format and json format.

    Converts an in-memory data dictionary or a path to a data dictionary file into a HEAL-specified tabular template by:
        1. Adding missing fields, and
        2. Converting fields from a specified mapping.
            NOTE: currently this mapping is only float/num to number or text/char to string (case insensitive)
                In future versions, there will be a specified module for csv input mappings.
    
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

    if isinstance(csvtemplate,(str,PathLike)):
        template_tbl = etl.fromdataframe(read_table(str(Path(csvtemplate))))
    else:
        template_tbl = etl.fromdataframe(pd.DataFrame(csvtemplate))

    # apply convert functions for fields that exist in input
    convertfields = {
        propname:fxn 
        for propname,fxn in mappings.items() 
        if propname in etl.fieldnames(template_tbl)
    }
    fields_csv = (
        template_tbl
        .convert(convertfields)
        .convertnumbers() #TODO: make the number conversions explicit
        .dicts()
    )

    fields_json = [convert_rec_to_json(rec) for rec in etl.dicts(template_tbl)]

    template_json = dict(**data_dictionary_props,data_dictionary=fields_json)
    template_csv = dict(**data_dictionary_props,data_dictionary=fields_csv)

    return {"templatejson":template_json,"templatecsv":template_csv}