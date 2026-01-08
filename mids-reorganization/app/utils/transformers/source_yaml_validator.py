import datetime
from pathlib import Path
import yaml

# VALIDATE YAML FILES
# This script validates source YAML files and should be run prior to the other four transformation scripts
# To prevent errors when generating HTML pages, errors must be fixed before proceeding with source file transformations.

today = datetime.date.today()
ts = today.strftime("%Y%m%d")

## Get PATHS
current_path = Path().absolute()
project_path = current_path.parent.parent.parent

def get_yaml_files_in_folder(folder_path):
	"""
	Get all YAML files in a specified folder.
	Args:
		folder_path (str or Path): Path to the folder to search
	"""
	folder = Path(folder_path)
	yaml_files = []

	if not folder.exists():
		print(f"Warning: Folder '{folder_path}' does not exist.")
		return yaml_files

	# Get all .yaml and .yml files
	for extension in ['*.yaml', '*.yml']:
		yaml_files.extend([str(f) for f in folder.glob(extension)])

	for yaml_file in yaml_files:
		validate_yaml_syntax(yaml_file)

	# return sorted(yaml_files)

results = []
def validate_yaml_syntax(yaml_file):
    try:
        with open(yaml_file, 'r') as f:
            yaml.safe_load(f)
        print(f"'{yaml_file}' has valid syntax.")
        results.append({yaml_file: "Valid YAML syntax"})    # Add valid to results list
    except yaml.YAMLError as e:
        print(f"YAML syntax error in '{yaml_file}': {e}")
        entry = {yaml_file: {e}}
        results.append(entry)   # Add error to results list
    finally:
        return results  # return results list for further processing if needed

#print(errors)
yaml_path = str(project_path) + '/app/md'
get_yaml_files_in_folder(yaml_path)
