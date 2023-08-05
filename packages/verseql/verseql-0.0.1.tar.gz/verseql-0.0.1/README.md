# SecretStore-verse
*Unified interfaces to the universe of secret stores*

SecretStore-verse aims to provide **unified and idiomatic** interfaces to secret stores across major cloud providers, cloud-agnostic providers, and open-source providers.

Quick links:
* [Supported Providers](#supported-providers)
* [Secret Store Concepts](#secret-store-concepts)
* [Installation](#installation)
* [Initialization](#initialization)
* [Operations](#operations)
* [Data Limits](#data-limits)
* [Implementation Notes](#implementation-notes)

## Supported Providers

The following providers are currently supported:
|Provider|Provider id|
|--------|-----------|
|Amazon Secrets Manager|amazon-secrets-manager|
|Azure Key Vault|azure-key-vault|
|Google Secret Manager|google-secret-manager|
|HashiCorp Vault|hashicorp-vault|
|IBM Cloud Secrets Manager|ibm-secrets-manager|
|Local SQLite (file<sup>1</sup> or in-memory)|local-sqlite|
|Local Environment Variables|local-environment|
> <sup>1</sup> This provider uses unencrypted local storage.

## Secret Store Concepts

### Secret
A secret is a name, value pair with optional metadata (tags). Secret value is stored as a string. Tags are key-value pairs of string.
* Secret name (string)
* Secret value (string)
* Tags (key-value pairs of strings)

All secret store providers support creating, updating, reading, and deleting secrets. Secrets are stored securely in storage. Refer to individual provider documentation on how they are stored and managed.

### Secret *id*
Secret *id* uniquely identifies the secret in storage and is used for reading and manipulating the secret. In most providers, the secret *name* is its *id*. In some providers, a new *id* is generated and returned when the secret is created to be later used in other operations. The following table shows how each provider assigns *id*.

|Provider|Secret id|
|--------|-----------|
|Amazon Secrets Manager|Same as *name*|
|Azure Key Vault|Same as *name*|
|Google Secret Manager|Same as *name*|
|HashiCorp Vault|Same as *name*|
|IBM Cloud Secrets Manager|Generated|
|Local SQLite|Same as *name*|
|Local Environment Variables|Same as *name*|

This package provides a unified interface to accomodate all providers. When a new secret is created (with name, value and tags), the *id* is returned. For providers that use *name* as id, the *name* is simply returned as id. For providers that generate id, the generated *id* is returned. The *id* can be consistently used to perform other [operations](#operations) on the secret.

### Versions
Secret values are versioned. When a new secret is created, it is associated with a ```version_id```. When the secret value is updated, a new version of the secret is created with a new ```version_id```. By default, reading a secret returns the newest version. Secret versions can be listed and older versions of the secret can be read using their respective version ids. 

Metadata (tags) is associated with the secret and not with each version. So, updating only the *tags* does not create a new secret version. 

### Soft-deletion
When a secret is deleted, some secret stores support soft-delete, where the secret is stored for a specified time period before it is destroyed permanently. During this period, deleted secrets can be recovered.

This package provides interfaces to both soft-delete a secret (if supported by the provider) and destroy the secret permanently.

## Installation
Install verse-storage-secretstore pip. Install provider-specific packages using the optional dependencies parameter (```[<provider-id>]```).

```
pip install verse-storage-secretstore[<provider-id>]
```

The table below shows how to install provider-specific packages:

|Provider|Install with provider id|Packages installed|
|--------|-----------|------------------|
|Amazon Secrets Manager|```pip install verse-storage-secretstore[amazon-secrets-manager]```|boto3|
|Azure Key Vault|```pip install verse-storage-secretstore[azure-key-vault]```|azure-identity, azure-keyvault-secrets, aiohttp|
|Google Secret Manager|```pip install verse-storage-secretstore[google-secret-manager]```|google-cloud-secret-manager|
|HashiCorp Vault|```pip install verse-storage-secretstore[hashicorp-vault]```|hvac|
|IBM Secrets Manager|```pip install verse-storage-secretstore[ibm-secrets-manager]```|ibm-secrets-manager-sdk|
|Local SQLite|```pip install verse-storage-secretstore[local-sqlite]```|*none*|
|Local Environment|```pip install verse-storage-secretstore[local-environment]```|*none*|

Multiple providers can be installed using comma-separated optional dependency parameter. An example below:
```
pip install verse-storage-secretstore[amazon-secrets-manager,azure-key-vault,google-secret-manager]
```

All providers can be installed using the ```all``` optional dependency parameter:
```
pip install verse-storage-secretstore[all]
```

## Initialization

The package supports both sync and async clients for all providers:

|Provider|Sync Support|Async Support|
|--------|----|-----|
|Amazon Secrets Manager|Yes|Yes|
|Azure Key Vault|Yes|Yes|
|Google Secret Manager|Yes|Yes*|
|HashiCorp Vault|Yes|Yes*|
|IBM Secrets Manager|Yes|Yes*|
|Local SQLite|Yes|Yes*|
|Local Environment|Yes|Yes*|
> *Sync interfaces are converted to async through Python [asyncio APIs](https://docs.python.org/3/library/asyncio-task.html#running-in-threads) because of the lack of native support in the provider packages.

### Getting the sync client

```python
from verse.storage.secretstore import SecretStore

client = SecretStore.get_client(provider_id, **provider_config_and_credentials)
```

### Getting the async client

```python
from verse.storage.secretstore import SecretStore

client = SecretStore.get_async_client(provider_id, **provider_config_and_credentials)
# ....
await client.close() # close async client
```

### Provider id, config, and credentials
There are many ways to configure credentials to each of the providers. This package tries to accommodate these methods through many optional config options.

> **Recommendation:** Keep the config and credentials in a config file (outside code) so that the code can be built once and deployed anywhere only by changing the config file.

#### Amazon Secrets Manager
For credentials, please refer to the official documentation [here](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html). 

```python
provider_id = "amazon-secrets-manager"
provider_config_and_credentials = 
{
  "region_name" = "<region-name>", #required config
  "aws_access_key_id" = "<aws-access-key-id>", #optional credential
  "aws_secret_access_key" = "<aws-secret-access-key>", #optional credential
  "aws_session_token" = "<aws-session-token>", #optional credential
  "profile_name" = "<profile-name>" #optional credential
}
```

#### Azure Key Vault
For credentials, please refer to the official documentation [here](https://learn.microsoft.com/en-us/azure/key-vault/secrets/quick-create-python?tabs=azure-cli) and [here](https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python).

```python
provider_id = "azure-key-vault"
provider_config_and_credentials = 
{
  "url" = "https://<key-vault-name>.vault.azure.net", #required config
  "tenant_id" = "<tenant-id>", #optional credential
  "client_id" = "<client-id>", #optional credential
  "client_secret" = "<client-secret>", #optional credential
}
```

#### Google Secret Manager
For credentials, please refer to the official documentation [here](https://cloud.google.com/secret-manager/docs/authentication) and [here](https://cloud.google.com/docs/authentication/provide-credentials-adc#on-prem).

```python
provider_id = "google-secret-manager"
provider_config_and_credentials = 
{
  "project_id" = "<project-id>", #required config
  "service_account_info" = "<service-account-info>", #optional credential serialized json
  "service_account_file" = "<service-account-file>", #optional credential json file path
}
```

#### HashiCorp Vault
For credentials, please refer to the official documentation [here](https://developer.hashicorp.com/vault/docs/auth) and [here](https://developer.hashicorp.com/vault/docs/auth/approle).

```python
provider_id = "hashicorp-vault"
provider_config_and_credentials = 
{
  "url" = "<url>", #required config
  "namespace" = "<namespace>", #required config
  "role_id" = "<role-id>", #optional credential
  "secret_id" = "<secret-id>", #optional credential
  "token" = "<token>", #optional credential
}
```

#### IBM Secrets Manager
For credentials, please refer to the official documentation [here](https://cloud.ibm.com/apidocs/secrets-manager/secrets-manager-v2?code=python#authentication).

```python
provider_id = "ibm-secrets-manager"
provider_config_and_credentials = 
{
  "url" = "<url>", #required config
  "secret_group_id" = "<secret_group_id>", #optional config, default value is "default"
  "api_key" = "<role-id>", #required credential
}
```
This provider supports grouping of secrets with a ```secret_group_id```. The client is initialized per secret group by providing the ```secret_group_id```. If no value is provided, it defaults to "default".

#### Local SQLite
```python
provider_id = "local-sqlite"
provider_config_and_credentials = 
{
  "database" = "secrets.db", #optional config (file or in-memory storage, defaults to ":memory:")
}
```

#### Local Environment Variables
```python
provider_id = "local-environment"
provider_config_and_credentials = None
```

## Operations
All major operations for creating, updating, reading, deleting, and destroying secrets are supported across all providers as long as the client has permissions to execute the individual operations.


| |Amazon|Azure|Google|HashiCorp|IBM|Local|Environment|
|-|------|-----|------|---------|---|------|-----------|
|[Create Secret](#create-secret)|✅|✅|✅|✅|✅|✅|✅|
|[Create or Update Secret](#create-or-update-secret)|✅|✅|✅|✅|✅|✅|✅|
|[Update Secret Value](#update-secret-value)|✅|✅|✅|✅|✅|✅|✅|
|[Update Secret Metadata](#update-secret-metadata)|✅|✅|✅|✅|✅|✅|❌|
|[Delete Secret](#delete-secret)<br/>*(soft-delete if supported)*|✅|✅|✅|✅|✅|✅|✅|
|[Destroy Secret](#destroy-secret)|✅|✅|✅|✅|✅|✅|✅|
|[Get Secret Value](#get-secret-value)|✅|✅|✅|✅|✅|✅|✅|
|[Get Secret Metadata](#get-secret-metadata)|✅|✅|✅|✅|✅|✅|❌|
|[List Secret Versions](#list-secret-versions)|✅|✅|✅|✅|✅|✅|✅|
|[List Secrets](#list-secrets)<sup>1</sup>|✅|✅<sup>2</sup>|✅|✅<sup>2,3</sup>|✅|✅|❌|
|[Recover Deleted Secret](#recover-deleted-secret)|✅|✅|❌|❌|❌|✅|❌|
|[Close](#close) *(async client only)*|✅|✅|✅|✅|✅|✅|✅|

> <sup>1</sup>Support for listing all secrets and support for basic filters on names and tags.
> <sup>2</sup>Filters are executed at the client.
> <sup>3</sup>Only secret name filter is supported. Only secret names are returned, not its metadata (tags).

> See detailed implementation notes [here](docs/implementation.md).

### Create Secret
```python
create_secret(name: str, value: str, tags: Optional[dict] = None, **kwargs: Any)
```
Creates a secret in the secret store.

#### Parameters
* **name** *(str)*: Secret name.
* **value** *(str)*: Secret string.
* *(optional)* **tags** *(dict)*: Dictionary of tags (str, str pairs).

#### Returns
* *dict*
  * **name** *(str)*: Secret name.
  * **version** *(str)*: Version id of the secret value. Different providers have different ways to generate version id. However, these ids are unique to a secret and can be used to query a specific version.

#### Raises
* **SecretExistsError**: Secret name already exists. 

#### Usage
```python
# Sync
response = client.create_secret("secret-name", "secret-value", {"tag1": "123", "tag2": "abc"})
print(response.version)

# Async
response = await client.create_secret("secret-name", "secret-value", {"tag1": "123", "tag2": "abc"})
print(response.version)
```

### Create or Update Secret
```python
create_or_update_secret(name: str, value: str, tags: Optional[dict] = None, **kwargs: Any)
```
Creates or update a secret in the secret store. If the secret doesn't exist, it has the same behavior as create_secret. If the secret already exists, it creates a new version of the secret value and updates the metadata.
> **Note**: This call is more efficient than ```create_secret``` [for certain providers if you are sure the secret does not exist](docs/implementation.md). If you are sure the secret already exists, using ```update_secret_value``` and ```update_secret_metadata``` is more efficient.

#### Parameters
* **name** *(str)*: Secret name.
* **value** *(str)*: Secret string.
* *(optional)* **tags** *(dict)*: Dictionary of tags (str, str pairs).

#### Returns
* *dict*
  * **name** *(str)*: Secret name.
  * **version** *(str)*: Version id of the secret value. Different providers have different ways to generate version id. However, these ids are unique to a secret and can be used to query a specific version.

#### Usage
```python
# Sync
response = client.create_or_update_secret("secret-name", "secret-value", {"tag1": "123", "tag2": "abc"})
print(response.version)

# Async
response = await client.create_or_update_secret("secret-name", "secret-value", {"tag1": "123", "tag2": "abc"})
print(response.version)
```

### Update Secret Value
```python
update_secret(name: str, value: str, **kwargs: Any)
```
Update the value of a secret and create a new version.

#### Parameters
* **name** *(str)*: Secret name.
* **value** *(str)*: Secret string.

#### Returns
* *dict*
  * **name** *(str)*: Secret name.
  * **version** *(str)*: Version id of the secret value.

#### Raises
* **SecretNotFoundError**: Secret name is not found.

#### Usage
```python
# Sync
response = client.update_secret("secret-name", "new-secret-value")
print(response.version)

# Async
response = await client.update_secret("secret-name", "new-secret-value")
print(response.version)
```

### Update Secret Metadata
```python
update_secret_metadata(name: str, tags: dict, **kwargs: Any)
```
Update the secret tags.

#### Parameters
* **name** *(str)*: Secret name.
* **tags** *(dict)*: Key value pairs of strings.

#### Returns
* *dict*
  * **name** *(str)*: Secret name.
  * **tags** *(dict)*: Tags updated.

#### Raises
* **SecretNotFoundError**: Secret name is not found.

#### Usage
```python
# Sync
response = client.update_secret_metadata("secret-name", "new-secret-value", {"newtag1": "789", "newtag2": "xyz"})

# Async
response = await client.update_secret_metadata("secret-name", {"newtag1": "789", "newtag2": "xyz"})
```

### Destroy Secret
```python
destroy_secret(name: str, **kwargs: Any)
```
Delete the secret permanently.
> *For Amazon Secrets Manager and Azure Key Vault, destroy operation at the server is executed asynchronously, so it might take a few seconds. Creating a new secret with the same name during that time period can throw an error.

#### Parameters
* **name** *(str)*: Secret name.

#### Returns
* *None*

#### Raises
* **SecretNotFoundError**: Secret name is not found.

#### Usage
```python
# Sync
client.destroy_secret("secret-name")

# Async
await client.destroy_secret("secret-name")
```

### Get Secret Value
```python
get_secret_value(name: str, version: Optional[str] = None, **kwargs: Any)
```
Get the secret value.

#### Parameters
* **name** *(str)*: Secret name.
* *(optional)* **version** *(str)*: Secret version. If version is not specified, the latest version is returned.

#### Returns
* *dict*
  * **name** *(str)*: Secret name.
  * **version** *(str)*: Secret version.
  * **value** *(str)*: Secret value.

#### Raises
* **SecretNotFoundError**: Secret name is not found.

#### Usage
```python
# Sync
response = client.get_secret_value("secret-name", "1")
print(response.value)

# Async
response = await client.get_secret_value("secret-name", "1")
print(response.value)
```
  
### Get Secret Metadata
```python
get_secret_metadata(name: str, **kwargs: Any)
```
Get the secret metadata.

#### Parameters
* **name** *(str)*: Secret name.

#### Returns
* *dict*
  * **name** *(str)*: Secret name.
  * **tags** *(dict)*: Metadata tags associated with the secret.
  * **created_at** *(datetime)*: Creation time of the secret.

#### Raises
* **SecretNotFoundError**: Secret name is not found.

#### Usage
```python
# Sync
response = client.get_secret_metadata("secret-name")
print(response.tags)
print(response.created_at)

# Async
response = await client.get_secret_value("secret-name")
print(response.tags)
print(response.created_at)
```

### List Secret Versions
```python
list_secret_versions(name: str, **kwargs: Any)
```
List all secret versions. The latest version is the first one in the list and the oldest version is the last one.

#### Parameters
* **name** *(str)*: Secret name.

#### Returns
* *List[dict]*
  * **name** *(str)*: Secret name.
  * **version** *(str)*: Secret version.
  * **created_at** *(datetime)*: Creation time of the secret version.

#### Raises
* **SecretNotFoundError**: Secret name is not found.

#### Usage
```python
# Sync
secret_versions = client.list_secret_versions("secret-name")
for secret_version in secret_versions:
  print(secret_version)

# Async
secret_versions = await client.list_secret_versions("secret-name")
for secret_version in secret_versions:
  print(secret_version)
```

### List Secrets
```python
list_secrets(filter: Optional[dict] = None, **kwargs: Any)
```
List all secrets in the store or secrets that satisfy a filter condition. Secrets can be filtered by name prefixes and exact tag matches. When multiple filters are provided (name and tag keys), they are evaluated as an AND condition. For name and each tag key, a list of values can be provided for matching, which evaluated as an OR condition first.
> HashiCorp Vault returns only the secret names on a list operation and not the secret metadata (tags) or the created time. Hence, only name filters are supported.

> For Azure Key Vault and HashiCorp Vault, all secrets are listed and filters are applied at the client.

> Amazon Secrets Manager applies prefix matches to both tag names and tag values. Secrets are further filtered at the client to keep semantics.

> Google Secret Manager applies substring matches to names. Secrets are further filtered at the client to keep semantics.

#### Parameters
* *(optional*) filter *(dict)*: Filter by name and tags. Name filter and each of tag filter is evaluated together with an AND filter.
  * *(optional)* "name" *(List[str])*: List of prefixes to match against the name *(startswith)*. Multiple values in the list are evaluated with an OR filter.
  * *(optional)* "tags" *(dict)*: Dictionary of tags to match.
    * tag *(List[str])*: List of values to match with the tag. Tag matching is exact. Multiple values in the list are evaluated with an OR filter.   

#### Returns
* *List[dict]*
  * **name** *(str)*: Secret name.
  * **tags** *(dict)*: Secret tags.
  * **created_at** *(datetime)*: Creation time of the secret.

#### Usage
```python
# List all secrets

# Sync
secret_versions = client.list_secrets()

#Async
secrets = await client.list_secrets()

# Filter secrets
filter = { "name": ["sec"], tags: { "tag1": ["123", "456"], "tag2": ["abc"] }
# translates to 
# secret.name.startsWith("sec") and 
# (secret.tags.tag1=="123" or secret.tags.tag1=="456") and 
# secret.tags.tag2=="abc"

# Sync
secret_versions = client.list_secrets(filter)

# Async
secrets = await client.list_secrets(filter)

for secret in secrets:
  print(secret)
```

### Delete Secret
> **Note**: This is a soft-delete operation. To permanently delete a secret, use [destroy_secret](#destroy-secret).
  
```python
delete_secret(name: str, **kwargs: Any)
```
Soft-delete the secret. The secret can be recovered until the recovery time window.

#### Parameters
* **name** *(str)*: Secret name.

#### Returns
* *None*

#### Raises
* **SecretNotFoundError**: Secret name is not found.

#### Usage
```python
# Sync
client.delete_secret("secret-name")

# Async
await client.delete_secret("secret-name")
```

### Recover Deleted Secret
```python
recover_deleted_secret(name: str, **kwargs: Any)
```
Recover a secret in soft-delete state.

#### Parameters
* **name** *(str)*: Secret name.

#### Returns
* *None*

#### Raises
* **SecretNotFoundError**: Secret name is not found.

#### Usage
```python
# Sync
client.recover_deleted_secret("secret-name")

# Async
await client.recover_deleted_secret("secret-name")
```

### Destroy Deleted Secret
```python
destroy_deleted_secret(name: str, **kwargs: Any)
```
Destroy a secret in soft-delete state.

#### Parameters
* **name** *(str)*: Secret name.

#### Returns
* *None*

#### Raises
* **SecretNotFoundError**: Secret name is not found.

#### Usage
```python
# Sync
client.destroy_deleted_secret("secret-name")

# Async
await client.destroy_deleted_secret("secret-name")
```

### Close
```python
close(**kwargs: Any)
```
Close the async client. Some providers require this to close the open connections.

#### Returns
* *None*

#### Usage
```python
# Async
client = SecretStore.get_async_client(provider_id, provider_config_and_credentials)
...
await client.close()
```

## Data Limits
The data limits enforced by individual providers are detailed [here](docs/limits.md). We recommend the following limits for maximum interoperability:

|Attribute|Recommended Limit|
|---------|-----|
|Secret name| Between 1 and 127 characters long. Alphanumerics and hyphens (dash). Keep it case insensitive.|
|Secret value| Up to 25k bytes|
|Tags|Up to 15 tags. Keys must be between 1 and 63 characters long. Keys must have a UTF-8 encoding of maximum 128 bytes. Keys must begin and end with an alphanumeric character. Keys may have dashes and underscores in between the alphanumerics characters. Values can be up to 63 characters long, have a UTF-8 encoding of maximum 128 bytes. Values may have alphanumerics characters, dashes, and underscores.|
|Versions| Up to 100 versions|
|Secrets| Up to 500,000|

> **_Note_**: These limits are only recommended, not enforced. If only certain specific providers are used, the data is only limited by [the individual provider limits](docs/limits.md).

## Implementation Notes
The implementation notes for each of operation across each provider is [here](docs/implementation.md).
