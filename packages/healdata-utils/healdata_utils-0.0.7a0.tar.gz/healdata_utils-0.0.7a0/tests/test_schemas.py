from healdata_utils.schemas import convert_frictionless_to_jsonschema
from pathlib import Path
import yaml


def test_convert_frictionless_to_jsonschema():
    with Path(__file__).parent.joinpath("data/test_frictionless_schema.yaml").open(
        mode="r"
    ) as f:
        frictionless_schema = yaml.safe_load(f)
    jsonschema_props = convert_frictionless_to_jsonschema(frictionless_schema)
    assert jsonschema_props == {
        "type": "object",
        "required": ["name", "description"],
        "properties": {
            "module": {
                "oneOf": [
                    {
                        "description": "Module (a place to put the section, form, or other broad category used \nto group variables.\n",
                        "title": "Module (i.e., section,form,category)",
                        "type": "string",
                    },
                    {"enum": [""]},
                ]
            },
            "name": {
                "description": "The name of a variable (i.e., field) as it appears in the data.\n",
                "title": "Variable Name",
                "type": "string",
            },
            "title": {
                "oneOf": [
                    {
                        "description": "The human-readable title of the variable.",
                        "title": "Variable Label (ie Title)",
                        "type": "string",
                    },
                    {"enum": [""]},
                ]
            },
            "description": {
                "description": "An extended description of the variable.",
                "title": "Variable Description",
                "type": "string",
            },
            "type": {
                "oneOf": [
                    {
                        "description": "A classification allowing the user (analyst, researcher or computer) to\nknow how to use the variable\n",
                        "title": "Variable Type",
                        "type": "string",
                        "enum": [
                            "boolean",
                            "any",
                            "date",
                            "yearmonth",
                            "string",
                            "integer",
                            "duration",
                            "number",
                            "geopoint",
                            "time",
                            "datetime",
                            "year",
                        ],
                    },
                    {"enum": [""]},
                ]
            },
            "format": {
                "oneOf": [
                    {
                        "description": "Indicates the format of the type specified in the `type` property. This\nmay describe the type of unit (such as for time fields like year or month)\nor the format of a date field (such as %y%m%d).\n",
                        "title": "Variable Format",
                        "type": "string",
                        "enum": [
                            "binary",
                            "email",
                            "any",
                            "uuid",
                            "object",
                            "uri",
                            "topojson",
                            "array",
                        ],
                    },
                    {"enum": [""]},
                ]
            },
            "constraints.maxLength": {
                "oneOf": [
                    {
                        "description": "Indicates the maximum length of an iterable (e.g., array, string, or\nobject). For example, if 'Hello World' is the longest value of a\ncategorical variable, this would be a maxLength of 11.\n",
                        "title": "Maximum Length",
                        "type": "integer",
                    },
                    {"enum": [""]},
                ]
            },
            "constraints.enum": {
                "oneOf": [
                    {
                        "description": "Constrains possible values to a set of values.",
                        "title": "Variable Possible Values",
                    },
                    {"enum": [""]},
                ]
            },
            "constraints.pattern": {
                "oneOf": [
                    {
                        "description": "A regular expression pattern the data MUST conform to.",
                        "title": "Regular Expression Pattern",
                        "type": "string",
                    },
                    {"enum": [""]},
                ]
            },
            "constraints.maximum": {
                "oneOf": [
                    {
                        "description": "Specifies the maximum value of a field (e.g., maximum -- or most\nrecent -- date, maximum integer etc). Note, this is different then\nmaxLength property.\n",
                        "title": "Maximum Value",
                        "type": "integer",
                    },
                    {"enum": [""]},
                ]
            },
            "encodings": {
                "oneOf": [
                    {
                        "description": 'Encodings (and mappings) allow categorical values to be stored as\nnumerical values. IMPORTANT: the ==key should be the value represented IN\nthe data== and the ==value should be the to-be-mapped label==. Many\nanalytic software programs use numerical encodings and some algorithms\nonly support numerical values. Additionally, this field provides a way to\nstore categoricals that are stored as  "short" labels (such as\nabbreviations)\n',
                        "title": "Variable Value Encodings (i.e., mappings; value labels)",
                    },
                    {"enum": [""]},
                ]
            },
            "ordered": {
                "oneOf": [
                    {
                        "description": "Indicates whether a categorical variable is ordered. This variable  is\nrelevant for variables that have an ordered relationship but not\nnecessarily  a numerical relationship (e.g., Strongly disagree < Disagree\n< Neutral < Agree).\n",
                        "title": "An ordered variable",
                    },
                    {"enum": [""]},
                ]
            },
            "missingValues": {
                "oneOf": [
                    {
                        "description": "A list of missing values specific to a variable.",
                        "title": "Missing Values",
                    },
                    {"enum": [""]},
                ]
            },
            "trueValues": {
                "oneOf": [
                    {
                        "description": "For boolean (true) variable (as defined in type field), this field allows\na physical string representation to be cast as true (increasing\nreadability of the field). It can include one or more values.\n",
                        "title": "Boolean True Value Labels",
                    },
                    {"enum": [""]},
                ]
            },
            "falseValues": {
                "oneOf": [
                    {
                        "description": "For boolean (false) variable (as defined in type field), this field allows\na physical string representation to be cast as false (increasing\nreadability of the field) that is not a standard false value. It can include one or more values.\n",
                        "title": "Boolean False Value Labels",
                    },
                    {"enum": [""]},
                ]
            },
            "repo_link": {
                "oneOf": [
                    {
                        "description": "A link to the variable as it exists on the home repository, if applicable\n",
                        "title": "Variable Repository Link",
                        "type": "string",
                    },
                    {"enum": [""]},
                ]
            },
            "cde_id": {
                "oneOf": [
                    {
                        "description": "The source and id for the NIH Common Data Elements program.",
                        "title": "Common Data Element Id",
                    },
                    {"enum": [""]},
                ]
            },
            "ontology_id": {
                "oneOf": [
                    {
                        "description": "Ontological information for the given variable as indicated  by the\nsource, id, and relation to the specified classification. One or more\nontology classifications can be specified. \n",
                        "title": "Ontology ID",
                    },
                    {"enum": [""]},
                ]
            },
            "univar_stats.median": {"oneOf": [{"type": "number"}, {"enum": [""]}]},
            "univar_stats.mean": {"oneOf": [{"type": "number"}, {"enum": [""]}]},
            "univar_stats.std": {"oneOf": [{"type": "number"}, {"enum": [""]}]},
            "univar_stats.min": {"oneOf": [{"type": "number"}, {"enum": [""]}]},
            "univar_stats.max": {"oneOf": [{"type": "number"}, {"enum": [""]}]},
            "univar_stats.mode": {"oneOf": [{"type": "number"}, {"enum": [""]}]},
            "univar_stats.count": {"oneOf": [{"type": "integer"}, {"enum": [""]}]},
            "univar_stats.twenty_five_percentile": {
                "oneOf": [{"type": "number"}, {"enum": [""]}]
            },
            "univar_stats.seventy_five_percentile": {
                "oneOf": [{"type": "number"}, {"enum": [""]}]
            },
            "univar_stats.cat_marginals": {"oneOf": [{"type": "array"}, {"enum": [""]}]},
        },
        "description": "Variable level metadata individual fields integrated into the variable level\nmetadata object within the HEAL platform metadata service.\n",
        "title": "HEAL Variable Level Metadata Fields",
    }