# Markdown and Templates

One of the primary goals of StaDocGen is to broaden the user base to all TDWG standards. The application was originally developed as part of the 
Latimer Core ratification process with this larger goal in mind. 
Markdown is primarily used in the header sections of home, termlist, and quick reference pages. Each markdown file is based on a source template, but quickly departs
from the shared origin by manually entering information specific to a standard. In order to maintain consistency and structure
across all TDWG standard documentation sites, the markdown files need to bge templated in the same manner as Jinja templates. Ideally, information
specific to a standard is entered into a specific set of fields in a yaml configuration file. The yaml variables are passed to a markdown 'template'. 
This workflow does provide consistency and structure, but can be overly restrictive. The goal is to establish a set of required fields that
must be submitted by every standard. The template used to present the required fields cannot be altered by a standard. The design is managed centrally 
and distributed accordingly. For this to work, standards must be provided the option to partially override the established templates or
at minimum, the ability to append custom content. 
