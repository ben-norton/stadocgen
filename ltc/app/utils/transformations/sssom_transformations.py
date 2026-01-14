from pathlib import Path
import pandas as pd
import shutil

namespace = 'ltc'
current_dir = Path().absolute()
path = current_dir.parent.parent

# 1.  Create copy of source csv
sssom_src = str(path)+'/data/sources/ltc_sssom_mapping.csv'
sssom_csv = str(path)+'/data/output/ltc-sssom.csv'
shutil.copy(sssom_src, sssom_csv)

sssom_df = pd.read_csv(sssom_csv, encoding='utf8')
# Create Term Column with Machine-readable version of the term
sssom_df['term_local_name'] = sssom_df['subject_id']
sssom_df.rename(columns={'term_uri': 'term_iri'}, inplace=True)
sssom_df['term_local_name'] = sssom_df['term_local_name'].str.replace('http://rs.tdwg.org/ltc/terms/', '')
sssom_df['term_local_name'] = sssom_df['term_local_name'].str.replace('http://purl.org/dc/terms/', '')
sssom_df['term_local_name'] = sssom_df['term_local_name'].str.replace('http://rs.tdwg.org/dwc/terms/', '')
sssom_df['term_local_name'] = sssom_df['term_local_name'].str.replace('https://schema.org/', '')
sssom_df['term_local_name'] = sssom_df['term_local_name'].str.replace('http://rs.tdwg.org/chrono/terms/', '')

# Create compound name to identify each term within the scope of a class
sssom_df['compound_name'] = sssom_df[["subject_category", "term_local_name"]].apply(".".join, axis=1)
# Create Term URI Column
sssom_df['term_iri'] = sssom_df['subject_id']

sssom_df.to_csv(sssom_csv, index=False, encoding='utf8')