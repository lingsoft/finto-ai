import requests
from elg.model import TextsResponseObject
import json

base_url = 'https://ai.finto.fi/v1/projects/'
def handle_text(project_id, text, limit, threshold):
  
  payload = {'text': text, 'limit': limit, 'threshold': threshold}
  res = requests.post(f'{base_url}{project_id}/suggest', data=payload)
  data = res.json()
  texts = [ {'role': 'alternative', 'content': obj['label'], 'score': obj['score'],
          'features': {k:v for k,v in obj.items() if k != 'label' and k!= 'score'} } 
          for obj in data['results'] ]
  return TextsResponseObject(texts=texts)
