from datetime import datetime
from typing import Annotated, Literal, Optional, Union

from pydantic import Field

from validio_sdk.scalars import CredentialId

from .base_model import BaseModel


class GetCredentialByResourceName(BaseModel):
    credential_by_resource_name: Optional[
        Annotated[
            Union[
                "GetCredentialByResourceNameCredentialByResourceNameCredential",
                "GetCredentialByResourceNameCredentialByResourceNameAwsCredential",
                "GetCredentialByResourceNameCredentialByResourceNameAwsRedshiftCredential",
                "GetCredentialByResourceNameCredentialByResourceNamePostgreSqlCredential",
                "GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredential",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="credentialByResourceName")


class GetCredentialByResourceNameCredentialByResourceNameCredential(BaseModel):
    typename__: Literal["Credential", "DemoCredential", "GcpCredential"] = Field(
        alias="__typename"
    )
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetCredentialByResourceNameCredentialByResourceNameAwsCredential(BaseModel):
    typename__: Literal["AwsCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetCredentialByResourceNameCredentialByResourceNameAwsCredentialConfig"


class GetCredentialByResourceNameCredentialByResourceNameAwsCredentialConfig(BaseModel):
    access_key: str = Field(alias="accessKey")


class GetCredentialByResourceNameCredentialByResourceNameAwsRedshiftCredential(
    BaseModel
):
    typename__: Literal["AwsRedshiftCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetCredentialByResourceNameCredentialByResourceNameAwsRedshiftCredentialConfig"


class GetCredentialByResourceNameCredentialByResourceNameAwsRedshiftCredentialConfig(
    BaseModel
):
    host: str
    port: int
    user: str
    default_database: str = Field(alias="defaultDatabase")


class GetCredentialByResourceNameCredentialByResourceNamePostgreSqlCredential(
    BaseModel
):
    typename__: Literal["PostgreSqlCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetCredentialByResourceNameCredentialByResourceNamePostgreSqlCredentialConfig"


class GetCredentialByResourceNameCredentialByResourceNamePostgreSqlCredentialConfig(
    BaseModel
):
    host: str
    port: int
    user: str
    default_database: str = Field(alias="defaultDatabase")


class GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredential(BaseModel):
    typename__: Literal["SnowflakeCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredentialConfig"


class GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredentialConfig(
    BaseModel
):
    account: str
    user: str


GetCredentialByResourceName.update_forward_refs()
GetCredentialByResourceNameCredentialByResourceNameCredential.update_forward_refs()
GetCredentialByResourceNameCredentialByResourceNameAwsCredential.update_forward_refs()
GetCredentialByResourceNameCredentialByResourceNameAwsCredentialConfig.update_forward_refs()
GetCredentialByResourceNameCredentialByResourceNameAwsRedshiftCredential.update_forward_refs()
GetCredentialByResourceNameCredentialByResourceNameAwsRedshiftCredentialConfig.update_forward_refs()
GetCredentialByResourceNameCredentialByResourceNamePostgreSqlCredential.update_forward_refs()
GetCredentialByResourceNameCredentialByResourceNamePostgreSqlCredentialConfig.update_forward_refs()
GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredential.update_forward_refs()
GetCredentialByResourceNameCredentialByResourceNameSnowflakeCredentialConfig.update_forward_refs()
