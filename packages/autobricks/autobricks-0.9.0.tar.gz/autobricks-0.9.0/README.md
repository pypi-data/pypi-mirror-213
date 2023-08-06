<img src="https://img.shields.io/badge/Python-v3.8-blue">

# Documentation

https://autobricks.readthedocs.io/en/latest/

# Development Setup

Create virual environment and install dependencies for local development:

```
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

# Configuration & Authentication

Azure databricks allows the following authentication methods:

- [Databricks User PAT Token](https://docs.microsoft.com/en-us/azure/databricks/dev-tools/api/latest/authentication)
- [Azure Service Principal](https://docs.microsoft.com/en-us/azure/databricks/dev-tools/api/latest/aad/)
- [Azure Service Principal over the Management End Point](https://docs.microsoft.com/en-us/azure/databricks/dev-tools/api/latest/aad/)

This library supports all by simply setting the following environment variables as required for each method. 
The AUTH_TYPE sets the authorisation mode and therefore what configuration to expect. 
Ensure that sensitive values are managed using secret redaction e.g. key vault or some other method.


| Variable              | User PAT | SP                  | SP on Mgmt Endpoint               |
|-----------------------|----------|---------------------|-----------------------------------|
|AUTH_TYPE              | USER     | SERVICE_PRINCIPAL   | SERVICE_PRINCIPAL_MGMT_ENDPOINT   |
|DBUTILSTOKEN           | &#10003; | &#10003;            | &#10003;                          |
|TENANT_ID              |          | &#10003;            | &#10003;                          |
|SP_CLIENT_ID           |          | &#10003;            | &#10003;                          |
|SP_CLIENT_SECRET       |          | &#10003;            | &#10003;                          |
|AD_RESOURCE            |          | &#10003;            | &#10003;                          |
|MGMT_RESOURCE_ENDPOINT |          |                     | &#10003;                          |
|WORKSPACE_NAME         |          |                     | &#10003;                          | 
|RESOURCE_GROUP         |          |                     | &#10003;                          |
|SUBSCRIPTION_ID        |          |                     | &#10003;                          |
|DATABRICKS_API_HOST    | &#10003; | &#10003;            | &#10003;                          |

Also note that library will use simple rest calls to retrieve tokens. An alternative approach 
is to leverage the adal library to authenticate. If you wish to authenticate over [adal](https://pypi.org/project/adal/) please
refer to following settings:

| Variable              | SP                     | SP on Mgmt Endpoint                  |
|-----------------------|------------------------|--------------------------------------|
|AUTH_TYPE              | SERVICE_PRINCIPAL_ADAL | SERVICE_PRINCIPAL_MGMT_ENDPOINT_ADAL |
|DBUTILSTOKEN           | &#10003;               | &#10003;                             |
|TENANT_ID              | &#10003;               | &#10003;                             |
|SP_CLIENT_ID           | &#10003;               | &#10003;                             |
|SP_CLIENT_SECRET       | &#10003;               | &#10003;                             |
|AD_RESOURCE            | &#10003;               | &#10003;                             |
|MGMT_RESOURCE_ENDPOINT |                        | &#10003;                             |
|WORKSPACE_NAME         |                        | &#10003;                             | 
|RESOURCE_GROUP         |                        | &#10003;                             |
|SUBSCRIPTION_ID        |                        | &#10003;                             |
|DATABRICKS_API_HOST    | &#10003;               | &#10003;                             |

When deciding between [adal](https://pypi.org/project/adal/) and rest calls the following is relevant:
- [adal](https://pypi.org/project/adal/) may not work in Azure DevOps in highly restricted private network setups
- Rest calls are more simple however if MS makes any changes to the API's the [adal](https://pypi.org/project/adal/) isn't there to abstract those changes.

The following variables will default.

| Variable              | Default                              |
|-----------------------|--------------------------------------|
|AUTH_TYPE              | SERVICE_PRINCIPAL                    |
|AD_RESOURCE            | 2ff814a6-3304-4ab8-85cb-cd0e6f879c1d |
|MGMT_RESOURCE_ENDPOINT | https://management.core.windows.net/ |

For testing, development and deployment and deployment substitute your own 
values between the angled brackets:

```
export AUTH_TYPE=USER
# export AUTH_TYPE=SERVICE_PRINCIPAL
# export AUTH_TYPE=SERVICE_PRINCIPAL_MGMT_ENDPOINT
# export AUTH_TYPE=SERVICE_PRINCIPAL_ADAL
# export AUTH_TYPE=SERVICE_PRINCIPAL_MGMT_ENDPOINT_ADAL

# required for AUTH_TYPE=USER
export DBUTILSTOKEN="<my_token>"

# required for AUTH_TYPE=SERVICE_PRINCIPAL
export TENANT_ID="<my_tenant_id>"
export SP_CLIENT_ID=<my_service_principal_client_id>
export SP_CLIENT_SECRET=<my_service_principal_secret>
export AD_RESOURCE=2ff814a6-3304-4ab8-85cb-cd0e6f879c1d

# required for AUTH_TYPE in (SERVICE_PRINCIPAL or SERVICE_PRINCIPAL_MGMT_ENDPOINT)
export MGMT_RESOURCE_ENDPOINT=https://management.core.windows.net/
export WORKSPACE_NAME=my_dbx_workspacename
export RESOURCE_GROUP=my_dbx_resourcegroup
export SUBSCRIPTION_ID=<my_subscription_id>
export DATABRICKS_API_HOST=<my_databricks_host_url>

```

Exporting variables doesn't make for a great development experience so the project uses pytest.ini for
mock environment variables. For example:

```
[pytest]
env =
    DATABRICKS_API_HOST=https://<my_databricks_host>.azuredatabricks.net
    DBUTILSTOKEN=<my_token>
    ...
```

**REMINDER: do NOT commit pytest.ini that contains real security tokens**

For convenience here is a yaml template for docker and build pipelines:

```
env:
    # AUTH_TYPE: USER
    AUTH_TYPE: SERVICE_PRINCIPAL
    # AUTH_TYPE: SERVICE_PRINCIPAL_MGMT_ENDPOINT
    # AUTH_TYPE: SERVICE_PRINCIPAL_ADAL
    # AUTH_TYPE: SERVICE_PRINCIPAL_MGMT_ENDPOINT_ADAL

    # required for AUTH_TYPE=USER
    # DBUTILSTOKEN: $(token)

    # required for AUTH_TYPE=SERVICE_PRINCIPAL
    TENANT_ID: $(tenant_id)
    SP_CLIENT_ID: $(service_principal_client_id)
    SP_CLIENT_SECRET: $(service_principal_secret)

    # required for AUTH_TYPE in (SERVICE_PRINCIPAL or SERVICE_PRINCIPAL_MGMT_ENDPOINT)
    WORKSPACE_NAME: $(dbx_workspace_name)
    RESOURCE_GROUP: $(dbx_resource_group)
    SUBSCRIPTION_ID: $(subscription_id)
    DATABRICKS_API_HOST: $(databricks_host_url)

```

# Build

Build python wheel:
```
python setup.py sdist bdist_wheel
```

There is a CI build configured for this repo that builds on main origin and publishes to PyPi.

# Test

Dependencies for testing:
```
pip install --editable .
```

Run tests:
```
pytest
```

Test Coverage:
```
pytest --cov=autobricks --cov-report=html
```

View the report in a browser:
```
./htmlcov/index.html
```


