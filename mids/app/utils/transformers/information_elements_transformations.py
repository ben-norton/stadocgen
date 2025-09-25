import pandas as pd
import shutil
import datetime
from pathlib import Path
import os

today = datetime.date.today()
ts = today.strftime("%Y%m%d")

namespace = 'mids'

# -------------------------------------------------------
# Paths
current_path = Path().absolute()
project_path = current_path.parent.parent.parent
# Source Files Path
source_file = str(project_path) + '/app/data/source/mids-repo/information_elements.tsv'
examples_source = str(project_path) + '/app/data/source/mids-repo/examples.tsv'

# Timestamped output path
# Create timestamped folder for working files (works in progress)
target_path = str(project_path) + '/app/data/output'
target_file = str(target_path) + '/information-elements.tsv'
examples_target = str(target_path) + '/examples.tsv'

# Create timestamped folder if it doesn't exist
if not os.path.isdir(target_path):
    os.mkdir(target_path)

# -------------------------------------------------------
# Create copies
# term_src > source_file
# term_csv > target_file
shutil.copy(source_file, target_file)
shutil.copy(examples_source, examples_target)

# -------------------------------------------------------
# Process
# mids_df > target_df
# Read
df = pd.read_csv(target_file, encoding="utf8",sep='\t')

# Renamez
df.rename(columns={'MIDSLevel_localName': 'class_name',
                    'informationElement_localName': 'term_local_name',
                    'term_added': 'term_created'
                   }, inplace=True)
# RDF Type
df['rdf_type'] = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#Property'

# Qualified Term
df['term_ns_name'] = 'mids:' + df['term_local_name']
df["term_created"] = pd.to_datetime(df["term_created"], format='%d/%m/%Y')
df["term_modified"] = pd.to_datetime(df["term_modified"], format='%d/%m/%Y')
df['class_pref_label'] = df['class_name'].str.replace('MIDS','MIDS Level ')

# Process Examples ------------------------------------------- */
df_examples = pd.read_csv(examples_target, encoding="utf8",sep='\t')
df_examples.rename(columns={'informationElement_localName': 'term_local_name'}, inplace=True)
df_examples.to_csv(examples_target, encoding="utf8",sep='\t',index=False)

examples_df = pd.read_csv(examples_target, sep='\t', lineterminator='\r', encoding='utf-8')
examples_df = examples_df.replace('\n',' ', regex=True)

df2 = examples_df.groupby('term_local_name')['example'].apply(list).reset_index(name="examples_list")
df2 = df2[df2['examples_list'].notna()]
df_final = pd.merge(df, df2, how="left", on=["term_local_name"])

#examplesPivotTarget = str(target_path) + '/examples_pivot.tsv'
#examples_pivot_df.to_csv(examplesPivotTarget, encoding="utf8",sep='\t',index=False)

df_final.to_csv(target_file, encoding="utf8",sep='\t',index=False)
