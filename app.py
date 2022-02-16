import utils
from elg import FlaskService
from elg.model import Failure
from elg.model import TextsResponse, TextRequest, StructuredTextRequest
from elg.model.base import StandardMessages


class Annif(FlaskService):

    def process_text(self, request: TextRequest):

        text = request.content
        project_id = 'yso-fi'
        limit = 10
        threshold = 0
        
        if request.params:
            project_id = request.params.get('project_id', 'yso-fi')
            limit = request.params.get('limit', 2)
            threshold = request.params.get('threshold', 0)
        try:
            res = utils.handle_text(project_id, text, limit, threshold)
        except Exception as err:
          detail = {'server error': str(err) }
          error = StandardMessages.generate_elg_service_internalerror(detail=detail)
          return Failure(errors=[error])
        return TextsResponse(texts=[res])

    # def process_structured_text(self, request: StructuredTextRequest):
      
    #     texts = request.texts
    #     res = []
    #     try:
    #       for i, text in enumerate(texts):
    #           project_id, limit, threshold = 'yso-fi', 2, 0
    #           content = text.content
    #           if text.features:
    #             project_id = text.features.get('project_id', 'yso-fi')
    #             limit = text.features.get('limit', 2)
    #             threshold = text.features.get('threshold', 0)
    #           res.append(utils.handle_text(project_id, content, limit, threshold))
    #     except Exception as err:
    #       detail = {'server error': str(err) }
    #       error = StandardMessages.generate_elg_service_internalerror(detail=detail)
    #       return Failure(errors=[error])
    #     return TextsResponse(texts=res)


flask_service = Annif("annif")
app = flask_service.app
