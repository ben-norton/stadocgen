# Overview
StaDocGen = Data Standards Documentation Generator
StaDocGen (Standards Documentation Generator) builds TDWG standards documentation web pages using the standardized set of CSV and Markdown source files. The primary purpose and original motivation 
for creating StaDocGen is to harmonize the design and content of TDWG standards documentation pages using the same set of CSV files utilized to generate RDF files as the primary data source for content. 
This was identified as key to the success of the platform. By using the existing set of CSV files, maintenance groups are not burdened with additional work to use StaDocGen. However, there are plenty 
of custom features and functionality a maintenance group may take advantage of if they chose to do so. 
        
To set up an StaDocGen instance for a standard, the shared folder is copied to a new directory with the namespace as the folder name. It's not ideal to make a separate directory for each standard, 
but it's necessary to fully support TDWG standards. The Flask and Flask frozen libraries use templates that are not modular, meaning they cant be shared nor stored in multiple directories. When standards 
don't follow the traditional structure, they need their own unique templates and build scripts that can't be shared. Instead of making a complicated structure where some standards share an instance 
and others are kept separate, a decision was made in the design of StaDocGen to give each standard its own instance.

## Architecture
Stadocgen is built using Python 3.11 with the Flask Framework for generating the web-based content. Further details are located in the
requirements.txt. Please consult that file for more details regarding the libraries used to create StaDocGen.

## Project Folders
Root Directories  

| Path | Title | Descrption |
| -- | -- | -- |
| /app | Application | Top-level application directory for a given standard. |
| /app/build | Build Output | Target folder for building webpages. The contents are published to the web |
| /app/data | Data | Contains all source and output csv files |
| /app/md | Markdown Content | Source markdown content for static (non-dynamically generated) webpage content |
| /app/static | Static Web Files | Static assets for presentation of webpages and specific interactive features such as ER Charts |
| /app/templates | Templates | Jinja webpage templates | 
| /app/utils | Utilities | Python scripts for manipulating and analyzing source and target CSV files |
