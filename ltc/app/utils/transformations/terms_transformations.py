from pathlib import Path
import pandas as pd
import shutil
import globals
import glob
import yaml

namespace = 'ltc'
current_dir = Path().absolute()
path = current_dir.parent.parent

# -------------------------------------------------------
# Create copies
term_src = str(path)+'/data/sources/ltc_terms_source.csv'
term_csv = str(path)+'/data/output/ltc-termlist.csv'
shutil.copy(term_src, term_csv)

ns_src = str(path)+'/data/sources/ltc_namespaces.csv'
ns_csv = str(path)+'/data/output/ltc-namespaces.csv'
shutil.copy(ns_src, ns_csv)

dt_src = str(path)+'/data/sources/ltc_datatypes.csv'
dt_csv = str(path)+'/data/output/ltc-datatypes.csv'
shutil.copy(dt_src, dt_csv)

# -------------------------------------------------------
# Terms
ltc_df = pd.read_csv(term_csv, encoding="utf8")

# Rename Columns
ltc_df.rename(columns={'term_localName': 'term_local_name',
                       'tdwgutility_organizedInClass': 'class_uri',
                       'tdwgutility_required': 'is_required',
                       'tdwgutility_repeatable': 'is_repeatable'}, inplace=True)
# Fix boolean values
ltc_df['is_required'] = ltc_df['is_required'].replace({'Yes': 'True'})
ltc_df['is_required'] = ltc_df['is_required'].replace({'No': 'False'})
ltc_df['is_repeatable'] = ltc_df['is_repeatable'].replace({'Yes': 'True'})
ltc_df['is_repeatable'] = ltc_df['is_repeatable'].replace({'No': 'False'})
# Create compound name column to uniquely identify each record
ltc_df['class_name'] = ltc_df['class_uri'].str.replace('http://rs.tdwg.org/dwc/terms/attributes/', '')
ltc_df['compound_name'] = ltc_df[["class_name", "term_local_name"]].apply(".".join, axis=1)


# Resave
ltc_df.to_csv(term_csv, index=False, encoding='utf8')

# ------------------------------------------------------------
# Namespaces
# Get namespaces file
ns_df = pd.read_csv(ns_csv, encoding="utf8")
# Rename namespaces columns
ns_df.rename(columns={'curie': 'namespace', 'value': 'namespace_iri'}, inplace=True)
# Add colon to namespace for merger with terms csv
ns_df['namespace'] = ns_df['namespace'].astype(str) + ':'

if 'ltc:' not in ns_df.values:
    ltc_row = {"namespace": "ltc:", "namespace_iri": "http://rs.tdwg.org/ltc/terms/"}
    ns_df = pd.concat([ns_df, pd.DataFrame([ltc_row])], ignore_index=True)
ns_df.to_csv(ns_csv, index=False, encoding='utf8')

# Merge Terms and Namespaces
ns_df = pd.read_csv(ns_csv, encoding="utf8")
ltc_df = pd.read_csv(term_csv, encoding="utf8")

ltc_df = pd.merge(ltc_df, ns_df[['namespace', 'namespace_iri']], on='namespace', how='inner')

# Create Term IRI
ltc_df['term_iri'] = ltc_df['namespace_iri'].astype(str) + ltc_df['term_local_name']
ltc_df['term_ns_name'] = ltc_df['namespace'].astype(str) + ltc_df['term_local_name']
ltc_df['term_version_iri'] = 'http://rs.tdwg.org/ltc/terms/' + ltc_df["term_local_name"] + '-' + ltc_df["term_modified"]

ltc_df.sort_values(by='term_local_name', axis='index', inplace=True, na_position='last')

# Data cleanup
ltc_df['examples'] = ltc_df['examples'].str.replace('"', '')
ltc_df['definition'] = ltc_df['definition'].str.replace('"', '')
ltc_df['usage'] = ltc_df['usage'].str.replace('"', '')
ltc_df['notes'] = ltc_df['notes'].str.replace('"', '')

# Resave terms file
ltc_df.to_csv(term_csv, index=False, encoding='utf8')

# ------------------------------------------------------------
# Datatypes
dt_df = pd.read_csv(dt_csv, encoding='utf8')
dt_df.rename(columns={'term_localName': 'term_local_name','tdwgutility_organizedInClass': 'class_name'}, inplace=True)
dt_df['compound_name'] = dt_df[["class_name", "term_local_name"]].apply(".".join, axis=1)

# Resave datatypes file
dt_df.to_csv(dt_csv, index=False, encoding='utf8')

# ------------------------------------------------------------
# Merge Terms and Datatypes
ltc_df = pd.merge(ltc_df, dt_df[['compound_name', 'datatype']], on='compound_name', how='left')
# Resave
ltc_df.to_csv(term_csv, index=False, encoding='utf8')








