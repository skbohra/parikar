from .celery import app

from main.models import Parik

'''
@app.task
def extract_keywords_bert(*args,**kwargs):
    kw_model = KeyBERT()
    parik = kwargs['parik']
    doc = parik.content
    keywords = kw_model.extract_keywords(doc)
    parik.bert_keywords = keywords
    parik.save()
'''
