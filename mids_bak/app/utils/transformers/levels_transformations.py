import pandas as pd
import shutil
from datetime import date
from pathlib import Path
import os

today = date.today()
ts = today.strftime("%Y%m%d")

namespace = 'mids'

# -------------------------------------------------------
# Paths
currentPath = Path().absolute()
projectPath = currentPath.parent.parent.parent
# Source Files Path
sourceFile = str(projectPath) + '/app/data/source/mids-repo/levels.tsv'

# Timestamped output path
# Create timestamped folder for working files (works in progress)
targetPath = str(projectPath) + '/app/data/output'
targetFile = str(targetPath) + '/levels.tsv'

# Create timestamped folder if it doesn't exist
if not os.path.isdir(targetPath):
    os.mkdir(targetPath)

# -------------------------------------------------------
# Create copies
# term_src > sourceFile
# term_csv > targetFile
shutil.copy(sourceFile, targetFile)

# -------------------------------------------------------
# Process
# ltc_df > target_df
# Read
df = pd.read_csv(targetFile, encoding="utf8",sep='\t')

df['level'] = df['term_local_name'].str.replace('MIDS','')
df['pref_label'] = 'MIDS Level ' + df['level']

# RDF Type
df['rdf_type'] = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#Class'

# Qualified Term
df['term_ns_name'] = 'mids:' + df['term_local_name']
df['namespace'] = 'mids:'

df.rename(columns={'notes': 'usage'
                   }, inplace=True)

# Resave timestamped
df.to_csv(targetFile, index=False, encoding='utf8',sep='\t')


