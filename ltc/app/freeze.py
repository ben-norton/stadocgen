from flask import Flask, render_template, abort
from flask_frozen import Freezer
from markupsafe import Markup
import markdown2
import pandas as pd
import yaml
import glob
import sys
app = Flask(__name__, template_folder='templates')
freezer = Freezer(app)

#app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['FREEZER_DESTINATION'] = 'build'
app.config['FREEZER_RELATIVE_URLS'] = False
app.config['FREEZER_IGNORE_MIMETYPE_WARNINGS'] = True
#app.config['FREEZER_IGNORE_MIMETYPE_WARNINGS'] = True

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
    with open(home_mdfile, encoding="utf8") as f:
        marked_text = markdown2.markdown(f.read())

    disclaimer_header_mdfile = 'md/translation-disclaimer-header.md'
    with open(disclaimer_header_mdfile, encoding="utf-8") as f:
        marked_disclaimer_header = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    disclaimer_mdfile = 'md/translation-disclaimer.md'
    with open(disclaimer_mdfile, encoding="utf-8") as f:
        marked_disclaimer = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    return render_template('home.html',
                           home_markdown=Markup(marked_text),
                           pageTitle='Home',
                           title=meta['title'],
                           acronym=meta['acronym'],
                           landingPage=meta['documentation-landing-page'],
                           githubRepo=meta['github-repo'],
                           slug='home',
                           translationDisclaimer=Markup(marked_disclaimer),
                           )
#French translated Homepage
@app.route('/fr/')
def home_fr():
    translations_yml = 'utils/translations.yml'
    yml_dict = []
    for yf in glob.glob(translations_yml, recursive=True):
        with open(yf, 'r', encoding='utf8') as f:
            lang_meta = yaml.load(f, Loader=yaml.FullLoader)
            yml_dict.append(lang_meta)

    lang = 'fr'
    language_code = 'fr'
    language_label = 'Français'

    home_mdfile = 'md/'+lang+'/home-content-'+lang+'.md'
    with open(home_mdfile, encoding="utf8") as f:
        marked_text = markdown2.markdown(f.read())

    disclaimer_mdfile = 'md/'+lang+'/translation-disclaimer-'+lang+'.md'
    with open(disclaimer_mdfile, encoding="utf-8") as f:
        marked_disclaimer = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    return render_template('fr/home-fr.html',
                           home_markdown=Markup(marked_text),
                           pageTitle='Home',
                           title=meta['title'],
                           acronym=meta['acronym'],
                           landingPage=meta['documentation-landing-page'],
                           githubRepo=meta['github-repo'],
                           slug='home',
                           translationDisclaimer = Markup(marked_disclaimer)
                           )

# French Terms Page
@app.route('/terms/fr/')
def terms_fr():

    translations_yml = 'utils/translations.yml'
    yml_dict = []
    for yf in glob.glob(translations_yml, recursive=True):
        with open(yf, 'r', encoding='utf8') as f:
            lang_meta = yaml.load(f, Loader=yaml.FullLoader)
            yml_dict.append(lang_meta)

    lang = 'fr'
    language_code = 'fr'
    language_label = 'Français'

    header_mdfile = 'md/'+lang+'/termlist-header-'+lang+'.md'
    with open(header_mdfile, encoding="utf-8") as f:
        marked_text = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    disclaimer_mdfile = 'md/'+lang+'/translation-disclaimer-'+lang+'.md'
    with open(disclaimer_mdfile, encoding="utf-8") as f:
        marked_disclaimer = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    disclaimer_header_mdfile = 'md/' + lang + '/translation-disclaimer-header-' + lang + '.md'
    with open(disclaimer_header_mdfile, encoding="utf-8") as f:
        marked_disclaimer_header = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    # Terms
    terms_csv = 'data/output/ltc-translations-termlist.csv'
    terms_df = pd.read_csv(terms_csv, encoding='utf-8')

    sssom_csv = 'data/output/ltc-sssom.csv'
    sssom_df = pd.read_csv(sssom_csv, encoding='utf-8')

    # Merge SSSOM Mappings with Terms
    terms_skos_df = pd.merge(
        terms_df, sssom_df[['compound_name', 'predicate_label', 'object_id', 'object_category', 'object_label',
                            'mapping_justification' ]],
        on=['compound_name'], how='left'
    )

    terms = terms_skos_df.sort_values(by=['class_name','term_local_name'])

    # Unique Class Names
    ltcCls = terms_df['class_name'].dropna().unique()

    # Terms by Class
    grpdict2 = terms_df.groupby('class_name')[['term_ns_name', 'term_local_name', 'namespace', 'compound_name','term_version_iri','term_modified']].apply(
        lambda g: list(map(tuple, g.values.tolist()))).to_dict()
    termsByClass = []

    for i in grpdict2:
        termsByClass.append({
            'class': i,
            'termlist': grpdict2[i]
        })

    return render_template('term-list.html',
                           headerMarkdown=Markup(marked_text),
                           ltcCls=ltcCls,
                           terms=terms,
                           sssom=sssom_df,
                           termsByClass=termsByClass,
                           uniqueTerms=terms,
                           pageTitle='Term List',
                           title=meta['title'],
                           acronym=meta['acronym'],
                           landingPage=meta['documentation-landing-page'],
                           githubRepo=meta['github-repo'],
                           slug='term-list',
                           languageCode=language_code,
                           languageLabel=language_label,
                           translationDisclaimer=Markup(marked_disclaimer),
                           translationDisclaimerHeader=Markup(marked_disclaimer_header)
                           )
# Terms Page (English)
@app.route('/terms/')
def terms():

    # Read translations YAML file
    language_code = 'en'
    language_label = ''
    header_mdfile = 'md/termlist-header.md'
    with open(header_mdfile, encoding="utf-8") as f:
        marked_text = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    disclaimer_header_mdfile = 'md/translation-disclaimer-header.md'
    with open(disclaimer_header_mdfile, encoding="utf-8") as f:
        marked_disclaimer_header = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    disclaimer_mdfile = 'md/translation-disclaimer.md'
    with open(disclaimer_mdfile, encoding="utf-8") as f:
        marked_disclaimer = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    # Terms
    terms_csv = 'data/output/ltc-termlist.csv'
    terms_df = pd.read_csv(terms_csv, encoding='utf-8')

    sssom_csv = 'data/output/ltc-sssom.csv'
    sssom_df = pd.read_csv(sssom_csv, encoding='utf-8')

    # Merge SSSOM Mappings with Terms
    terms_skos_df = pd.merge(
        terms_df, sssom_df[['compound_name', 'predicate_label', 'object_id', 'object_category', 'object_label', 'mapping_justification' ]],
        on=['compound_name'], how='left'
    )

    terms = terms_skos_df.sort_values(by=['class_name','term_local_name'])

    # Unique Class Names
    ltcCls = terms_df['class_name'].dropna().unique()

    # Terms by Class
    grpdict2 = terms_df.groupby('class_name')[['term_ns_name', 'term_local_name', 'namespace', 'compound_name','term_version_iri','term_modified']].apply(
        lambda g: list(map(tuple, g.values.tolist()))).to_dict()
    termsByClass = []

    for i in grpdict2:
        termsByClass.append({
            'class': i,
            'termlist': grpdict2[i]
        })

    return render_template('term-list.html',
                           headerMarkdown=Markup(marked_text),
                           ltcCls=ltcCls,
                           terms=terms,
                           sssom=sssom_df,
                           termsByClass=termsByClass,
                           uniqueTerms=terms,
                           pageTitle='Term List',
                           title=meta['title'],
                           acronym=meta['acronym'],
                           landingPage=meta['documentation-landing-page'],
                           githubRepo=meta['github-repo'],
                           slug='term-list',
                           languageCode=language_code,
                           languageLabel=language_label,
                           translationDisclaimer=Markup(marked_disclaimer),
                           translationDisclaimerHeader=Markup(marked_disclaimer_header)
                           )

@app.route('/quick-reference/')
def quickReference():
    header_mdfile = 'md/quick-reference-header.md'
    with open(header_mdfile, encoding="utf8") as f:
        marked_text = markdown2.markdown(f.read())

    # Quick Reference Main
    df = pd.read_csv('data/output/ltc-termlist.csv', encoding='utf8')
    df['examples'] = df['examples'].str.replace(r'"', '')
    df['definition'] = df['definition'].str.replace(r'"', '')
    df['usage'] = df['usage'].str.replace(r'"', '')
    df['notes'] = df['notes'].str.replace(r'"', '')

    # Group by Class
    grpdict = df.fillna(-1).groupby('class_name')[['namespace', 'term_local_name', 'label', 'definition',
                                                   'usage', 'notes', 'examples', 'rdf_type', 'class_name',
                                                   'is_required', 'is_repeatable', 'compound_name',
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


@app.route('/resources/')
def docResources():
    header_mdfile = 'md/resources-header.md'
    with open(header_mdfile, encoding="utf8") as f:
        marked_text = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    sssom_mdfile = 'md/sssom-reference.md'
    with open(sssom_mdfile, encoding="utf8") as f:
        marked_sssom = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    return render_template('resources.html',
                           headerMarkdown=Markup(marked_text),
                           sssomRefMarkdown=Markup(marked_sssom),
                           pageTitle='Resources',
                           title=meta['title'],
                           acronym=meta['acronym'],
                           landingPage=meta['documentation-landing-page'],
                           githubRepo=meta['github-repo'],
                           slug='resources'
    )



if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(port=8000)