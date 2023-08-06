import logging


class QuestionClassifier:
    
    def __init__(self,resources_dir):
        self.logger = logging.getLogger('muheqa')
        self.logger.debug("initializing Question Classifier ...")
            
    def get_category(self,question):
        # category: boolean, literal or resource
        # type: date, number or string
        result_dict = {
            'question': question,
            'category': 'literal',
            'type': 'string'
        }       
        return result_dict
            