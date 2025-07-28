import json

import requests
import re
import logging
import pandas as pd

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

schema_objects = json.load(open('./schemas.json'))


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
        'class_name': 'ods:' + class_name,
        'is_required': schema.get('is_required'),
        'is_repeatable': True,
        'compound_name': class_name,
        'namespace_iri': 'http://rs.dissco.eu/opends/terms/',
        'term_iri': 'http://rs.dissco.eu/opends/terms/' + class_name,
        'term_ns_name': 'ods:' + class_name,
        'datatype': ''
    })
    iterate_over_object(json_data, term_array, class_name)
    set_required(json_data, term_array)


def set_required(json_data, term_array):
    if json_data.get('required') is not None:
        for required_term in json_data.get('required'):
            term = next((item for item in term_array if item["term_ns_name"] == required_term), None)
            if term is not None:
                term['is_required'] = True


def iterate_over_object(json_data, term_array, class_name):
    for term_key in json_data.get('properties'):
        if term_key in ['@id', '@type']:
            continue
        term_value = json_data.get('properties').get(term_key)
        term_local_name = term_key.split(':')[1]
        namespace = determine_namespace(term_key)
        is_class = term_value.get('properties') is not None
        term_array.append({
            'namespace': namespace,
            'term_local_name': term_key,
            'label': camel_case_to_title(term_local_name),
            'definition': term_value.get('description'),
            'usage': '',
            'notes': '',
            'examples': format_array(term_value, 'examples'),
            'enum': format_array(term_value, 'enum'),
            'rdf_type': determine_rdf_type(is_class),
            'class_name': 'ods:' + class_name if 'ods:' not in class_name else class_name,
            'is_required': False,
            'is_repeatable': False,
            'compound_name': class_name + '.' + term_local_name,
            'namespace_iri': determine_namespace_uri(namespace),
            'term_iri': determine_namespace_uri(namespace) + term_local_name,
            'term_ns_name': term_key,
            'datatype': determine_type(term_value, term_key)
        })
        if term_value.get('properties'):
            iterate_over_object(term_value, term_array, term_key)
            set_required(term_value, term_array)
        if term_key == 'ods:hasRelatedPIDs':
            class_name = 'RelatedPID'
            term_array.append({
                'namespace': 'ods:',
                'term_local_name': class_name,
                'label': camel_case_to_title(class_name),
                'definition': 'Indicates to which other Digital Object the tombstoned record is related to. This can be used when a digital object has been split or merged into other Digital Objects.',
                'usage': '',
                'notes': '',
                'examples': '',
                'rdf_type': 'http://www.w3.org/2000/01/rdf-schema#Class',
                'class_name': 'ods:' + class_name if 'ods:' not in class_name else class_name,
                'is_required': False,
                'is_repeatable': True,
                'compound_name': class_name,
                'namespace_iri': 'http://rs.dissco.eu/opends/terms/',
                'term_iri': 'http://rs.dissco.eu/opends/terms/' + class_name,
                'term_ns_name': 'ods:' + class_name,
                'datatype': ''
            })
            iterate_over_object(term_value.get('items'), term_array, class_name)
            set_required(term_value, term_array)
        if term_key == 'ods:hasRoles':
            class_name = 'Role'
            term_array.append({
                'namespace': 'ods:',
                'term_local_name': class_name,
                'label': camel_case_to_title(class_name),
                'definition': 'A role is a named entity that can be assigned to an agent. It is used to describe the function of an agent in a specific context.',
                'usage': '',
                'notes': '',
                'examples': '',
                'rdf_type': 'http://www.w3.org/2000/01/rdf-schema#Class',
                'class_name': 'ods:' + class_name if 'ods:' not in class_name else class_name,
                'is_required': False,
                'is_repeatable': True,
                'compound_name': class_name,
                'namespace_iri': 'http://rs.dissco.eu/opends/terms/',
                'term_iri': 'http://rs.dissco.eu/opends/terms/' + class_name,
                'term_ns_name': 'ods:' + class_name,
                'datatype': ''
            })
            iterate_over_object(term_value.get('items'), term_array, class_name)
            set_required(term_value, term_array)
            class_name = 'Agent'
        if term_key == 'ods:hasPredicates':
            class_name = 'Predicate'
            term_array.append({
                'namespace': 'ods:',
                'term_local_name': class_name,
                'label': camel_case_to_title(class_name),
                'definition': 'Descripes a predicate that can be used to filter the target Digital Objects this object applies to.',
                'usage': '',
                'notes': '',
                'examples': '',
                'rdf_type': 'http://www.w3.org/2000/01/rdf-schema#Class',
                'class_name': 'ods:' + class_name if 'ods:' not in class_name else class_name,
                'is_required': False,
                'is_repeatable': True,
                'compound_name': class_name,
                'namespace_iri': 'http://rs.dissco.eu/opends/terms/',
                'term_iri': 'http://rs.dissco.eu/opends/terms/' + class_name,
                'term_ns_name': 'ods:' + class_name,
                'datatype': ''
            })
            iterate_over_object(term_value.get('items'), term_array, class_name)
            set_required(term_value, term_array)



def determine_type(term_value, term_key):
    term_type = term_value.get('type')
    type_dict = {
        "ods:hasCitations": "ods:Citation",
        "ods:hasEntityRelationships": "ods:EntityRelationship",
        "ods:hasEvents": "ods:Event",
        "ods:hasLocation": "ods:Location",
        "ods:hasAgents": "ods:Agent",
        "ods:hasRoles": "ods:Role",
        "ods:hasAssertions": "ods:Assertion",
        "ods:hasIdentifiers": "ods:Identifier",
        "ods:hasChronometricAges": "ods:ChronometricAge",
        "ods:hasTombstoneMetadata": "ods:TombstoneMetadata",
        "ods:hasTaxonIdentifications": "ods:TaxonIdentification",
        "ods:hasSpecimenParts": "ods:SpecimenPart",
        "prov:wasAssociatedWith": "ods:Agent",
        "ods:hasIdentifications": "ods:Identification",
        "ods:dependency": "string",
        "oa:value": "string",
        "ods:changeValue": "object",
        "ods:hasDefaultMapping": "ods:DefaultMapping",
        "ods:hasTermMapping": "ods:TermMapping",
        "ods:hasProvAgent": "ods:Agent",
        "ods:hasEnvironmentalVariables": "ods:EnvironmentalVariable",
        "ods:hasSecretVariables": "ods:SecretVariable",
        "ods:hasRelatedPIDs": "ods:RelatedPID",
        "ods:metadataLanguages": "string",
        "dcterms:format": "string",
        "dcterms:subject": "string",
        "ac:tag": "string",
        "ods:filters": "string",
        "ods:hasTargetDigitalObjectFilter": "ods:TargetDigitalObjectFilter",
        "ods:predicateValues": "string|number|boolean",
        "ods:hasPredicates": "ods:Predicate",
        "ods:specimenMachineAnnotationServices": "string",
        "ods:mediaMachineAnnotationServices": "string"
    }
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
    abbreviations = ['Id', 'Wkt', 'Uri', 'Url', 'Nfc', 'Srs', 'Html', 'Mids', 'Pid', 'Gupri']
    title_str = ' '.join(list(map(lambda word: word.upper() if word in abbreviations else word, title_str.split(' '))))
    return title_str


def generate_class_diagram(df, schema_object):
    class_df = df.query('rdf_type == "http://www.w3.org/2000/01/rdf-schema#Class"')
    class_mermaid_string = 'classDiagram\n'
    for index, row in class_df.iterrows():
        class_mermaid_string += f' class {row["term_local_name"]} {{ \n'
        class_name = 'ods:' + row["term_local_name"]
        property_df = df.query(
            'rdf_type == "http://www.w3.org/1999/02/22-rdf-syntax-ns#Property" and class_name == @class_name')
        for prop_index, prop_row in property_df.iterrows():
            class_mermaid_string += f'   {prop_row["term_local_name"]} : {prop_row["datatype"]} \n'
        class_mermaid_string += ' }\n'
    with open(f'../../templates/includes/resources/diagrams/class-diagrams/{schema_object.get("csv_prefix")}-full.html',
              'w') as text_file:
        text_file.write(class_mermaid_string)
    logging.info(f'Class diagram for object: {schema_object.get("csv_prefix")} has been successfully generated')


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
            logging.exception(f"An error occurred: {e}")
        df = pd.DataFrame(term_array)
        df.to_csv(csv_file_path, index=False)
        generate_class_diagram(df, schema_object)


if __name__ == "__main__":
    main()
