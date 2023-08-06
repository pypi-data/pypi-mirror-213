# HEAL Data Utilities

The HEAL data utilities python package provides data packaging tools for the HEAL data ecosystem to facilitate data discovery,sharing, and harmonization with a focus on the HEAL platform data consultancy (DSC).
 
Currently, the focus of the repo is on generating data-dictionaries (see Variable level metadata section below). However, in the future, this will be expanded for all heal specific data packaging functions (e.g., study and file level metadata and data).

## Installation

To install the latest official release of healdata-utils, from your computer's command prompt, run:

`pip install healdata-utils`

to install the working, un-released version from this git repository, run:

`pip install git+https://github.com/norc-heal/healdata-utils.git`


### Variable level metadata (data dictionaries)

[![Binder](http://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/norc-heal/healdata-utils/HEAD?labpath=notebooks%2Fdemos%2Finputs-to-heal-data-dictionary.ipynb) 

The healdata-utils variable level metadata (vlmd) tool inputs a variety of different input file types and exports HEAL-formatted data dictionaries (JSON and CSV formats). Additionally, exported validation (ie "error") reports provide the user information as to a. if the exported data dictionary is valid according to HEAL specifications (see the schema repository [here](https://github.com/norc-heal/heal-metadata-schemas/tree/main/variable-level-metadata-schema)).


## Basic usage 

The vlmd tool can be used via python or the command line.

### Using from python

From your current working directory in python, run:

```python
from healdata_utils.cli import convert_to_vlmd

# description and title are optional. If submitting through platform, can fill these out there.
description = "This is a proof of concept to demonstrate the healdata-utils functionality"
title = "Healdata-utils Demonstration Data Dictionary"
healdir = "output" # can also specify a file name if desired (eg output/thisismynewdd.csv)
inputpath = "input/my-redcap-data-dictionary-export.csv"

data_dictionaries = convert_to_vlmd(
    filepath=inputpath,
    outputdir=healdir, 
    inputtype=input_type, #if not specified, looks for suffix
    data_dictionary_props={"title":title,"description":description} #data_dictionary_props is optional
)
```

> This will output the data dictionaries to the specified output directory (see ooutput section below) and also save the json/csv versions in the `data_dictionaries` object.

> For the available input file formats (ie the available choices for the `inputtype` parameter), one can run (from python):

```python
from healdata_utils.cli import input_descriptions

input_descriptions

```

The `input_descriptions` object contains the choice for `inputtype` as the key and the description as the value.

### Using from the command line

From your current working directory run:
(note the `\` at the end of each line signals a line continuation for ease in understanding the long one line command.) Again the `--title` and `--description` options are optional.
For descriptions on the different flags/options, run `vlmd --help`

```bash

vlmd --filepath "data/example_pyreadstat_output.sav" \
--outputdir "output-cli" \
--title "Healdata-utils Demonstration Data Dictionary" \
--description "This is a proof of concept to demonstrate the healdata-utils functionality" 
```

### Output

Both the python and command line routes will result in a JSON and CSV version of the HEAL  data dictionary in the output folder along with 
the validation reports in the `errors` folder. See below:

- `input/input/my-redcap-data-dictionary-export.csv` : your input file

- `output/errors/heal-csv-errors.json`: outputted validation report for table in csv file against frictionless schema
    - see schema [here](https://github.com/norc-heal/heal-metadata-schemas/blob/main/variable-level-metadata-schema/schemas/frictionless/csvtemplate/fields.json)
- `output/errors/heal-json-errors.json`:  outputted jsonschema validation report.
    - see schema [here](https://github.com/norc-heal/heal-metadata-schemas/blob/main/variable-level-metadata-schema/schemas/jsonschema/data-dictionary.json)

- `output/heal-csvtemplate-data-dictionary.csv`: This is the CSV data dictionary
- `output/heal-jsontemplate-data-dictionary.json`: This is the JSON version of the data dictionary

> Note, only the JSON version will have the user-specified `title` and `description`


### Examples

See the below notebooks demonstrating use and workflows using the `convert_to_vlmd` in python and `vlmd` in the command line. 

> Clicking on the "binder badges" will bring you to an interactive notebook page where you can test out the notebooks. Here, healdata-utils comes pre-installed.

1. Generating a heal data dictionary from a variety of input files 

- [click here for static notebook ](notebooks/demos/inputs-to-heal-data-dictionary.ipynb) 
- click binder badge for interactive [![Binder](http://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/norc-heal/healdata-utils/HEAD?labpath=notebooks%2Fdemos%2Finputs-to-heal-data-dictionary.ipynb) 

2. [in development] Creating and iterating over a csv data dictionary to create a valid data dictionary file [click here](notebooks/demos/demo-csvtemplate-validation.ipynb)
