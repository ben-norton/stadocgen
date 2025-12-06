# Specifications

### Website Structure and Markdown
The standards documentation websites are comprised of a specific set of html pages, two are required. Each page is assigned a url slug for programmatic use.

| Page Title      | [slug]           | Description                        | Example                    | Is Required |
|-----------------|------------------|------------------------------------|----------------------------|------------|
| Home            | [home]           | The documentation website homepage | https://tdwg.github.io/ltc | Yes        |
| Terms List      | [terms-list]     | Normative terms list               |                            | Yes        |
| Quick Reference | [quick-reference] | Non-normative documentation        |                            | No         |
| Resources       | [resources]      | Support documentation and diagrams |                            | No         |

The markdown files are source of webpage content, mainly at the top of each page. 

The naming convention is [page slug]-[block].md
Where page slug is the URL slug for the specific page and the block refers to the location of the content on the page.
#### Blocks
* Content - Main Body
* Header - Page Header

The app can be configured to parse additional blocks and slugs.
### Markdown Files
home-content.md
quick-reference-header.md
resources-header.md
sssom-reference.md
termlist-header.md

## CSV Files
The CSV workflow transforms the source set of CSV files (see list below) and generates a target set for publishing on the web using a set of python transformation scripts
1. Source Files: [project root]/app/data/source-files
2. Transformation Target Files: [project root]/app/data/output (For storing the output from transformations scripts)

## Conventions and Logistics
1. Most directories have an explanatory README file that provides detailed information about the respective folder. Please consult these files for additional information.
2. Source files are populated by copying the files from the respective GitHub repo directly into the data/source-files folder. Once copied into StaDocGen, the original files
are preserved in their original state without being subject to any programmatic alteration. The only time a source file is altered is when a new version is copied from the
source repository. In this instance the existing file is overwritten by the more recent version.


