from pathlib import Path
import pandas as pd
import shutil
import globals
import glob
import yaml
from functools import reduce

# Script to transform the single source translation file into a separate file for each translation
# Columns are grouped by language tag suffix, then each group is copied to a separate file.
# Only languages specified in the translations.yml file will be generated
# Workflow
# latimer-translations.csv > ltc-<lang>-translations.csv > ltc-translations-termlist.csv
# translation-transformations.py > terms-transformations.py

namespace = 'ltc'
current_dir = Path().absolute()
root_dir = globals.get_project_root()
project_dir = str(root_dir) +'/'+namespace+'/app'
translations_src = str(project_dir)+'/data/sources/latimer-translations.csv'
translations_csv = str(project_dir)+'/data/output/latimer-translations.csv'

# Create copies
shutil.copy(translations_src, translations_csv)

# Read translations YAML file
translations_yml = str(root_dir)+'/'+namespace+'/app/utils/translations.yml'
yml_dict = []
for yf in glob.glob(translations_yml, recursive=True):
    with open(yf, 'r') as f:
        meta = yaml.load(f, Loader=yaml.FullLoader)


# -------------------------------------------------------


source_df = pd.read_csv(translations_csv, encoding="utf8", skip_blank_lines=True)
for k in meta['Languages']:

    # Get language tag and filter columns in source translation file
    lang = k['code']
    source_df.rename(columns={'term_localName': 'term_local_name'}, inplace=True)
    source_df.sort_values(by='term_local_name', axis='index', inplace=True, na_position='last')
    patterns = [lang+'$', 'term_local_name']
    combined_pattern = reduce(lambda x, y: f'{x}|{y}', patterns)
    lang_df = source_df.filter(regex=combined_pattern)

    translations_target = str(project_dir) + '/data/output/ltc-'+lang+'-translations.csv'

    lang_df.to_csv(translations_target, index=False, encoding='utf8')
