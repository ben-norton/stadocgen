# StaDocGen
This application was originally build by [Ben Norton](https://orcid.org/0000-0002-5819-9134) for the Latimer Core TDWG standard.
The original application can be found at https://github.com/ben-norton/stadocgen-development.
It has been forked and adapted by DiSSCo for the purpose of generating documentation for the open Digital Specimen standard.
DiSSCo changed the layout and added some functionality to the original application.
However, the idea behind the application and the general architecture and layout is still the same.
DiSSCo reuses this application to be in line with existing TDWG standards and to ease findability as both serve the same user group.

## DiSSCo Application Specifics
The DiSSCo version of the application contains a few changes to the original.
DiSSCo contains not just one object but a range of objects for each we created a terms, guide and resources page.
This means we morphed the menu in a dropdown button with the different objects as submenus.

We also wanted the csv-files to be based on the json schemas we publish on https://schemas.dissco.tech.
For this we created a utility file which generates or updates the csv files behind the terms and guides pages.
For the resources, the classDiagrams are also generated based on the json schemas, expect the Class Relationships at the bottom.
The Entity Relationship diagrams are also manual created.
These can easily being made by hand based on the Class Diagrams.
The script to generate this content needs to be kicked off by hand, by running the python main function in the `utlis/generation/main.py`.

## Running the application
There are several ways to run the application.
From an IDE, from the command line, or from a Docker container.
For each of these methods, you will need to have Python installed on your machine and have port 8080 available on your machine.

### IDE
Make sure you have a virtual environment set up and activated.
Install the requirements with `pip install -r requirements.txt`.
Run the `main.py` file in the `StaDocGen` directory.

### Command line
Make sure you have a virtual environment set up and activated.
Install the requirements with `pip install -r requirements.txt`.
Run the `main.py` file in the `StaDocGen` directory with `python main.py`.

### Docker
Make sure you have Docker installed on your machine.
Build the Docker image with `docker build -t dissco-terms-documentation .`.
Run the Docker container with `docker run -p 8080:8080 dissco-terms-documentation`.
