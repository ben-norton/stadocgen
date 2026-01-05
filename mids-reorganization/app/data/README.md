# Data README
This directory contains all original source csv files and the transformed versions as part of StaDocGen for presentation purposes.

## Output
| File | Description | Script                    |
| -- | -- |---------------------------|
| mids-abcd-sssom.csv | Mappings to ABCD | process_source_mappings.py |
| mids-dwc-sssom.csv | Mappings of information elements to Darwin Core | process_source_mappings.py |
| mids-information-elements | MIDS Information Elements Metadata (no level correlation) | information_elements_transformations.py |
| mids-levels.csv | Core MIDS Levels Metadata | levels_transformations.py |
| mids-master-list | Merged master list of MIDS Information Elements and Levels | merge_source_files.py     |
| mids-mappings | Merged ABCD and DWC mapping files | merge_source_files.py  |

Transformation sequence
copy-source-files.py > information_elements_transformations.py > levels_transformations.py > process_source_mappings.py > merge_source_files.py
