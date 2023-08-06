import muheqa.connector as mhqa

kb = mhqa.connect(dbpedia=True)
question = "Who is the father of Barack Obama"
response = kb.query(question)
print("Query:",question)
print("Response:",response)