from .models import Font,FontColor
#from keybert import KeyBERT

def get_random_font():
    font = Font.objects.order_by('?').first()
    return font.font_name

def get_random_color():
    font_color = FontColor.objects.order_by('?').first()
    return font_color.hexcode

'''
def extract_keywords_bert(text):
    kw_model = KeyBERT()
    keywords = kw_model.extract_keywords(text)
    return keywords
'''
