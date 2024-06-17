from flask import Flask, render_template
from markupsafe import Markup
import markdown2
import pandas as pd

app = Flask(__name__)


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
    home_mdfile = 'app/md/opends/home-content.md'
    with open(home_mdfile, encoding="utf8") as f:
        marked_text = markdown2.markdown(f.read())
    return render_template('home.html',
                           homemd=Markup(marked_text),
                           title='Home',
                           slug='home')


@app.route('/terms')
def terms():
    header_mdfile = 'app/md/opends/termlist-header.md'

    with open(header_mdfile, encoding="utf8") as f:
        marked_text = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    # Terms
    terms_csv = 'app/data/opends/opends-termlist.csv'
    terms_df = pd.read_csv(terms_csv, encoding='utf8')

    skoscsv = 'app/data/opends/opends-skos.csv'
    skos_df = pd.read_csv(skoscsv, encoding='utf8')

    sssomcsv = 'app/data/opends/opends-sssom.csv'
    sssom_df = pd.read_csv(sssomcsv, encoding='utf8')

    terms_skos_df1 = pd.merge(
        terms_df, skos_df[['term_iri', 'skos_mappingRelation', 'related_termName']], on=['term_iri'], how='left'
    )
    terms_skos_df = pd.merge(
        terms_skos_df1, sssom_df[['compound_name', 'predicate_label', 'object_id', 'object_category', 'object_label',
                                  'mapping_justification']],
        on=['compound_name'], how='left'
    )

    terms = terms_skos_df.sort_values(by=['class_name'])
    terms['examples'] = terms['examples'].str.replace(r'"', '')
    terms['definition'] = terms['definition'].str.replace(r'"', '')
    terms['usage'] = terms['usage'].str.replace(r'"', '')
    terms['notes'] = terms['notes'].str.replace(r'"', '')

    # Unique Class Names
    opends_classes = terms_df["class_name"].dropna().unique()

    # Terms by Class
    grpdict2 = terms_df.groupby('class_name')[['term_ns_name', 'term_local_name', 'namespace', 'compound_name']].apply(
        lambda g: list(map(tuple, g.values.tolist()))).to_dict()
    terms_by_class = []

    for i in grpdict2:
        terms_by_class.append({
            'class': i,
            'termlist': grpdict2[i]
        })

    return render_template('termlist.html',
                           headerMarkdown=Markup(marked_text),
                           ltcCls=opends_classes,
                           terms=terms,
                           sssom=sssom_df,
                           termsByClass=terms_by_class,
                           pageTitle='Open Digital Specimen Terms (In Progress)',
                           title='Term List',
                           slug='termlist'
                           )


@app.route('/quick-reference')
def quickReference():
    header_mdfile = 'app/md/opends/quick-reference-header.md'
    with open(header_mdfile, encoding="utf8") as f:
        marked_text = markdown2.markdown(f.read())

    # Quick Reference Main
    df = pd.read_csv('app/data/opends/opends-termlist.csv', encoding='utf8')
    df['examples'] = df['examples'].str.replace(r'"', '')
    df['definition'] = df['definition'].str.replace(r'"', '')
    df['usage'] = df['usage'].str.replace(r'"', '')
    df['notes'] = df['notes'].str.replace(r'"', '')

    # Group by Class
    grpdict = df.fillna(-1).groupby('class_name')[['namespace', 'term_local_name', 'label', 'definition',
                                                   'usage', 'notes', 'examples', 'rdf_type', 'class_name',
                                                   'is_required', 'is_repeatable', 'compound_name',
                                                   'datatype', 'term_ns_name', 'term_iri']].apply(
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
                           pageTitle='Open Digital Specimen Quick Reference Guide (In Progress)',
                           title='Quick Reference',
                           slug='quick-reference',
                           requiredTerms=required_df,
                           requiredClasses=required_classes_df
                           )


@app.route('/resources')
def docResources():
    header_mdfile = 'app/md/opends/resources-header.md'
    with open(header_mdfile, encoding="utf8") as f:
        marked_text = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    sssom_mdfile = 'app/md/opends/sssom-reference.md'
    with open(sssom_mdfile, encoding="utf8") as f:
        marked_sssom = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    return render_template('resources.html',
                           headerMarkdown=Markup(marked_text),
                           sssomRefMarkdown=Markup(marked_sssom),
                           pageTitle='Open Digital Specimen Core Resources (In Progress)',
                           title='Resources',
                           slug='resources'
                           )
