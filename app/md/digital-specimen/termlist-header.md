# Digital Specimen List of Terms (In Progress)

**Title**
: Digital Specimen List of Terms

**Date version issued**
: 2024-06-17

**Date created**
: 2024-06-17

**This version**
: 0.3.0

**Latest version**
: 0.3.0

**Abstract**
: The Digital Specimen object is the core object within the DiSSCo infrastructure.
It contains all information relevant to the Digital Specimen.
The Digital Specimen object itself is connected to a range of other objects such as Identifiers, Citations or Events.
Most of these other objects are optional and have a one-to-many relationship with the Digital Specimen.
This makes the Digital Specimen very flexible.
The basis for the structure of the Digital Specimen object has been made in the [GBIF UM](https://www.gbif.org/composition/HjlTr705BctcnaZkcjRJq/gbif-new-data-model) as well as the [Darwin Core TDWG standard](https://dwc.tdwg.org/terms/).

**Main contributors**
: [Sam Leeflang](https://orcid.org/0000-0002-5669-2769), [Soulaine Theocharides](https://orcid.org/0000-0001-7573-4330), [Tom Dijkema](https://orcid.org/0000-0001-9790-9277), [Wouter Addink](https://orcid.org/0000-0002-3090-1761), [Sharif Islam](https://orcid.org/0000-0001-8050-0299), [Claus Weiland](https://orcid.org/0000-0003-0351-6523), [Jonas Grieb](https://orcid.org/0000-0002-8876-1722), [David Fichtmüller](https://orcid.org/0000-0002-0829-5849)

**Creator**
: Distributed Infrastructure for Scientific Collections (DiSSCo)

**Bibliographic citation**
: Distributed Infrastructure for Scientific Collections. 2024. Digital Specimen List of Terms.

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
However, the DigitalSpecimen and the Digital Entity are more complex objects.
They can contain classes as nested object in itself.
In general, class names are capitalized, use the UpperCamelCase naming convention and are singular.
For example, the class that represents a Digital Specimen is called `DigitalSpecimen`.
The properties of a class start with a lowercase and use the lowerCamelCase naming convention.
When a class contains a property which contains a list of another class we use the convention `hasXXX` where XXX is the class name.
For example, the DigitalSpecimen can contain a list of Event objects, so it has a property called `hasEvent`.
When a class is directly nested (not through a list) we use the class name as property name.
For example, the Location class contains the property `ods:GeoReference` which contains the Geo Reference class.  

When terms are borrowed from other vocabularies, such as Darwin Core, Annotation Vocabulary, Schema.org or others, we use the same naming convention as in the original vocabulary.
This could conflict with the openDS vocabulary naming convention.

## 2 Borrowed Vocabulary <span id="2-borrowed-vocabulary"></span>
When terms are borrowed from other vocabularies, openDS uses the IRIs, common abbreviations, and namespace prefixes in use in those vocabularies. The IRIs are normative, but abbreviations and namespace prefixes have no impact except as an aid to reading the documentation.

Table 1. Vocabularies from which terms have been borrowed (non-normative)

| Vocabulary                                                                | Abbreviation | Namespaces and abbreviations                                               |
|---------------------------------------------------------------------------|--------------|----------------------------------------------------------------------------|
| [Darwin Core](https://dwc.tdwg.org/terms/)                                | DwC          | `dwc: = http://rs.tdwg.org/dwc/terms/`                                     
| [Darwin Core IRI Terms](https://dwc.tdwg.org/terms/)                      | DwC IRI      | `dwciri: = http://rs.tdwg.org/dwc/terms/`                                  
| [Darwin Core Chronometric Age Vocabulary](https://tdwg.github.io/chrono/) | Chrono       | `chrono: = http://rs.tdwg.org/chrono/terms/`                               
| [Dublin Core](http://dublincore.org/documents/dcmi-terms/)                | DC           | `dcterms: = http://purl.org/dc/terms/`                                     |

## 3 Namespaces, Prefixes and Term Names <span id="3-namespace-prefixes-term-names"></span>
The namespace of terms borrowed from other vocabularies is that of the original. 
The namespace of de openDS terms is http://rs.dissco.eu/opends/terms/. In the table of terms, each term entry has a row with the term name. 
This term name is generally an “unqualified name” preceded by a widely accepted prefix designating an abbreviation for the namespace It is RECOMMENDED that implementers who need a namespace prefix for the openDS namespace use ods. 
In this web document, hovering over a term in the Index By Term Name list below will reveal a complete URL that can be used in other web documents to link to this document’s treatment of that term, even if it is from a borrowed vocabulary. 
