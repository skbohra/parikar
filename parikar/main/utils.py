from .models import Font,FontColor
#from keybert import KeyBERT

def get_random_font():
    font = Font.objects.order_by('?').first()
    return font.font_name

def get_random_color():
    font_color = FontColor.objects.order_by('?').first()
    return font_color.hexcode




import base64
import requests
import os

def stability_text_to_image(text,api_key):

    url = api_key.url

    body = {
      "steps": 40,
      "width": 512,
      "height": 512,
      "seed": 0,
      "cfg_scale": 5,
      "samples": 1,
      "style_preset": "cinematic",
      "text_prompts": [
        {
          "text": text,
          "weight": 1
        },
        {
          "text": "blurry, bad",
          "weight": -1
        }
      ],
    }

    headers = {
      "Accept": "application/json",
      "Content-Type": "application/json",
      "Authorization": "Bearer "+api_key.api_key,
    }

    response = requests.post(
      url,
      headers=headers,
      json=body,
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()

    return data 
    '''
    # make sure the out directory exists
    if not os.path.exists("./out"):
        os.makedirs("./out")

    for i, image in enumerate(data["artifacts"]):
        with open(f'./out/txt2img_{image["seed"]}.png', "wb") as f:
            f.write(base64.b64decode(image["base64"]))
    '''
