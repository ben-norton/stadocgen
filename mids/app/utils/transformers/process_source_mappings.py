import csv
from config import get_project_root
import pandas as pd
import urllib.request
import shutil

root = get_project_root()

# Mapping source files are stored as *.tsv (tab-delimited). StaDocGen parses CSV when generating documentation. This script converts the source tsv to source csv.
# Files:
# DWC

# SOURCE FILES
# dwc_tsv = str(root) + '/mids/app/data/source/mids-repo/sssom_dwc_biology_mappings.sssom.tsv'
dwc_biology_tsv = str(root) + '/mids/app/data/source/mids-repo/mids_dwc_biology_1.sssom.tsv'
dwc_geology_tsv = str(root) + '/mids/app/data/source/mids-repo/mids_dwc_geology_1.sssom.tsv'
abcd_biology_tsv = str(root) + '/mids/app/data/source/mids-repo/mids_abcd_biology_1.sssom.tsv'

# TARGET FILES
dwc_biology_sssom = str(root) + '/mids/app/data/output/mids-dwc-biology-sssom.tsv'
dwc_biology_unique = str(root) + '/mids/app/data/output/mids-dwc-biology-sssom-unique.tsv'
dwc_geology_sssom = str(root) + '/mids/app/data/output/mids-dwc-geology-sssom.tsv'
dwc_geology_unique = str(root) + '/mids/app/data/output/mids-dwc-geology-sssom-unique.tsv'
abcd_biology_sssom = str(root) + '/mids/app/data/output/mids-abcd-biology-sssom.tsv'
abcd_biology_unique = str(root) + '/mids/app/data/output/mids-abcd-biology-sssom-unique.tsv'



# ------------------------------------------------------------
# READ TSV FILES
df_dwc_biology = pd.read_csv(dwc_biology_tsv, encoding='utf8',sep='\t')
df_dwc_geology = pd.read_csv(dwc_geology_tsv, encoding='utf8',sep='\t')
df_abcd_biology = pd.read_csv(abcd_biology_tsv, encoding="utf8",sep='\t')

# ------------------------------------------------------------
# Generate Unique Class-Property Pairs
# DWC Biology
df_dwc_biology_mapping = df_dwc_biology[['sssom:subject_category','sssom:subject_id']].drop_duplicates()
df_dwc_biology_mapping.rename(columns={'sssom:subject_id': 'qualified_term',
                    'sssom:subject_category': 'class_name'
                   }, inplace=True)
df_dwc_biology_mapping['term_local_name'] = df_dwc_biology_mapping['qualified_term'].str.replace('mids:', '')
df_dwc_biology_mapping.to_csv(dwc_biology_unique, index=False, encoding='utf8',sep='\t')

# DWC Geology
df_dwc_geology_mapping = df_dwc_geology[['sssom:subject_category','sssom:subject_id']].drop_duplicates()
df_dwc_geology_mapping.rename(columns={'sssom:subject_id': 'qualified_term',
                    'sssom:subject_category': 'class_name'
                   }, inplace=True)
df_dwc_geology_mapping['term_local_name'] = df_dwc_geology_mapping['qualified_term'].str.replace('mids:', '')
df_dwc_geology_mapping.to_csv(dwc_geology_unique, index=False, encoding='utf8',sep='\t')

# ABCD Biology
df_abcd_biology = pd.read_csv(abcd_biology_tsv, encoding="utf8",sep='\t')
# Generate Unique Class-Property Pairs for ABCD
df_abcd_biology_mapping = df_abcd_biology[['sssom:subject_category','sssom:subject_id']].drop_duplicates()
df_abcd_biology_mapping.rename(columns={'sssom:subject_id': 'qualified_term',
                    'sssom:subject_category': 'class_name'
                   }, inplace=True)
df_abcd_biology_mapping['term_local_name'] = df_abcd_biology_mapping['qualified_term'].str.replace('mids:', '')
df_abcd_biology_mapping.to_csv(abcd_biology_unique, index=False, encoding='utf8',sep='\t')

# ------------------------------------------------------------
# WRITE NEW MAPPINGS FILES
# DWC BIOLOGY
df_dwc_biology['object_source_version'] = 'http://rs.tdwg.org/dwc/terms'
# Replace colon in column names with underscores - jinja2 template reserved character
df_dwc_biology.columns = df_dwc_biology.columns.str.replace(':','_', regex=True)
# Create persistent URLs
df_dwc_biology['object_url'] = df_dwc_biology['sssom_object_id'].str.replace('dwc:','http://rs.tdwg.org/dwc/terms/')
df_dwc_biology['subject_url'] = df_dwc_biology['sssom_subject_id'].str.replace('mids:','https://tdwg.github.io/mids/information-elements#')
df_dwc_biology['object_namespace'] = 'dwc'
df_dwc_biology.to_csv(dwc_biology_sssom, index=False, encoding='utf8',sep='\t')

# DWC GEOLOGY
df_dwc_geology['object_source_version'] = 'http://rs.tdwg.org/dwc/terms'
# Replace colon in column names with underscores - jinja2 template reserved character
df_dwc_geology.columns = df_dwc_geology.columns.str.replace(':','_', regex=True)
# Create persistent URLs
df_dwc_geology['object_url'] = df_dwc_geology['sssom_object_id'].str.replace('dwc:','http://rs.tdwg.org/dwc/terms/')
df_dwc_geology['subject_url'] = df_dwc_geology['sssom_subject_id'].str.replace('mids:','https://tdwg.github.io/mids/information-elements#')
df_dwc_geology['object_namespace'] = 'dwc'
df_dwc_geology.to_csv(dwc_geology_sssom, index=False, encoding='utf8',sep='\t')

# ABCD BIOLOGY
df_abcd_biology['object_source_version'] = 'http://www.tdwg.org/schemas/abcd/2.06'
# Replace colon in column names with underscores - jinja2 template reserved character
df_abcd_biology.columns = df_abcd_biology.columns.str.replace(':','_', regex=True)
# Create persistent URLs
df_abcd_biology['object_url'] = df_abcd_biology['sssom_object_id'].str.replace('abcd:','http://rs.tdwg.org/abcd/terms/')
df_abcd_biology['subject_url'] = df_abcd_biology['sssom_subject_id'].str.replace('mids:','https://tdwg.github.io/mids/information-elements#')
df_abcd_biology['object_namespace'] = 'abcd'
df_abcd_biology.to_csv(abcd_biology_sssom, index=False, encoding='utf8',sep='\t')
