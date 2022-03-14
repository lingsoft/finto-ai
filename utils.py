import requests
from elg.model import TextsResponseObject

base_url = 'https://ai.finto.fi/v1/projects/'


def handle_text(project_id, text, limit, threshold):
    payload = {'text': text, 'limit': limit, 'threshold': threshold}
    res = requests.post(f'{base_url}{project_id}/suggest', data=payload)
    texts_response = []
    if res.ok:
        data = res.json()
        for obj in data["results"]:
            texts_response.append(
                TextsResponseObject(role='alternative',
                                    content=obj['label'],
                                    score=obj['score'],
                                    features={
                                        k: v
                                        for k, v in obj.items()
                                        if k != 'label' and k != 'score'
                                    }))
        return texts_response
    else:
        data = res.json()
        detail = data['detail']
        raise Exception(f'Error from internal call to finto.ai: {detail}')
