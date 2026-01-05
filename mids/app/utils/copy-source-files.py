import urllib.request
import os
import config as cfg

'''
Copies source data files and markdown content files from the MIDS repository (https://github.com/tdwg/mids) to the StaDocGen repository
This script is run manually as a prerequisite to the documentation generator process
'''
root_dir = cfg.get_project_root()

download_urls =  [
    "https://raw.githubusercontent.com/tdwg/mids/refs/heads/main/source/terms/information_elements.tsv",
    "https://raw.githubusercontent.com/tdwg/mids/refs/heads/main/source/terms/levels.tsv",
    "https://raw.githubusercontent.com/tdwg/mids/refs/heads/main/source/terms/examples.tsv",
    "https://raw.githubusercontent.com/tdwg/mids/refs/heads/main/source/mappings/mids_abcd_biology_1.sssom.tsv",
    "https://raw.githubusercontent.com/tdwg/mids/refs/heads/main/source/mappings/mids_abcd_biology_1.sssom.yml",
    "https://raw.githubusercontent.com/tdwg/mids/refs/heads/main/source/mappings/mids_dwc_biology_1.sssom.tsv",
    "https://raw.githubusercontent.com/tdwg/mids/refs/heads/main/source/mappings/mids_dwc_biology_1.sssom.yml",
    "https://raw.githubusercontent.com/tdwg/mids/refs/heads/main/source/mappings/mids_dwc_geology_1.sssom.tsv",
    "https://raw.githubusercontent.com/tdwg/mids/refs/heads/main/source/mappings/mids_dwc_geology_1.sssom.yml",

]
download_md_urls =  [
    "https://raw.githubusercontent.com/tdwg/mids/refs/heads/main/source/md/about-content.md",
    "https://raw.githubusercontent.com/tdwg/mids/refs/heads/main/source/md/home-content.md",
    "https://raw.githubusercontent.com/tdwg/mids/refs/heads/main/source/md/information-elements-header.md",
    "https://raw.githubusercontent.com/tdwg/mids/refs/heads/main/source/md/mappings-header.md",
    "https://raw.githubusercontent.com/tdwg/mids/refs/heads/main/source/md/resources-content.md",
    "https://raw.githubusercontent.com/tdwg/mids/refs/heads/main/source/md/sssom-reference.md",
    "https://raw.githubusercontent.com/tdwg/mids/refs/heads/main/source/resources/glossary.yml",
    "https://raw.githubusercontent.com/tdwg/mids/refs/heads/main/source/resources/tools.yml",
]
target_dir = str(root_dir) + '/mids/app/data/source/mids-repo'
target_md_dir = str(root_dir) + '/mids/app/md'

for url in download_urls:
    file_name = os.path.basename(url)
    local_path = os.path.join(target_dir, file_name)
    urllib.request.urlretrieve(url, local_path)
    print('Downloaded ' + url)

for md_url in download_md_urls:
    md_file_name = os.path.basename(md_url)
    local_md_path = os.path.join(target_md_dir, md_file_name)
    urllib.request.urlretrieve(md_url, local_md_path)
    print('Downloaded ' + md_url)
