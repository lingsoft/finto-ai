from elg.model import TextsResponseObject
import unittest
import requests
from utils import handle_text

class TestResponseStucture(unittest.TestCase):
    project_url = 'https://ai.finto.fi/v1/projects'
    project_id = 'yso-fi'
    text = 'Finto AI ehdottaa tekstille sopivia aiheita. Palvelu perustuu Annif-työkaluun.'
    limit = 2
    threshold = 0

    def test_finto_ai_api_response_status_code(self):
        """Should return status code 200, otherwise proxy api will not work
        """

        status_code = requests.get(self.project_url).status_code
        self.assertEqual(status_code, 200)

    def test_handle_text_util_type_return(self):
        """Given four required paramteres:
        project_id. text and limit, threhold
        Function handle_text should return a list"""

        response = handle_text(self.project_id, self.text, self.limit, self.threshold)
        self.assertIsInstance(response, list)
    
    def test_handle_text_util_content_return(self):
        """Given four required paramteres:
        project_id. text and limit, threhold
        Function handle_text should return a list of objects, each object
        should have TextsResponseObject type"""

        response = handle_text(self.project_id, self.text, self.limit, self.threshold)
        for res in response:
            self.assertIsInstance(res, TextsResponseObject)
            self.assertEqual(res.role, 'alternative')
            
    def test_handle_text_util_inner_level_return(self):
        """Given four required paramteres:
        project_id. text and limit, threhold
        TextsResponseObject from handle_text util should contain
        four required properties"""
        
        response = handle_text(self.project_id, self.text, self.limit, self.threshold)
        for res in response:
            for prop in ['role', 'content', 'score', 'features']:
                self.assertIn(prop, res.__dict__.keys())


if __name__ == '__main__':
    unittest.main()