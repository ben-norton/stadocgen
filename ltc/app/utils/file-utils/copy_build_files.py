import shutil
import os
import config as cfg

# Refreshes published documentation webpages for Latimer Core.
# Copy Build Files from StaDocGen to /docs in LtC Repo

# Important! Change the target directory to your local LtC repo
# First step. Test and Build Flask Site using StaDocGen (see README file for testing and build flask pages)
# Commit changes to StaDocGen Repository
#


root_dir = cfg.get_project_root()
source_dir = str(root_dir) + '/ltc/app/build'
target_dir = 'G:/repos/tdwg/ltc/docs' # Change to reflect your local filesystem


def copy_files():
	files = os.listdir(source_dir)
	for f in files:
		shutil.copy2(os.path.join(source_dir, f), target_dir)

copy_files()