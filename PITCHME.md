---

#### Frictionless Data, Frictionless Development

---

#### What is data / document management about?

![Cloudstuff](cloud.jpg)

---
#### Means many things to many people
---

#### As a data scientist I want:
* Reproducible analyses
* Flexibility to work with legacy scripts
* Test-driven data science
* Seamless package management for disparate data sources
---
#### As a developer I additionally want:
* Architectural guidance
* Polygot persistence
* Ability to swap out tools
* Single point of responsibility for each module
---
#### As an ops person I also want
* Declarative tools that are easy to containerise
* Streaming data for low memory usage
* Consistent data formats across varied customers
* A tool appropriate for the data sizes involved (<1M rows per collection)
---
#### What is Zegami and why are Zegami interested in Frictionless data?
* Zegami makes visual information more accesible for exploration, search and discovery
* Zegami allows data scientists to validate machine learning models visually
* Zegami works on top of any tabular data format
---
#### Who are Zegami's users?
* People managment - HR and Schools
* Data scientists
* Museum curators
* Scientists
---
#### As an evangelist for Zegami I want:
* Interoperability with customer datastores
* To do the right thing - open source, open standards
* Standards that work for both end and CLI tools
* CLI usability for non-coders
---

* Frictionless data provides cross-platform ways of describing and using datasets
    * Data package management
    * Building blocks for data
        * import
        * validation
        * processing
        * export
        * display
        * apis
---
#### <a href="http://frictionlessdata.io/tools/" target="_blank">frictionlessdata.io/tools/</a>

---
* The community is great, pull requests are merged quickly
* When you are struggling with a data model for a task or a schema, frictionless data's standards provide guidance
* Frictionless data does for me as a data engineer what djangopackages does for me as a web developer

---
#### For example:
* <a href="http://frictionlessdata.io/tools/#mira" target="_blank">Mira - A web api for csv datasets</a>
* <a href="https://github.com/frictionlessdata/datapackage-pipelines#join" target="_blank">How to model a join in a database </a>

---
#### OK, enough chat, let's build an end-to-end tool using frictionless data

---
#### Imaginary Brief

* Research how styles of railway posters from the National Railway Museum collection have changed over time

---
#### Tasks

* Download and preprocess data and images
* Run some deep learning to find patterns
* Present the results in a ui allowing update of tags
* Make the updates available again in a standardised format

---

#### Which of the frictionless data tools and standards?

* <a href="http://okfnlabs.org/blog/2017/02/27/datapackage-pipelines.html" target="_blank">Datapackage-pipelines</a> - declarative flow control
* <a href="https://github.com/frictionlessdata/tableschema-py" target="_blank">Tableschema-py</a> - to infer the schema and validate new data
* <a href="https://github.com/frictionlessdata/tabulator-py" target="_blank">Tabulator</a> - a common interface for import and export of tabular data
* Standards - <a href="http://frictionlessdata.io/data-packages/" target="_blank">datapackages</a>, <a href="http://dataprotocols.readthedocs.io/en/latest/json-table-schema.html" target="_blank">json table schema</a>,  <a href="https://github.com/frictionlessdata/datapackage-pipelines" target="_blank"> datapackage-pipeline</a> spec
* Other interoperable tools along the way

---
#### OK so where do we start?

---

#### Get tabular data from a jsonapi source

---
#### Intro to tabulator-py

* Tabulator-py is the successor project to "messytables"
* A library for reading and writing tabular data (csv/xls/json/etc).
* Reads data from local, remote, stream or text sources
* Custom loaders, parsers and writers
---
#### Interface

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

#### What do we want our custom parser to do? 

* Let's write a test...

+++?code=smdataproject/tests/test_parser.py&lang=python

@[17](Test data url (see below))
@[20-21](Pass in our custom parser) 
@[25-29](Check we get a single item json out in the correct format)

+++

#### Test data

* Hosted on github because we don't want to patch http or hammer external API

+++?code=data/smdatasetpagenumber0&lang=json

@[546](Changed the next link to test pagination)

+++

* Let's make that pass
* Use the [https://github.com/frictionlessdata/tabulator-py/blob/563e3cc9355e456d2da309990ad8b8354b4ce180/tabulator/parsers/json.py](tabulator json parser) as a template.

+++?code=smdataproject/jsonapi_parser.py&lang=python

@[68](Add a pagination loop)
@[73](Set the startng row number on each iteration)
@[83-89](Get the next page url and load in data for next loop)
@[90-91](Break out of the loop if no next link)

---

#### Make the parser support normalisation

* We would like to convert the json to an array of the desired fields
* tabulator.Stream is already using ijson parser 
* This has support for iterating keys in json
* We can pass in a schema which encodes the exact json normalisation desired

---

#### Which fields do we want and what are they called in ijson language?

* Parse the json and print a field list, for example:

+++?code=smdataproject/generate_field_list.py&lang=python

+++?code=data/fieldlist.yaml&lang=yaml

* Examples:

@[40-41](The id)
@[460-461](The title/name of the poster)

---

#### Now we know what we are aiming for we can write a test

+++?code=smdataproject/tests/test_normalising_parser.py&lang=python

@[42-58](Added the schema with our ijson paths)
@[68](Pass the schema into the new parser)
@[71-118](Cheat with the assertion by first printing stuff until it looks right...)

---

#### Make a few assumptions based on what I have needed over the years

---

* The high level data array required is still passed separately to the parser
* We always want to parse single values of type string, number or boolean
* Where those values are repeated due to lists or lists of dicts, concatenate them

---

#### The end result

+++?code=smdataproject/normalising_parser.py&lang=python

@[65-87](Use ijson to iterate json in an event-driven way)

* Similar to native Java JSON Object building
* Ask me about this afterwards if you want to know more

---

* Now need to download images in a piepline after we get the data
* Need a pipeline spec yaml file

+++?code=smdataproject/pipeline-spec.yaml&lang=yaml

@[1-10](Add some metadata)
@[12-15](Add the data package arguments)
@[53-56](Custom job to download the data)
@[56-62](Custom job to download the images)

---
* Simple custom job stream_remote_resources_custom

+++?code=smdataproject/stream_remote_resources_custom.py&lang=python
@[3](Monkey-path the custom module)

---
* Another custom job for download_images
* This time we need to edit the data and add an image field
+++?code=smdataproject/download_images.py&lang=python
@[11-20](Initially we update the datapackage to include a local field name)


