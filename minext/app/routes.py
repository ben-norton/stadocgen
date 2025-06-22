from app import app
from flask import render_template
from markupsafe import Markup
import markdown2
import pandas as pd
import yaml
import os.path, time

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


'''
@app.route('/pygments.css')
def pygments_css():
    return pygments_style_defs('tango'), 200, {'Content-Type': 'text/css'}
'''

# Homepage with content stored in markdown file
@app.route('/')
def home():
    home_mdfile = 'app/md/home-content.md'
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

@app.route('/terms')
def terms():
    language_code = 'en'
    language_label = ''
    header_mdfile = 'app/md/termlist-header.md'
    with open(header_mdfile, encoding="utf-8") as f:
        marked_text = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

# Metadata Terms
    meta_csv = 'app/data/output/metadata-terms.csv'
    meta_df = pd.read_csv(meta_csv, encoding='utf-8')
    # Terms
    terms_csv = 'app/data/output/minext-termlist.csv'
    terms_df = pd.read_csv(terms_csv, encoding='utf-8')

    terms = terms_df.sort_values(by=['class_name','term_local_name'])

    # Unique Class Names
    termsCls = terms_df['class_name'].dropna().unique()

    # Terms by Class
#    grpdict2 = terms_df.sort_values(['class_name','term_local_name'],ascending=False).groupby('class_name')[['term_ns_name', 'term_local_name', 'namespace', 'compound_name', 'rdf_type']].apply(
#        lambda g: list(map(tuple, g.values.tolist()))).to_dict()

    grpdict2 = terms_df.fillna(-1).groupby('class_name')[['term_ns_name', 'term_local_name', 'namespace', 'compound_name', 'rdf_type']].apply(
        lambda g: list(map(tuple, g.values.tolist()))).to_dict()
    termsByClass = []

    for i in grpdict2:
        termsByClass.append({
            'class': i,
            'termlist': grpdict2[i]
        })
    return render_template('term-list.html',
                           headerMarkdown=Markup(marked_text),
                           metadataTerms=meta_df,
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

@app.route('/quick-reference')
def quickReference():
    header_mdfile = 'app/md/quick-reference-header.md'
    marked_text = ''
    with open(header_mdfile, encoding="utf-8") as f:
        marked_text = markdown2.markdown(f.read())

    # Quick Reference Main
    df = pd.read_csv('app/data/output/minext-termlist.csv', encoding='utf-8')
    df['examples'] = df['examples'].str.replace(r'"', '')
    df['definition'] = df['definition'].str.replace(r'"', '')
    df['usage'] = df['usage'].str.replace(r'"', '')
    df['notes'] = df['notes'].str.replace(r'"', '')

    # Group by Class
    grpdict = df.fillna(-1).groupby('class_name')[['namespace', 'term_local_name', 'label', 'definition',
                                                   'usage', 'notes', 'examples', 'rdf_type', 'class_name',
                                                   'is_required', 'compound_name',
                                                   'datatype', 'term_ns_name', 'term_iri', 'term_version_iri','term_modified']].apply(
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

    required_df = terms_df.loc[(terms_df['is_required'] == True) &
                               (terms_df['rdf_type'] == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#Property')]

    required_classes_df = terms_df.loc[(terms_df['is_required'] == True) &
                           (terms_df['rdf_type'] == 'http://www.w3.org/2000/01/rdf-schema#Class')]


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