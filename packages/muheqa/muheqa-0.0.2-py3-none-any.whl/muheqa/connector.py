import muheqa.connection as connection

def connect(wikidata=True,dbpedia=False,d4c=False):
	return connection.Connection(wikidata, dbpedia, d4c)