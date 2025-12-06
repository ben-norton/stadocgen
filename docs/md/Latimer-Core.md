# Latimer Core
Docs Homepage: https://ltc.tdwg.org
Development Docs Homepage: Not applicable
GitHub Repo: https://github.com/tdwg/ltc
Task Group Landing Page: https://www.tdwg.org/community/cd/
Instance Type: Local
Instance Notes: Latimer Core was the first standard to utilize StaDocGen. The original development and design was done in coincidence with the review and ratification of LtC
Description: 

Folder Structure:
Source CSV Files: 
[repo]\source\terms\
    abcd.csv
    chrono.csv
    dcterms.csv
    dwc.csv
    ltc.csv
    ltc_categories.csv
    ltc_datatypes.csv
    ltc_terms_source.csv
    schema.csv
    mapping\
        ltc_skos_mapping.csv
        ltc_sssom_mapping.csv


## Transformations
Transformation scripts
After local CSV and markdown files have been refreshed from source repository, run the following transformations scripts
app/utils/transformations/terms_transformations.py
app/utils/transformations/ltc-paths.py
app/utils/transformations/skos-transformations.py
app/utils/transformations/sssom-transformations.py