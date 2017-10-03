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
* New tools that work with legacy scripts
* Test-driven data science
---
#### As a developer I want to:
* Get more out of python iterators
* Ability to swap out languages and databases
* Single point of responsibility for each module
---
#### As an ops person I want
* Declarative tools that are easy to containerise
* Streaming data for low memory usage
* Consistent data formats across varied customers
---
#### What is Zegami and why are Zegami interested in Frictionless data?

---?image=assets/Pic-1.jpg

---?image=assets/Pic-2.jpg

---?image=assets/Pic-3.jpg

---?image=assets/Pic-5.jpg

---?image=assets/Pic-11.jpg

---
#### As an evangelist for Zegami I want:
* Interoperability with customer datastores
* To do the right thing - open source, open standards
* Standards that work for both front-end and CLI tools
---
#### What is Frictionless Data?

![Frictionless Data](http://frictionlessdata.io/img/data-package-decouple.png)

---

#### OK, I learn best by doing

---
#### Let's test out these Frictionless Data tools

---

* Research how styles of railway posters from the National Railway Museum collection have changed over time

---
#### Tasks

* Download and preprocess data and images
* Run some deep learning to find patterns
* Present the results in a ui allowing update of tags

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
* Custom loaders, parsers and writers supporting urls, streams, files and databases
---
#### Interface

* The (custom) parser used is set by changing the format parameter and passing in a class


```python   
    from tabulator import Stream
    
    
    with Stream(
        "http://source_uri", 
        custom_parsers={'json-api': CustomParser}
        format="json-api"
        ) as stream:
        
        for array in stream.read():
            process(array)
```
---

##### What do we want our custom parser to do? 

* Let's write a test, source code [here](https://github.com/strets123/frictionless-pres/blob/master/smdataproject/tests/test_parser.py).

```python
    def test_stream(self):
        with tabulator.Stream(
            self.url,
            format="json-api", 
            custom_parsers={     
                "json-api": jsonapi_parser.JSONAPIParser
                },
            property='data',
            ) as stream:
```   
---          
##### Check we get a single item json out in the correct format
```python
            for index, item in enumerate(stream):
                self.assertTrue(isinstance(item[0], dict))
                self.assertIn("attributes", item[0])
                self.assertIn("id", item[0])
                self.assertIn("links", item[0])
                self.assertEqual(len(item), 1)
```

---

#### Test data

* Hosted on github because we don't want to patch http or hammer external API

---?code=data/smdatasetpagenumber0&lang=json

@[546](Changed the next link to test pagination)

---

* Let's make that pass
* Use the <a href="https://github.com/frictionlessdata/tabulator-py/blob/563e3cc9355e456d2da309990ad8b8354b4ce180/tabulator/parsers/json.py" target="_blank">tabulator json parser</a> as a template.
---

* We need to change the way that the iterator of `tabulator.Stream` yields results
* This is done by editing the `_iter_extended_rows` function
---
* Original function looks like this:
```python
    def __iter_extended_rows(self):
        path = 'item'
        if self.__property is not None:
            path = '%s.item' % self.__property
        items = ijson.items(self.__chars, path)
        for row_number, item in enumerate(items, start=1):
            if isinstance(item, (tuple, list)):
                yield (row_number, None, list(item))
            elif isinstance(item, dict):
                keys = []
                values = []
                for key in sorted(item.keys()):
                    keys.append(key)
                    values.append(item[key])
                yield (row_number, list(keys), list(values))
            else:
                if not self.__force_parse:
                    message = 'JSON item has to be list or dict'
                    raise exceptions.SourceError(message)
                yield (row_number, None, [])
```

---
* Add a pagination loop

```python
        start_rownum = 1
        while True:
            path = 'item'
            if self.__property is not None:
                path = '%s.item' % self.__property
```

---

* Get the next page of data and continue looping
```python
            json_obj = ijson.items(self.__chars,'')
            for k in json_obj:
                next_url = k["links"]["next"]
                break                                 # Get the next url
            if next_url is not None:
                self.__chars = self.__loader.load(    # Get more data
                next_url, 
                encoding=self.__encoding)
                self.__chars.seek(0)
            else:
                break # Break out of the loop if no next link
```
---

#### Make the parser support normalisation

* We would like to convert the json to an array of the desired fields
* tabulator.Stream is already using ijson parser 
* We can use this to walk through the json structure and flatten the keys

---

#### Which fields do we want and what are they called in ijson language?

* Parse the json and print a field list, for example:

---?code=smdataproject/generate_field_list.py&lang=python

---?code=data/fieldlist.yaml&lang=yaml

@[5-6](The id)
@[561-562](The title/name of the poster)

---
* I then created a [test](https://github.com/strets123/frictionless-pres/blob/master/smdataproject/tests/test_normalising_parser.py) and a [parser](https://github.com/strets123/frictionless-pres/blob/master/smdataproject/normalising_parser.py) which can accept ijson paths

---
#### Let's run this parser with datapackage-pipelines

* Also need to download images in a pipeline after we get the data
* To use datapackage-pipelines we need a `pipeline-spec.yaml` file
* For more info on the spec, see [documentation](https://github.com/frictionlessdata/datapackage-pipelines)

---?code=smdataproject/pipeline-spec.yaml&lang=yaml

@[1-10](Add some metadata)
@[12-15](Add the data package arguments)
@[53-56](Custom job to download the data)
@[56-62](Custom job to download the images)

---
* Simple custom job stream_remote_resources_custom

---?code=smdataproject/stream_remote_resources_custom.py&lang=python
@[3](Need to contribute a better way to do this...)

---
* Another custom job for download_images
* This time we need to edit the data and add an image field

---?code=smdataproject/download_images.py&lang=python
@[11-20](Initially we update the datapackage to include a local field name)
---
# OK so let's run our first pipeline

---
We install the dependencies like this:
```bash
    git clone --recurse-submodules https://github.com/strets123/frictionless-pres
    cd frictionless-pres
    conda create -n dpp theano tensorflow keras pillow pandas scikit-learn
    source activate dpp
    pip install datapackage-pipelines
    cd smdataproject
```

    
---

I use the datapackage-pipelines cli (dpp) to view the pipelines (in smdataproject directory)
```bash
    dpp
    
    Available Pipelines:
    INFO    :Main                            :Skipping redis connection, host:None, port:6379
    - ./science-museum-posters (*)
    - ./science-museum-feature-extract (E)
        Dirty dependency: Cannot run until all dependencies are executed
        Dependency unsuccessful: Cannot run until all dependencies are successfully executed
    - ./science-museum-join (E)
        Missing dependency: Couldn't open datapackage datapackage.json
    - ./science-museum-feature-tsne (E)
        Missing dependency: Failed to find a pipeline dependency
```
---
* To run the pipelines I use:

```bash
    dpp run ./science-museum-posters
```

---
Now for the deep learning step using pandas, tensorflow and keras with the resnet training dataset.

* Subrepo pandas code uses `read_csv` which is not streaming
* Create new pipelines which depend on the initial one


---?code=smdataproject/pipeline-spec.yaml&lang=yaml

@[65-69](Dump out the data)
@[71-85](Add a step to run feature extraction as a subprocess)
@[71-85](Add a step to run feature extraction as a subprocess)
@[86-98](Run the dimensionality reduction step to convert the feautres to a scatter plot)

---
#### Custom job to run a subprocess

---
+++?code=smdataproject/run_shell_command.py&lang=python
@[37-39](pass in the arguments from parameters)
@[16-23](Ensure subprocess output is logged)
@[6-8](Use logging module not print)

---
* For more on the deep learning scripts used see Zegami CTO Roger Noble's<a href="https://tech.zegami.com/comparing-pre-trained-deep-learning-models-for-feature-extraction-c617da54641" target="_blank">blog post here</a>

---
* The output from the dimensionality reduction looks like this:
* The x and y coordinates allow images to be clustered in a plane


    id,x,y
    1975-8398,18.7974,-14.4037
    2000-7803,3.64917,10.2163
    1977-5672,6.50948,21.1126

* We need to join this to our original dataset, we can do this with datapackages pipelines

---?code=smdataproject/pipeline-spec.yaml&lang=yaml

@[106-125](Tell datapackages-pipelines about the data we just created)
@[137-150](Join the datasets together - can be either a format string or a list)
@[152-155](Dump out the finished data)

---

#### And this is what the data looks like in [Zegami](https://demo.zegami.com/science%20museum%20railway%20posters)


---


#### Conclusions from the railway poster project

---
* The training data is from resnet - need a network trained on fonts and layout instead to study poster design
* Simply splitting the images by date in Zegami gives some interesting results

---
#### Conclusions after using frictionless data projects

---
* Tabulator has a great interface and is really flexible and well tested
* The datapackage pipelines spec is great, as is the CLI
* We have many ideas for how we would like to improve the underlying codebase and would love for others to join us working on it
---
#### OK so what else can the frictionless data tools do for me?

---

#### <a href="http://frictionlessdata.io/tools/" target="_blank">frictionlessdata.io/tools/</a>


---
#### Tableschema makes data transfer easy:
* <a href="https://github.com/frictionlessdata/tableschema-bigquery-py" target="_blank">Store in BigQuery</a>
* <a href="https://github.com/frictionlessdata/tableschema-pandas-py" target="_blank">Use in Pandas</a>
* <a href="https://github.com/frictionlessdata/tableschema-sql-py" target="_blank">Convert to SQL with tableschema sql</a>
* <a href="https://github.com/frictionlessdata/tableschema-elasticsearch-py" target="_blank">Create an elasticsearch index with tableschema-elasticsearch-py</a>
* <a href="https://github.com/frictionlessdata/tableschema-spss-py" target="_blank">Pull data from SPSS</a>
* Coming soon - go contribute : <a href="https://github.com/frictionlessdata/tableschema-ui" target="_blank">Edit your schemata with tableschema-ui</a>
---
####  Tableschema lets you switch languages
* Understand your data in <a href="https://github.com/frictionlessdata/tableschema-ui" target="_blank">Java
* Switch to <a href="https://github.com/frictionlessdata/tableschema-go"  target="_blank">Golang for a project
* Work with <a href="https://github.com/frictionlessdata/tableschema-rb"  target="_blank">Ruby</a>
* Coming soon: Clojure and R
---
#### Using the tableschema standard allows use of many repository owners' tools
* Repository management with <a href="https://ckan.org/features/" target="_blank">CKAN</a>
* Lighter weight repository managment with <a href="https://github.com/datahuborg/datahub" target="_blank">MIT's datahub</a>
* Update apis for the data from data packages with <a href="http://okfnlabs.org/blog/2014/09/11/data-api-for-data-packages-with-dpm-and-ckan.html" target="_blank">CKAN datastore</a>
* Data package distribution with <a href="http://okfnlabs.org/projects/dpm/" target="_blank">dpm</a>
---
#### Similar tools and standards

* [json_normalize](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.io.json.json_normalize.html) is part of the Pandas library and does a similar kind of json normalisation
* Trifacta Wrangler (successor to data wrangler) provides numerous methods for data wrangling and code generation
* [odo](http://odo.pydata.org/en/latest/) from continuum provides a similar interface to tabulator but the underlying [datashape](https://github.com/blaze/datashape/blob/master/docs/source/overview.rst) schema system is less extensible and more minimal.

---
#### Summary

* Frictionless data and OKFN have created some time-saving tools and standards
* The community is great, pull requests are merged quickly
* When you are struggling with a data model for a task or a schema, frictionless data's standards provide guidance
* Tools tend to be well balanced in terms to who has influenced their development

---

#### Acknowledgments

* Thanks to the team at Frictionless data / OKFN
* Thanks to the Science Museum and National Railways Museum for making the data available
* Thanks to the team at <a href="http://okfnlabs.org/blog/2017/02/27/datapackage-pipelines.html" target="_blank">Openspending for creating the datapackage pipelines project</a>
* To the team at Zegami (we are hiring) 
* To everyone for listening

---

#### Questions

* Sign up for beta access to Zegami cloud and API [here](https://zegami.com/cloud/)















