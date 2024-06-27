# Source System List of Terms (In Progress)

**Title**
: Source System List of Terms

**Date version issued**
: 2024-06-17

**Date created**
: 2024-06-17

**This version**
: 0.3.0

**Latest version**
: 0.3.0

**Abstract**
: The Source System object prodivdes information about the data providing system.
Most important is the endpoint of the system through which we can retrieve the data and the data standard that is being
used.
At the moment the software supports the data standards: Darwin Core Archive and BioCASe endpoints.
The Source System object points to the Mapping object which it uses to map the data correctly.

**Main contributors**
: [Sam Leeflang](https://orcid.org/0000-0002-5669-2769), [Soulaine Theocharides](https://orcid.org/0000-0001-7573-4330), [Tom Dijkema](https://orcid.org/0000-0001-9790-9277)

**Creator**
: Distributed Infrastructure for Scientific Collections (DiSSCo)

**Bibliographic citation**
: Distributed Infrastructure for Scientific Collections. 2024. Source System List of Terms.

## 1 Introduction <span id="1-introduction"></span>

### 1.1 Status of the content of this document <span id="11-status-of-the-content-of-this-document"></span>

The openDS data specification is in active development.
This document is work in progres and might change until version 1.0.0 is released.
Its main function at the moment is to inform the community about the current state of the data model and to gather
feedback.
We hope to include the feedback from the community and reach a first major version of the data model by the end of 2024.

### 1.2 RFC 2119 key words <span id="12-rfc-2119-key-words"></span>

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and
“OPTIONAL” in this document are to be interpreted as described in BCP 14 RFC 2119 and RFC 8174 when, and only when, they
appear in all capitals, as shown here.

## 2 Borrowed Vocabulary <span id="2-borrowed-vocabulary"></span>

When terms are borrowed from other vocabularies, openDS uses the IRIs, common abbreviations, and namespace prefixes in
use in those vocabularies. The IRIs are normative, but abbreviations and namespace prefixes have no impact except as an
aid to reading the documentation.

Table 1. Vocabularies from which terms have been borrowed (non-normative)

| Vocabulary                                  | Abbreviation | Namespaces and abbreviations                                               |
|---------------------------------------------|--------------|----------------------------------------------------------------------------| 
| [Latimer Core](https://ltc.tdwg.org/terms/) | LtC          | `lct: = 	http://rs.tdwg.org/ltc/terms/`                                    |
| [Schema.org](https://schema.org/)           | Schema       | `schema: =  https://schema.org/version/latest/schemaorg-current-https.rdf` | 

## 3 Namespaces, Prefixes and Term Names <span id="3-namespace-prefixes-term-names"></span>

The namespace of terms borrowed from other vocabularies is that of the original.
The namespace of de openDS terms is http://rs.dissco.eu/opends/terms/. In the table of terms, each term entry has a row
with the term name.
This term name is generally an “unqualified name” preceded by a widely accepted prefix designating an abbreviation for
the namespace It is RECOMMENDED that implementers who need a namespace prefix for the openDS namespace use ods.
In this web document, hovering over a term in the Index By Term Name list below will reveal a complete URL that can be
used in other web documents to link to this document’s treatment of that term, even if it is from a borrowed vocabulary. 
