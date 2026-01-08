import numpy as np
import pandas as pd
from datetime import date
from pathlib import Path
import csv
import os

today = date.today()
ts = today.strftime("%Y%m%d")

# Paths
currentPath = Path().absolute()
projectPath = currentPath.parent.parent.parent

def merge_sources():

    # Source Files Path
    # levelsFile = str(projectPath) + '/app/data/output/levels.tsv'
    infoElFile = str(projectPath) + '/app/data/output/information-elements.tsv'
    termsFile = str(projectPath) + '/app/data/output/master-list.tsv'

    # Create empty template if file doesn't exist
    if not os.path.isdir(termsFile):
        fields = ['namespace','term_local_name','label','definition','usage','notes','examples','rdf_type','term_created','term_modified',
                  'compound_name','namespace_iri','term_iri','term_ns_name','term_version_iri','datatype','purpose','alt_label']
        with open(termsFile, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames = fields, delimiter='\t')
            writer.writeheader()

    # Read Source FIles
    # df_levels = pd.read_csv(levelsFile, encoding='utf8',sep='\t')
    df_infoElements = pd.read_csv(infoElFile, encoding='utf8',sep='\t')
    df_terms = pd.read_csv(termsFile, encoding='utf8',sep='\t')

    # Merge Dataframes
    #mergeFrames = [df_levels, df_infoElements]
    #df_terms = pd.concat([df_terms,df_levels])
    df_final = pd.concat([df_terms,df_infoElements])
    df_final['term_uri'] = 'https://mids.tdwg.org/information-elements/index.html#' + df_final['term_local_name']

    ## Save Merged File
    df_final.to_csv(termsFile, index=False, encoding='utf8',sep='\t')

    ### Merge Mappings
    dwc_biology_file = str(projectPath) + '/app/data/output/mids-dwc-biology-sssom.tsv'
    dwc_geology_file = str(projectPath) + '/app/data/output/mids-dwc-geology-sssom.tsv'
    dwc_paleo_file = str(projectPath) + '/app/data/output/mids-dwc-paleontology-sssom.tsv'
    abcd_biology_file = str(projectPath) + '/app/data/output/mids-abcd-biology-sssom.tsv'

    mappingsFile = str(projectPath) + '/app/data/output/mappings.tsv'

    df_dwc_biology = pd.read_csv(dwc_biology_file, encoding='utf8',sep='\t')
    df_dwc_geology = pd.read_csv(dwc_geology_file, encoding='utf8',sep='\t')
    df_dwc_paleo = pd.read_csv(dwc_paleo_file, encoding='utf8',sep='\t')
    df_abcd_biology = pd.read_csv(abcd_biology_file, encoding='utf8',sep='\t')

    # Fix missing columns so they match
    if 'sssom_object_source' not in df_dwc_biology:
        df_dwc_biology['sssom_object_source'] = np.nan
    if 'sssom_object_source' not in df_dwc_geology:
        df_dwc_geology['sssom_object_source'] = np.nan
    if 'sssom_object_source' not in df_dwc_paleo:
        df_dwc_paleo['sssom_object_source'] = np.nan
    if 'sssom_reviewer_id' not in df_abcd_biology:
        df_abcd_biology['sssom_reviewer_id'] = np.nan
    if 'sssom_reviewer_label' not in df_abcd_biology:
        df_abcd_biology['sssom_reviewer_label'] = np.nan

    df_dwc_biology['discipline'] = 'Biology'
    df_dwc_geology['discipline'] = 'Geology'
    df_dwc_paleo['discipline'] = 'Paleontology'
    df_abcd_biology['discipline'] = 'Biology'

    # Concatenate SSSOM Dataframes
    df_mappings = pd.concat([df_abcd_biology,df_dwc_biology,df_dwc_geology,df_dwc_paleo])
    df_mappings.drop_duplicates(subset=['sssom_subject_id', 'sssom_subject_category', 'sssom_predicate_id', 'sssom_object_id', 'sssom_object_category'], keep='first', inplace=True)
    df_mappings.reset_index(inplace=True,drop=True)

    # Add term column with namespace prefix
    df_mappings['term_local_name'] = df_mappings['sssom_subject_id'].str.replace('mids:', '')

    # Create auto-increment column
    df_mappings.insert(0, 'mapping_number', range(1, 1 + len(df_mappings)))

    # Write Final Mappings files
    df_mappings.to_csv(mappingsFile, encoding='utf8',sep='\t')
    return False

merge_sources()
