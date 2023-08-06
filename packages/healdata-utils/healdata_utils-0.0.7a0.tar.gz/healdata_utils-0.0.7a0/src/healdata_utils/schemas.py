import requests

jsonschema_url = (
"https://raw.githubusercontent.com/norc-heal/"
"heal-metadata-schemas/mbkranz/variable-lvl-dev/"
"variable-level-metadata-schema/schemas/jsonschema/fields.json"
)
csvschema_url = (
        "https://raw.githubusercontent.com/norc-heal/heal-metadata-schemas/"
        "mbkranz/variable-lvl-dev/"
        "variable-level-metadata-schema/schemas/frictionless/csvtemplate/fields.json"
    )

# TODO: currently using fields.json and hardcoding -- use data_dictionaries.json 
healjsonschema = {
    'type':'object',
    'required':[
        'title',
        'data_dictionary'
    ],
    'properties':{
        'title':{'type':'string'},
        'description':{'type':'string'},
        'data_dictionary':{
            'type':'array',
            'items':requests.get(jsonschema_url).json()}
    }
}
healcsvschema = requests.get(csvschema_url).json()   



