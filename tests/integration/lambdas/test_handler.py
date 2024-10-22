from unittest                           import TestCase
from unittest.mock                      import patch
from starlette.testclient               import TestClient
from cbr_user_session.lambdas.handler   import main, app
from cbr_user_session.utils.Version     import version__cbr_user_session

class test_handler(TestCase):

    @classmethod
    def setUp(cls):
        cls.client = TestClient(app)

    def test_ping(self):
        response = self.client.get("/info/ping")
        assert response.json() == {'pong': '42'}

    def test_version(self):
        response = self.client.get("/info/version")
        assert response.json() == {'version': version__cbr_user_session}

    def test_docs(self):
        response = self.client.get("/docs")
        assert response.status_code == 200
        assert "swagger-ui"         in response.text

    def test_openapi(self):
        response = self.client.get("/openapi.json")
        assert response.status_code            == 200
        assert response.json().get("openapi")  == '3.1.0'

    @patch("cbr_user_session.lambdas.handler.uvicorn.run")
    def test_uvicorn_run(self, mock_uvicorn_run):                                   # Call the main function, which should now trigger uvicorn.run.
        main()
        mock_uvicorn_run.assert_called_once_with(app, host="0.0.0.0", port=8080)    # Check if uvicorn.run was called with the expected arguments.