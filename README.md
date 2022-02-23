# ELG API for Finto AI Open API

The docker container built from this repo acts as a proxy container which routes 
[ELG](https://european-language-grid.readthedocs.io/en/stable/all/A3_API/LTInternalAPI.html) 
compatible requests to [finto.ai](https://api.annif.org/v1/ui/) open API 
and returns ELG compatible response.

The Finto API responds with subject suggestions for a given text. It is 
based on [Annif](http://annif.org/) developed mainly at the National 
Library of Finland. Annif is an automated subject indexing toolkit with 
Apache license 2.0. This ELG proxy is published under the same license.

This ELG API was developed in EU's CEF project: 
[Microservices at your service](https://www.lingsoft.fi/en/microservices-at-your-service-bridging-gap-between-nlp-research-and-industry)

## Local development

Setup virtualenv, dependencies
```
python3 -m venv finto-venv
source finto-venv/bin/activate
python3 -m pip install -r requirements.txt
```
Run the development mode flask app

```
FLASK_ENV=development flask run --host 0.0.0.0 --port 8000
```

## Unit testing for utils.py that handle proxy API
````
python3 -m unittest  -v
````

## Building the docker image

```
docker build -t finto-ai:elg .
```

Or pull directly ready-made image `docker pull lingsoft/finto-ai:tagname`.

## Deploying the service

```
docker run -d -p <port>:8000 --init finto-ai:elg
```

## Example call

```
curl -H "Content-Type: application/json" -d @text-request.json http://localhost:8000/process
```

### Text request

```json
{
    "type": "text",
    "params": {"limit": 2, "project_id": "yso-fi"},
    "content": "Finto AI ehdottaa tekstille sopivia aiheita. Palvelu perustuu Annif-työkaluun."
}
```

The `content` property contains text, `params` property is optional and 
can be used to control number of limit indexes return, threshold on score 
of result return and project_id.

- `project-id` (str, default = `yso-fi`)
  - currently Finto AI supports 3 project-id: `yso-fi`, `yso-en` and `yso-sv`, information about these project can be queried by 
  ```
  curl -X GET --header 'Accept: application/json' 'https://ai.finto.fi/v1/projects'
  ```

- `limit` (int, default = 5)
  - maximum number of subjects to return

- `threshold` (float, default = 0)
  - minimum score threshold, below which results will not be returned

### Response

```json
{
  "response": {
    "type": "texts",
    "texts": [
      {
        "role": "alternative",
        "content": "palvelut",
        "score": 0.25875118374824524,
        "features": {
          "notation": null,
          "uri": "http://www.yso.fi/onto/yso/p838"
        }
      },
      {
        "role": "alternative",
        "content": "suunnittelu",
        "score": 0.0792069360613823,
        "features": {
          "notation": null,
          "uri": "http://www.yso.fi/onto/yso/p1377"
        }
      }
    ]
  }
}
```

- `content`
  - the subject label of given content from sent request
- `score` (float)
  - confidence score of the indexed subject
- `notation` (str)
  - notation of the indexed subject, for example "42.42"
- `uri` (str)
  - link to Finto ontology
