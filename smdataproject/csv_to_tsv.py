from datapackage_pipelines.wrapper import ingest, spew
import pandas


def convert_to_tsv(resource):
    fn = resource + '/data/' + resource
    df = pandas.read_csv(fn + '.csv',
                         sep=',')
    df.to_csv(fn + '.tsv',  sep='\t')


parameters, datapackage, res_iter = ingest()

convert_to_tsv(
    parameters["resources"][0]
)

spew(datapackage, res_iter)
