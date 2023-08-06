PYMEX package is a collection of modules providing tools for accessing interaction
data distributed by The IMEx Consortium partners as well as for parsing, transformation
and construction of PSI-MI endorsed interaction data files.
=======
Modules
=======

- `pymex.xmlrecord` - A generic, configurable XML record serializer/deserializer. 
- `pymex.mif` - PSI-MI XML format support (versions 2.5.4 and 3.0.0). 
- `pymex.pypsiq` - PSICQUC server access.

===========
Quick Start
===========

    from lxml import etree as ET
    import pymex.mif


