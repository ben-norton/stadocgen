# MinExt README
Project: StaDocGen
Created: 2025-12-05

- Source terms file must use the following column headers: term,label,class_name,material_scope,definition,examples,usage_note,source,rdf_type,datatype,is_required,notes,editorial_notes,namespace,namespace_iri
- All files in the data/sources directory should remain in verbatim form. Any changes to the source terms files should be done in the MinExt repository, then copied into StaDocGen using the copy-source-files.py utility.
- To generate the source data files run copy_source_files.py then terms_transformations.py
- 