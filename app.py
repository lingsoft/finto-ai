from multiprocessing.sharedctypes import Value
import utils
from elg import FlaskService
from elg.model import Failure, TextsResponse, TextRequest
from elg.model.base import StandardMessages


class Finto(FlaskService):
    def process_text(self, request: TextRequest):
        text = request.content
        project_id = self.url_param('project_id')
        limit = 5
        threshold = 0

        if request.params:
            limit = request.params.get('limit', limit)
            try:
                limit = int(limit)
            except ValueError:
                invalid_type_msg = 'Submitted parameter limit is not a number'
                error = StandardMessages.generate_elg_service_internalerror(
                    params=[invalid_type_msg])
                return Failure(errors=[error])

            if limit < 0:
                err_msg = 'Submitted parameter limit is negative'

                error = StandardMessages.generate_elg_service_internalerror(
                    params=[err_msg])
                return Failure(errors=[error])
            threshold = request.params.get('threshold', threshold)
        try:
            res = utils.handle_text(project_id, text, limit, threshold)
        except Exception as err:
            error = StandardMessages.generate_elg_service_internalerror(
                params=[str(err)])
            return Failure(errors=[error])
        return TextsResponse(texts=res)


flask_service = Finto(name="finto", path="/process/<project_id>")
app = flask_service.app
