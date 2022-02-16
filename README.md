
# ELG API for Finto AI Open API

The docker container built from this repo acts as a "proxy" container which routes [ELG](https://european-language-grid.readthedocs.io/en/stable/all/A3_API/LTInternalAPI.html) compatible requests to [finto.ai](https://api.annif.org/v1/ui/) open API and returns ELG compatible response.

The Finto API responds with subject suggestions for a given text. It is based on [Annif](http://annif.org/)
developed mainly at the National Library of Finland. Annif is an automated subject indexing toolkit which has Apache licence 2.0.

This ELG API was developed in EU's CEF project: [Microservices at your service](https://www.lingsoft.fi/en/microservices-at-your-service-bridging-gap-between-nlp-research-and-industry)

## Local development

Setup virtualenv, dependencies
```
python3 -m venv annif-venv
source annif-venv/bin/activate
python3 -m pip install -r requirements
```
Run the development mode flask app

```
FLASK_ENV=development flask run --host 0.0.0.0 --port 8000
```

## Building the docker image

```
docker build -t annif-elg .
```

## Deploying the service

```
docker run -d -p <port>:8000 --init --memory="512M" --cpus=0.5 --restart always annif-elg
```

## REST API

### Call pattern

#### URL

```
http://<host>:<port>/process
```

Replace `<host>` and `<port>` with the host name and port where the 
service is running.

#### HEADERS

```
Content-type : application/json
```

#### BODY

Text Request
```
{
"type":"text",
"params": // optional
"content": "text for subject indexing"
}

```

The `content` property contains texts, `params` property can be used to control number of limit indexes return, threshold on score of result return and project_id. For example:

```
"params": {"project_id": "yso-en", "limit": 2, "threshold": 0.02},
```

Default values of project-id is "yso-fi", limit is 2 and threshod is 0

<!-- Or structuredText Request
```json
{
"type":"structuredText",
"texts": [
    {
      "content": "first content",
      "features": // optional
    },
    {
      "content": "second content",
      "features": // optional
    }
  ]
}
``` -->

The `texts` property contains list of content objects, each object has required property `content` and optional `features` property which is used to control `project_id` and `limit` as stated in Text Request body's `params` property.

#### RESPONSE

```json
{
  "response":{
    "type":"texts",
    "texts":[
      {
        "texts": [
          {
            "content": "label of first subject",
            "features": {
            "label": "label of first subject",
            "notation": null,
            "score": "float",
            "uri": "url of subject from corresponding project_id used"
            }
          },
          {
            "content": "label of second subject ",
            "features": {
            "label": "label of second subject",
            "notation": null,
            "score": "float",
            "uri": "url of subject from corresponding project_id used"
            }
          },
        ]
      }
    ]
  }
}
```


### Response structure

- `content` and `label` (str)
  - the subject label of given content from sent request
- `score` (float)
  - confidence score of the indexed subject
- `notation` (str)
  - notaion of the indexed subject, for example "42.42"

### Optional parameters in body request

In text request, placed below parameters object as value of 'params' property. 
<!-- In structured text request, place below parameters as value of `features` property of each content object of `texts` property, if needs. -->
- `project-id` (str)
  - currently Finto AI supports 3 project-id: `yso-fi`, `yso-en` and `yso-sv`, information about these project can be queried by 
  ```
  curl -X GET --header 'Accept: application/json' 'https://ai.finto.fi/v1/projects'
  ```

- `limit` (int)
  - maximum number of subjects to return

- `threshold` (float)
  - minimum score threshold, below which results will not be returned


### Example Text Request call

Text Request
```
curl --location --request POST 'http://localhost:8000/process' \
--header 'Content-Type: application/json' \
--data-raw '{
"type":"text",
"params":{"limit": 2, "project_id": "yso-fi"},
"content": "Koneoppiminen on tekoälyn osa-alue, jonka tarkoituksena on saada ohjelmisto toimimaan entistä paremmin pohjatiedon ja mahdollisen käyttäjän toiminnan perusteella"
}'
```

### Response should be

```json
{
  "response": {
    "type": "texts",
    "texts": [
      {
        "texts": [
          {
            "role": "alternative",
            "content": "teko\u00e4ly",
            "score": 0.474902480840683,
            "features": {
              "notation": null,
              "uri": "http://www.yso.fi/onto/yso/p2616"
            }
          },
          {
            "role": "alternative",
            "content": "koneoppiminen",
            "score": 0.2404150515794754,
            "features": {
              "notation": null,
              "uri": "http://www.yso.fi/onto/yso/p21846"
            }
          }
        ]
      }
    ]
  }
}
```


<!-- ### Example Structured Text Request call

Structured Text Request
```
curl --location --request POST 'http://localhost:8000/process' \
--header 'Content-Type: application/json' \
--data-raw '{
"type":"structuredText",
"texts": [
    {
    "content": "Koneoppiminen on tekoälyn osa-alue, jonka tarkoituksena on saada ohjelmisto toimimaan entistä paremmin pohjatiedon ja mahdollisen käyttäjän toiminnan perusteella",
    "features": {"limit": 2, "project_id": "yso-fi"}
    },
    {
    "content": "Machine learning (ML) is the study of computer algorithms that can improve automatically through experience and by the use of data",
    "features": {"limit": 2, "project_id": "yso-en"}
    }
    ]
}'
``` 

### Response should be

```json
{
    "response": {
        "type": "texts",
        "texts": [
            {
                "texts": [
                    {
                        "content": "tekoäly",
                        "features": {
                            "label": "tekoäly",
                            "notation": null,
                            "score": 0.474902480840683,
                            "uri": "http://www.yso.fi/onto/yso/p2616"
                        }
                    },
                    {
                        "content": "koneoppiminen",
                        "features": {
                            "label": "koneoppiminen",
                            "notation": null,
                            "score": 0.2404150515794754,
                            "uri": "http://www.yso.fi/onto/yso/p21846"
                        }
                    }
                ]
            },
            {
                "texts": [
                    {
                        "content": "algorithms",
                        "features": {
                            "label": "algorithms",
                            "notation": null,
                            "score": 0.5066971778869629,
                            "uri": "http://www.yso.fi/onto/yso/p14524"
                        }
                    },
                    {
                        "content": "machine learning",
                        "features": {
                            "label": "machine learning",
                            "notation": null,
                            "score": 0.43361249566078186,
                            "uri": "http://www.yso.fi/onto/yso/p21846"
                        }
                    }
                ]
            }
        ]
    }
}
``` -->
