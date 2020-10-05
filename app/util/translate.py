from os import environ
import requests
import json


def translate(text, source_language, dest_language):
    auth = {'Ocp-Apim-Subscription-Key': environ.get('MICROSOFT_TRANSLATE_KEY'),
            'Ocp-Apim-Subscription-Region': environ.get('MICROSOFT_TRANSLATE_REGION')}
    r = requests.post('https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&from={}&to={}'.format(source_language, dest_language),
                      headers=auth,
                      json=[{'text': text}])
    if r.status_code != 200:
        return 'Error: the translation service failed'
    return json.loads(r.content.decode('utf-8-sig'))[0]['translations'][0]['text']


