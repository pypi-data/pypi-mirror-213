import unittest
from http.client import FORBIDDEN
from unittest.mock import patch

from httpx import Response

from oblv_ctl.exceptions import HTTP_CLIENT_ERROR_MESSAGE
from oblv_ctl.models.http_validation_error import HTTPValidationError
from oblv_ctl.models.repo_dynamic_service import RepoDynamicService
from oblv_ctl.models.validation_error import ValidationError
from oblv_ctl.oblv_client import OblvClient
from tests.unit.constants import (
    API_GW_REQUEST_ID,
    BAD_REQUEST_MESSAGE,
    EXCEPTION_OCCURED,
    KEY_APIGW_REQUESTID,
    KEY_MESSAGE,
    KEY_VALID_ERROR_LOC,
    REPO_SERVICES,
    USER_ID,
    USER_TOKEN,
    VALID_ERROR_MESSAGE,
    VALID_ERROR_VALUE,
)


class TestRepoServices(unittest.TestCase):

    client = OblvClient(token=USER_TOKEN, oblivious_user_id=USER_ID)

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

    def getForbiddenResponse():
        res = Response(403, json=FORBIDDEN)
        return res

    def getSuccessResponse():
        res = Response(200, json={"total_pages": 1, "services": REPO_SERVICES})
        return res

    @patch("httpx.request", return_value=getBadRequestResponse())
    def test_bad_request(self, sync):
        try:
            self.client.repo_services(repo_name="Repo_Name", repo_owner="Owner_Name")
            assert False
        except Exception as e:
            assert e.args[0]==BAD_REQUEST_MESSAGE

    @patch("httpx.request", return_value=getHTTPExceptionResponse())
    def test_http_exception_request(self, sync):
        try:
            self.client.repo_services(repo_name="Repo_Name", repo_owner="Owner_Name")
            assert False
        except Exception as e:
            assert e.args[0]==HTTP_CLIENT_ERROR_MESSAGE.format(API_GW_REQUEST_ID)

    @patch("httpx.request", return_value=getFailedValidationResponse())
    def test_failed_validation_request(self, sync):
        try:
            self.client.repo_services(repo_name="Repo_Name", repo_owner="Owner_Name")
            assert False
        except Exception as e:
            assert e.args[0]=="Invalid {} provided".format(KEY_VALID_ERROR_LOC)


    @patch("httpx.request", return_value=getForbiddenResponse())
    def test_bad_authentication_request(self, sync):
        try:
            self.client.repo_services(repo_name="Repo_Name", repo_owner="Owner_Name")
            assert False
        except Exception as e:
            assert e.args[0]=="The session associated with this profile has expired or is otherwise invalid. To refresh this session use the authenticate method with the corresponding profile."

    @patch("httpx.request", return_value=getSuccessResponse())
    def test_success_request(self, sync):
        obj = [RepoDynamicService.from_dict(x) for x in REPO_SERVICES]
        self.assertEqual(self.client.repo_services(repo_name="Repo_Name", repo_owner="Owner_Name").services, obj)

if __name__ == '__main__':
    unittest.main()
