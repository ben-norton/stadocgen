# Source File Specifications

## MIDS Levels
File: levels.tsv
File contains the MIDS levels that are considered semantically equivalent to rdfs:Class in the class-property RDF structure.

| Source column | Qualified Term |
| -- | -- | 
| term_local_name | rdfs:label |
| alt_label | skos:altLabel |
| definition | skos:definition |
| notes | skos:note |
| purpose | purpose |


## Information Elements
File: information_elements.tsv

| Source column | Qualified Term |
| -- | -- |
| namespace | namespace |
| MIDSLevel_localName | Class name |
| informationElement_localName | rdfs:label |
| definition | skos:definition |
| usage | vann:usageNote |
| recommendations | recommendation |
| rdf_type | rdf:type |
| isRequiredBy | dcterms:isRequiredBy |
| term_added | dcterms:created |
| term_modified | dcterms:modified |



### Mappings to TDWG fields



### Processing Notes
MIDS-levels-draft.csv
1. Add column rdf_type
2. Set all rdf_type values http://www.w3.org/2000/01/rdf-schema#Class
3. Change column names:
    level > term_local_name
    prefLabel > label
    shortDescription > definition
    longDescription > notes

## Information Elements

## MIDS Levels
File: mids_information_elements_draft.csv

### Terms Table
| source column name | qualified term                   | target column name | remarks                                                                   |
| -- |----------------------------------|--------------------|---------------------------------------------------------------------------|
| namespace | | | |
| informationElement_localName | | | |
| label | | | |
| definition | | | |
| usage | | | |
| recommendations | | | |
| examples | | | |
| rdg_type | | | |
| tdwgutility_required | | | |
| tdwgutility_repeatable | | | |
| term_status | | | |
| term_added | | | |
| term_modified | | | |


### Mappings to TDWG fields


### Processing Notes
mids_information_elements_draft.csv
1. Set rdf_type to http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
2. Column name changes 
   informationElement_localName > term_local_name
   usage > purpose
   recommendations > usage_note
   tdwgutility_required > is_required
   tdwgutility_repeatable > is_repeatable
   term_status >editorial_note
3. Update boolean
4. Add scope_note
5. Populate scope_note with value in parentheses in is_required
6. Delete term_modified, term_added - Needs to reflect ratification date in this context

## Merged File Fields
namespace
term_local_name
label
definition
usage
notes
examples
rdf_type
class_name
is_required
is_repeatable
term_created
term_modified
compound_name
namespace_iri
term_iri
term_ns_name
term_version_iri
datatype
purpose
scope_note
usage_note
editorial_note