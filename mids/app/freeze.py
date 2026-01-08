from flask import Flask, render_template, jsonify, Response
from flask_frozen import Freezer
from markupsafe import Markup
import sys
import markdown2
import pandas as pd
import yaml
from datetime import date
app = Flask(__name__, template_folder='templates')
freezer = Freezer(app)

#app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['FREEZER_DESTINATION'] = 'build'
app.config['FREEZER_RELATIVE_URLS'] = True
#app.config['FREEZER_IGNORE_MIMETYPE_WARNINGS'] = True

# Resolve differences in relative paths with routes.py file
relpath = ''

with open('meta.yml') as metadata:
    meta = yaml.safe_load(metadata)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html',
                           pageTitle='404 Error'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html',
                           pageTitle='500 Unknown Error'), 500

@app.route('/')
def home():
    today = date.today()
    lastModified = today.strftime("%Y-%m-%d")
    home_mdfile = str(relpath) + 'md/home-content.md'
    with open(home_mdfile, encoding="utf8") as f:
        marked_text = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])
    return render_template('home.html',
                           home_markdown=Markup(marked_text),
                           pageTitle='Home',
                           title=meta['title'],
                           acronym=meta['acronym'],
                           landingPage=meta['links']['landing_page'],
                           githubRepo=meta['links']['github_repository'],
                           slug='home',
                           lastModified=lastModified
                           )

@app.route('/information-elements/')
def information_elements():
    home_mdfile = str(relpath) + 'md/information-elements-header.md'
    with open(home_mdfile, encoding="utf8") as f:
        marked_text = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    discipline_terms_tsv = str(relpath) + 'data/output/disciplines_terms.tsv'
    discipline_terms_df = pd.read_csv(discipline_terms_tsv, sep='\t', lineterminator='\n', encoding='utf-8')
    discipline_terms_df = discipline_terms_df.replace(r'\n', ' ', regex=True)

    # Read Information Elements from Master List (see transformation scripts)
    information_elements_tsv = str(relpath) + 'data/output/master-list.tsv'
    information_elements_df = pd.read_csv(information_elements_tsv, sep='\t', lineterminator='\n', encoding='utf-8')
    information_elements_df = information_elements_df.replace(r'\n', ' ', regex=True)
    information_elements_df['anchor_name'] = information_elements_df['term_local_name'].str.lower()
    information_elements_df = information_elements_df.sort_values(by=['term_local_name'])

    # Read MIDS Levels
    levels_tsv = str(relpath) + 'data/output/levels.tsv'
    levels_df = pd.read_csv(levels_tsv, sep='\t', lineterminator='\n', encoding='utf-8')
    levels = levels_df.sort_values(by=['term_local_name'])
    levels_df['level'] = levels_df['term_local_name'].map(lambda x: x.lstrip('+-').rstrip('MIDS'))

    # Read Examples convert rows to comma-separated string from list
    examples_tsv = str(relpath) + 'data/output/examples.tsv'
    examples_df = pd.read_csv(examples_tsv, sep='\t', lineterminator='\r', encoding='utf-8')
    examples_df = examples_df.replace('\n', '', regex=True)
    df2 = examples_df.groupby('term_local_name')['example'].apply(list).reset_index(name="examples_list")
    df2['examples_list'] = df2['examples_list'].apply(lambda x: "|".join(map(str, x)))

    # Merge Examples with Information Elements
    merged_df = pd.merge(information_elements_df, df2[['term_local_name', 'examples_list']], on="term_local_name",
                         how="left")
    merged_df.rename(columns={'examples_list_y': 'examples_list'}, inplace=True)

    schemas_tsv = str(relpath) + 'data/output/schemas.tsv'
    schemas_df = pd.read_csv(schemas_tsv, sep='\t', lineterminator='\n', encoding='utf-8')

    # Simple Schemas Dataframe
    schemas = schemas_df.sort_values(by=['level', 'informationElement'])

    # Schemas by Level
    schemas_grpdict = schemas_df.groupby('level')[
        ['discipline','informationElement','identifier']].apply(
             lambda g: list(map(tuple, g.values.tolist()))).to_dict()
    schemas_by_level = []
    for i in schemas_grpdict:
        schemas_by_level.append({
            'level': i,
            'schemasList': schemas_grpdict[i]
    })

    sizes_df = schemas_df.groupby(['discipline','level']).size().to_frame('count')
    max_counts = sizes_df.groupby('level').max()





    return render_template('information-elements.html',
                           headerMarkdown=Markup(marked_text),
                           pageTitle='Information Elements',
                           title=meta['title'],
                           acronym=meta['acronym'],
                           landingPage=meta['links']['landing_page'],
                           githubRepo=meta['links']['github_repository'],
                           slug='information-elements',
                           levels=levels,
                           informationElements=merged_df,
                           examples=examples_df,
                           disciplinesTerms=discipline_terms_df,
                           schemas=schemas,
                           schemasByLevel=schemas_by_level
                           )

@app.route('/mappings/')
def mappings():
    mappings_mdfile = str(relpath) + 'md/mappings-header.md'
    with open(mappings_mdfile, encoding="utf8") as f:
        marked_text = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    sssom_mdfile = str(relpath) + 'md/sssom-reference.md'
    with open(sssom_mdfile, encoding="utf8") as f:
        sssom_marked_text = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    mappings_tsv = str(relpath) + 'data/output/mappings.tsv'
    mappings_df_csv = pd.read_csv(mappings_tsv, sep='\t', lineterminator='\r', encoding='utf-8', skipinitialspace=True)

    mappings_df_csv = mappings_df_csv.fillna('')
    mappings_df_csv['anchor_name'] = mappings_df_csv['term_local_name'].str.lower()
    mappings_df = mappings_df_csv.sort_values(by=['sssom_subject_category','sssom_subject_id','sssom_object_category','sssom_object_id'])


    return render_template('mappings.html',
                           headerMarkdown=Markup(marked_text),
                           sssomReference=Markup(sssom_marked_text),
                           pageTitle='MIDS Mappings',
                           title=meta['title'],
                           acronym=meta['acronym'],
                           landingPage=meta['links']['landing_page'],
                           githubRepo=meta['links']['github_repository'],
                           slug='mappings',
                           mappings=mappings_df,
                           )

@app.route('/resources/')
def resources():
    content_mdfile = str(relpath) + 'md/resources-content.md'
    with open(content_mdfile, encoding="utf8") as f:
        marked_text = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    with open(str(relpath) + 'md/tools.yml') as tools_yml:
        tools_meta = yaml.safe_load(tools_yml)

    with open(str(relpath) + 'md/glossary.yml') as glossary_yml:
        glossary_meta = yaml.safe_load(glossary_yml)

    return render_template('resources.html',
                           content_markdown=Markup(marked_text),
                           tools_metadata=tools_meta,
                           glossary_metadata=glossary_meta,
                           pageTitle='Resources',
                           title=meta['title'],
                           acronym=meta['acronym'],
                           landingPage=meta['links']['landing_page'],
                           githubRepo=meta['links']['github_repository'],
                           slug='resources')
@app.route('/about/')
def about():
    about_mdfile = str(relpath) + 'md/about-content.md'
    with open(about_mdfile, encoding="utf8") as f:
        marked_text = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    return render_template('about.html',
        about_markdown=Markup(marked_text),
        pageTitle='About MIDS',
        title=meta['title'],
        acronym=meta['acronym'],
        landingPage=meta['links']['landing_page'],
        githubRepo=meta['links']['github_repository'],
        slug='about')


#API Requests for Table Filters
@app.route('/api/data.json')
def get_data():
    """Return all data as JSON"""
    mappings_tsv = str(relpath) + 'data/output/mappings.tsv'
    mappings_df = pd.read_csv(mappings_tsv, sep='\t', lineterminator='\r', encoding='utf-8', skipinitialspace=True, index_col=0)
    df_cleaned = mappings_df.dropna(how='all')
    json_string = df_cleaned.to_json(orient="records")
    return Response(json_string, mimetype='application/json')

@app.route('/api/filters.json')
def get_filters():
    """Return unique values for each filterable column"""
    mappings_tsv = str(relpath) + 'data/output/mappings.tsv'
    mappings_df = pd.read_csv(mappings_tsv, sep='\t', lineterminator='\r', encoding='utf-8', skipinitialspace=True, index_col=0)
    mappings_df = mappings_df.fillna('')
    df_cleaned = mappings_df.dropna(how='all')
    unique_levels = df_cleaned['sssom_subject_category'].unique()
    unique_infoElements = df_cleaned['sssom_subject_id'].unique()
    unique_disciplines = df_cleaned['discipline'].unique()
    levels = unique_levels.tolist()
    infoElements = unique_infoElements.tolist()
    disciplines = unique_disciplines.tolist()

    return jsonify({
        'levels': levels,
        'infoElements': infoElements,
        'disciplines': disciplines
    })





if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(port=8001)