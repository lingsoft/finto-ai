import utils
from elg import FlaskService
from elg.model import Failure, TextsResponse, TextRequest
from elg.model.base import StandardMessages


class Finto(FlaskService):
    def process_text(self, request: TextRequest):
        text = request.content
        project_id = 'yso-fi'
        limit = 5
        threshold = 0

        if request.params:
            project_id = request.params.get('project_id', project_id)
            limit = request.params.get('limit', limit)
            threshold = request.params.get('threshold', threshold)
        try:
            res = utils.handle_text(project_id, text, limit, threshold)
        except Exception as err:
            detail = {'server error': str(err)}
            error = StandardMessages.generate_elg_service_internalerror(
                detail=detail)
            return Failure(errors=[error])
        return TextsResponse(texts=res)


flask_service = Finto("finto")
app = flask_service.app
