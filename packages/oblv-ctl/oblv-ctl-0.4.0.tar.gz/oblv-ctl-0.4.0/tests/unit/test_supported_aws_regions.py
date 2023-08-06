import imp
import unittest
from http.client import FORBIDDEN
from unittest.mock import patch

from httpx import Response

from oblv_ctl.exceptions import (BadRequestError, HTTPClientError,
                             ParamValidationError, UnauthorizedTokenError)
from oblv_ctl.models.account import Account
from oblv_ctl.models.http_validation_error import HTTPValidationError
from oblv_ctl.models.validation_error import ValidationError
from oblv_ctl.oblv_client import OblvClient
from tests.unit.constants import (API_GW_REQUEST_ID, BAD_REQUEST_MESSAGE,
                                  DEPLOYMENT, EXCEPTION_OCCURED, GITHUB,
                                  GITHUB_USER_ID, GITHUB_USER_LOGIN,
                                  KEY_APIGW_REQUESTID, KEY_MESSAGE,
                                  KEY_VALID_ERROR_LOC, SUPPORTED_REGIONS,
                                  USER_ID, USER_TOKEN, VALID_ERROR_MESSAGE,
                                  VALID_ERROR_VALUE)


class TestSupportedAWSRegions(unittest.TestCase):

    client = OblvClient(token=USER_TOKEN, oblivious_user_id=USER_ID)

    def setUp(self) -> None:
        super().setUp()
        
    def getForbiddenResponse():
        res = Response(403, json=FORBIDDEN)
        return res

    def getSuccessResponse():
        res = Response(200, json=SUPPORTED_REGIONS)
        return res
    
    @patch("httpx.request", return_value=getForbiddenResponse())
    def test_bad_authentication_request(self, sync):
        try:
            self.client.supported_aws_regions()
        except Exception as e:
            assert e.args[0]=="The session associated with this profile has expired or is otherwise invalid. To refresh this session use the authenticate method with the corresponding profile."

    @patch("httpx.request", return_value=getSuccessResponse())
    def test_success_request(self, sync):
        self.assertEqual(self.client.supported_aws_regions().to_dict(), SUPPORTED_REGIONS)


if __name__ == '__main__':
    unittest.main()
