Multiple and Heterogeneous Question-Answering (MuHeQA) system

## Quick Start!

Install the `muheqa` package:
````python
pip install muheqa
````

Create a new connection to Wikidata, or DBpedia, or D4C (Drugs4Covid). *The first time it may take a few minutes to download the required models*:
````python
import muheqa.connector as mhqa

wikidata = mhqa.connect(wikidata=True)
````

And finally, make a question in natural language!:
````python
response = wikidata.query("Who is the father of Barack Obama")
print("Response:",response)
````



