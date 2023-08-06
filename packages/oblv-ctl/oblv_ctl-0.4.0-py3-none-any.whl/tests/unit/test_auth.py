import unittest
from unittest.mock import patch

from httpx import Response

from oblv_ctl.exceptions import AuthenticationError, BadRequestError, HTTPClientError, ParamValidationError
from oblv_ctl.models.http_validation_error import HTTPValidationError
from oblv_ctl.models.validation_error import ValidationError
from oblv_ctl.auth import authenticate
from oblv_ctl.oblv_client import OblvClient
from tests.unit.constants import (
    API_GW_REQUEST_ID,
    BAD_REQUEST_MESSAGE,
    EXCEPTION_OCCURED,
    KEY_APIGW_REQUESTID,
    KEY_MESSAGE,
    KEY_VALID_ERROR_LOC,
    USER_ID,
    USER_TOKEN,
    VALID_ERROR_MESSAGE,
    VALID_ERROR_VALUE,
)


class TestAuth(unittest.TestCase):

    random_api_key = "sakjdhsksldhks"
    
    def setUp(self) -> None:
        super().setUp()

    def getBadRequestResponse():
        res = Response(400, json={KEY_MESSAGE: BAD_REQUEST_MESSAGE})
        return res

    def getHTTPExceptionResponse():
        res = Response(500, json={KEY_MESSAGE: EXCEPTION_OCCURED}, headers={
                       KEY_APIGW_REQUESTID: API_GW_REQUEST_ID})
        return res

    def getFailedValidationResponse():
        data = HTTPValidationError(
            [ValidationError([KEY_VALID_ERROR_LOC], VALID_ERROR_MESSAGE, VALID_ERROR_VALUE)])
        res = Response(422, json=data.to_dict())
        return res

    def getInvalidCredentialResponse():
        res = Response(401, json={KEY_MESSAGE: BAD_REQUEST_MESSAGE}, text='{{KEY_MESSAGE}: {BAD_REQUEST_MESSAGE}}')
        return res

    def getSuccessResponse():
        res = Response(200, json={"token": USER_TOKEN, "user_id": USER_ID})
        return res

    # @patch("oblv_package.src.auth.authenticate_with_email_authenticate_email_post.request.post",return_value=getSuccessResponse())
    @patch("httpx.request", return_value=getBadRequestResponse())
    def test_bad_request(self, sync):
        with self.assertRaises(BadRequestError) as cm:
            authenticate(self.random_api_key)

        the_exception = cm.exception
        self.assertEqual(the_exception.__str__(), BAD_REQUEST_MESSAGE)

    @patch("httpx.request", return_value=getHTTPExceptionResponse())
    def test_http_exception_request(self, sync):
        with self.assertRaises(HTTPClientError) as cm:
            authenticate(self.random_api_key)
        the_exception = cm.exception
        self.assertEqual(the_exception.__str__(
        ), 'An HTTP Client raised an unhandled exception. Kindly raise a request to the support team, along with the {} for resolution.'.format(API_GW_REQUEST_ID))

    @patch("httpx.request", return_value=getFailedValidationResponse())
    def test_failed_validation_request(self, sync):
        with self.assertRaises(ParamValidationError) as cm:
            authenticate(self.random_api_key)

        the_exception = cm.exception
        self.assertEqual(the_exception.__str__(), "Invalid {} provided".format(KEY_VALID_ERROR_LOC))

    @patch("httpx.request", return_value=getInvalidCredentialResponse())
    def test_bad_authentication_request(self, sync):
        with self.assertRaises(AuthenticationError) as cm:
            authenticate(self.random_api_key)

        the_exception = cm.exception
        self.assertEqual(the_exception.__str__(
        ), "Invalid credentials provided. Kindly verify the same and try again.")

    @patch("httpx.request", return_value=getSuccessResponse())
    def test_success_request(self, sync):
        client = OblvClient(token=USER_TOKEN, oblivious_user_id=USER_ID)
        result_client = authenticate(self.random_api_key)
        self.assertEqual(result_client.token, client.token)
        self.assertEqual(result_client.oblivious_user_id, client.oblivious_user_id)


if __name__ == '__main__':
    unittest.main()
