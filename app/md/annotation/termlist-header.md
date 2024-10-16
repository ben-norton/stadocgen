# Annotation List of Terms 

**Title**
: Annotation List of Terms

**Date version issued**
: 2024-10-15

**Date created**
: 2024-10-15

**This version**
: 0.4.0

**Latest version**
: 0.4.0

**Abstract**
: 
The data model for an Annotation within the DiSSCo infrastructure. This model is inspired by the W3C Web Annotation model. An annotation can be attached to any digital object in the DiSSCo infrastructure, and can contain any of the following motivations:

adding: The user wants to add new information to the object  
assessing: The user wants to assess the quality of the data in the object  
editing: The user wants to edit an existing value of the object  
commenting: The user wants to make a generic comment on the object  
deleting: The user wants to tombstone the object
There are several levels on which an annotation can be made:
The whole object: The annotation is made on the whole object, used when a user wants to create a comment on, for example, the whole Digital Specimen
A class: The annotation is made on the whole class, used when a user wants to add, for example, an additional Identification  
An individual property: The annotation is made on a specific property of the class, used when a user wants to edit a particular field, for example, the collector of a specimen  
A RegionOfInterest: The annotation is made on a specific region of the object. This type of annotation is mainly used when it is attached to a digital media object. For example, it can indicate a specific ROI in an image and attach a value to that ROI.  
The value of the annotation can be attached in the body. This can be in the form of an array of strings. When a full class is replaced, the body can contain the full new class in JSON format.  

The AggregateRating has not been implemented yet.

**Main contributors**
: [Sam Leeflang](https://orcid.org/0000-0002-5669-2769), [Soulaine Theocharides](https://orcid.org/0000-0001-7573-4330), [Tom Dijkema](https://orcid.org/0000-0001-9790-9277), [Sharif Islam](https://orcid.org/0000-0001-8050-0299)

**Creator**
: Distributed Infrastructure for Scientific Collections (DiSSCo)

**Bibliographic citation**
: Distributed Infrastructure for Scientific Collections. 2024. Annotation List of Terms.

## 1 Introduction <span id="1-introduction"></span>
### 1.1 Status of the content of this document <span id="11-status-of-the-content-of-this-document"></span>
The openDS data specification is in active development.
This document is work in progres and might change until version 1.0.0 is released.
Its main function at the moment is to inform the community about the current state of the data model and to gather feedback.
We hope to include the feedback from the community and reach a first major version of the data model by the end of 2024.

### 1.2 RFC 2119 key words <span id="12-rfc-2119-key-words"></span>
The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in BCP 14 RFC 2119 and RFC 8174 when, and only when, they appear in all capitals, as shown here.

### 1.3 Naming Convention <span id="13-categories-of-terms"></span>
This document contains all the terms in use the DiSSCo Digital Objects.
Most objects can be directly related to a openDS class, for example the Machine Annotation Service, or the Source System.
However, the Digital Specimen and the Digital Media are more complex objects.
They can contain classes as nested object in itself.
In general, class names are capitalized, use the UpperCamelCase naming convention and are singular.
For example, the class that represents a Digital Specimen is called `DigitalSpecimen`.
The properties of a class start with a lowercase and use the lowerCamelCase naming convention.
When a class contains a property which contains a list of another class we use the convention `hasXXXs` where XXX is the class name.
The properties name ends with an `s` to indicate that it is plural and contains an array of objects.
For example, the Digital Specimen can contain a list of Event objects, so it has a property called `hasEvents`.
When a class is directly nested (not through a list) we use the same `hasXXX` construction.
This name does not end with an `s` but is singular, indicating that it contains a single nested object.
For example, the Location class contains the property `hasGeoreference` which contains the Geo Reference class.   

When terms are borrowed from other vocabularies, such as Darwin Core, Annotation Vocabulary, Schema.org or others, we use the same naming convention as in the original vocabulary.
This could conflict with the openDS vocabulary naming convention.

## 2 Borrowed Vocabulary <span id="2-borrowed-vocabulary"></span>
When terms are borrowed from other vocabularies, openDS uses the IRIs, common abbreviations, and namespace prefixes in use in those vocabularies. The IRIs are normative, but abbreviations and namespace prefixes have no impact except as an aid to reading the documentation.

Table 1. Vocabularies from which terms have been borrowed (non-normative)

| Vocabulary                                                       | Abbreviation | Namespaces and abbreviations                                               |
|------------------------------------------------------------------|--------------|----------------------------------------------------------------------------| 
| [Dublin Core](http://dublincore.org/documents/dcmi-terms/)       | DC           | `dcterms: = http://purl.org/dc/terms/`                                     |
| [Schema.org](https://schema.org/)                                | Schema       | `schema: =  https://schema.org/version/latest/schemaorg-current-https.rdf` |
| [Resource Description Framework](https://www.w3.org/RDF/)         | RDF          | `rdf: = http://www.w3.org/1999/02/22-rdf-syntax-ns#`                       |
| [Web Annotation](https://www.w3.org/TR/annotation-vocab/)         | OA           | `oa: = http://www.w3.org/ns/oa#`                                           |
| [Activity Streams](https://www.w3.org/TR/activitystreams-vocabulary/) | AS         | `as: = https://www.w3.org/ns/activitystreams#`                             |


## 3 Namespaces, Prefixes and Term Names <span id="3-namespace-prefixes-term-names"></span>
The namespace of terms borrowed from other vocabularies is that of the original. 
The namespace of de openDS terms is http://rs.dissco.eu/opends/terms/. In the table of terms, each term entry has a row with the term name. 
This term name is generally an “unqualified name” preceded by a widely accepted prefix designating an abbreviation for the namespace It is RECOMMENDED that implementers who need a namespace prefix for the openDS namespace use ods. 
In this web document, hovering over a term in the Index By Term Name list below will reveal a complete URL that can be used in other web documents to link to this document’s treatment of that term, even if it is from a borrowed vocabulary. 
