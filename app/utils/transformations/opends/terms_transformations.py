from pathlib import Path
import pandas as pd

namespace = 'opends'
current_dir = Path().absolute()
path = current_dir.parent.parent.parent

# -------------------------------------------------------
# Create copies
term_csv = str(path)+'/data/opends/opends-termlist.csv'

ns_csv = str(path)+'/data/opends/opends-namespaces.csv'

dt_csv = str(path)+'/data/opends/opends-datatypes.csv'

# -------------------------------------------------------
# Terms
opends_df = pd.read_csv(term_csv, encoding="utf8")

# Rename Columns
opends_df.rename(columns={'term_localName': 'term_local_name',
                       'tdwgutility_organizedInClass': 'class_name',
                       'tdwgutility_required': 'is_required',
                       'tdwgutility_repeatable': 'is_repeatable'}, inplace=True)
# Fix boolean values
opends_df['is_required'] = opends_df['is_required'].replace({'Yes': 'True'})
opends_df['is_required'] = opends_df['is_required'].replace({'No': 'False'})
opends_df['is_repeatable'] = opends_df['is_repeatable'].replace({'Yes': 'True'})
opends_df['is_repeatable'] = opends_df['is_repeatable'].replace({'No': 'False'})
# Create compound name column to uniquely identify each record
opends_df['compound_name'] = opends_df[["class_name", "term_local_name"]].apply(".".join, axis=1)
# Resave
opends_df.to_csv(term_csv, index=False, encoding='utf8')

# ------------------------------------------------------------
# Namespaces
# Get namespaces file
ns_df = pd.read_csv(ns_csv, encoding="utf8")
# Rename namespaces columns
ns_df.rename(columns={'curie': 'namespace', 'value': 'namespace_iri'}, inplace=True)
# Add colon to namespace for merger with terms csv
ns_df['namespace'] = ns_df['namespace'].astype(str) + ':'

if 'opends:' not in ns_df.values:
    opends_row = {"namespace": "opends:", "namespace_iri": "http://rs.dissco.eu/opends/terms/"}
    ns_df = pd.concat([ns_df, pd.DataFrame([opends_row])], ignore_index=True)

ns_df.to_csv(ns_csv, index=False, encoding='utf8')

# Merge Terms and Namespaces
ns_df = pd.read_csv(ns_csv, encoding="utf8")
opends_df = pd.read_csv(term_csv, encoding="utf8")

opends_df = pd.merge(opends_df, ns_df[['namespace', 'namespace_iri']], on='namespace', how='inner')

# Create Term IRI
opends_df['term_iri'] = opends_df['namespace_iri'].astype(str) + opends_df['term_local_name']
opends_df['term_ns_name'] = opends_df['namespace'].astype(str) + opends_df['term_local_name']


# Resave terms file
opends_df.to_csv(term_csv, index=False, encoding='utf8')

# ------------------------------------------------------------
# Datatypes
dt_df = pd.read_csv(dt_csv, encoding='utf8')
dt_df.rename(columns={'term_localName': 'term_local_name','tdwgutility_organizedInClass': 'class_name'}, inplace=True)
dt_df['compound_name'] = dt_df[["class_name", "term_local_name"]].apply(".".join, axis=1)
# Resave datatypes file
dt_df.to_csv(dt_csv, index=False, encoding='utf8')

# ------------------------------------------------------------
# Merge Terms and Datatypes
opends_df = pd.merge(opends_df, dt_df[['compound_name', 'datatype']], on='compound_name', how='left')
# Resave
opends_df.to_csv(term_csv, index=False, encoding='utf8')
