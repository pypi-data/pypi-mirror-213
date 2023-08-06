import pandas as pd
from healdata_utils.utils import to_int_if_base10
from healdata_utils.io import read_pyreadstat
from ..jsontemplate.conversion import convert_templatejson

from datetime import datetime


def convert_readstat(file_path,
    data_dictionary_props={}):
    """
    Converts a "metadata-rich" (ie statistical software file) 
    into a HEAL-specified data dictionary in both csv format and json format.

    This function relies on [readstat](https://github.com/Roche/pyreadstat) which supports SPSS (sav and por), 
    SAS (sas7bdat), and Stata (dta). 

    > Currently, this function uses both data and metadata to generate 
    a HEAL specified data dictionary. That is, types are inferred from the 
    data (so at least test or synthetic data needed) while everything else is taken 
    from the metadata (eg missing values, variable labels, variable value labels etc)

    Parameters
    ----------
    csvtemplate : str or path-like or any object
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

    Notes
    -----
    ## Missing values (from pyreadstat docs)

    SPSS only supports 3 discrete missing in addition to ranges.
    For POC, only using discrete. TODO: use range(lo,hi+1) to do ranges; JCOIN Core Measures, for example, will need this
    
    From module documentation on missing values:

    - SPSS
        missing_ranges: a dict with keys being variable names. 
        Values are a list of dicts. 
        Each dict contains two keys, 'lo' and 'hi' being the lower boundary and higher boundary for the missing range. 
        Even if the value in both lo and hi are the same, the two elements will always be present. 
        This appears for SPSS (sav) files when using the option user_missing=True: user defined missing values appear not as nan but as their true value and this dictionary stores the information about which values are to be considered missing.
    
    - Stata/SAS
        missing_user_values: a dict with keys being variable names. 
        Values are a list of character values (A to Z and _ for SAS, a to z for SATA) 
        representing user defined missing values in SAS and STATA. 
        This appears when using user_missing=True in read_sas7bdat or read_dta 
        if user defined missing values are present.

    """
    
    _,meta = read_pyreadstat(file_path,user_missing=True) # get user missing values (for stata/sas will make string so need sep call to infer types)
    df,_ = read_pyreadstat(file_path) # dont fill user defined missing vals (to get correct types)
    df = df.convert_dtypes() #TODO: use visions package for inference (from pandas profile project)
    fields = pd.io.json.build_table_schema(df,index=False)['fields'] #converts to frictionless Table Schema


    for field in fields:
        field.pop('extDtype',None)
        fieldname = field['name']

        value_labels = meta.variable_value_labels.get(fieldname)
        missing_values = meta.missing_user_values.get(fieldname,[])
        missing_ranges = meta.missing_ranges.get(fieldname,[])

        #see NOTE in docstring (on missing values): 
        # below maps SPSS missing values
        for items in missing_ranges:
            values = list(set(items.values()))
            if len(values)==1:
                if isinstance(values[0],datetime):
                    missing_values.append(str(values[0]))
                else:
                    missing_values.append(values[0])
            else:
                raise Exception("Currently, only discrete values are supported")

        if value_labels:
            field['encodings'] = value_labels
            #NOTE: enums are assumed if labels represent entire set of values
            # this avoids value labels that are, for example, partials such as top/bottom encodings
            enums = set(value_labels.keys()).difference(set(missing_values))
            constraints_enums = {'constraints':{'enum':[str(v) for v in enums]}}
            field.update(constraints_enums)

        #NOTE/TODO: for SPSS no functionality for incorporating missing ranges
        
        if missing_values:
            field['missingValues'] = missing_values

        variable_label = meta.column_names_to_labels.get(fieldname)
        if variable_label:
            field['description'] = variable_label

    data_dictionary = data_dictionary_props.copy()
    data_dictionary['data_dictionary'] = fields 

    package = convert_templatejson(data_dictionary)
    return package
