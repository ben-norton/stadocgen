from flask import Flask, render_template
from flask_frozen import Freezer
from markupsafe import Markup
import sys
import markdown2
import pandas as pd
import yaml
import os.path, time
app = Flask(__name__, template_folder='templates')
freezer = Freezer(app)

#app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['FREEZER_DESTINATION'] = 'build'
app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_IGNORE_MIMETYPE_WARNINGS'] = True

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


# Homepage with content stored in markdown file

@app.route('/')
def home():
    home_mdfile = 'md/home-content.md'
    md_lastModified = time.ctime(os.path.getmtime(home_mdfile))
    print("last modified: %s" % time.ctime(os.path.getmtime(home_mdfile)))

    with open(home_mdfile, encoding="utf8") as f:
        marked_text = markdown2.markdown(f.read())
    return render_template('home.html',
                           home_markdown=Markup(marked_text),
                           pageTitle='Home',
                           title=meta['title'],
                           acronym=meta['acronym'],
                           status=meta['status'],
                           landingPage=meta['documentation-landing-page'],
                           githubRepo=meta['github-repo'],
                           slug='home',
                           lastModified=md_lastModified
                           )

@app.route('/terms/')
def terms():
    language_code = 'en'
    language_label = ''
    header_mdfile = 'md/termlist-header.md'
    with open(header_mdfile, encoding="utf-8") as f:
        marked_text = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    # Metadata Terms
    meta_csv = 'data/output/metadata-termlist.csv'
    meta_df = pd.read_csv(meta_csv, encoding='utf-8')
    published_metadata_df = meta_df[meta_df['is_published']==True]

    print(published_metadata_df)

    # Terms
    terms_csv = 'data/output/minext-termlist.csv'
    terms_df = pd.read_csv(terms_csv, encoding='utf-8')
    terms = terms_df.sort_values(by=['class_name', 'term_local_name'])

    # Unique Class Names
    termsCls = terms_df[['class_ns_name','class_name']].drop_duplicates()

    # Group terms by class for index and table organization
    grpdict2 = terms_df.fillna(-1).groupby('class_name')[
        ['term_ns_name', 'term_local_name', 'namespace', 'compound_name', 'rdf_type']].apply(
        lambda g: list(map(tuple, g.values.tolist()))).to_dict()
    termsByClass = []

    for i in grpdict2:
        termsByClass.append({
            'class': i,
            'termlist': grpdict2[i]
        })
    return render_template('term-list.html',
                           headerMarkdown=Markup(marked_text),
                           metadataTerms=published_metadata_df,
                           termsCls=termsCls,
                           terms=terms,
                           termsByClass=termsByClass,
                           uniqueTerms=terms,
                           pageTitle='Term List',
                           status=meta['status'],
                           title=meta['title'],
                           acronym=meta['acronym'],
                           landingPage=meta['documentation-landing-page'],
                           githubRepo=meta['github-repo'],
                           slug='terms',
                           languageCode=language_code,
                           languageLabel=language_label
                           )

@app.route('/quick-reference/')
def quickReference():
    language_code = 'en'
    language_label = ''
    header_mdfile = 'md/quick-reference-header.md'
    marked_text = ''
    with open(header_mdfile, encoding="utf-8") as f:
        marked_text = markdown2.markdown(f.read())

    # Quick Reference Main
    df = pd.read_csv('data/output/minext-termlist.csv', encoding='utf-8')

    # Group by Class
    grpdict = df.fillna(-1).groupby('class_name')[['namespace', 'term_local_name', 'label',
                                                   'definition', 'usage_note', 'note',
                                                   'examples', 'rdf_type', 'class_name',
                                                   'is_required', 'compound_name', 'datatype',
                                                   'term_ns_name', 'term_iri', 'material_category',
                                                   'assertion_type_iri']].apply(
        lambda g: list(map(tuple, g.values.tolist()))).to_dict()
    grplists = []
    for i in grpdict:
        grplists.append({
            'class': i,
            'termlist': grpdict[i]
        })

    # Required values
    terms_df = df[['namespace', 'term_local_name', 'label', 'class_name',
                   'is_required', 'rdf_type', 'compound_name']].sort_values(by=['class_name'])

    required_df = terms_df.loc[(terms_df['is_required']==True) &
                               (terms_df['rdf_type'] == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#Property')]

    required_classes_df = terms_df.loc[(terms_df['is_required']==True) &
                                       (terms_df['rdf_type'] == 'http://www.w3.org/2000/01/rdf-schema#Class')]
    print(required_classes_df.head())

    return render_template('quick-reference.html',
                           headerMarkdown=Markup(marked_text),
                           grplists=grplists,
                           requiredTerms=required_df,
                           requiredClasses=required_classes_df,
                           pageTitle='Quick Reference Guide',
                           title=meta['title'],
                           acronym=meta['acronym'],
                           landingPage=meta['documentation-landing-page'],
                           githubRepo=meta['github-repo'],
                           slug='quick-reference'
                           )

'''
@app.route('/material-categories/')
def materialCategories():
    language_code = 'en'
    language_label = ''
    header_mdfile = 'md/material-categories-header.md'
    marked_text = ''
    with open(header_mdfile, encoding="utf-8") as f:
        marked_text = markdown2.markdown(f.read())

    # Quick Reference Main
    df = pd.read_csv('data/output/minext-termlist.csv', encoding='utf-8')

    specimen_df = df[df['material_category'] == 'Specimen']
    constituent_part_df = df[df['material_category'] == 'Constituent Part']

    # Group by Material Category
    grpdict = df.fillna(-1).groupby('material_category')[['namespace', 'term_local_name', 'label',
                                                       'definition', 'usage_note', 'note',
                                                       'examples', 'rdf_type', 'class_name',
                                                       'is_required', 'compound_name', 'datatype',
                                                       'term_ns_name', 'term_iri', 'material_category']].apply(
        lambda g: list(map(tuple, g.values.tolist()))).to_dict()
    grplists = []
    for i in grpdict:
        grplists.append({
            'category': i,
            'termlist': grpdict[i]
        })

    # Required values

    return render_template('material-categories.html',
                           headerMarkdown=Markup(marked_text),
                           grplists=grplists,
                           specimenTerms=specimen_df,
                           constituentPartTerms=constituent_part_df,
                           pageTitle='Material Categories',
                           title=meta['title'],
                           acronym=meta['acronym'],
                           landingPage=meta['documentation-landing-page'],
                           githubRepo=meta['github-repo'],
                           slug='material-categories',
                           languageCode=language_code,
                           languageLabel=language_label
                           )

'''


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(port=7000)