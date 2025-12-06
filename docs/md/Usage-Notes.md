# Usage Notes
This file contains notes recorded while using Stadocgen to generate documentation pages.
Task: Latimer Core Documentation Pages
Date: 20231208
Changes 
1. ltc-namespaces.csv file no longer exists in the source repo. Rename namespace.csv under the rs.tdwg folder to ltc-namespaces.csv. Renamed the columns to march the transformation scripts, then added a colon to each namespace prefix to allow a join between the namespaces and termlist files.
2. New namespaces file was causing the ltc-terms merge to drop 100 200 terms. I dropped the new version and replaced it with the previous version, then ran the script. It worked.
Date: 20240101
1. Templated the top section of termlist header 
