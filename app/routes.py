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


@app.route('/digital-specimen-terms')
def digitalSpecimenTerms():
    header_mdfile = 'app/md/digital-specimen/termlist-header.md'
    term_file = 'app/data/opends/digital-specimen-termlist.csv'

    marked_text, opends_classes, sssom_df, terms, terms_by_class = generate_terms(header_mdfile, term_file)

    return render_template('termlist.html',
                           headerMarkdown=Markup(marked_text),
                           ltcCls=opends_classes,
                           terms=terms,
                           sssom=sssom_df,
                           termsByClass=terms_by_class,
                           pageTitle='Digital Specimen Terms',
                           title='Digital Specimen Term List',
                           slug='digital-specimen-term-list'
                           )


@app.route('/machine-annotation-service-terms')
def machineAnnotationServiceTerms():
    header_mdfile = 'app/md/machine-annotation-service/termlist-header.md'
    term_file = 'app/data/opends/machine-annotation-service-termlist.csv'

    marked_text, opends_classes, sssom_df, terms, terms_by_class = generate_terms(header_mdfile, term_file)

    return render_template('termlist.html',
                           headerMarkdown=Markup(marked_text),
                           ltcCls=opends_classes,
                           terms=terms,
                           sssom=sssom_df,
                           termsByClass=terms_by_class,
                           pageTitle='Machine Annotation Service Terms',
                           title='Machine Annotation Service Term List',
                           slug='machine-annotation-service-term-list'
                           )


@app.route('/digital-media-terms')
def digitalMediaTerms():
    header_mdfile = 'app/md/digital-media/termlist-header.md'
    term_file = 'app/data/opends/digital-media-termlist.csv'

    marked_text, opends_classes, sssom_df, terms, terms_by_class = generate_terms(header_mdfile, term_file)

    return render_template('termlist.html',
                           headerMarkdown=Markup(marked_text),
                           ltcCls=opends_classes,
                           terms=terms,
                           sssom=sssom_df,
                           termsByClass=terms_by_class,
                           pageTitle='Digital Media Term',
                           title='Digital Media Term List',
                           slug='digital-media-term-list'
                           )


@app.route('/annotation-terms')
def annotationTerms():
    header_mdfile = 'app/md/annotation/termlist-header.md'
    term_file = 'app/data/opends/annotation-termlist.csv'

    marked_text, opends_classes, sssom_df, terms, terms_by_class = generate_terms(header_mdfile, term_file)

    return render_template('termlist.html',
                           headerMarkdown=Markup(marked_text),
                           ltcCls=opends_classes,
                           terms=terms,
                           sssom=sssom_df,
                           termsByClass=terms_by_class,
                           pageTitle='Annotation Term',
                           title='Annotation Term List',
                           slug='annotation-term-list'
                           )


@app.route('/create-update-tombstone-event-terms')
def createUpdateTombstoneEventTerms():
    header_mdfile = 'app/md/create-update-tombstone-event/termlist-header.md'
    term_file = 'app/data/opends/create-update-tombstone-event-termlist.csv'

    marked_text, opends_classes, sssom_df, terms, terms_by_class = generate_terms(header_mdfile, term_file)

    return render_template('termlist.html',
                           headerMarkdown=Markup(marked_text),
                           ltcCls=opends_classes,
                           terms=terms,
                           sssom=sssom_df,
                           termsByClass=terms_by_class,
                           pageTitle='Create Update Tombstone Event Term',
                           title='Create Update Tombstone Event Term List',
                           slug='create-update-tombstone-event-term-list'
                           )


@app.route('/data-mapping-terms')
def dataMappingTerms():
    header_mdfile = 'app/md/data-mapping/termlist-header.md'
    term_file = 'app/data/opends/data-mapping-termlist.csv'

    marked_text, opends_classes, sssom_df, terms, terms_by_class = generate_terms(header_mdfile, term_file)

    return render_template('termlist.html',
                           headerMarkdown=Markup(marked_text),
                           ltcCls=opends_classes,
                           terms=terms,
                           sssom=sssom_df,
                           termsByClass=terms_by_class,
                           pageTitle='Data Mapping Term',
                           title='Data Mapping Term List',
                           slug='data-mapping-term-list'
                           )


@app.route('/source-system-terms')
def sourceSystemTerms():
    header_mdfile = 'app/md/source-system/termlist-header.md'
    term_file = 'app/data/opends/source-system-termlist.csv'

    marked_text, opends_classes, sssom_df, terms, terms_by_class = generate_terms(header_mdfile, term_file)

    return render_template('termlist.html',
                           headerMarkdown=Markup(marked_text),
                           ltcCls=opends_classes,
                           terms=terms,
                           sssom=sssom_df,
                           termsByClass=terms_by_class,
                           pageTitle='Source System Term',
                           title='Source System Term List',
                           slug='source-system-term-list'
                           )


@app.route('/digital-specimen-guide')
def digitalSpecimenGuide():
    header_mdfile = 'app/md/digital-specimen/quick-reference-header.md'
    term_file = 'app/data/opends/digital-specimen-termlist.csv'
    grplists, marked_text, required_classes_df, required_df = generate_guide(header_mdfile, term_file)

    return render_template('quick-reference.html',
                           headerMarkdown=Markup(marked_text),
                           grplists=grplists,
                           pageTitle='Digital Specimen Quick Reference Guide ',
                           title='Digital Specimen Quick Reference',
                           slug='digital-specimen-guide',
                           requiredTerms=required_df,
                           requiredClasses=required_classes_df
                           )


@app.route('/digital-media-guide')
def digitalMediaGuide():
    header_mdfile = 'app/md/digital-media/quick-reference-header.md'
    term_file = 'app/data/opends/digital-media-termlist.csv'
    grplists, marked_text, required_classes_df, required_df = generate_guide(header_mdfile, term_file)

    return render_template('quick-reference.html',
                           headerMarkdown=Markup(marked_text),
                           grplists=grplists,
                           pageTitle='Digital Media Quick Reference Guide ',
                           title='Digital Media Quick Reference',
                           slug='digital-media-guide',
                           requiredTerms=required_df,
                           requiredClasses=required_classes_df
                           )


@app.route('/annotation-guide')
def annotationGuide():
    header_mdfile = 'app/md/annotation/quick-reference-header.md'
    term_file = 'app/data/opends/annotation-termlist.csv'
    grplists, marked_text, required_classes_df, required_df = generate_guide(header_mdfile, term_file)

    return render_template('quick-reference.html',
                           headerMarkdown=Markup(marked_text),
                           grplists=grplists,
                           pageTitle='Annotation Quick Reference Guide ',
                           title='Annotation Quick Reference',
                           slug='annotation-guide',
                           requiredTerms=required_df,
                           requiredClasses=required_classes_df
                           )


@app.route('/machine-annotation-service-guide')
def machineAnnotationServiceGuide():
    header_mdfile = 'app/md/machine-annotation-service/quick-reference-header.md'
    term_file = 'app/data/opends/machine-annotation-service-termlist.csv'
    grplists, marked_text, required_classes_df, required_df = generate_guide(header_mdfile, term_file)

    return render_template('quick-reference.html',
                           headerMarkdown=Markup(marked_text),
                           grplists=grplists,
                           pageTitle='Machine Annotation Service Quick Reference Guide ',
                           title='Machine Annotation Service Quick Reference',
                           slug='machine-annotation-service-guide',
                           requiredTerms=required_df,
                           requiredClasses=required_classes_df
                           )


@app.route('/create-update-tombstone-event-guide')
def createUpdateTombstoneGuide():
    header_mdfile = 'app/md/create-update-tombstone-event/quick-reference-header.md'
    term_file = 'app/data/opends/create-update-tombstone-event-termlist.csv'
    grplists, marked_text, required_classes_df, required_df = generate_guide(header_mdfile, term_file)

    return render_template('quick-reference.html',
                           headerMarkdown=Markup(marked_text),
                           grplists=grplists,
                           pageTitle='Create Update Tombstone Event Quick Reference Guide ',
                           title='Create Update Tombstone Event Quick Reference',
                           slug='create-update-tombstone-event-guide',
                           requiredTerms=required_df,
                           requiredClasses=required_classes_df
                           )


@app.route('/data-mapping-guide')
def dataMappingGuide():
    header_mdfile = 'app/md/data-mapping/quick-reference-header.md'
    term_file = 'app/data/opends/data-mapping-termlist.csv'
    grplists, marked_text, required_classes_df, required_df = generate_guide(header_mdfile, term_file)

    return render_template('quick-reference.html',
                           headerMarkdown=Markup(marked_text),
                           grplists=grplists,
                           pageTitle='Data Mapping Quick Reference Guide ',
                           title='Data Mapping Quick Reference',
                           slug='data-mapping-guide',
                           requiredTerms=required_df,
                           requiredClasses=required_classes_df
                           )


@app.route('/source-system-guide')
def sourceSystemGuide():
    header_mdfile = 'app/md/source-system/quick-reference-header.md'
    term_file = 'app/data/opends/source-system-termlist.csv'
    grplists, marked_text, required_classes_df, required_df = generate_guide(header_mdfile, term_file)

    return render_template('quick-reference.html',
                           headerMarkdown=Markup(marked_text),
                           grplists=grplists,
                           pageTitle='Source System Quick Reference Guide ',
                           title='Source System Quick Reference',
                           slug='source-system-event-guide',
                           requiredTerms=required_df,
                           requiredClasses=required_classes_df
                           )


@app.route('/digital-specimen-resources')
def digitalSpecimenResources():
    file_prefix = 'digital-specimen'
    header_mdfile = 'app/md/digital-specimen/resources-header.md'
    with open(header_mdfile, encoding="utf8") as f:
        marked_text = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    sssom_mdfile = 'app/md/opends/sssom-reference.md'
    with open(sssom_mdfile, encoding="utf8") as f:
        marked_sssom = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    class_diagram = retrieve_diagram('class-diagrams', file_prefix)
    er_diagram = retrieve_diagram('er-diagrams', file_prefix)

    return render_template('resources.html',
                           headerMarkdown=Markup(marked_text),
                           sssomRefMarkdown=Markup(marked_sssom),
                           pageTitle='Digital Specimen Core Resources ',
                           classDiagram=class_diagram,
                           erDiagram=er_diagram,
                           title='Digital Specimen Resources',
                           slug='digital-specimen-resources'
                           )


@app.route('/digital-media-resources')
def digitalMediaResources():
    file_prefix = 'digital-media'
    header_mdfile = 'app/md/digital-media/resources-header.md'
    with open(header_mdfile, encoding="utf8") as f:
        marked_text = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    sssom_mdfile = 'app/md/opends/sssom-reference.md'
    with open(sssom_mdfile, encoding="utf8") as f:
        marked_sssom = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    class_diagram = retrieve_diagram('class-diagrams', file_prefix)
    er_diagram = retrieve_diagram('er-diagrams', file_prefix)

    return render_template('resources.html',
                           headerMarkdown=Markup(marked_text),
                           sssomRefMarkdown=Markup(marked_sssom),
                           pageTitle='Digital Media Core Resources ',
                           classDiagram=class_diagram,
                           erDiagram=er_diagram,
                           title='Digital Media Resources',
                           slug='digital-media-resources'
                           )


@app.route('/annotation-resources')
def annotationResources():
    file_prefix = 'annotation'
    header_mdfile = 'app/md/annotation/resources-header.md'
    with open(header_mdfile, encoding="utf8") as f:
        marked_text = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    sssom_mdfile = 'app/md/opends/sssom-reference.md'
    with open(sssom_mdfile, encoding="utf8") as f:
        marked_sssom = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    class_diagram = retrieve_diagram('class-diagrams', file_prefix)
    er_diagram = retrieve_diagram('er-diagrams', file_prefix)

    return render_template('resources.html',
                           headerMarkdown=Markup(marked_text),
                           sssomRefMarkdown=Markup(marked_sssom),
                           pageTitle='Annotation Core Resources ',
                           classDiagram=class_diagram,
                           erDiagram=er_diagram,
                           title='Annotation Resources',
                           slug='annotation-resources'
                           )


@app.route('/create-update-tombstone-event-resources')
def createUpdateTombstoneEventResources():
    file_prefix = 'create-update-tombstone-event'
    header_mdfile = 'app/md/create-update-tombstone-event/resources-header.md'
    with open(header_mdfile, encoding="utf8") as f:
        marked_text = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    sssom_mdfile = 'app/md/opends/sssom-reference.md'
    with open(sssom_mdfile, encoding="utf8") as f:
        marked_sssom = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    class_diagram = retrieve_diagram('class-diagrams', file_prefix)
    er_diagram = retrieve_diagram('er-diagrams', file_prefix)

    return render_template('resources.html',
                           headerMarkdown=Markup(marked_text),
                           sssomRefMarkdown=Markup(marked_sssom),
                           pageTitle='Create Update Tombstone Event Resources ',
                           classDiagram=class_diagram,
                           erDiagram=er_diagram,
                           title='Create Update Tombstone Event Resources',
                           slug='create-update-tombstone-event-resources'
                           )


@app.route('/machine-annotation-service-resources')
def machineAnnotationServiceResources():
    file_prefix = 'machine-annotation-service'
    header_mdfile = 'app/md/machine-annotation-service/resources-header.md'
    with open(header_mdfile, encoding="utf8") as f:
        marked_text = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    sssom_mdfile = 'app/md/opends/sssom-reference.md'
    with open(sssom_mdfile, encoding="utf8") as f:
        marked_sssom = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    class_diagram = retrieve_diagram('class-diagrams', file_prefix)
    er_diagram = retrieve_diagram('er-diagrams', file_prefix)

    return render_template('resources.html',
                           headerMarkdown=Markup(marked_text),
                           sssomRefMarkdown=Markup(marked_sssom),
                           pageTitle='Machine Annotation Service Resources ',
                           classDiagram=class_diagram,
                           erDiagram=er_diagram,
                           title='Machine Annotation Service Resources',
                           slug='machine-annotation-service-resources'
                           )


@app.route('/data-mapping-resources')
def dataMappingResources():
    file_prefix = 'data-mapping'
    header_mdfile = 'app/md/data-mapping/resources-header.md'
    with open(header_mdfile, encoding="utf8") as f:
        marked_text = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    sssom_mdfile = 'app/md/opends/sssom-reference.md'
    with open(sssom_mdfile, encoding="utf8") as f:
        marked_sssom = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    class_diagram = retrieve_diagram('class-diagrams', file_prefix)
    er_diagram = retrieve_diagram('er-diagrams', file_prefix)

    return render_template('resources.html',
                           headerMarkdown=Markup(marked_text),
                           sssomRefMarkdown=Markup(marked_sssom),
                           pageTitle='Mapping Resources ',
                           classDiagram=class_diagram,
                           erDiagram=er_diagram,
                           title='Mapping Resources',
                           slug='data-mapping-resources'
                           )


@app.route('/source-system-resources')
def sourceSystemResources():
    file_prefix = 'source-system'
    header_mdfile = 'app/md/source-system/resources-header.md'
    with open(header_mdfile, encoding="utf8") as f:
        marked_text = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    sssom_mdfile = 'app/md/opends/sssom-reference.md'
    with open(sssom_mdfile, encoding="utf8") as f:
        marked_sssom = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    class_diagram = retrieve_diagram('class-diagrams', file_prefix)
    er_diagram = retrieve_diagram('er-diagrams', file_prefix)

    return render_template('resources.html',
                           headerMarkdown=Markup(marked_text),
                           sssomRefMarkdown=Markup(marked_sssom),
                           pageTitle='Source System Resources ',
                           classDiagram=class_diagram,
                           erDiagram=er_diagram,
                           title='Source System Resources',
                           slug='source-system-resources'
                           )


def generate_terms(header_mdfile, term_file):
    with open(header_mdfile, encoding="utf8") as f:
        marked_text = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])
    # Terms
    terms_csv = term_file
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
    return marked_text, opends_classes, sssom_df, terms, terms_by_class


def generate_guide(header_mdfile, term_file):
    with open(header_mdfile, encoding="utf8") as f:
        marked_text = markdown2.markdown(f.read())
    # Quick Reference Main
    df = pd.read_csv(term_file, encoding='utf8')
    df['examples'] = df['examples'].str.replace(r'"', '')
    df['definition'] = df['definition'].str.replace(r'"', '')

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
    return grplists, marked_text, required_classes_df, required_df


def retrieve_diagram(diagram_type, file_prefix):
    diagram_file = f'app/templates/includes/resources/diagrams/{diagram_type}/{file_prefix}-full.html'
    with open(diagram_file, encoding="utf8") as f:
        diagram = f.read()
    return diagram
