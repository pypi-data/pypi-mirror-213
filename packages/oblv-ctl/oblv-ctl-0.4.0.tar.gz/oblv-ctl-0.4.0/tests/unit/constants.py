USER_ID = "user_id"
USER_LOGIN = "user_login"
USER_TOKEN = "user_token"
USER_EMAIL = "user_email"
USER_NAME = "user_name"
BAD_REQUEST_MESSAGE = "Bad Request"
API_GW_REQUEST_ID = "dummy-request-id"
EXCEPTION_OCCURED = "Exception Occured"
FORBIDDEN = "Forbidden"
SUCCESS="Success"
KEY_MESSAGE = "message"
KEY_APIGW_REQUESTID = "apigw-requestid"
KEY_VALID_ERROR_LOC = "location"
VALID_ERROR_MESSAGE = "Invalid Message"
VALID_ERROR_VALUE = "value"
GITHUB_USER_ID = "123456"
GITHUB_USER_LOGIN = "github_user_login"
OLD_PASS="Oldpass123#"
NEW_PASS="Newpass123#"
GITHUB = "github"
RANDOM_PUBLIC_KEY = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnLMkUkUTDrI2QIkyzF9iULdvjzpJHDIjV1r9X1R9D4wbzpC8cmwblSOD9gS9iZQaEijBzlc1gbe3fXMhwM6XImVQ7xn1lfQ7WZcfwTLK+V1lqIBIqn/Y+hxhecbWKM25RIRoAJ/jIfL608ltydbsl0oaMaEnU1r5PwNh5vGp8vVPsEN0DwgyJjrA6qTv1ZqeSoPuNwcQJH07U9tRngIABf5mKzUfRphX011CqISgKh8drwtac7nRxL452fD5eErRVTa6vrTfvKV5H4SUM3uJIuLE718xEM0QRaWfSSBD2hPCbpCSqaaAUFGgI3oEJ7LbA3z3pGmcKAUTVIwIDAQAB"
INVALID_PUBLIC_KEY = "MIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEf452fD5eErRVTa6vrTfvKV5H4SUM3uJIuLE718xEM0QRaWfSSBD2hPCbpCSqaaAUFGgI3oEJ7LbA3z3pGmcKAUTVIwIDAQAB"
USER_REPO = {
    "repo_id": 123456,
    "name": "Repo_Name",
    "is_private": False,
    "owner_login": "Owner_Login",
    "account_type": "github"
}
VCS_REPO_RESPONSE = {
    "repos": [{
        "repo_id": 506983974,
        "name": "Oblivious",
        "full_name": "ObliviousAI/Oblivious",
        "is_private": False,
        "owner_login": "ObliviousAI",
        "description": "\u2728 A single place to post issues & feature requests",
        "html_url": "https://github.com/ObliviousAI/Oblivious",
        "git_url": "git://github.com/ObliviousAI/Oblivious.git",
        "clone_url": "https://github.com/ObliviousAI/Oblivious.git",
        "default_branch": "master",
        "updated_at": "2022-09-01T20:29:36Z",
        "account_type": "github"
    },
        {
        "repo_id": 123456,
        "name": "Repo_Name",
                "full_name": "Owner_Login/Repo_Name",
                "is_private": False,
                "owner_login": "Owner_Login",
                "account_type": "github",
        "description": "Some Description",
        "html_url": "https://github.com/Owner_Login/Repo_Name",
        "git_url": "git://github.com/Owner_Login/Repo_Name.git",
        "clone_url": "https://github.com/Owner_Login/Repo_Name.git",
        "default_branch": "master",
        "updated_at": "2022-09-12T20:29:36Z",
        "account_type": "github"
    }],
  "total_pages": 1,
  "message": ""
}
REPO_WITH_SERVICE={
        "repo_id": 123456,
        "name": "Repo_Name",
                "full_name": "Owner_Login/Repo_Name",
                "is_private": False,
                "owner_login": "Owner_Login",
                "account_type": "github",
        "description": "Some Description",
        "html_url": "https://github.com/Owner_Login/Repo_Name",
        "git_url": "git://github.com/Owner_Login/Repo_Name.git",
        "clone_url": "https://github.com/Owner_Login/Repo_Name.git",
        "default_branch": "master",
        "updated_at": "2022-09-12T20:29:36Z",
        "account_type": "github",
        "services": [{
            "ref": "master",
            "sha": "some sha",
            "type": "branch",
            "service_validated": True
        }]
    }

REPO_REFS={"branch":["master","dummy"],"tags":["v1.0"]}
USER_SERVICES = [{
    "repo_id": "123456",
    "repo_name": "Repo_Name",
    "repo_owner": "Owner_Name",
    "account_type": "github",
    "ref": "master",
    "sha": "some sha",
    "type": "branch",
    "service_validated": True
}]
REPO_SERVICES = [{
    "ref": "master",
    "sha": "some sha",
    "type": "branch",
    "service_validated": True
}]
SERVICE_YAML_CONTENT={
  "auth": [
    {
      "auth_name": "Auth",
      "auth_type": "signed_headers"
    }
  ],
  "base_image": "oblv_ubuntu_18_04_proxy_nsm_api_python_3_8",
  "build_args": [],
  "meta": {
    "author": "Team Oblivious",
    "author_email": "hello@oblivious.ai",
    "git": "https://github.com/ObliviousAI/FastAPI-Enclave-Services.git",
    "version": "0.1.0"
  },
  "paths": [
    {
      "access": "user",
      "path": "/hello/",
      "short_description": "Hello world example"
    }
    ],
    "outbound": [
      {
        "domain": "example.com",
        "name": "example",
        "port": 443,
        "type": "tcp"
      }
    ]
  }
DEPLOYMENT_ID="deployment_id"
DEPLOYMENT={
    "deployment_id": DEPLOYMENT_ID,
    "deployment_name": "deployment_name",
    "account_type": "github",
    "owner": USER_ID,
    "owner_login": USER_LOGIN,
    "repo_name": "Repo_Name",
    "repo_owner": "Owner_Name",
    "tags": [],
    "branch_release": "master",
    "current_state": "Running",
    "visibility": "private",
    "is_dev_env": True,
    "creation_time": "01-06-2022 19:50:02",
    "sha": "some sha",
    "is_deleted": True,
    "instance": {
        "region_name": "us-east-1",
        "stack_name": "stack name",
        "instance_type": "c5.xlarge",
        "instance_url": "instance url",
        "service_url": "service url",
        "build_log_location": ""
    },
    "pcr_codes": ["pcr0codeletters","pcr1codeletters","pcr2codeletters"],
    "credit_utilization_per_hour": 68,
    "build_args": {
        "auth": {},
        "users": {
            "user": [{
                "user_name": "some_user",
                "public key": "MIIBCgKCAQEA1MuTZlPrs845FZOFm8TTeakJKr1FmW3JxAc64IafZw3WYvP1wtQOH4eSgJm5138RG1Hdg4gmWkS/4PbstxTpciwX80ARKbi8Jv7UkayeKBeLT7j7B+aRxebIJUH0THstST9nFO+10MTuNY7+AXNzfYR6PihtfmQIDAQAA",
                "user_login": "u-185b6de2-837a-4cbb-93fc-d1c9f96f3b04"
            }]
        },
        "infra_reqs": {
            "CPUs": 2,
            "RAM": 4000
        }
    },
    "shared_users": [],
    "history": [{
        "action": "STARTED",
        "timestamp": "01-06-2022 19:55:42"
    }]
}
SUPPORTED_REGIONS={
  "us-east-1": "US East (N. Virginia)",
  "us-west-2": "US West (Oregon)",
  "eu-central-1": "Europe (Frankfurt)",
  "eu-west-2": "Europe (London)"
}
DEPLOYMENT_ROLES=[{
    "role_name": "user",
    "role_description": "User Role"
}]
ARGUMENTS_RESPONSE={
  "sha": "some_sha",
  "arg_schema": {
    "some_key": "some_value"
  }
}
CREATE_DEPLOYMENT_INPUT= {
    "owner": "Owner Name",
    "repo": "Repo Name",
    "account_type": "github",
    "ref": "master",
    "ref_type": "branch",
    "region_name": "us-east-1",
    "deployment_name": "deployment name",
    "visibility": "private",
    "is_dev_env": True,
    "tags": [],
    "build_args": {
        "auth": {},
        "users": {
            "user": [{
                "user_name": "some_user",
                "public key": "MIIBCgKCAQEA1MuTZlPrs845FZOFm8TTeakJKr1FmW3JxAc64IafZw3WYvP1wtQOH4eSgJm5138RG1Hdg4gmWkS/4PbstxTpciwX80ARKbi8Jv7UkayeKBeLT7j7B+aRxebIJUH0THstST9nFO+10MTuNY7+AXNzfYR6PihtfmQIDAQAA",
                "user_login": "u-185b6de2-837a-4cbb-93fc-d1c9f96f3b04"
            }]
        },
        "infra_reqs":"c5.xlarge"
    }
}
