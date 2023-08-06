import muheqa.connector as mhqa

wikidata = mhqa.connect(wikidata=True)
question = "Who is the father of Barack Obama"
response = wikidata.query(question)
print("Query:",question)
print("Response:",response)