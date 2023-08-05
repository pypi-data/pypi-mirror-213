from unittest import TestCase
from unittest.mock import MagicMock, Mock

from dnastack.http.authenticators.abstract import Authenticator
from dnastack.http.session import HttpSession, ClientError
from requests import Session


class TestHttpSession(TestCase):

    def test_submit_403_status_code(self):

        # Create a mock authenticator
        authenticator_mock = MagicMock(Authenticator)
        authenticator_mock.before_request.return_value = None
        authenticator_mock.session_id = 1

        # Create a mock response with status code 403
        response_mock = Mock()
        response_mock.status_code = 403
        response_mock.ok = False
        response_mock.text = "Test data"

        # Create a mock session
        session_mock = MagicMock(Session)
        session_mock.get.return_value = response_mock


        http_session = HttpSession(authenticators=[authenticator_mock], session=session_mock, suppress_error=False)
        with self.assertRaises(ClientError) as e:
            http_session.submit(method="get", url="http://example-url.com")
        self.assertEqual(e.exception.response.status_code, 403)
