### Frictionless data presentation

#### Installation

    git clone --recurse-submodules https://github.com/strets123/frictionless-pres
    cd frictionless-pres
    conda create -n dpp theano tensorflow keras pillow pandas scikit-learn
    source activate dpp
    pip install datapackage-pipelines
    cd smdataproject
    
#### Running dpp

You must be in the smdataproject directory to run the pipelines as they depend on each-other

    cd smdataproject
    
    dpp
    
At this point you should see the output like this
    
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

