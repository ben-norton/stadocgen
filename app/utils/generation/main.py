import requests
import re
import pandas as pd

schema_objects = [
    {
        'csv_prefix': 'digital-specimen',
        'objects': [
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/digital-specimen/0.3.0/digital-specimen.json',
                'class_name': 'DigitalSpecimen',
                'class_description': 'A digital representation of a physical specimen',
                'is_required': True
            }
            ,
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/digital-specimen/0.3.0/material-entity.json',
                'class_name': 'MaterialEntity',
                'class_description': 'Material Entities that are part of the Digital Specimen',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/digital-specimen/0.3.0/identification.json',
                'class_name': 'Identification',
                'class_description': 'The Identification of a specimen',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/digital-specimen/0.3.0/event.json',
                'class_name': 'Event',
                'class_description': 'The Event that occurred at a particular time and place',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/digital-specimen/0.3.0/location.json',
                'class_name': 'Location',
                'class_description': 'The Location of the digital specimen',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/agent.json',
                'class_name': 'Agent',
                'class_description': 'The Agent of the digital specimen',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/assertion.json',
                'class_name': 'Assertion',
                'class_description': 'The Assertion of the digital specimen',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/citation.json',
                'class_name': 'Citation',
                'class_description': 'The Citation of the digital specimen',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/entity-relationship.json',
                'class_name': 'EntityRelationship',
                'class_description': 'The Entity Relationship of the digital specimen',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/identifier.json',
                'class_name': 'Identifier',
                'class_description': 'The Identifier of the digital specimen',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/digital-specimen/0.3.0/chronometric-age.json',
                'class_name': 'ChronometricAge',
                'class_description': 'The Chronometric Age of the digital specimen',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/tombstone-metadata.json',
                'class_name': 'TombstoneMetadata',
                'class_description': 'The tombstone metadata about the tombstoned digital object',
                'is_required': False
            }
        ]
    },
    {
        'csv_prefix': 'digital-media',
        'objects': [
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/digital-media/0.3.0/digital-media.json',
                'class_name': 'DigitalMedia',
                'class_description': 'A digital representation of an media object such as a Image or Sound Recording',
                'is_required': True
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/agent.json',
                'class_name': 'Agent',
                'class_description': 'The Agent of the digital specimen',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/assertion.json',
                'class_name': 'Assertion',
                'class_description': 'The Assertion of the digital specimen',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/citation.json',
                'class_name': 'Citation',
                'class_description': 'The Citation of the digital specimen',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/entity-relationship.json',
                'class_name': 'EntityRelationship',
                'class_description': 'The Entity Relationship of the digital specimen',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/identifier.json',
                'class_name': 'Identifier',
                'class_description': 'The Identifier of the digital specimen',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/tombstone-metadata.json',
                'class_name': 'TombstoneMetadata',
                'class_description': 'The tombstone metadata about the tombstoned digital object',
                'is_required': False
            }
        ]
    },
    {
        'csv_prefix': 'machine-annotation-service',
        'objects': [
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/machine-annotation-service/0.3.0/machine-annotation-service.json',
                'class_name': 'MachineAnnotationService',
                'class_description': 'A Machine Annotation Service',
                'is_required': True
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/tombstone-metadata.json',
                'class_name': 'TombstoneMetadata',
                'class_description': 'The tombstone metadata about the tombstoned digital object',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/agent.json',
                'class_name': 'Agent',
                'class_description': 'Description of the agents connected to the digital object',
                'is_required': False
            }
        ]
    },
    {
        'csv_prefix': 'annotation',
        'objects': [
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/annotation/0.3.0/annotation.json',
                'class_name': 'Annotation',
                'class_description': 'Annotation model based on the W3C Web Annotation Data Model (https://www.w3.org/TR/annotation-model/)',
                'is_required': True
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/tombstone-metadata.json',
                'class_name': 'TombstoneMetadata',
                'class_description': 'The tombstone metadata about the tombstoned digital object',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/agent.json',
                'class_name': 'Agent',
                'class_description': 'Description of the agents connected to the digital object',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/annotation/0.3.0/annotation-target.json',
                'class_name': 'AnnotationTarget',
                'class_description': 'Description of the target of the annotation',
                'is_required': True
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/annotation/0.3.0/annotation-body.json',
                'class_name': 'AnnotationBody',
                'class_description': 'Description of the body of the annotation',
                'is_required': True
            }
        ],
    },
    {
        'csv_prefix': 'create-update-tombstone-event',
        'objects': [
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/create-update-tombstone-event/0.3.0/create-update-tombstone-event.json',
                'class_name': 'CreateUpdateTombstoneEvent',
                'class_description': 'Create Update Tombstone Event, based on W3C PROV Data Model (https://www.w3.org/TR/prov-o/)',
                'is_required': True
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/agent.json',
                'class_name': 'Agent',
                'class_description': 'Description of the agents connected to the digital object',
                'is_required': False
            }
        ]
    },
    {
        'csv_prefix': 'data-mapping',
        'objects': [
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/data-mapping/0.3.0/data-mapping.json',
                'class_name': 'Mapping',
                'class_description': 'Mapping data model, used for data-mapping between different data models',
                'is_required': True
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/tombstone-metadata.json',
                'class_name': 'TombstoneMetadata',
                'class_description': 'The tombstone metadata about the tombstoned digital object',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/agent.json',
                'class_name': 'Agent',
                'class_description': 'Description of the agents connected to the digital object',
                'is_required': False
            }
        ]
    },
    {
        'csv_prefix': 'source-system',
        'objects': [
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/source-system/0.3.0/source-system.json',
                'class_name': 'SourceSystem',
                'class_description': 'Source System Model, used to describe data providing systems',
                'is_required': True
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/tombstone-metadata.json',
                'class_name': 'TombstoneMetadata',
                'class_description': 'The tombstone metadata about the tombstoned digital object',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/agent.json',
                'class_name': 'Agent',
                'class_description': 'Description of the agents connected to the digital object',
                'is_required': False
            }
        ]
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
    if namespace == 'oa:':
        return 'http://www.w3.org/ns/oa#'
    if namespace == 'rdf:':
        return 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
    if namespace == 'schema:':
        return 'http://schema.org/'
    if namespace == 'schema:':
        return 'http://www.w3.org/ns/prov#'
    if namespace == 'as:':
        return 'http://www.w3.org/ns/activitystreams#'
    if namespace == 'foaf:':
        return 'http://xmlns.com/foaf/0.1/'
    if namespace == 'rdfs:':
        return 'http://www.w3.org/2000/01/rdf-schema#'
    if namespace == 'ltc:':
        return 'http://rs.tdwg.org/ltc/terms/'
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


def add_relationships(class_mermaid_string, class_relationships, top_class_name):
    if top_class_name == 'DigitalSpecimen':
        return add_digital_specimen_relationships(class_mermaid_string)
    elif top_class_name == 'DigitalEntity':
        return class_mermaid_string + class_relationships + 'Agent -- Identifier \n'
    else:
        return class_mermaid_string + class_relationships


def generate_class_diagram(df, schema_object):
    class_df = df.query('rdf_type == "http://www.w3.org/2000/01/rdf-schema#Class"')
    class_relationships = ''
    class_mermaid_string = 'classDiagram\n'
    top_class_name = class_df.iloc[0]['term_local_name']
    for index, row in class_df.iterrows():
        class_mermaid_string += f' class {row["term_local_name"]} {{ \n'
        property_df = df.query(
            'rdf_type == "http://www.w3.org/1999/02/22-rdf-syntax-ns#Property" and class_name == @row["term_local_name"]')
        for prop_index, prop_row in property_df.iterrows():
            class_mermaid_string += f'   {prop_row["term_local_name"]} : {prop_row["datatype"]} \n'
        class_mermaid_string += ' }\n'
        if index > 0:
            class_relationships += f'{top_class_name} -- {row["term_local_name"]} \n'
    class_mermaid_string = add_relationships(class_mermaid_string, class_relationships, top_class_name)
    with open(f'../../templates/includes/resources/diagrams/class-diagrams/{schema_object.get("csv_prefix")}-full.html',
              'w') as text_file:
        text_file.write(class_mermaid_string)
    print(f'Class diagram for object: {schema_object.get("csv_prefix")} has been successfully generated')


def add_digital_specimen_relationships(mermaid_string):
    return mermaid_string + """
    DigitalSpecimen -- MaterialEntity
    DigitalSpecimen -- Identification
    DigitalSpecimen -- Event
    DigitalSpecimen -- Citation
    DigitalSpecimen -- Identifier
    DigitalSpecimen -- Assertion
    DigitalSpecimen -- Agent
    DigitalSpecimen -- EntityRelationship
    DigitalSpecimen -- ChronometricAge
    DigitalSpecimen -- TombstoneMetadata
    Event -- Location
    Event -- Assertion
    Location -- GeoReference
    Location -- GeologicalContext
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
    for schema_object in schema_objects:
        csv_file_path = f"../../data/opends/{schema_object.get('csv_prefix')}-termlist.csv"
        term_array = []
        try:
            for schema in schema_object.get('objects'):
                endpoint = schema.get('endpoint')
                json_data = fetch_json_schema(endpoint)
                format_json(term_array, json_data, schema)
                print(f"JSON data from {endpoint} has been successfully written to {csv_file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
        df = pd.DataFrame(term_array)
        df.to_csv(csv_file_path, index=False)
        generate_class_diagram(df, schema_object)


if __name__ == "__main__":
    main()
