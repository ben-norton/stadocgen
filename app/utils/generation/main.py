import requests
import re
import logging
import pandas as pd

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

schema_objects = [
    {
        'csv_prefix': 'digital-specimen',
        'objects': [
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/digital-specimen/0.3.0/digital-specimen.json',
                'class_name': 'DigitalSpecimen',
                'class_description': 'A digital representation of a physical specimen, following the concept of the FAIR Digital Object (FDO). Each physical specimen that has been administrated as a separate entity will be a Digital Specimen.',
                'is_required': True
            }
            ,
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/digital-specimen/0.3.0/material-entity.json',
                'class_name': 'MaterialEntity',
                'class_description': 'Contains the information about the Material object attached to the Digital Specimen. The array will always have one MaterialEntity object of type `ods:Specimen` which is the main MaterialEntity object of the Digital Specimen. It can have additional MaterialEntities which will then be a `ods:SpecimenPart`',
                'is_required': True
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/digital-specimen/0.3.0/identification.json',
                'class_name': 'Identification',
                'class_description': 'A generic identification class, containing information about who and when the identification was made, including the status of the identification.',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/digital-specimen/0.3.0/event.json',
                'class_name': 'Event',
                'class_description': 'A generic event class containing information about a particular activity at a certain place an time. An example is the collecting event.',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/digital-specimen/0.3.0/location.json',
                'class_name': 'Location',
                'class_description': 'A generic location class containing information about a where a specific event took place.',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/agent.json',
                'class_name': 'Agent',
                'class_description': 'A generic agent class, containing information about the actor who performed an activity. This could be a person, an organization or a machine.',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/assertion.json',
                'class_name': 'Assertion',
                'class_description': 'A generic assertion class, containing information about a statement that is made about a digital object. An example is the measurement of the leaf or the wingspan of a specimen.',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/citation.json',
                'class_name': 'Citation',
                'class_description': 'A generic class containing the information about a citation in which the Digital Object is mentioned or which had influence on the Digital Object.',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/entity-relationship.json',
                'class_name': 'EntityRelationship',
                'class_description': 'Describes relationships between digital object and any external resources. An example could be a relationship to the Sequence record of the specimen in a DNA database.',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/identifier.json',
                'class_name': 'Identifier',
                'class_description': 'A generic Identifier class which can be attached to multiple classes. It captures information about any identifier of the class.',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/digital-specimen/0.3.0/chronometric-age.json',
                'class_name': 'ChronometricAge',
                'class_description': 'An approximation of a temporal position (in the sense conveyed by https://www.w3.org/TR/owl-time/#time:TemporalPosition) that is supported via evidence.',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/tombstone-metadata.json',
                'class_name': 'TombstoneMetadata',
                'class_description': 'The tombstone metadata about the tombstoned digital object, including the what, who and when of the tombstoning.',
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
                'class_description': 'A generic agent class, containing information about the actor who performed an activity. This could be a person, an organization or a machine.',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/assertion.json',
                'class_name': 'Assertion',
                'class_description': 'A generic assertion class, containing information about a statement that is made about a digital object. An example is the measurement of the leaf or the wingspan of a specimen.',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/citation.json',
                'class_name': 'Citation',
                'class_description': 'A generic class containing the information about a citation in which the Digital Object is mentioned or which had influence on the Digital Object.',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/entity-relationship.json',
                'class_name': 'EntityRelationship',
                'class_description': 'Describes relationships between digital object and any external resources. An example could be a relationship to the Sequence record of the specimen in a DNA database.',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/identifier.json',
                'class_name': 'Identifier',
                'class_description': 'A generic Identifier class which can be attached to multiple classes. It captures information about any identifier of the class.',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/tombstone-metadata.json',
                'class_name': 'TombstoneMetadata',
                'class_description': 'The tombstone metadata about the tombstoned digital object, including the what, who and when of the tombstoning.',
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
                'class_description': 'A machine agent which will perform an action on the Digital Object potentially resulting in a new annotation on the object',
                'is_required': True
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/tombstone-metadata.json',
                'class_name': 'TombstoneMetadata',
                'class_description': 'The tombstone metadata about the tombstoned digital object, including the what, who and when of the tombstoning.',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/agent.json',
                'class_name': 'Agent',
                'class_description': 'A generic agent class, containing information about the actor who performed an activity. This could be a person, an organization or a machine.',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/secret-variable.json',
                'class_name': 'SecretVariable',
                'class_description': 'A class containing information about which secret the Machine Annotation Service requires. The secret value will be supplied separately to DiSSCo.',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/environmental-variable.json',
                'class_name': 'EnvironmentalVariable',
                'class_description': 'A class containing information about which (non-secret) environmental values the application requires.',
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
                'class_description': 'A new or additional piece of information about a Digital Object. The Annotation model is based on the W3C Web Annotation Data Model (https://www.w3.org/TR/annotation-model/)',
                'is_required': True
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/tombstone-metadata.json',
                'class_name': 'TombstoneMetadata',
                'class_description': 'The tombstone metadata about the tombstoned digital object, including the what, who and when of the tombstoning.',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/agent.json',
                'class_name': 'Agent',
                'class_description': 'A generic agent class, containing information about the actor who performed an activity. This could be a person, an organization or a machine.',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/annotation/0.3.0/annotation-target.json',
                'class_name': 'AnnotationTarget',
                'class_description': 'The AnnotationTarget describes the Digital Object the annotation is attached to, could contain additional information on which part of the object the annotation is attached to.',
                'is_required': True
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/annotation/0.3.0/annotation-body.json',
                'class_name': 'AnnotationBody',
                'class_description': 'Describes the body of the annotation. The body is the full content of the annotation, as provided by the agent.',
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
                'class_description': 'An provenance event describing any change that has been made to a Digital Object, this could be the creation, modification or tombstoning of an object. Model is based on the W3C PROV Data Model (https://www.w3.org/TR/prov-o/)',
                'is_required': True
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/agent.json',
                'class_name': 'Agent',
                'class_description': 'A generic agent class, containing information about the actor who performed an activity. This could be a person, an organization or a machine.',
                'is_required': False
            }
        ]
    },
    {
        'csv_prefix': 'data-mapping',
        'objects': [
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/data-mapping/0.3.0/data-mapping.json',
                'class_name': 'DataMapping',
                'class_description': 'This object described the data mapping for used when ingesting the data. It can set default values or contain an explicit mapping between the local term and an openDS term. This object is attached to a source system object.',
                'is_required': True
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/tombstone-metadata.json',
                'class_name': 'TombstoneMetadata',
                'class_description': 'The tombstone metadata about the tombstoned digital object, including the what, who and when of the tombstoning.',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/agent.json',
                'class_name': 'Agent',
                'class_description': 'A generic agent class, containing information about the actor who performed an activity. This could be a person, an organization or a machine.',
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
                'class_description': 'The Source System describes the system from which the data is ingested. It contains information about the system, the endpoint and the data mapping.',
                'is_required': True
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/tombstone-metadata.json',
                'class_name': 'TombstoneMetadata',
                'class_description': 'The tombstone metadata about the tombstoned digital object, including the what, who and when of the tombstoning.',
                'is_required': False
            },
            {
                'endpoint': 'https://schemas.dissco.tech/schemas/fdo-type/shared-model/0.3.0/agent.json',
                'class_name': 'Agent',
                'class_description': 'A generic agent class, containing information about the actor who performed an activity. This could be a person, an organization or a machine.',
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
    if namespace == 'prov:':
        return 'http://www.w3.org/ns/prov#'
    if namespace == 'as:':
        return 'http://www.w3.org/ns/activitystreams#'
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
            'examples': format_array(term_value, 'examples'),
            'enum': format_array(term_value, 'enum'),
            'rdf_type': determine_rdf_type(is_class),
            'class_name': compound_name,
            'is_required': False,
            'is_repeatable': False,
            'compound_name': class_name + '.' + term_local_name,
            'namespace_iri': determine_namespace_uri(namespace),
            'term_iri': determine_namespace_uri(namespace) + term_local_name,
            'term_ns_name': term_key,
            'datatype': determine_type(term_value, term_key)
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
                'definition': 'A taxonomic determination, containing the full taxonomic tree of the identification.',
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


def determine_type(term_value, term_key):
    term_type = term_value.get('type')
    type_dict = {'ods:hasCitation': 'ods:Citation', 'ods:language': 'string',
                 'ods:hasEntityRelationship': 'ods:EntityRelationship', 'ods:hasEvent': 'ods:Event',
                 'ods:hasLocation': 'ods:Location', 'ods:hasAgent': 'ods:Agent', 'ods:hasAssertion': 'ods:Assertion',
                 'ods:hasIdentifier': 'ods:Identifier', 'ods:hasChronometricAge': 'ods:ChronometricAge',
                 'ods:hasTombstoneMetadata': 'ods:TombstoneMetadata',
                 'ods:hasTaxonIdentification': 'ods:TaxonIdentification',
                 'ods:hasMaterialEntity': 'ods:MaterialEntity', 'ods:hasRelatedPID': 'object',
                 'prov:wasAssociatedWith': 'ods:Agent', 'ods:hasIdentification': 'ods:Identification',
                 'ods:dependency': 'string', 'oa:value': 'string', 'ods:changeValue': 'object',
                 'ods:DefaultMapping': 'ods:DefaultMapping', 'ods:FieldMapping': 'ods:FieldMapping',
                 'ods:hasProvAgent': 'ods:Agent', 'ods:hasEnvironmentalVariable': 'ods:EnvironmentalVariable',
                 'ods:hasSecretVariable': 'ods:SecretVariable'}
    if term_type != 'array':
        return term_type
    else:
        return f'array<{type_dict[term_key]}>'


def format_array(term_value, term_attributes):
    return '| '.join(map(str, term_value.get(term_attributes))) if term_value.get(term_attributes) is not None else ''


def determine_rdf_type(is_class: bool) -> str:
    if is_class:
        return 'http://www.w3.org/2000/01/rdf-schema#Class'
    else:
        return 'http://www.w3.org/1999/02/22-rdf-syntax-ns#Property'


def determine_namespace(term: str) -> str:
    return term.split(':')[0] + ':'


def camel_case_to_title(camel_case_str):
    # Split the camel case string at each uppercase letter, insert space, and capitalize each word
    title_str = re.sub(r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])', ' ', camel_case_str).title()
    abbreviations = ['Id', 'Wkt', 'Uri', 'Url', 'Nfc', 'Srs', 'Html', 'Mids', 'Pid']
    title_str = ' '.join(list(map(lambda word: word.upper() if word in abbreviations else word, title_str.split(' '))))
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
    logging.info(f'Class diagram for object: {schema_object.get("csv_prefix")} has been successfully generated')


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
    Location -- Georeference
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
                if json_data is not None:
                    format_json(term_array, json_data, schema)
                    logging.info(f"JSON data from {endpoint} has been successfully written to {csv_file_path}")
                else:
                    logging.error(f"An error occurred while fetching JSON data from {endpoint}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        df = pd.DataFrame(term_array)
        df.to_csv(csv_file_path, index=False)
        generate_class_diagram(df, schema_object)


if __name__ == "__main__":
    main()
