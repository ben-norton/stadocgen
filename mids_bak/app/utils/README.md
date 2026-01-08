# Python Utilities README
**[app/utils]**  
This folder contains a collection of useful profiling python scripts and the transformation
files required to generate the MIDS webpages.

## Contents
**[app/utils/schemas]**  
Scripts for generating schema files from documentation source files. These are not
needed to generate the MIDS webpages. Rather, they are for informational purposes.
  
**[app/utils/transformers]**  
Scripts needed to 'transform' source CSV files into datasets that serve as the backend for the MIDS webpages.
These scripts must be run to generate the MIDS webpages. To generate the source files for the MIDS webpages, run the copy-source-files.py first, then
see the documentation in the transformers folder.


