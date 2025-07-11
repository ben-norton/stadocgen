from app import app
from flask import render_template
from markupsafe import Markup
import markdown2
import pandas as pd
import yaml
from tabulate import tabulate

relpath = 'app/'

with open('app/meta.yml') as metadata:
    meta = yaml.safe_load(metadata)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html',
                           pageTitle='404 Error'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html',
                           pageTitle='500 Unknown Error'), 500

# Homepage with content stored in markdown file
@app.route('/')
def home():
    home_mdfile = str(relpath) + 'md/home-content.md'
    title = meta['title'] + ' (MIDS)'
    with open(home_mdfile, encoding="utf8") as f:
        marked_text = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])
    return render_template('home.html',
                           home_markdown=Markup(marked_text),
                           pageTitle='Home',
                           title=title,
                           acronym=meta['acronym'],
                           landingPage=meta['links']['landing_page'],
                           githubRepo=meta['links']['github_repository'],
                           slug='home'
                           )

@app.route('/information-elements')
def information_elements():
    home_mdfile = str(relpath) + 'md/information-elements-header.md'
    with open(home_mdfile, encoding="utf8") as f:
        marked_text = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    # Read Information Elements from Master List (see transformation scripts)
    information_elements_tsv = str(relpath) + 'data/output/master-list.tsv'
    information_elements_df = pd.read_csv(information_elements_tsv, sep='\t', lineterminator='\n', encoding='utf-8')
    information_elements_df = information_elements_df.sort_values(by=['class_name', 'term_local_name'])
    print(information_elements_df['usage'])
    # Read MIDS Levels (rdfs:Class)
    levels_tsv = str(relpath) + 'data/output/levels.tsv'
    levels_df = pd.read_csv(levels_tsv, sep='\t', lineterminator='\n', encoding='utf-8')
    levels = levels_df.sort_values(by=['term_local_name'])
    levels_df['level'] = levels_df['term_local_name'].map(lambda x: x.lstrip('+-').rstrip('MIDS'))

    # Read SSSOM Mappings
    mappings_tsv = str(relpath) + 'data/output/mappings.tsv'
    mappings_df = pd.read_csv(mappings_tsv, sep='\t', lineterminator='\r', encoding='utf-8', skipinitialspace=True)

    # Read Examples convert rows to comma-separated string from list
    examples_tsv = str(relpath) + 'data/output/examples.tsv'
    examples_df = pd.read_csv(examples_tsv, sep='\t', lineterminator='\r', encoding='utf-8')
    examples_df = examples_df.replace('\n', '', regex=True)
    df2 = examples_df.groupby('term_local_name')['example'].apply(list).reset_index(name="examples_list")
    df2['examples_list'] = df2['examples_list'].apply(lambda x: "|".join(map(str, x)))

    # Merge Examples with Information Elements
    merged_df = pd.merge(information_elements_df, df2[['term_local_name','examples_list']], on="term_local_name", how="left")
    merged_df.rename(columns={'examples_list_y': 'examples_list'}, inplace=True)


    # Group Information Elements by Level
    grpdict2 = information_elements_df.groupby('class_pref_label')[
        ['term_ns_name', 'term_local_name', 'namespace', 'compound_name', 'term_version_iri', 'term_modified']].apply(
        lambda g: list(map(tuple, g.values.tolist()))).to_dict()
    information_elements_by_level = []
    for i in grpdict2:
        information_elements_by_level.append({
            'class': i,
            'informationElementList': grpdict2[i]
        })

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
                           mappings=mappings_df,
                           informationElementsByLevel=information_elements_by_level,
                           examples=examples_df
                           )

@app.route('/mappings')
def mappings():
    mappings_mdfile = str(relpath) + 'md/mappings-header.md'
    with open(mappings_mdfile, encoding="utf8") as f:
        marked_text = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    sssom_mdfile = str(relpath) + 'md/sssom-reference.md'
    with open(sssom_mdfile, encoding="utf8") as f:
        sssom_marked_text = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    mappings_tsv = str(relpath) + 'data/output/mappings.tsv'
    mappings_df = pd.read_csv(mappings_tsv, sep='\t', lineterminator='\r', encoding='utf-8', skipinitialspace=True)

    mappings_df = mappings_df.fillna('')

    return render_template('mappings.html',
                           headerMarkdown=Markup(marked_text),
                           sssomReference=Markup(sssom_marked_text),
                           pageTitle='Mappings',
                           title=meta['title'],
                           acronym=meta['acronym'],
                           landingPage=meta['links']['landing_page'],
                           githubRepo=meta['links']['github_repository'],
                           slug='mappings',
                           mappings=mappings_df,
                           )

@app.route('/resources')
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

@app.route('/about')
def about():
    about_mdfile = str(relpath) + 'md/about-content.md'
    with open(about_mdfile, encoding="utf8") as f:
        marked_text = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    return render_template('about.html',
        about_markdown=Markup(marked_text),
        pageTitle='About',
        title=meta['title'],
        acronym=meta['acronym'],
        landingPage=meta['links']['landing_page'],
        githubRepo=meta['links']['github_repository'],
        slug='about')