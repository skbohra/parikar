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



@app.task
def hackernews_bot(*args,**kwargs):
    url = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
    username = "hacker_news_bot"
    user = User.objects.get(username=username)
    api_response = requests.get(url)
    if api_response.status == 200:
        posts = api_response.json()
        for post in posts.items():
            post_url = "https://hacker-news.firebaseio.com/v0/item/%d.json?print=pretty" % post
            post_response = requests.get(post_url)
            data['url']  = url
            try:
                instant_parik = InstantParik.objects.get(user=user,url=url)
                downloaded = trafilatura.fetch_url(url)
                text = trafilatura.extract(downloaded,include_comments=False)
                try:
                    metadata = trafilatura.extract_metadata(downloaded)
                    title = metadata.title
                except:
                    metadata = None
                    title = url

            except InstantParik.DoesNotExist:
                instant_parik = InstantParik(user=user,url=url,content=text,description=url,tags="",title=title)
                instant_parik.save()
                animation = Animation.objects.get(pk=1)
    
                parik = Parik(title=title,user=request.user,content=text,description=url,tags="",created_on=datetime.datetime.now(),to_wrap=True,animation=animation,shuffle_colors_by_line=True,shuffle_fonts_by_line=True)
                parik.save()
                instant.is_user_saved = True
                instant.parik = parik
                instant.save()


             





 
