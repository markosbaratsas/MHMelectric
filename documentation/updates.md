# Introduction
This file intends to describe the changes implemented in the documentation of MHMelectric project.

# Changes

### SRS - StRS documents
There were not major changes in the documentation regarding the SRS and StRS documents, since they describe an ideal and abstract version of our software project.
We implemented a simplified version, consisting of two use cases: `Payment & Charging` and `Publishing of Periodic Bill`. Regarding those, here are the omitted functionalities:
1. `Payment & Charging`: in the ideal scenario, car owners would be able to search for nearby charging stations and corresponding charge programs on map and select the most convenient one.
2. `Publishing of Periodic Bill`: ideally, users would be notified by email everytime a new periodic bill is published, with a link to the implemented web app page showing periodic bills in detail. There, they could choose between a variety of payment methods. In the implemented version, there is no notification via emal and it is assumed that by pressing the Pay button, users would be redirected to a safe environment of payment supported by Third Party Payment System.
    
### UML diagrams
There were changes concerning only the Entity Relantionship and the Class diagram. The first versions were conducted before the beginning of the develompent of our software project, during which modifications arised intending to better adjust to the actual implementation. The initial version of the diagrams is included in the Vpp project named MHMelectric-old.vpp, as the updated one in MHMelectric.vpp.