import pandas as pd
from pathlib import Path
import json

currentPath = Path().absolute()
projectPath = currentPath.parent.parent.parent

# This file writes the JSON files used by the interactive mappings table that allows usere to filter by specific attributes
# The JSON files are used as API request endpoints in the freeze.py and subsequent build files

def write_json_filter_files():
	# --------------------------------------------------------------------------------------------
	# Write filters.json

	# Get source files
	output_filters_json = str(projectPath) + '/app/api/filters.json'
	output_build_filters_json = str(projectPath) + '/app/build/api/filters.json' # Build Directory
	mappings_tsv = str(projectPath) + '/app/data/output/mappings.tsv'

	# Read source file and remove empty items
	mappings_df = pd.read_csv(mappings_tsv, sep='\t', lineterminator='\r', encoding='utf-8', skipinitialspace=True,
	                          index_col=0)
	mappings_df = mappings_df.fillna('')
	df_cleaned = mappings_df.dropna(how='all')
	# Get Unique Items from Columns to create filters
	unique_levels = df_cleaned['sssom_subject_category'].unique()
	unique_infoElements = df_cleaned['sssom_subject_id'].unique()
	unique_disciplines = df_cleaned['discipline'].unique()

	# Create lists for each filter and remove empty strings
	disciplines = list(filter(None, unique_disciplines.tolist()))
	levels = list(filter(None, unique_levels.tolist()))
	infoElements = list(filter(None, unique_infoElements.tolist()))

	# Write filter lists to a json file for use by the application
	with open(output_filters_json, "w") as f:
		json.dump([{'levels': levels,'infoElements': infoElements,'disciplines': disciplines}],f)

	# Write JSON to Build directory
	with open(output_build_filters_json, 'w') as fb:
		json.dump([{'levels': levels,'infoElements': infoElements,'disciplines': disciplines}],fb)

	#--------------------------------------------------------------------------------------------
	# Write data.json

	# Set Files
	output_json = str(projectPath) + '/app/api/data.json'
	mappings_tsv = str(projectPath) + '/app/data/output/mappings.tsv'
	output_build_data_json = str(projectPath) + '/app/build/api/data.json'  # Build File

	# Read source file as dataframe
	mappings_df = pd.read_csv(mappings_tsv, sep='\t', lineterminator='\r', encoding='utf-8', skipinitialspace=True,
	                          index_col=0)
	df_cleaned = mappings_df.dropna(how='all')
	# Convert dataframe to json
	json_string = df_cleaned.to_json(orient="records")

	# Write JSON to file for testing
	with open(output_json, 'w') as outfile:
		outfile.write(json_string)

	# Write JSON to Build directory
	with open(output_build_data_json, 'w') as outfile:
		outfile.write(json_string)

if __name__ == "__main__":
	write_json_filter_files()

