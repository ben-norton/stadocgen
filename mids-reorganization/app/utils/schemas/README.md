# Schemas README
This directory contains a set of scripts that inspects source files and generates a schema and stats files for each.

## Scripts
1. generate-csvstats.py | Generates stats for each csv file in the source directory
2. generate-table-schemas.py | Generates table schemas for each csv file in the source directory

## Notes
1. You may need to alter the csv source path in the generator scripts
2. Output is stored in timestamped directories in the format YYYYMMDD (day is the timestamp level of granularity)
3. If the timestamp is unchanged (script is run twice on the same day), the scripts will overwrite existing output
Last Updated: 20241223