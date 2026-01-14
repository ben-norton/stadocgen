# Transformers README
This directory contains the data transformation scripts run prior to generating the documentation webpages.
Last Modifed: 20250925

: Source Files: [stadocgen root]/mids/app/data/source
: Target Directory: [stadocgen root]/mids/app/data/output

## Contents
1. copy_source_files.py
2. source_yaml_validator.py
3. process_files.py
4. merge_source_files.py
5. write_filters_json.py

## Basic Workflow
Sequence: source_yaml_validator.py > process_source_mappings.py > levels_transformations.py > information_elements_transformations.py > merge_source_files.py > write_filters_json.py
***Files in the data\source must be downloaded manually or using the copy-source-files.py script***

**source_yaml_validator.py**
- Validates the source yaml files
- Results returned in the console. Errors found must be fixed before proceeding.

**process_files.py** 
- Downloads latest version of both the ABCD and DWC SSSOM mapping files
- Converts source tsv to csv
- Generates lists of unique class - property pairs (for mapping classes to properties)
- Copies source csv file to output directory verbatim (without transformations)  
- Result stored under mids-schema-maps
- Transforms source MIDS Levels and Information Elements CSV files
- Output from transformations is copied to the data/output folder

**merge_source_files.py**
- Merges the transformed MIDS levels and Information Elements CSV files into a single MIDS Termlist CSV
- Joins the merged dataframe to the mids_class_property_map.csv (the result of process_source_mappings) to append the class_name to information_elements

**write_filters_json.py**
- Generates the data.json and filters.json files used by the interactive mappings table

## Notes
1. All files in the source directory are preserved in their original state upon import into stadocgen.
2. Source files are only updated when a more recent version is imported (copied) into StaDocGen. 
3. **Important!**
- MIDS Levels are equivalent to Classes and labeled accordingly in the final mids_termlist.csv file
- Information Elements are equivalent to properties and labeled accordingly in the final mids_termlist.csv file
