import os
import json
import muheqa.connector as mhqa

kb = mhqa.connect(dbpedia=True)

# assign directory
input_directory = '/Users/cbadenes/Library/CloudStorage/Dropbox/Trabajo/Carlos/Academic/DoctoradoIA/estancias/2023/Cardiff/plan_trabajo/dataset/questions'
output_directory = '/Users/cbadenes/Library/CloudStorage/Dropbox/Trabajo/Carlos/Academic/DoctoradoIA/estancias/2023/Cardiff/plan_trabajo/dataset/answers'

def answer_evidences(news):
    for annotation in news['annotation_values']:
        for value in annotation['5w1h_value']:
            question = value['kb_question_en']
            print(question)
            response = kb.query(question, max_answers=3)
            print(response)
            #d4c_response = d4c.query(question, max_answers=3)
            #print("D4C:", d4c_response)
            #kbs_response = kbs.query(question, max_answers=3)
            #value['kbs_response'] = kbs_response
    return news  



# iterate over files in that directory
counter = 1
for filename in os.listdir(input_directory):
    input_path = os.path.join(input_directory, filename)
    output_path = os.path.join(output_directory, filename)
    print("[",counter,"]",input_path)
    counter += 1
    # checking if it is a file
    if os.path.isfile(output_path):
        continue
    if os.path.isfile(input_path):                
        with open(input_path, "r") as jsonFile:
            data = json.load(jsonFile)
        annotated_news = answer_evidences(data)         