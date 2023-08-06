import logging
import muheqa.summary.summarizer as sm
import muheqa.evidence.discoverer as ds
import muheqa.answer.composer as cp


class Connection:

	def __init__(self, wikidata=True,dbpedia=False,d4c=False):
		self.logger = logging.getLogger('muheqa')
		self.logger.debug("initializing MuHeQA ...")
		self.summarizer = sm.Summarizer()
		self.discoverer = ds.Discoverer()
		self.composer   = cp.Composer()
		self.wikidata  = wikidata
		self.dbpedia    = dbpedia
		self.d4c        = d4c 

	def query(self,question,max_answers=1,max_resources=3,by_name=True,by_properties=True,by_description=True):
		self.logger.debug("Question: " + question)
		sentences = self.summarizer.get_sentences(question,max_resources,self.wikidata,self.dbpedia,self.d4c,by_name,by_properties,by_description)
		if (len(sentences) == 0):
			self.logger.warn("no summary created")
			return sentences
		evidences = self.discoverer.get_evidences(question,sentences,max_answers)
		self.logger.debug("Evidences: " + str(evidences))
		answers   = self.composer.get_answers(question,evidences,max_answers)
		self.logger.debug("Answers: " + str(answers))
		return answers

