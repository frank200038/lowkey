# Lowkey enhanced with Multi-view capacity

# Repo structure
- [/lowkey](./lowkey) - Main project.
  -  [/collabtypes](./lowkey/collabtypes) - Type system for [collaborative modeling](#Metamodeling).
  -  [/lww](./lowkey/lww) - Low-level [CRDT system](#CRDT-specifications).
  -  [/network](./lowkey/network) - ZeroMQ-based distributed [network infrastructure](#Architecture-and-patterns).
- [/lowkey-examples](./lowkey-examples) - Examples.

# Setup guide
- Clone this repository.
- Install requirements via ```pip install -r requirements.txt```.
- Install the framework as an editable local package via ```pip install -e [path_to_the_project]```. (Use ```pip uninstall lowkey``` if not needed anymore.)
- To run an example included in the repository, please refer to README file present in each example located in [/lowkey-examples](./lowkey-examples).

# References

## Metamodeling

<img src="https://raw.githubusercontent.com/david-istvan/collabserver-modeling/main/docs/modelverse.PNG?raw=true"/>

Source: [Van Mierlo, Barroca, Vangheluwe, Syriani, Kühne. Multi-Level Modelling in the Modelverse. Proceedings of MULTI 2014.](http://miso.es/multi/2014/proceedings_MULTI.pdf#page=89)


## CRDT specifications

[Shapiro M, Preguiça N, Baquero C, Zawirski M. A comprehensive study of convergent and commutative replicated data types (Doctoral dissertation, Inria–Centre Paris-Rocquencourt; INRIA)](https://hal.inria.fr/file/index/docid/555588/filename/techreport.pdf)

## Network architecture and patterns

<img src="https://raw.githubusercontent.com/david-istvan/collabserver-modeling/main/docs/zmq_pattern.PNG?raw=true"/>

Source: [ZMQ: Reliable Pub-Sub with Update republishing](https://zguide.zeromq.org/docs/chapter5/#Republishing-Updates-from-Clients)

## Multi-view Modeling
Source: [Cicchetti A, Ciccozzi F, Pierantonio A. Multi-view approaches for software and system modelling: A systematic suvery. Software & Systems Modeling 2019:18](https://link.springer.com/content/pdf/10.1007/s10270-018-00713-w.pdf)

Further pointers:
* [Ephemeral values](https://zguide.zeromq.org/docs/chapter5/#Ephemeral-Values)
* [Reactor](https://zguide.zeromq.org/docs/chapter5/#Using-a-Reactor)

## Command language
* ```CREATE -name [name] -typedBy [type] [-attributeName [value]]*```
* ```LINK -from [fromClabject].[associationName] -to [toClabject] [-attributeName [value]]*```
* ```UPDATE (-name [name] | -id [id]) [-attributeName [newValue]]*```
* `CREATEVIEWPOINT -typedBy [type] -viewPointName [ViewPointName] -types {[Types]}`
* `APPLYVIEW -name [ViewName] -applyOn [EntityName] -viewPoint [ViewPointName]`
* ~~```DELETE (-name {name} | -id {id})```~~ (Not currently supported, but will be in the future)