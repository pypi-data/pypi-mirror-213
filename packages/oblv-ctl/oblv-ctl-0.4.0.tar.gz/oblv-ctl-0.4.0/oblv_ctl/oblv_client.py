"""OblvClient

Python Client for calling open APIs supported by Oblivious

"""
import sys
import requests
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from oblv_ctl.exceptions import BadRequestError
from oblv_ctl.models.name_input import NameInput
from oblv_ctl.api.account import get_user_accounts_user_account_get
from oblv_ctl.api.auth import logout_session_logout_delete
from oblv_ctl.api.deployment import (
    create_new_deployment_deployment_post,
    delete_deployment_deployment_delete,
    generate_build_args_deployment_arguments_get,
    get_available_deployments_deployment_available_get,
    get_deployment_info_deployment_get,
    get_deployment_roles_deployment_roles_get,
    get_supported_regions_deployment_supported_regions_get,
    get_user_owned_deployments_deployment_owned_get,
    create_new_deployment_deployment_static_post
)
from oblv_ctl.api.repo import (
    get_all_repos_repo_linked_get,
    get_repo_from_vcs_repo_get,
    get_repo_refs_repo_refs_get,
    get_repo_repo_repo_owner_repo_name_get,
    search_repo_from_vcs_repo_search_get,
)
from oblv_ctl.api.service import (
    add_update_repo_dynamic_service_service_dynamic_put,
    delete_dynamic_service_service_dynamic_delete,
    get_repo_dynamic_services_repo_service_get,
    get_user_dynamic_services_user_service_dynamic_get,
    get_service_yaml_content_repo_service_data_get,
    create_static_service_service_static_post,
    get_static_service_service_static_get,
    get_user_static_services_user_service_static_get,
    get_marketplace_services_service_marketplace_get,
    request_marketplace_addition_service_marketplace_request_put,
    delete_static_service_service_static_delete,
    get_static_service_build_logs_service_static_logs_get,
    get_docker_image_service_static_docker_get,
    remove_service_from_marketplace_service_marketplace_delete
)
from oblv_ctl.api.user import (
    add_user_public_shared_key_user_psk_put,
    get_user_deployment_credit_usage_user_credit_usage_get,
    get_user_profile_view_user_profile_get,
    get_user_public_shared_key_user_psk_get,
    update_user_name_user_name_put,
    update_user_password_user_password_put,
)
from oblv_ctl.client import AuthenticatedClient
from oblv_ctl.config import URL
from oblv_ctl.exceptions import BadYamlData
from oblv_ctl.models import (
    PSK,
    CreateDeploymentInput,
    UserPasswordInput,
    DynamicServiceYamlInput,
    StaticServiceInput,
    StaticDeploymentInput
)
from .utils import bcolors


def _method_wrapper(function):
        """
        A wrapper method for exception logging
        """

        def wrap(*args, **kwargs):
            """Method to call the requested method in try-catch block"""

            try:
                return function(*args, **kwargs)
            except Exception as exception:
                print(
                    bcolors.RED
                    + bcolors.BOLD
                    + "Exception"
                    + bcolors.BLACK
                    + bcolors.ENDC
                    + f": {str(exception)}",
                    file=sys.stderr,
                )
                raise exception

        return wrap

class OblvClient(AuthenticatedClient):
    """
    Client for making API calls to Oblivious
    """

    @_method_wrapper
    def logout(self):
        """Logout Session

        This API invalidates the user's token.

        After a successul response, the user will not be able to use the auth token provided in the auth APIs.

        Returns:
            None
        """
        try:
            logout_session_logout_delete.sync(
                client=self, oblivious_user_id=self.oblivious_user_id
            )
        except Exception as exception:
            raise exception
        finally:
            self.token = ""
            self.oblivious_user_id = ""

    ###### Account Method ######

    @_method_wrapper
    def accounts(self):
        """Get User Accounts
         API to fetch user's linked VCS accounts
        Returns:
            List[Account]
        """
        return get_user_accounts_user_account_get.sync(
            client=self, oblivious_user_id=self.oblivious_user_id
        )

    ############################

    ####### User Methods #######
    @_method_wrapper
    def psk(self):
        """Get User PSK
         API to fetch user's psk
        Returns:
            str
        """
        return get_user_public_shared_key_user_psk_get.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            user_id=self.oblivious_user_id,
        )

    @_method_wrapper
    def credit_usage(self):
        """Get User Credit Usage
         API to fetch user's credit usage
        Returns:
            UserCreditUtilization
        """
        return get_user_deployment_credit_usage_user_credit_usage_get.sync(
            client=self, oblivious_user_id=self.oblivious_user_id
        )

    @_method_wrapper
    def set_psk(self, public_key):
        """Update user's publically shareable key
        API to update user's publically shareable key
        Args:
            public_key (str): Public Key to be shared
        Returns:
            None
        """

        json_body = PSK(public_key)
        return add_user_public_shared_key_user_psk_put.sync(
            client=self, oblivious_user_id=self.oblivious_user_id, json_body=json_body
        )

    @_method_wrapper
    def update_name(self, name):
        """Update Name
        API to update the name.
        Args:
            name (str): User Name
        Returns:
            None
        """
        update_user_name_user_name_put.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            json_body=NameInput(name),
        )

    @_method_wrapper
    def update_password(self, old_pass, new_pass):
        """Update User's Password
         API to update user's password
        Args:
            old_pass (str): Old Password
            new_pass (str): New Password
        Returns:
            None
        """
        json_body = UserPasswordInput(old_password=old_pass, password=new_pass)
        update_user_password_user_password_put.sync(
            client=self, oblivious_user_id=self.oblivious_user_id, json_body=json_body
        )

    @_method_wrapper
    def user_profile(self):
        """Get User Profile
         API to fetch user's profile details
        Returns:
            UserProfileResponse
        """
        return get_user_profile_view_user_profile_get.sync(
            client=self, oblivious_user_id=self.oblivious_user_id
        )

    ############################

    ####### Repo Methods #######
    @_method_wrapper
    def get_repo(self, owner, name):
        """Get User Repo
         API to fetch user's repo information
        Args:
            owner (str): Repo Owner
            name (str): Repo Name
        Returns:
            Repo
        """
        return get_repo_repo_repo_owner_repo_name_get.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            repo_owner=owner,
            repo_name=name,
        )

    @_method_wrapper
    def search_repo(self, keyword):
        """Add Repo Service With Yaml
         API to search a repository in VCS, on which the user has access.
        Args:
            keyword (str): Search Keyword
        Returns:
            List[Repo]
        """
        return search_repo_from_vcs_repo_search_get.sync(
            client=self, oblivious_user_id=self.oblivious_user_id, search_string=keyword
        )

    @_method_wrapper
    def linked_repos(self):
        """Get User Repos
         API to fetch user's repo without services
        Returns:
            List[RepoAllResponse]
        """
        return get_all_repos_repo_linked_get.sync(
            client=self, oblivious_user_id=self.oblivious_user_id
        )

    @_method_wrapper
    def repo_refs(self, owner, name):
        """Get Repo Refs
         API to fetch the repository refs (branches and tags).
        Args:
            owner (str): Repo Owner
            name (str): Repo Name
        Returns:
            RefResponse
        """
        return get_repo_refs_repo_refs_get.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            repo_owner=owner,
            repo_name=name,
        )

    @_method_wrapper
    def repos(self, page: int = 1, per_page: int = 10):
        """Get Repos From VCS
         API to get all the repositories from VCS, on which the user has access (via their own account, or by
        any organization they are member of).
        Args:
            page (int):  Page (Default 1)
            per_page (int):  Repositiories Per Page (Default 10)
        Returns:
            VCSRepoResponse
        """
        return get_repo_from_vcs_repo_get.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            page=page,
            per_page=per_page,
        )

    ############################

    ##### Services Methods #####
    @_method_wrapper
    def add_service(
        self,
        repo_owner: str,
        repo_name: str,
        ref: str,
        ref_type: str = "branch",
        data: dict = None,
    ):
        """Add Repo Service
         API to create a service after validation.
        Args:
            repo_owner (str): Repo's Owner Name
            repo_name (str): Repo Name
            ref (str): Service Ref
            ref_type (Union[Unset, None, str]):  Ref Type branch/tag (Default 'branch')
            data (dict): Service Yaml Content in dictionary format. If provided, service.yaml file will be created/updated based on its existence.
        Returns:
            ServiceValidationResponse
        """
        if data:
            try:
                req = requests.get(URL + "/service_schema", timeout=self.timeout)
                if req.status_code != 200:
                    raise BadRequestError("Failed to validate service yaml data")
                validate(data, req.json())
            except ValidationError as exception:
                raise BadYamlData(exception.message) from exception
            except Exception as exception:
                raise exception
        json_body = DynamicServiceYamlInput.from_dict(data)
        return add_update_repo_dynamic_service_service_dynamic_put.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            ref=ref,
            ref_type=ref_type,
            repo_owner=repo_owner,
            repo_name=repo_name,
            json_body=json_body,
        )

    @_method_wrapper
    def remove_service(
        self, repo_owner: str, repo_name: str, ref: str, ref_type: str = "branch"
    ):
        """Delete Repo Service
         API to delete a service. It does not delete the existing deployments created from this service.
        Args:
            repo_owner (str): Repo's Owner Name
            repo_name (str): Repo Name
            ref (str): Service Ref
            ref_type (Union[Unset, None, str]):  Ref Type branch/tag (Default 'branch')
        Returns:
            None
        """
        delete_dynamic_service_service_dynamic_delete.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            ref=ref,
            ref_type=ref_type,
            repo_name=repo_name,
            repo_owner=repo_owner,
        )

    @_method_wrapper
    def service_content(
        self, repo_owner: str, repo_name: str, ref: str, ref_type: str = "branch"
    ):
        """Get Service Yaml Content

         API to fetch the service.yaml content as object for the given ref. The ref need not be a service. It
        returns the sample service, if service.yaml not found.

        Args:
            ref (str): Service Ref
            ref_type (Union[Unset, None, str]): Whether the ref is a branch or tag. Default: 'branch'.
            repo_owner (str): Repository owner for service
            repo_name (str): Repository name for service

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            ServiceYamlContent
        """
        return get_service_yaml_content_repo_service_data_get.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            repo_owner=repo_owner,
            repo_name=repo_name,
            ref=ref,
            ref_type=ref_type,
        )

    @_method_wrapper
    def repo_services(
        self,
        repo_owner: str,
        repo_name: str,
        page: int = 1,
        per_page: int = 10,
        get_all: bool = False,
    ):
        """Get Repo Services

         Fetch all the services available for the given repository.

        Args:
            page (Union[Unset, None, int]): Requested page Default: 1.
            per_page (Union[Unset, None, int]): Responses per page Default: 10.
            get_all (Union[Unset, None, bool]): Get all responses. Precedence over *page* and
                *per_page* parameters
            repo_owner (str): Repository owner for service
            repo_name (str): Repository name for service

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            ServiceListRepoDynamicService
        """
        return get_repo_dynamic_services_repo_service_get.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            repo_owner=repo_owner,
            repo_name=repo_name,
            page=page,
            per_page=per_page,
            get_all=get_all,
        )

    @_method_wrapper
    def user_services(
        self,
        page: int = 1,
        per_page: int = 10,
        get_all: bool = False,
        search_keyword: str = "",
    ):
        """Get User Services
         API to fetch user's services
        Args:
            page (int):  Page (Default 1)
            per_page (str): services per page (Default 10)
            search_keyword (str): Search Keyword and is applied on repo full name (Default "")
            get_all (bool): To fetch all services at once (Default False)

        Returns:
            UserServiceListUserDynamicService
        """
        return get_user_dynamic_services_user_service_dynamic_get.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            page=page,
            per_page=per_page,
            get_all=get_all,
            search_term=search_keyword,
        )

    @_method_wrapper
    def update_service(
        self,
        repo_owner: str,
        repo_name: str,
        ref,
        ref_type: str = "branch",
        data: dict = None,
    ):
        """Update Repo Service With Yaml
         API to update a service, along with updating the service.yaml file. After updating the service.yaml file, the service is validate as well (for missing Dockerfile).
        Args:
            repo_owner (str): Repo's Owner Name
            repo_name (str): Repo Name
            ref (str): Service Ref
            ref_type (Union[Unset, None, str]):  Ref Type branch/tag (Default 'branch')
            data (dict): Service Yaml Content in dictionary format. If provided, service.yaml file will be created/updated based on its existence.

        Returns:
            ServiceValidationResponse
        """
        if data:
            try:
                req = requests.get(URL + "/service_schema", timeout=self.timeout)
                if req.status_code != 200:
                    raise BadRequestError("Failed to validate service yaml data")
                validate(data, req.json())
            except ValidationError as exception:
                raise BadYamlData(exception.message) from exception
            except Exception as exception:
                raise exception
        json_body = DynamicServiceYamlInput.from_dict(data)
        return add_update_repo_dynamic_service_service_dynamic_put.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            ref=ref,
            ref_type=ref_type,
            repo_owner=repo_owner,
            repo_name=repo_name,
            json_body=json_body,
        )

    @_method_wrapper
    def revalidate_service(
        self, repo_owner: str, repo_name: str, ref: str, ref_type: str = "branch"
    ):
        """Validate Repo Service
         API to validate a service with supported service schema. The checks include
        - Presence of service.yaml in ./oblivious folder.
        - Presence of Dockerfile in ./oblivious folder.
        - Content of service.yaml must be valid with respect to supported service schema.
        Args:
            repo_owner (str): Repo's Owner Name
            repo_name (str): Repo Name
            ref (str): Service Ref
            ref_type (Union[Unset, None, str]):  Ref Type branch/tag (Default 'branch')
        Returns:
            ServiceValidationResponse
        """
        json_body = DynamicServiceYamlInput.from_dict({})
        return add_update_repo_dynamic_service_service_dynamic_put.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            ref=ref,
            ref_type=ref_type,
            repo_owner=repo_owner,
            repo_name=repo_name,
            json_body=json_body,
        )

    @_method_wrapper
    def add_static_service(
        self,
        name: str,
        description: str,
        repo_owner: str,
        repo_name: str,
        ref: str,
        arguments: dict = None,
    ) -> None:
        """Add Static Service
        Create a new static/pre-built service.

        Args:
            repo_owner (str): Repo's Owner Name
            repo_name (str): Repo Name
            name (str): Service name. The name should start with an alphabet and can only contain numbers, alphabets, '_',
            '-'
            description (str): Service description
            ref (str): The commit sha or the ref from which the service is to be created.
            arguments (Union[Unset, StaticServiceInputArguments]): The arguments for docker build. From your service.yaml,
                the arguments added under "build_args".
        """
        if arguments is None:
            arguments = {}
        json_body = StaticServiceInput(
            name=name,
            description=description,
            repo_full_name="/".join([repo_owner, repo_name]),
            ref=ref,
            arguments=arguments,
        )
        result = create_static_service_service_static_post.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            json_body=json_body,
        )
        print(result)

    @_method_wrapper
    def user_static_services(
        self,
        page: int = 1,
        per_page: int = 10,
        get_all: bool = False,
        search_keyword: str = "",
    ):
        """Get User Services
         API to fetch user's services
        Args:
            page (int):  Page (Default 1)
            per_page (str): services per page (Default 10)
            search_keyword (str): Search Keyword and is applied on repo full name (Default "")
            get_all (bool): To fetch all services at once (Default False)

        Returns:
            UserServiceListUserStaticService
        """
        return get_user_static_services_user_service_static_get.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            page=page,
            per_page=per_page,
            get_all=get_all,
            search_term=search_keyword,
        )

    @_method_wrapper
    def get_static_service(self, service: str):
        """Get User Services
         API to fetch user's services
        Args:
            oblivious_user_id (str): User id
            service (str): Service name or id

        Returns:
            StaticService
        """
        return get_static_service_service_static_get.sync(
            client=self, oblivious_user_id=self.oblivious_user_id, service=service
        )

    @_method_wrapper
    def delete_static_service(self, service: str):
        """Get User Services
         API to fetch user's services
        Args:
            oblivious_user_id (str): User id
            service (str): Service name or id

        Returns:
            None
        """
        delete_static_service_service_static_delete.sync(
            client=self, oblivious_user_id=self.oblivious_user_id, service=service
        )

    @_method_wrapper
    def marketplace_services(
        self,
        page: int = 1,
        per_page: int = 10,
        get_all: bool = False,
        name_filter: str = "",
        repo_filter: str = "",
    ):
        """Get marketplace services

         To get all the marketplace services. These are the static services publically available for
        everyone's use.

        Args:
            page (Union[Unset, None, int]): Requested page Default: 1.
            per_page (Union[Unset, None, int]): Responses per page Default: 10.
            get_all (Union[Unset, None, bool]): Get all responses. Precedence over *page* and
                *per_page* parameters
            name_filter (Union[Unset, None, str]): Name filter for services Default: ''.
            repo_filter (Union[Unset, None, str]): Repo filter for services Default: ''.

        Returns:
           ServiceListMarketPlaceService
        """

        return get_marketplace_services_service_marketplace_get.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            page=page,
            per_page=per_page,
            get_all=get_all,
            name_filter=name_filter,
            repo_filter=repo_filter,
        )

    @_method_wrapper
    def add_service_to_marketplace(self, service: str):
        """Request to move a static service to marketplace

         Request a static service to be made available in the marketplace.

        Args:
            service (str): Service name or id

        Returns:
            None
        """
        request_marketplace_addition_service_marketplace_request_put.sync(
            client=self, oblivious_user_id=self.oblivious_user_id, service=service
        )

    @_method_wrapper
    def remove_service_from_marketplace(self, service: str):
        """Remove from Marketplace

        Remove a service from marketplace.

        Args:
            service (str): Service name or id

        Returns:
            None
        """
        remove_service_from_marketplace_service_marketplace_delete.sync(
            client=self, oblivious_user_id=self.oblivious_user_id, service=service
        )
    
    @_method_wrapper
    def get_static_service_docker_logs(self, service: str):
        """Get Build Logs

        Get build logs for static service build

        Args:
            service (str): Service name or id

        Returns:
            str
        """
        return get_static_service_build_logs_service_static_logs_get.sync(
            client=self, oblivious_user_id=self.oblivious_user_id, service=service
        )

    @_method_wrapper
    def get_docker_image_url(self, service: str):
        """Get static service docker image download url

        To fetch download url of docker image for the static service. 
        
        Use this pre-signed url to download the docker image or directly load to docker.
        
        To load the image directly to docker execute the command -
        "wget <url> | docker load"

        Args:
            service (str): Service name or id

        Returns:
            str
        """
        return get_docker_image_service_static_docker_get.sync(
            client=self, oblivious_user_id=self.oblivious_user_id, service=service
        )

    ############################

    #### Deployment Methods ####

    @_method_wrapper
    def deployment_info(self, deployment_id):
        """Get Deployment
         API to fetch a deployment's details.
        Args:
            deployment_id (str): Deployment Id
        Returns:
            DeploymentResponse
        """
        return get_deployment_info_deployment_get.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            deployment_id=deployment_id,
        )

    @_method_wrapper
    def create_deployment(self, deployment: CreateDeploymentInput):
        """Create Deployment
         API to create a new deployment.
        Args:
            deployment (CreateDeploymentInput): Deployment Details Input
        Returns:
            CreateDeploymentResponse
        """
        return create_new_deployment_deployment_post.sync(
            client=self, oblivious_user_id=self.oblivious_user_id, json_body=deployment
        )

    @_method_wrapper
    def create_static_service_deployment(self, deployment: StaticDeploymentInput):
        """Create Deployment
         API to create a new deployment from static service.
        Args:
            deployment (StaticDeploymentInput): Deployment Details Input
        Returns:
            CreateDeploymentResponse
        """
        return create_new_deployment_deployment_static_post.sync(
            client=self, oblivious_user_id=self.oblivious_user_id, json_body=deployment
        )


    @_method_wrapper
    def remove_deployment(self, deployment_id):
        """Delete Deployment
         API to initiate termination of a deployment.
        Args:
            deployment_id (str): Deployment Id
        Returns:
            MessageModel
        """
        return delete_deployment_deployment_delete.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            deployment_id=deployment_id,
        )

    @_method_wrapper
    def generate_deployment_build_args(self, owner: str, repo: str, ref: str):
        """Get Build Deployment Arguments
        API to fetch the arguments schema necessary for creating a deployment. It also gives the commit sha,
        at which point it was generated. This is to be passed to the create deployment API.
        Note - A service could have different build args schema depending on the service's commit history.
        Args:
            owner (str): Repo Owner
            repo (str): Repo Name
            ref (str): Service Ref
        Returns:
            BuildArgsSchema
        """
        return generate_build_args_deployment_arguments_get.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            repo=repo,
            owner=owner,
            ref=ref,
        )

    @_method_wrapper
    def available_deployments(self):
        """Get Available Deployments
         API to fetch all the deployments the user can connect to.
        Returns:
            List[DeploymentComplete]
        """
        return get_available_deployments_deployment_available_get.sync(
            client=self, oblivious_user_id=self.oblivious_user_id
        )

    @_method_wrapper
    def deployment_roles(self, deployment_id):
        """Get Deployment Roles
         API to get a deployment's roles.
        Args:
            deployment_id (str): Deployment Id
        Returns:
            List[RoleResponse]
        """
        return get_deployment_roles_deployment_roles_get.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            deployment_id=deployment_id,
        )

    @_method_wrapper
    def supported_aws_regions(self):
        """Deployment Supported Regions
         API to fetch a deployment's details.
        Returns:
            dict
        """
        return get_supported_regions_deployment_supported_regions_get.sync(client=self)

    @_method_wrapper
    def deployments(self):
        """Get Owned Deployments
         API to fetch a user's owned deployments.
        Returns:
            List[DeploymentResponse]
        """
        return get_user_owned_deployments_deployment_owned_get.sync(
            client=self, oblivious_user_id=self.oblivious_user_id
        )

    ############################
