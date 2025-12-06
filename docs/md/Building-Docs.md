# Building Docs
## Frozen-Flask
https://frozen-flask.readthedocs.io/en/latest/
Frozen-flask generates a set of static html files from a flask application. Most work in StaDocGen 
is done using a Flask Application (main.py). TDWG documentation websites are hosted on GitHub using the 
static site generator, GitHub Pages. The advantage of using GitHUb Pages is ease of use. A website can be hosted directly
from a repository. Then hosting service is limited to static files. Dynamic server-side applications are not directly
supported (Ruby is supported to a limited extent). Therefore, dynamically generated pages must be converted into
static files for hosting. Here, Frozen-flask serves this purpose.

To build the documentation pages, the flask application "freezes" the output files. The output is stored in the build directory.
The two files, routes.py and freeze.py are deceptively similar. There are several critical differences that must be preserved in order to build
the output files.
1. All routes in the freeze.py file are wrapped in forward slashing, both leading and trailing. In routes.py, only the leading forward slash is needed.
2. The freeze command is run from the app directory. Therefore, paths in the freeze file are relative to the app directory. Routes is run from the root folder using the main.py file. All paths in the routes.py file are relative to the project root folder.
3. To run the development site (routes.py), switch to the root directory, then run flask run.
4. To build the documentation pages using freeze, change to the app directory, then run *python freeze.py build*.
