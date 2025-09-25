# Transformers README
This directory contains the data transformation scripts run prior to generating the documentation webpages.
Last Modifed: 20250925

: Source Files: [stadocgen root]/mids/app/data/source/mids-repo
: Target Directory: [stadocgen root]/mids/app/data/output

## Contents
1. process_source_mappings.py
2. levels_transformations.py
3. information_elements_transformations.py
4. merge_source_files.py

## Basic Workflow
Sequence: process_source_mappings.py > levels_transformations.py > information_elements_transformations.py > merge_source_files.py 
***Files in the data\source\mids-repo must be downloaded manually or using the copy-source-files.py script***

**process_source_mappings.py** 
- Downloads latest version of both the ABCD and DWC SSSOM mapping files
- Converts source tsv to csv
- Generates lists of unique class - property pairs (for mapping classes to properties)
- Copies source csv file to output directory verbatim (without transformations)  
- Result stored under mids-schema-maps

**levels_transformations.py** and **information_elements_transformations.py**
- Transforms source MIDS Levels and Information Elements CSV files
- Output from transformations is copied to the data/output folder

**merge_source_files.py**
- Merges the transformed MIDS levels and Information Elements CSV files into a single MIDS Termlist CSV
- Joins the merged dataframe to the mids_class_property_map.csv (the result of process_source_mappings) to append the class_name to information_elements

## Notes
1. All files in the source directory are preserved in their original state upon import into stadocgen.
2. Source files are only updated when a more recent version is imported (copied) into StaDocGen. 
3. **Important!**
- MIDS Levels are equivalent to Classes and labeled accordingly in the final mids_termlist.csv file
- Information Elements are equivalent to properties and labeled accordingly in the final mids_termlist.csv file
