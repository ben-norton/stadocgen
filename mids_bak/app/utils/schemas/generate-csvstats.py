import csvkit
from datetime import date
from pathlib import Path
import os
import glob

today = date.today()
ts = today.strftime("%Y%m%d")

# Paths
currentPath = Path().absolute()
projectPath = currentPath.parent.parent.parent

# Source Files Path
sourcePath = str(projectPath) + '/app/data/output/'

# Timestamped output path
targetPath = str(currentPath)+'/csvstats/'+str(ts)

# Create timestamped folder if it doesn't exist
if not os.path.isdir(targetPath):
    os.mkdir(targetPath)

# iterating over all files and generate stats
sourceFiles = str(sourcePath) + "*.csv"
for f in glob.glob(sourceFiles):
    stemName = Path(f).stem
    if(stemName == 'mids_information_elements_draft'):
        destFile = 'mids-information-elements-csvstats.csv'
    elif(stemName == 'MIDS-levels-draft'):
        destFile = 'mids-levels-csvstats.csv'
    else:
        destFile = stemName + '-csvstats.csv'
    dest = str(targetPath) + '/' + destFile
    os.system("csvstat " + f + " > " + dest)
