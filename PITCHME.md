---

#### Frictionless Data, Frictionless Development

---

#### What is data management about?

![Cloudstuff](cloud.jpg)
+++

* As a data scientist I want:
    * Reproducible analyses
    * Reusable, modular code
    * Test-driven data science
+++
* As a developer I additionally want:
    * Architectural guidance
    * Polygot persistence
    * Ability to swap out tools
+++
* As an ops person I also want
    * Declarative tools that are easy to containerise
    * Streaming data for low memory usage
    * Consisten data formats across varied customers
---
* Who are Zegami's users?
    * People managment - HR and Schools
    * Data scientists
    * Museum curators
    * Scientists
+++
* As an evangelist for Zegami I want:
    * Interoperability with customer datastores
    * To do the right thing - open source, open standards
    * Different user levels
        * Standards should work in the front end too

---

* Frictionless data provides cross-platform ways of describing and using datasets
    * Easier to switch tools
    * Building blocks for
        * import
        * validation
        * processing
        * export
        * display
        * apis
---
#### <a href="http://frictionlessdata.io/tools/" target="_blank">frictionlessdata.io/tools/</a>

+++

---
* When you are struggling with a data model for a task or a schema, frictionless data's standards provide guidance

---
#### OK, enough chat, let's build an end-to-end tool using frictionless data

---
#### Imaginary Brief

Research how styles of railway poster have changed over time

* Download and preprocess data and images
* Run some deep learning to find patterns
* Present the results in a ui allowing update of tags
* Make the updates available again in a standardised format

---

#### Which of the frictionless data tools and standards?

* Datapackage-pipelines - declarative flow control
* Tableschema-py - to infer the schema and validate new data
* Tabulator - a common interface for import and export
* Standards - datapackages, json table schema (also json-patch)
* Other interoperable tools along the way

---

#### Goal is to extend the frictionless data tools so we can write a pipeline that looks like this:



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

@[14](Test data url (see below))
@[17-18](Pass in our custom parser) 
@[22-26](Check we get a single item json out in the correct format)

+++

#### Test data

* Hosted on github because we don't want to patch http or hammer external API

+++?code=data/smdataset?page[number]=0&lang=javascript

@[546](Changed the next link to test pagination)

* Let's make that pass
* Use the [](tabulator json parser) as a template

+++?code=smdataproject/parser.py&lang=python

@[66](Add a pagination loop)
@[73](Set the startng row number on each iteration)
@[85-91](Get the next page url and load in data for next loop)
@[92-93](Break out of the loop if no next link)

---

#### Make the parser support normalisation

* We would like to convert the json to an array of the desired fields
* tabulator.Stream is already using ijson parser 
* This has support for iterating keys in json
* We can pass in a schema which encodes the exact json normalisation desired

---

#### Which fields to we want and what are they called in ijson language

* Parse the json and print a field list, for example:

+++?code=smdataproject/generate_field_list.py&lang=python

+++?code=data/fieldlist.txt

* Examples:

@[40-41](The id)
@[460-461](The title/name of the poster)

---

#### Now we know what we are aiming for we can write a test

+++?code=smdataproject/tests/test_normalising_parser.py&lang=python

@[35-46](Added the schema with our ijson paths)
@[55](Pass the schema into the new parser)
@[58-113](Cheat with the assertion by first printing stuff until it looks right...)

---

#### Make a few assumptions based on what I have needed over the years

---

* The high level data array required is still passed separately to the parser
* We always want to parse single values of type string, number or boolean
* Where those values are repeated due to lists or lists of dicts, concatenate them
* Any logic needed can be done on the normalised data afterwards

---

#### The end result

+++?code=smdataproject/normalising_parser.py&lang=python







---

#### But NumPy and Pandas have data schemata which can be exported via the datashape project

#### Or we can just use SQL for everything...
---

#### You can interpolate all these data formats using odo 
#### You can view things in my jupyter dashboard or via the rosetta install
#### install
:smiley: datascientist
:confused: Scientists in data-immature disciplines
:confused: Data curators
:confused: HR, Marketing etc
---

* Enterprise architecture didn't just go away because we invented the data science buzzword. 
* If we like to say data is everywhere let's help all the stakholders...







