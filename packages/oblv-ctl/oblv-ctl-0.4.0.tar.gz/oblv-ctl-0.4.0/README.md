# oblv-ctl

A Python library to access Oblivious APIs.

## Usage

First, create a client, with your API key. This key can be created in the
[Oblivious Console UI](https://console.oblivious.ai/). Go to the
settings page, and create your ApiKey. Once done, the client can be
created as follows

``` {.python}
from oblv_ctl import authenticate
client = authenticate(apikey=*your_key_here*)
```


Using this client, all the Oblivious actions can be performed, including the deployment of enclaves. Below is a step-by-step guide, to creating your first deployment.


The deployments can be created in two ways - using a pre-built static service or dynamically deploying the code.

# Dynamic Service Deployment
### 1 Create a service

A service refers to a branch/tag of your repository that needs to be
deployed. For your first service. you can use the repository
[ObliviousAI/FastAPI-Enclave-Services](https://github.com/ObliviousAI/FastAPI-Enclave-Services).
Execute the below command to create the service.

``` {.python}
client.add_service(repo_owner="ObliviousAI",repo_name="FastAPI-Enclave-Services", ref="master", data = {
    "auth": [
        {
            "auth_name": "auth_name",
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
    "roles": [
        {
            "role_auth": "auth_name",
            "role_cardinality": 1,
            "role_description": "Role for the data scientist",
            "role_name": "user"
        }
    ],
    "traffic": {
        "inbound": [
            {
                "name": "main_io",
                "port": 80,
                "type": "tcp"
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
})
```

The data provided here is sample service data. You can update the data as per your requirements, adhering to the schema.
The response for the call above gives results as follows - 


>{ \
>&nbsp;&nbsp;&nbsp;&nbsp;"message": "Success", \
>&nbsp;&nbsp;&nbsp;&nbsp;"service":&nbsp;&nbsp;&nbsp;&nbsp;{ \
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"ref": "master", \
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"service_validated": true, \
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"sha": "6b1b3e9cf6b0cb7264aad2fc80d91a009ccf0fc1", \
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"type": "branch" \
>&nbsp;&nbsp;&nbsp;&nbsp;} \
>} 


You have now successfully created your first service, and it can be now deployed to an enclave.

### 2 Enclave Creation

To create an enclave, you need to decide on a few of the parameters -

-   **deployment_name** - A unique deployment name. You cannot have two
    running deployments with the same name.
-   **region_name** - could be one of the AWS regions from
    - ***us-east-1*** (N. Virginia) 
    - ***us-west-2*** (Oregon)
    - ***eu-central-1*** (Frankfurt)
    - ***eu-west-2*** (London)
-   **visibility** - ***private*** or ***public***
-   **is_dev_env** - ***True*** or ***False***.
-   **tags** - A list of tags for your deployment
-   **account_type** - This is the VCS type, and only GitHub*** is
    supported for now.
-   **build_args** - Arguments specific to your deployment. It includes adding users to their roles with their public keys, runtime arguments and
    any additional arguments for your build. It also includes the infra
    size needed for the deployment. The options are -
    -   ***c5.xlarge*** - CPU:4 RAM:8 GB \-- Credit Utilization: 68.0/hr
    -   ***m5.xlarge*** - CPU:4 RAM:16 GB \-- Credit Utilization:
        76.8/hr
    -   ***r5.xlarge*** - CPU:4 RAM:32 GB \-- Credit Utilization:
        100.8/hr
    -   ***c5.2xlarge*** - CPU:8 RAM:16 GB \-- Credit Utilization:
        136.0/hr
    -   ***m5.2xlarge*** - CPU:8 RAM:32 GB \-- Credit Utilization:
        153.6/hr

A valid example for *build_args* for the service you created -


```
args = {
    "users": {
      "admin": [
        {
          "user_name": "<your name>",
          "public key": "<your public key>"
        }
      ]
    },
    "infra_reqs": "m5.xlarge",  
}

```

> 📝 **Note:**
>
> <b>admin</b> here
> is the role defined for the deployment in service.yaml
> file
>
> The service used,
> does not have requirements for any runtime or build arguments, so not
> needed here.

``` {.python}
from oblv_ctl.models import CreateDeploymentInput
input = CreateDeploymentInput(
    owner="ObliviousAI",
    repo="FastAPI-Enclave-Services",
    account_type="github",
    ref="master",
    ref_type="branch",
    region_name="us-east-1",
    deployment_name="Depl",
    visibility="private",
    is_dev_env=True,
    tags=[],
    build_args=args
)
response = client.create_deployment(input)
```


On successful request, enclave creation is initiated, and it returns an
id for the deployment, which can be later used to track the status and
connection details for the enclave.

### 3 Enclave Information
To check the state of the deployment, run

``` {.python}
client.deployment_info(response.deployment_id).current_state
```

> 'CFT Initiated'


When the deployment state becomes ***Running***, it indicates that the
enclave is now available for connection.

To connect to the enclave, you need **Oblv CLI** installed in your
system. The commands to use the CLI can be found in this
[documentation](https://docs.oblivious.ai/cli/usage_examples).

Cli binaries can be found [here](https://docs.oblivious.ai/cli/binaries)

The URL to connect to the enclave using CLI can be accessed using

``` {.python}
client.deployment_info(response.deployment_id).instance.service_url
```

>
>'https://conso-appli-15aiaxip9pcxk-94364694.enclave.oblivious.ai'
>


The PCR codes can be found using

``` {.python}
client.deployment_info(response.deployment_id).pcr_codes
```

>['d8dd856bacf4a8f0840ab530579b906091803e818e01dc4b8f51c247a7adfcfe55b4ef5f17be6d53bb952d92d87a376c',
'bcdf05fefccaa8e55bf2c8d6dee9e79bbff31e34bf28a99aa19e6b29c37ee80b214a414b7607236edf26fcb78654e63f','79477bad9504a347afb557a8ccd6f62ea61243311dff39f66944f5150242128da0cd070f0ce629c6beb6bb4f0b52f5ed' ]


# Static Service Deployment
In this type of deployment, services are prebuilt and kept ahead of time. You can either create you static service first and then go ahead for deployment, or you could simply use a service available in marketplace.

### 1 Create a service
Execute the below command to create a static service.

```python
oblv_client.add_static_service(
    name="first deployment",
    description="First Static Service creation",
    repo_owner="ObliviousAI",
    repo_name="FastAPI-Enclave-Services",
    ref="60d7c177be25cc9758520580f78f7d6b135b17c8",
    arguments={}
)
```


### 2 Enclave Creation
Execute the below command to create deployment from static service. 

```python
from oblv_ctl.models import StaticDeploymentInput
obj = StaticDeploymentInput(
    service="<service_id>",
    deployment_name="first_static_deployment",
    region_name="us-east-1",
    is_dev_env=True,
    runtime_args="somthing",
    users = {"somerole": [{"user_name": "<your name>", "public key": "<your public key>"}]},
    infra_reqs="m5.xlarge",
    marketplace=False
)
oblv_client.create_static_service_deployment(obj)
```

The next steps for getting deployment information and the pcr codes are same for both the service types and can be found [here](#3-enclave-information).