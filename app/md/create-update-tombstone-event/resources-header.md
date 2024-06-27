# Create Update Delete Tombstone Resources (In Progress)
This page contains an assortment of resources to help explain the structure and relationship of the Create Update Tombstone Event object.
The Create Update Tombstone Event data model is based on the W3C PROV model and is used to track the history of an object in the DiSSCo infrastructure.
Within each object (Agent, Activity, Entity) are properties which indicate the relationship to each-other.
For example the Entity has a property `wasGeneratedBy` which indicates the Activity that generated the Entity.
While the serialisation is in json it follows semantic approach of the model and it should be relatively easy to serialise it to RDF. 
![Alt text](https://www.w3.org/TR/prov-o/diagrams/starting-points.svg "The W3C PROV model")

Note that we don't use the [PROV-JSON Serilization proposal](https://www.w3.org/submissions/prov-json/) as it has been stale for a long time.
We also feel that it overcomplicated the model especially for the relatively simple use case we have in DiSSCo.
