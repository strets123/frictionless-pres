---

# Frictionless Data, Frictionless Development

---

# What is data management about?

![Cloudstuff](cloud.jpeg)

---

# How do we address these problems?

* Tools
* Standards
* (Processes)

---

* What stakeholders do our tools and standards need to cater for?

pic - BI people, data generators (e.g. lab scientists, logistics people, data curators) data scientists, academics
But also the even less technical people:
HR people, Marketing people

---

* How should our tools be architected?

vendor platforms vs microservices vs mvp tools that do one things well vs sacrificing accesability for flexibility vs setting
up academic comittees to devise a long boring and unusable standard

---

* Frictionless data aims to bridge these disperate fields to provide cross-platform ways of describing and using datasets
* When a bespoke tool is needed, frictionless data provides some great building blocks across the stack to help with
* import, validation, processing, export and display
* When you are struggling with a data model for a task or a schema, frictionless data's standards provide guidance
frictionless data picture
---

# But NumPy and Pandas have data schemata which can be exported via the datashape project

# Or we can just use SQL for everything...
---

# You can interpolate all these data formats using odo 
# You can view things in my jupyter dashboard or via the rosetta install
# install
:smiley: datascientist
:confused: Scientists in data-immature disciplines
:confused: Data curators
:confused: HR, Marketing etc
---

* Enterprise architecture didn't just go away because we invented the data science buzzword. 
* If we like to say data is everywhere let's help all the stakholders...

---
# OK, enough chat, let's build an end-to-end tool using frictionless data

---
# Imaginary Brief

Research how styles of railway poster have changed over time

* Download data and images
* Do some preprocessing
* Run some deep learning over them to dimension reduce the style and find patterns
* Present the results in a ui allowing update of tags
* Save the updates
* Make the updates available again in a standardised format

---

# Which of the frictionless data tools and standards are we going to use?

* Datapackages-pipelines - declarative flow control
* Tableschema-py - to infer the schema and validate new data
* Tabulator - a common interface for import and export
* Standards - datapackages and json table schema
* Other interoperable tools along the way

---

# OK, let's get started...

---

# Download data and images

The dataset is in the JSON-API format and available from:

https://collection.sciencemuseum.org.uk/search/categories/railway%20posters,%20notices%20&%20handbills?page[number]=1
---


