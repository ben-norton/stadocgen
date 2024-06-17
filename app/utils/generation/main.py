import requests
import re
import pandas as pd

schema_objects = [
    {
        'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/digital-specimens/0.3.0/digital-specimen.json',
        'class_name': 'DigitalSpecimen',
        'class_description': 'A digital representation of a physical specimen',
        'is_required': True
    }
    ,
    {
        'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/digital-specimens/0.3.0/material-entity.json',
        'class_name': 'MaterialEntity',
        'class_description': 'Material Entities that are part of the Digital Specimen',
        'is_required': False
    },
    {
        'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/digital-specimens/0.3.0/identification.json',
        'class_name': 'Identification',
        'class_description': 'The Identification of a specimen',
        'is_required': False
    },
    {
        'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/digital-specimens/0.3.0/event.json',
        'class_name': 'Event',
        'class_description': 'The Event that occurred at a particular time and place',
        'is_required': False
    },
    {
        'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/digital-specimens/0.3.0/location.json',
        'class_name': 'Location',
        'class_description': 'The Location of the digital specimen',
        'is_required': False
    },
    {
        'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-models/0.3.0/agent.json',
        'class_name': 'Agent',
        'class_description': 'The Agent of the digital specimen',
        'is_required': False
    },
    {
        'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-models/0.3.0/assertion.json',
        'class_name': 'Assertion',
        'class_description': 'The Assertion of the digital specimen',
        'is_required': False
    },
    {
        'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-models/0.3.0/citation.json',
        'class_name': 'Citation',
        'class_description': 'The Citation of the digital specimen',
        'is_required': False
    },
    {
        'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-models/0.3.0/entity-relationship.json',
        'class_name': 'EntityRelationship',
        'class_description': 'The Entity Relationship of the digital specimen',
        'is_required': False
    },
    {
        'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-models/0.3.0/identifier.json',
        'class_name': 'Identifier',
        'class_description': 'The Identifier of the digital specimen',
        'is_required': False
    },
    {
        'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/digital-media-objects/0.3.0/digital-entity.json',
        'class_name': 'DigitalEntity',
        'class_description': 'The Digital Entity in the form of media objects',
        'is_required': False
    }
]


def fetch_json_schema(endpoint):
    response = requests.get(endpoint)
    response.raise_for_status()  # Ensure we notice bad responses
    return response.json()


def determine_namespace_uri(namespace: str) -> str:
    if namespace == 'dwc:':
        return 'http://rs.tdwg.org/dwc/terms/'
    if namespace == 'dwciri:':
        return 'http://rs.tdwg.org/dwc/iri/'
    if namespace == 'dcterms:':
        return 'http://purl.org/dc/terms/'
    if namespace == 'chrono:':
        return 'http://rs.tdwg.org/chrono/terms/'
    if namespace == 'ods:':
        return 'http://rs.dissco.eu/opends/terms/'
    if namespace == 'ac:':
        return 'http://rs.tdwg.org/ac/terms/'
    else:
        return ''


def format_json(term_array, json_data, schema):
    class_name = schema.get('class_name')
    term_array.append({
        'namespace': 'ods:',
        'term_local_name': class_name,
        'label': camel_case_to_title(class_name),
        'definition': schema.get('class_description'),
        'usage': '',
        'notes': '',
        'examples': '',
        'rdf_type': 'http://www.w3.org/2000/01/rdf-schema#Class',
        'class_name': class_name,
        'is_required': schema.get('is_required'),
        'is_repeatable': True,
        'compound_name': class_name,
        'namespace_iri': 'http://rs.dissco.eu/opends/terms/',
        'term_iri': 'http://rs.dissco.eu/opends/terms/' + class_name,
        'term_ns_name': 'ods:' + class_name,
        'datatype': ''
    })
    iterate_over_object(json_data, term_array, class_name, class_name)
    set_required(json_data, term_array)


def set_required(json_data, term_array):
    if json_data.get('required') is not None:
        for required_term in json_data.get('required'):
            term = next((item for item in term_array if item["term_ns_name"] == required_term), None)
            if term is not None:
                term['is_required'] = True


def iterate_over_object(json_data, term_array, class_name, compound_name):
    for term_key in json_data.get('properties'):
        if term_key in ['@id', '@type']:
            continue
        term_value = json_data.get('properties').get(term_key)
        term_local_name = term_key.split(':')[1]
        namespace = determine_namespace(term_key)
        is_class = term_value.get('properties') is not None
        term_array.append({
            'namespace': namespace,
            'term_local_name': term_local_name,
            'label': camel_case_to_title(term_local_name),
            'definition': term_value.get('description'),
            'usage': '',
            'notes': '',
            'examples': term_value.get('examples'),
            'rdf_type': determine_rdf_type(is_class),
            'class_name': compound_name,
            'is_required': False,
            'is_repeatable': False,
            'compound_name': class_name + '.' + term_local_name,
            'namespace_iri': determine_namespace_uri(namespace),
            'term_iri': determine_namespace_uri(namespace) + term_local_name,
            'term_ns_name': term_key,
            'datatype': term_value.get('type')
        })

        if term_value.get('properties'):
            iterate_over_object(term_value, term_array, term_key, term_local_name)
            set_required(term_value, term_array)
        if term_key == 'ods:hasTaxonIdentification':
            class_name = 'TaxonIdentification'
            term_array.append({
                'namespace': 'ods:',
                'term_local_name': class_name,
                'label': camel_case_to_title(class_name),
                'definition': 'A taxonomic identification of the specimen',
                'usage': '',
                'notes': '',
                'examples': '',
                'rdf_type': 'http://www.w3.org/2000/01/rdf-schema#Class',
                'class_name': class_name,
                'is_required': False,
                'is_repeatable': True,
                'compound_name': class_name,
                'namespace_iri': 'http://rs.dissco.eu/opends/terms/',
                'term_iri': 'http://rs.dissco.eu/opends/terms/' + class_name,
                'term_ns_name': 'ods:' + class_name,
                'datatype': ''
            })
            iterate_over_object(term_value.get('items'), term_array, 'ods:' + class_name, class_name)
            set_required(term_value, term_array)


def determine_rdf_type(is_class: bool) -> str:
    if is_class:
        return 'http://www.w3.org/2000/01/rdf-schema#Class'
    else:
        return 'http://www.w3.org/1999/02/22-rdf-syntax-ns#Property'


def determine_namespace(term: str) -> str:
    return term.split(':')[0] + ':'


def camel_case_to_title(camel_case_str):
    # Split the camel case string at each uppercase letter, insert space, and capitalize each word
    title_str = re.sub('([a-z])([A-Z])', r'\1 \2', camel_case_str).title()
    return title_str


def generate_class_diagram(df):
    class_mermaid_string = prepare_class_diagram()
    class_df = df.query('rdf_type == "http://www.w3.org/2000/01/rdf-schema#Class"')
    for index, row in class_df.iterrows():
        class_mermaid_string += f' class {row["term_local_name"]} {{ \n'
        property_df = df.query(
            'rdf_type == "http://www.w3.org/1999/02/22-rdf-syntax-ns#Property" and class_name == @row["term_local_name"]')
        for prop_index, prop_row in property_df.iterrows():
            class_mermaid_string += f'   {prop_row["term_local_name"]} : {prop_row["datatype"]} \n'
        class_mermaid_string += ' }\n'
    class_mermaid_string = add_relationships(class_mermaid_string)
    with open("../../templates/includes/resources/diagrams/class-diagrams/opends-full.html", "w") as text_file:
        text_file.write(class_mermaid_string)
    print("Class diagram has been successfully generated")


def prepare_class_diagram():
    return '''
    <button class="js-toggle-fullscreen-btn toggle-fullscreen-btn" aria-label="Enter fullscreen mode" onclick="openFullscreen('C1');">
	<svg class="toggle-fullscreen-svg" width="28" height="28" viewBox="-2 -2 28 28">
		<g class="icon-fullscreen-enter">
			<path d="M 2 9 v -7 h 7" />
			<path d="M 22 9 v -7 h -7" />
			<path d="M 22 15 v 7 h -7" />
			<path d="M 2 15 v 7 h 7" />
		</g>

		<g class="icon-fullscreen-leave">
			<path d="M 24 17 h -7 v 7" />
			<path d="M 0 17 h 7 v 7" />
			<path d="M 0 7 h 7 v -7" />
			<path d="M 24 7 h -7 v -7" />
		</g>
     </svg>
  </button>
  <pre class="mermaid" id="green-class-diagram">
  classDiagram\n
  '''


def add_relationships(mermaid_string):
    return mermaid_string + """
    DigitalSpecimen -- MaterialEntity
    DigitalSpecimen -- Identification
    DigitalSpecimen -- Event
    DigitalSpecimen -- Citation
    DigitalSpecimen -- Identifier
    DigitalSpecimen -- Assertion
    DigitalSpecimen -- Agent
    DigitalSpecimen -- EntityRelationship
    Event -- Location
    Event -- Assertion
    Location -- GeoReference
    Location -- GeologicalContext
    DigitalEntity -- Agent
    DigitalEntity -- Citation
    DigitalEntity -- Identifier
    DigitalEntity -- EntityRelationship
    MaterialEntity -- Event
    MaterialEntity -- Citation
    MaterialEntity -- Identifier
    MaterialEntity -- EntityRelationship
    MaterialEntity -- Agent
    MaterialEntity -- Assertion
    MaterialEntity -- Identification
    Agent -- Identifier
    Identification -- Citation
    Identification -- TaxonIdentification
    """


def determine_class_name(row):
    class_name = row["class_name"]
    if '.' in class_name:
        return class_name.split('.')[1]
    else:
        return class_name


def main():
    csv_file_path = '../../data/opends/opends-termlist.csv'
    term_array = []
    try:
        for schema in schema_objects:
            endpoint = schema.get('endpoint')
            json_data = fetch_json_schema(endpoint)
            format_json(term_array, json_data, schema)
            print(f"JSON data from {endpoint} has been successfully written to {csv_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
    df = pd.DataFrame(term_array)
    df.to_csv(csv_file_path, index=False)
    generate_class_diagram(df)


if __name__ == "__main__":
    main()
