---

^### Frictionless Data, Frictionless Development

---

^### What is data management about?

![Cloudstuff](cloud.jpeg)

---

^### How do we address these problems?

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

^### But NumPy and Pandas have data schemata which can be exported via the datashape project

^### Or we can just use SQL for everything...
---

^### You can interpolate all these data formats using odo 
^### You can view things in my jupyter dashboard or via the rosetta install
^### install
:smiley: datascientist
:confused: Scientists in data-immature disciplines
:confused: Data curators
:confused: HR, Marketing etc
---

* Enterprise architecture didn't just go away because we invented the data science buzzword. 
* If we like to say data is everywhere let's help all the stakholders...

---
^### OK, enough chat, let's build an end-to-end tool using frictionless data

---
^### Imaginary Brief

Research how styles of railway poster have changed over time

* Download data and images
* Do some preprocessing
* Run some deep learning over them to dimension reduce the style and find patterns
* Present the results in a ui allowing update of tags
* Save the updates
* Make the updates available again in a standardised format

---

^### Which of the frictionless data tools and standards are we going to use?

* Datapackages-pipelines - declarative flow control
* Tableschema-py - to infer the schema and validate new data
* Tabulator - a common interface for import and export
* Standards - datapackages, json table schema (also json-patch)
* Other interoperable tools along the way

---

^### Goal is to extend the frictionless data tools so we can write a pipeline that looks like this:

    science-museum-posters:
      title: Posters from the Science Museum augmented with image similarity 
      description: Metadata about posters - locations and images
      pipeline:
        -
          run: add_metadata
          parameters:
            name: 'science-museum'
            title: 'Posters from the Science Museum augmented with image similarity'
            homepage: 'https://collection.sciencemuseum.org.uk/'
        -
          run: add_resource
          parameters:
            url:
            jsonapi+https://collection.sciencemuseum.org.uk/search/categories/railway%20posters,%20notices%20&%20handbills
            name: smjsondata
            pathtojsonlist: data
        - 
          run: stream_remote_resources
          parameters:
            resources: ['smjsondata']
        -
          run: apply_jsonpatch
          parameters:
            resources: 'smjsondata'
            target: 'smtabulardata'
        - 
          run: download_images
          parameters:
            resources: 'smtabulardata'
            target: local_images_list
        - 
          run: generate_tsne_plot
          parameters:
            source: local_images_list
            target: results_stream
---

^### OK so where do we start?

---

^### Get tabular data from a jsonapi source

---
^### Intro to tabulator-py

* Tabulator-py is the successor project to "messytables"
* A library for reading and writing tabular data (csv/xls/json/etc).
* Reads data from local, remote, stream or text sources
* Custom loaders, parsers and writers
---
^### Interface

    from tabulator import Stream

    with Stream('http://my-url/path.csv', headers=1) as stream:
        stream.headers # [header1, header2, ..]
            for row in stream:
                    row  # [value1, value2, ..]

* The (custom) parser used is set by changing the format parameter and passing in a class
    with Stream(
        "http://source_uri", 
        custom_parsers={'json-api': CustomParser}
        format="json-api"
        ) as stream:
        
        stream.read()
---

^### What do we want our custom parser to do? Let's write a test...

+++?code=smdataproject/tests/test_stream.py&lang=python

@[14] 
@[17-18] 
@[22-26] 

