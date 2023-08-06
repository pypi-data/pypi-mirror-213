"""
Type annotations for verifiedpermissions service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_verifiedpermissions/type_defs/)

Usage::

    ```python
    from mypy_boto3_verifiedpermissions.type_defs import ActionIdentifierTypeDef

    data: ActionIdentifierTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence

from .literals import DecisionType, PolicyTypeType, ValidationModeType

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "ActionIdentifierTypeDef",
    "EntityIdentifierTypeDef",
    "CognitoUserPoolConfigurationTypeDef",
    "ContextDefinitionTypeDef",
    "ResponseMetadataTypeDef",
    "ValidationSettingsTypeDef",
    "CreatePolicyTemplateInputRequestTypeDef",
    "DeleteIdentitySourceInputRequestTypeDef",
    "DeletePolicyInputRequestTypeDef",
    "DeletePolicyStoreInputRequestTypeDef",
    "DeletePolicyTemplateInputRequestTypeDef",
    "DeterminingPolicyItemTypeDef",
    "EvaluationErrorItemTypeDef",
    "GetIdentitySourceInputRequestTypeDef",
    "IdentitySourceDetailsTypeDef",
    "GetPolicyInputRequestTypeDef",
    "GetPolicyStoreInputRequestTypeDef",
    "GetPolicyTemplateInputRequestTypeDef",
    "GetSchemaInputRequestTypeDef",
    "IdentitySourceFilterTypeDef",
    "IdentitySourceItemDetailsTypeDef",
    "PaginatorConfigTypeDef",
    "ListPolicyStoresInputRequestTypeDef",
    "PolicyStoreItemTypeDef",
    "ListPolicyTemplatesInputRequestTypeDef",
    "PolicyTemplateItemTypeDef",
    "StaticPolicyDefinitionDetailTypeDef",
    "StaticPolicyDefinitionItemTypeDef",
    "StaticPolicyDefinitionTypeDef",
    "SchemaDefinitionTypeDef",
    "UpdateCognitoUserPoolConfigurationTypeDef",
    "UpdateStaticPolicyDefinitionTypeDef",
    "UpdatePolicyTemplateInputRequestTypeDef",
    "AttributeValueTypeDef",
    "EntityItemTypeDef",
    "EntityReferenceTypeDef",
    "TemplateLinkedPolicyDefinitionDetailTypeDef",
    "TemplateLinkedPolicyDefinitionItemTypeDef",
    "TemplateLinkedPolicyDefinitionTypeDef",
    "ConfigurationTypeDef",
    "CreateIdentitySourceOutputTypeDef",
    "CreatePolicyOutputTypeDef",
    "CreatePolicyStoreOutputTypeDef",
    "CreatePolicyTemplateOutputTypeDef",
    "GetPolicyTemplateOutputTypeDef",
    "GetSchemaOutputTypeDef",
    "PutSchemaOutputTypeDef",
    "UpdateIdentitySourceOutputTypeDef",
    "UpdatePolicyOutputTypeDef",
    "UpdatePolicyStoreOutputTypeDef",
    "UpdatePolicyTemplateOutputTypeDef",
    "CreatePolicyStoreInputRequestTypeDef",
    "GetPolicyStoreOutputTypeDef",
    "UpdatePolicyStoreInputRequestTypeDef",
    "IsAuthorizedOutputTypeDef",
    "IsAuthorizedWithTokenOutputTypeDef",
    "GetIdentitySourceOutputTypeDef",
    "ListIdentitySourcesInputRequestTypeDef",
    "IdentitySourceItemTypeDef",
    "ListIdentitySourcesInputListIdentitySourcesPaginateTypeDef",
    "ListPolicyStoresInputListPolicyStoresPaginateTypeDef",
    "ListPolicyTemplatesInputListPolicyTemplatesPaginateTypeDef",
    "ListPolicyStoresOutputTypeDef",
    "ListPolicyTemplatesOutputTypeDef",
    "PutSchemaInputRequestTypeDef",
    "UpdateConfigurationTypeDef",
    "UpdatePolicyDefinitionTypeDef",
    "EntitiesDefinitionTypeDef",
    "PolicyFilterTypeDef",
    "PolicyDefinitionDetailTypeDef",
    "PolicyDefinitionItemTypeDef",
    "PolicyDefinitionTypeDef",
    "CreateIdentitySourceInputRequestTypeDef",
    "ListIdentitySourcesOutputTypeDef",
    "UpdateIdentitySourceInputRequestTypeDef",
    "UpdatePolicyInputRequestTypeDef",
    "IsAuthorizedInputRequestTypeDef",
    "IsAuthorizedWithTokenInputRequestTypeDef",
    "ListPoliciesInputListPoliciesPaginateTypeDef",
    "ListPoliciesInputRequestTypeDef",
    "GetPolicyOutputTypeDef",
    "PolicyItemTypeDef",
    "CreatePolicyInputRequestTypeDef",
    "ListPoliciesOutputTypeDef",
)

ActionIdentifierTypeDef = TypedDict(
    "ActionIdentifierTypeDef",
    {
        "actionType": str,
        "actionId": str,
    },
)

EntityIdentifierTypeDef = TypedDict(
    "EntityIdentifierTypeDef",
    {
        "entityType": str,
        "entityId": str,
    },
)

_RequiredCognitoUserPoolConfigurationTypeDef = TypedDict(
    "_RequiredCognitoUserPoolConfigurationTypeDef",
    {
        "userPoolArn": str,
    },
)
_OptionalCognitoUserPoolConfigurationTypeDef = TypedDict(
    "_OptionalCognitoUserPoolConfigurationTypeDef",
    {
        "clientIds": Sequence[str],
    },
    total=False,
)

class CognitoUserPoolConfigurationTypeDef(
    _RequiredCognitoUserPoolConfigurationTypeDef, _OptionalCognitoUserPoolConfigurationTypeDef
):
    pass

ContextDefinitionTypeDef = TypedDict(
    "ContextDefinitionTypeDef",
    {
        "contextMap": Mapping[str, "AttributeValueTypeDef"],
    },
    total=False,
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

ValidationSettingsTypeDef = TypedDict(
    "ValidationSettingsTypeDef",
    {
        "mode": ValidationModeType,
    },
)

_RequiredCreatePolicyTemplateInputRequestTypeDef = TypedDict(
    "_RequiredCreatePolicyTemplateInputRequestTypeDef",
    {
        "policyStoreId": str,
        "statement": str,
    },
)
_OptionalCreatePolicyTemplateInputRequestTypeDef = TypedDict(
    "_OptionalCreatePolicyTemplateInputRequestTypeDef",
    {
        "clientToken": str,
        "description": str,
    },
    total=False,
)

class CreatePolicyTemplateInputRequestTypeDef(
    _RequiredCreatePolicyTemplateInputRequestTypeDef,
    _OptionalCreatePolicyTemplateInputRequestTypeDef,
):
    pass

DeleteIdentitySourceInputRequestTypeDef = TypedDict(
    "DeleteIdentitySourceInputRequestTypeDef",
    {
        "policyStoreId": str,
        "identitySourceId": str,
    },
)

DeletePolicyInputRequestTypeDef = TypedDict(
    "DeletePolicyInputRequestTypeDef",
    {
        "policyStoreId": str,
        "policyId": str,
    },
)

DeletePolicyStoreInputRequestTypeDef = TypedDict(
    "DeletePolicyStoreInputRequestTypeDef",
    {
        "policyStoreId": str,
    },
)

DeletePolicyTemplateInputRequestTypeDef = TypedDict(
    "DeletePolicyTemplateInputRequestTypeDef",
    {
        "policyStoreId": str,
        "policyTemplateId": str,
    },
)

DeterminingPolicyItemTypeDef = TypedDict(
    "DeterminingPolicyItemTypeDef",
    {
        "policyId": str,
    },
)

EvaluationErrorItemTypeDef = TypedDict(
    "EvaluationErrorItemTypeDef",
    {
        "errorDescription": str,
    },
)

GetIdentitySourceInputRequestTypeDef = TypedDict(
    "GetIdentitySourceInputRequestTypeDef",
    {
        "policyStoreId": str,
        "identitySourceId": str,
    },
)

IdentitySourceDetailsTypeDef = TypedDict(
    "IdentitySourceDetailsTypeDef",
    {
        "clientIds": List[str],
        "userPoolArn": str,
        "discoveryUrl": str,
        "openIdIssuer": Literal["COGNITO"],
    },
    total=False,
)

GetPolicyInputRequestTypeDef = TypedDict(
    "GetPolicyInputRequestTypeDef",
    {
        "policyStoreId": str,
        "policyId": str,
    },
)

GetPolicyStoreInputRequestTypeDef = TypedDict(
    "GetPolicyStoreInputRequestTypeDef",
    {
        "policyStoreId": str,
    },
)

GetPolicyTemplateInputRequestTypeDef = TypedDict(
    "GetPolicyTemplateInputRequestTypeDef",
    {
        "policyStoreId": str,
        "policyTemplateId": str,
    },
)

GetSchemaInputRequestTypeDef = TypedDict(
    "GetSchemaInputRequestTypeDef",
    {
        "policyStoreId": str,
    },
)

IdentitySourceFilterTypeDef = TypedDict(
    "IdentitySourceFilterTypeDef",
    {
        "principalEntityType": str,
    },
    total=False,
)

IdentitySourceItemDetailsTypeDef = TypedDict(
    "IdentitySourceItemDetailsTypeDef",
    {
        "clientIds": List[str],
        "userPoolArn": str,
        "discoveryUrl": str,
        "openIdIssuer": Literal["COGNITO"],
    },
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

ListPolicyStoresInputRequestTypeDef = TypedDict(
    "ListPolicyStoresInputRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

PolicyStoreItemTypeDef = TypedDict(
    "PolicyStoreItemTypeDef",
    {
        "policyStoreId": str,
        "arn": str,
        "createdDate": datetime,
    },
)

_RequiredListPolicyTemplatesInputRequestTypeDef = TypedDict(
    "_RequiredListPolicyTemplatesInputRequestTypeDef",
    {
        "policyStoreId": str,
    },
)
_OptionalListPolicyTemplatesInputRequestTypeDef = TypedDict(
    "_OptionalListPolicyTemplatesInputRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

class ListPolicyTemplatesInputRequestTypeDef(
    _RequiredListPolicyTemplatesInputRequestTypeDef, _OptionalListPolicyTemplatesInputRequestTypeDef
):
    pass

_RequiredPolicyTemplateItemTypeDef = TypedDict(
    "_RequiredPolicyTemplateItemTypeDef",
    {
        "policyStoreId": str,
        "policyTemplateId": str,
        "createdDate": datetime,
        "lastUpdatedDate": datetime,
    },
)
_OptionalPolicyTemplateItemTypeDef = TypedDict(
    "_OptionalPolicyTemplateItemTypeDef",
    {
        "description": str,
    },
    total=False,
)

class PolicyTemplateItemTypeDef(
    _RequiredPolicyTemplateItemTypeDef, _OptionalPolicyTemplateItemTypeDef
):
    pass

_RequiredStaticPolicyDefinitionDetailTypeDef = TypedDict(
    "_RequiredStaticPolicyDefinitionDetailTypeDef",
    {
        "statement": str,
    },
)
_OptionalStaticPolicyDefinitionDetailTypeDef = TypedDict(
    "_OptionalStaticPolicyDefinitionDetailTypeDef",
    {
        "description": str,
    },
    total=False,
)

class StaticPolicyDefinitionDetailTypeDef(
    _RequiredStaticPolicyDefinitionDetailTypeDef, _OptionalStaticPolicyDefinitionDetailTypeDef
):
    pass

StaticPolicyDefinitionItemTypeDef = TypedDict(
    "StaticPolicyDefinitionItemTypeDef",
    {
        "description": str,
    },
    total=False,
)

_RequiredStaticPolicyDefinitionTypeDef = TypedDict(
    "_RequiredStaticPolicyDefinitionTypeDef",
    {
        "statement": str,
    },
)
_OptionalStaticPolicyDefinitionTypeDef = TypedDict(
    "_OptionalStaticPolicyDefinitionTypeDef",
    {
        "description": str,
    },
    total=False,
)

class StaticPolicyDefinitionTypeDef(
    _RequiredStaticPolicyDefinitionTypeDef, _OptionalStaticPolicyDefinitionTypeDef
):
    pass

SchemaDefinitionTypeDef = TypedDict(
    "SchemaDefinitionTypeDef",
    {
        "cedarJson": str,
    },
    total=False,
)

_RequiredUpdateCognitoUserPoolConfigurationTypeDef = TypedDict(
    "_RequiredUpdateCognitoUserPoolConfigurationTypeDef",
    {
        "userPoolArn": str,
    },
)
_OptionalUpdateCognitoUserPoolConfigurationTypeDef = TypedDict(
    "_OptionalUpdateCognitoUserPoolConfigurationTypeDef",
    {
        "clientIds": Sequence[str],
    },
    total=False,
)

class UpdateCognitoUserPoolConfigurationTypeDef(
    _RequiredUpdateCognitoUserPoolConfigurationTypeDef,
    _OptionalUpdateCognitoUserPoolConfigurationTypeDef,
):
    pass

_RequiredUpdateStaticPolicyDefinitionTypeDef = TypedDict(
    "_RequiredUpdateStaticPolicyDefinitionTypeDef",
    {
        "statement": str,
    },
)
_OptionalUpdateStaticPolicyDefinitionTypeDef = TypedDict(
    "_OptionalUpdateStaticPolicyDefinitionTypeDef",
    {
        "description": str,
    },
    total=False,
)

class UpdateStaticPolicyDefinitionTypeDef(
    _RequiredUpdateStaticPolicyDefinitionTypeDef, _OptionalUpdateStaticPolicyDefinitionTypeDef
):
    pass

_RequiredUpdatePolicyTemplateInputRequestTypeDef = TypedDict(
    "_RequiredUpdatePolicyTemplateInputRequestTypeDef",
    {
        "policyStoreId": str,
        "policyTemplateId": str,
        "statement": str,
    },
)
_OptionalUpdatePolicyTemplateInputRequestTypeDef = TypedDict(
    "_OptionalUpdatePolicyTemplateInputRequestTypeDef",
    {
        "description": str,
    },
    total=False,
)

class UpdatePolicyTemplateInputRequestTypeDef(
    _RequiredUpdatePolicyTemplateInputRequestTypeDef,
    _OptionalUpdatePolicyTemplateInputRequestTypeDef,
):
    pass

AttributeValueTypeDef = TypedDict(
    "AttributeValueTypeDef",
    {
        "boolean": bool,
        "entityIdentifier": EntityIdentifierTypeDef,
        "long": int,
        "string": str,
        "set": Sequence[Dict[str, Any]],
        "record": Mapping[str, Dict[str, Any]],
    },
    total=False,
)

_RequiredEntityItemTypeDef = TypedDict(
    "_RequiredEntityItemTypeDef",
    {
        "identifier": EntityIdentifierTypeDef,
    },
)
_OptionalEntityItemTypeDef = TypedDict(
    "_OptionalEntityItemTypeDef",
    {
        "attributes": Mapping[str, "AttributeValueTypeDef"],
        "parents": Sequence[EntityIdentifierTypeDef],
    },
    total=False,
)

class EntityItemTypeDef(_RequiredEntityItemTypeDef, _OptionalEntityItemTypeDef):
    pass

EntityReferenceTypeDef = TypedDict(
    "EntityReferenceTypeDef",
    {
        "unspecified": bool,
        "identifier": EntityIdentifierTypeDef,
    },
    total=False,
)

_RequiredTemplateLinkedPolicyDefinitionDetailTypeDef = TypedDict(
    "_RequiredTemplateLinkedPolicyDefinitionDetailTypeDef",
    {
        "policyTemplateId": str,
    },
)
_OptionalTemplateLinkedPolicyDefinitionDetailTypeDef = TypedDict(
    "_OptionalTemplateLinkedPolicyDefinitionDetailTypeDef",
    {
        "principal": EntityIdentifierTypeDef,
        "resource": EntityIdentifierTypeDef,
    },
    total=False,
)

class TemplateLinkedPolicyDefinitionDetailTypeDef(
    _RequiredTemplateLinkedPolicyDefinitionDetailTypeDef,
    _OptionalTemplateLinkedPolicyDefinitionDetailTypeDef,
):
    pass

_RequiredTemplateLinkedPolicyDefinitionItemTypeDef = TypedDict(
    "_RequiredTemplateLinkedPolicyDefinitionItemTypeDef",
    {
        "policyTemplateId": str,
    },
)
_OptionalTemplateLinkedPolicyDefinitionItemTypeDef = TypedDict(
    "_OptionalTemplateLinkedPolicyDefinitionItemTypeDef",
    {
        "principal": EntityIdentifierTypeDef,
        "resource": EntityIdentifierTypeDef,
    },
    total=False,
)

class TemplateLinkedPolicyDefinitionItemTypeDef(
    _RequiredTemplateLinkedPolicyDefinitionItemTypeDef,
    _OptionalTemplateLinkedPolicyDefinitionItemTypeDef,
):
    pass

_RequiredTemplateLinkedPolicyDefinitionTypeDef = TypedDict(
    "_RequiredTemplateLinkedPolicyDefinitionTypeDef",
    {
        "policyTemplateId": str,
    },
)
_OptionalTemplateLinkedPolicyDefinitionTypeDef = TypedDict(
    "_OptionalTemplateLinkedPolicyDefinitionTypeDef",
    {
        "principal": EntityIdentifierTypeDef,
        "resource": EntityIdentifierTypeDef,
    },
    total=False,
)

class TemplateLinkedPolicyDefinitionTypeDef(
    _RequiredTemplateLinkedPolicyDefinitionTypeDef, _OptionalTemplateLinkedPolicyDefinitionTypeDef
):
    pass

ConfigurationTypeDef = TypedDict(
    "ConfigurationTypeDef",
    {
        "cognitoUserPoolConfiguration": CognitoUserPoolConfigurationTypeDef,
    },
    total=False,
)

CreateIdentitySourceOutputTypeDef = TypedDict(
    "CreateIdentitySourceOutputTypeDef",
    {
        "createdDate": datetime,
        "identitySourceId": str,
        "lastUpdatedDate": datetime,
        "policyStoreId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreatePolicyOutputTypeDef = TypedDict(
    "CreatePolicyOutputTypeDef",
    {
        "policyStoreId": str,
        "policyId": str,
        "policyType": PolicyTypeType,
        "principal": EntityIdentifierTypeDef,
        "resource": EntityIdentifierTypeDef,
        "createdDate": datetime,
        "lastUpdatedDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreatePolicyStoreOutputTypeDef = TypedDict(
    "CreatePolicyStoreOutputTypeDef",
    {
        "policyStoreId": str,
        "arn": str,
        "createdDate": datetime,
        "lastUpdatedDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreatePolicyTemplateOutputTypeDef = TypedDict(
    "CreatePolicyTemplateOutputTypeDef",
    {
        "policyStoreId": str,
        "policyTemplateId": str,
        "createdDate": datetime,
        "lastUpdatedDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPolicyTemplateOutputTypeDef = TypedDict(
    "GetPolicyTemplateOutputTypeDef",
    {
        "policyStoreId": str,
        "policyTemplateId": str,
        "description": str,
        "statement": str,
        "createdDate": datetime,
        "lastUpdatedDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSchemaOutputTypeDef = TypedDict(
    "GetSchemaOutputTypeDef",
    {
        "policyStoreId": str,
        "schema": str,
        "createdDate": datetime,
        "lastUpdatedDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutSchemaOutputTypeDef = TypedDict(
    "PutSchemaOutputTypeDef",
    {
        "policyStoreId": str,
        "namespaces": List[str],
        "createdDate": datetime,
        "lastUpdatedDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateIdentitySourceOutputTypeDef = TypedDict(
    "UpdateIdentitySourceOutputTypeDef",
    {
        "createdDate": datetime,
        "identitySourceId": str,
        "lastUpdatedDate": datetime,
        "policyStoreId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdatePolicyOutputTypeDef = TypedDict(
    "UpdatePolicyOutputTypeDef",
    {
        "policyStoreId": str,
        "policyId": str,
        "policyType": PolicyTypeType,
        "principal": EntityIdentifierTypeDef,
        "resource": EntityIdentifierTypeDef,
        "createdDate": datetime,
        "lastUpdatedDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdatePolicyStoreOutputTypeDef = TypedDict(
    "UpdatePolicyStoreOutputTypeDef",
    {
        "policyStoreId": str,
        "arn": str,
        "createdDate": datetime,
        "lastUpdatedDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdatePolicyTemplateOutputTypeDef = TypedDict(
    "UpdatePolicyTemplateOutputTypeDef",
    {
        "policyStoreId": str,
        "policyTemplateId": str,
        "createdDate": datetime,
        "lastUpdatedDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreatePolicyStoreInputRequestTypeDef = TypedDict(
    "_RequiredCreatePolicyStoreInputRequestTypeDef",
    {
        "validationSettings": ValidationSettingsTypeDef,
    },
)
_OptionalCreatePolicyStoreInputRequestTypeDef = TypedDict(
    "_OptionalCreatePolicyStoreInputRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)

class CreatePolicyStoreInputRequestTypeDef(
    _RequiredCreatePolicyStoreInputRequestTypeDef, _OptionalCreatePolicyStoreInputRequestTypeDef
):
    pass

GetPolicyStoreOutputTypeDef = TypedDict(
    "GetPolicyStoreOutputTypeDef",
    {
        "policyStoreId": str,
        "arn": str,
        "validationSettings": ValidationSettingsTypeDef,
        "createdDate": datetime,
        "lastUpdatedDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdatePolicyStoreInputRequestTypeDef = TypedDict(
    "UpdatePolicyStoreInputRequestTypeDef",
    {
        "policyStoreId": str,
        "validationSettings": ValidationSettingsTypeDef,
    },
)

IsAuthorizedOutputTypeDef = TypedDict(
    "IsAuthorizedOutputTypeDef",
    {
        "decision": DecisionType,
        "determiningPolicies": List[DeterminingPolicyItemTypeDef],
        "errors": List[EvaluationErrorItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

IsAuthorizedWithTokenOutputTypeDef = TypedDict(
    "IsAuthorizedWithTokenOutputTypeDef",
    {
        "decision": DecisionType,
        "determiningPolicies": List[DeterminingPolicyItemTypeDef],
        "errors": List[EvaluationErrorItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetIdentitySourceOutputTypeDef = TypedDict(
    "GetIdentitySourceOutputTypeDef",
    {
        "createdDate": datetime,
        "details": IdentitySourceDetailsTypeDef,
        "identitySourceId": str,
        "lastUpdatedDate": datetime,
        "policyStoreId": str,
        "principalEntityType": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListIdentitySourcesInputRequestTypeDef = TypedDict(
    "_RequiredListIdentitySourcesInputRequestTypeDef",
    {
        "policyStoreId": str,
    },
)
_OptionalListIdentitySourcesInputRequestTypeDef = TypedDict(
    "_OptionalListIdentitySourcesInputRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
        "filters": Sequence[IdentitySourceFilterTypeDef],
    },
    total=False,
)

class ListIdentitySourcesInputRequestTypeDef(
    _RequiredListIdentitySourcesInputRequestTypeDef, _OptionalListIdentitySourcesInputRequestTypeDef
):
    pass

IdentitySourceItemTypeDef = TypedDict(
    "IdentitySourceItemTypeDef",
    {
        "createdDate": datetime,
        "details": IdentitySourceItemDetailsTypeDef,
        "identitySourceId": str,
        "lastUpdatedDate": datetime,
        "policyStoreId": str,
        "principalEntityType": str,
    },
)

_RequiredListIdentitySourcesInputListIdentitySourcesPaginateTypeDef = TypedDict(
    "_RequiredListIdentitySourcesInputListIdentitySourcesPaginateTypeDef",
    {
        "policyStoreId": str,
    },
)
_OptionalListIdentitySourcesInputListIdentitySourcesPaginateTypeDef = TypedDict(
    "_OptionalListIdentitySourcesInputListIdentitySourcesPaginateTypeDef",
    {
        "filters": Sequence[IdentitySourceFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListIdentitySourcesInputListIdentitySourcesPaginateTypeDef(
    _RequiredListIdentitySourcesInputListIdentitySourcesPaginateTypeDef,
    _OptionalListIdentitySourcesInputListIdentitySourcesPaginateTypeDef,
):
    pass

ListPolicyStoresInputListPolicyStoresPaginateTypeDef = TypedDict(
    "ListPolicyStoresInputListPolicyStoresPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListPolicyTemplatesInputListPolicyTemplatesPaginateTypeDef = TypedDict(
    "_RequiredListPolicyTemplatesInputListPolicyTemplatesPaginateTypeDef",
    {
        "policyStoreId": str,
    },
)
_OptionalListPolicyTemplatesInputListPolicyTemplatesPaginateTypeDef = TypedDict(
    "_OptionalListPolicyTemplatesInputListPolicyTemplatesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListPolicyTemplatesInputListPolicyTemplatesPaginateTypeDef(
    _RequiredListPolicyTemplatesInputListPolicyTemplatesPaginateTypeDef,
    _OptionalListPolicyTemplatesInputListPolicyTemplatesPaginateTypeDef,
):
    pass

ListPolicyStoresOutputTypeDef = TypedDict(
    "ListPolicyStoresOutputTypeDef",
    {
        "nextToken": str,
        "policyStores": List[PolicyStoreItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPolicyTemplatesOutputTypeDef = TypedDict(
    "ListPolicyTemplatesOutputTypeDef",
    {
        "nextToken": str,
        "policyTemplates": List[PolicyTemplateItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutSchemaInputRequestTypeDef = TypedDict(
    "PutSchemaInputRequestTypeDef",
    {
        "policyStoreId": str,
        "definition": SchemaDefinitionTypeDef,
    },
)

UpdateConfigurationTypeDef = TypedDict(
    "UpdateConfigurationTypeDef",
    {
        "cognitoUserPoolConfiguration": UpdateCognitoUserPoolConfigurationTypeDef,
    },
    total=False,
)

UpdatePolicyDefinitionTypeDef = TypedDict(
    "UpdatePolicyDefinitionTypeDef",
    {
        "static": UpdateStaticPolicyDefinitionTypeDef,
    },
    total=False,
)

EntitiesDefinitionTypeDef = TypedDict(
    "EntitiesDefinitionTypeDef",
    {
        "entityList": Sequence[EntityItemTypeDef],
    },
    total=False,
)

PolicyFilterTypeDef = TypedDict(
    "PolicyFilterTypeDef",
    {
        "principal": EntityReferenceTypeDef,
        "resource": EntityReferenceTypeDef,
        "policyType": PolicyTypeType,
        "policyTemplateId": str,
    },
    total=False,
)

PolicyDefinitionDetailTypeDef = TypedDict(
    "PolicyDefinitionDetailTypeDef",
    {
        "static": StaticPolicyDefinitionDetailTypeDef,
        "templateLinked": TemplateLinkedPolicyDefinitionDetailTypeDef,
    },
    total=False,
)

PolicyDefinitionItemTypeDef = TypedDict(
    "PolicyDefinitionItemTypeDef",
    {
        "static": StaticPolicyDefinitionItemTypeDef,
        "templateLinked": TemplateLinkedPolicyDefinitionItemTypeDef,
    },
    total=False,
)

PolicyDefinitionTypeDef = TypedDict(
    "PolicyDefinitionTypeDef",
    {
        "static": StaticPolicyDefinitionTypeDef,
        "templateLinked": TemplateLinkedPolicyDefinitionTypeDef,
    },
    total=False,
)

_RequiredCreateIdentitySourceInputRequestTypeDef = TypedDict(
    "_RequiredCreateIdentitySourceInputRequestTypeDef",
    {
        "policyStoreId": str,
        "configuration": ConfigurationTypeDef,
    },
)
_OptionalCreateIdentitySourceInputRequestTypeDef = TypedDict(
    "_OptionalCreateIdentitySourceInputRequestTypeDef",
    {
        "clientToken": str,
        "principalEntityType": str,
    },
    total=False,
)

class CreateIdentitySourceInputRequestTypeDef(
    _RequiredCreateIdentitySourceInputRequestTypeDef,
    _OptionalCreateIdentitySourceInputRequestTypeDef,
):
    pass

ListIdentitySourcesOutputTypeDef = TypedDict(
    "ListIdentitySourcesOutputTypeDef",
    {
        "nextToken": str,
        "identitySources": List[IdentitySourceItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateIdentitySourceInputRequestTypeDef = TypedDict(
    "_RequiredUpdateIdentitySourceInputRequestTypeDef",
    {
        "policyStoreId": str,
        "identitySourceId": str,
        "updateConfiguration": UpdateConfigurationTypeDef,
    },
)
_OptionalUpdateIdentitySourceInputRequestTypeDef = TypedDict(
    "_OptionalUpdateIdentitySourceInputRequestTypeDef",
    {
        "principalEntityType": str,
    },
    total=False,
)

class UpdateIdentitySourceInputRequestTypeDef(
    _RequiredUpdateIdentitySourceInputRequestTypeDef,
    _OptionalUpdateIdentitySourceInputRequestTypeDef,
):
    pass

UpdatePolicyInputRequestTypeDef = TypedDict(
    "UpdatePolicyInputRequestTypeDef",
    {
        "policyStoreId": str,
        "policyId": str,
        "definition": UpdatePolicyDefinitionTypeDef,
    },
)

_RequiredIsAuthorizedInputRequestTypeDef = TypedDict(
    "_RequiredIsAuthorizedInputRequestTypeDef",
    {
        "policyStoreId": str,
    },
)
_OptionalIsAuthorizedInputRequestTypeDef = TypedDict(
    "_OptionalIsAuthorizedInputRequestTypeDef",
    {
        "principal": EntityIdentifierTypeDef,
        "action": ActionIdentifierTypeDef,
        "resource": EntityIdentifierTypeDef,
        "context": ContextDefinitionTypeDef,
        "entities": EntitiesDefinitionTypeDef,
    },
    total=False,
)

class IsAuthorizedInputRequestTypeDef(
    _RequiredIsAuthorizedInputRequestTypeDef, _OptionalIsAuthorizedInputRequestTypeDef
):
    pass

_RequiredIsAuthorizedWithTokenInputRequestTypeDef = TypedDict(
    "_RequiredIsAuthorizedWithTokenInputRequestTypeDef",
    {
        "policyStoreId": str,
    },
)
_OptionalIsAuthorizedWithTokenInputRequestTypeDef = TypedDict(
    "_OptionalIsAuthorizedWithTokenInputRequestTypeDef",
    {
        "identityToken": str,
        "accessToken": str,
        "action": ActionIdentifierTypeDef,
        "resource": EntityIdentifierTypeDef,
        "context": ContextDefinitionTypeDef,
        "entities": EntitiesDefinitionTypeDef,
    },
    total=False,
)

class IsAuthorizedWithTokenInputRequestTypeDef(
    _RequiredIsAuthorizedWithTokenInputRequestTypeDef,
    _OptionalIsAuthorizedWithTokenInputRequestTypeDef,
):
    pass

_RequiredListPoliciesInputListPoliciesPaginateTypeDef = TypedDict(
    "_RequiredListPoliciesInputListPoliciesPaginateTypeDef",
    {
        "policyStoreId": str,
    },
)
_OptionalListPoliciesInputListPoliciesPaginateTypeDef = TypedDict(
    "_OptionalListPoliciesInputListPoliciesPaginateTypeDef",
    {
        "filter": PolicyFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListPoliciesInputListPoliciesPaginateTypeDef(
    _RequiredListPoliciesInputListPoliciesPaginateTypeDef,
    _OptionalListPoliciesInputListPoliciesPaginateTypeDef,
):
    pass

_RequiredListPoliciesInputRequestTypeDef = TypedDict(
    "_RequiredListPoliciesInputRequestTypeDef",
    {
        "policyStoreId": str,
    },
)
_OptionalListPoliciesInputRequestTypeDef = TypedDict(
    "_OptionalListPoliciesInputRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
        "filter": PolicyFilterTypeDef,
    },
    total=False,
)

class ListPoliciesInputRequestTypeDef(
    _RequiredListPoliciesInputRequestTypeDef, _OptionalListPoliciesInputRequestTypeDef
):
    pass

GetPolicyOutputTypeDef = TypedDict(
    "GetPolicyOutputTypeDef",
    {
        "policyStoreId": str,
        "policyId": str,
        "policyType": PolicyTypeType,
        "principal": EntityIdentifierTypeDef,
        "resource": EntityIdentifierTypeDef,
        "definition": PolicyDefinitionDetailTypeDef,
        "createdDate": datetime,
        "lastUpdatedDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPolicyItemTypeDef = TypedDict(
    "_RequiredPolicyItemTypeDef",
    {
        "policyStoreId": str,
        "policyId": str,
        "policyType": PolicyTypeType,
        "definition": PolicyDefinitionItemTypeDef,
        "createdDate": datetime,
        "lastUpdatedDate": datetime,
    },
)
_OptionalPolicyItemTypeDef = TypedDict(
    "_OptionalPolicyItemTypeDef",
    {
        "principal": EntityIdentifierTypeDef,
        "resource": EntityIdentifierTypeDef,
    },
    total=False,
)

class PolicyItemTypeDef(_RequiredPolicyItemTypeDef, _OptionalPolicyItemTypeDef):
    pass

_RequiredCreatePolicyInputRequestTypeDef = TypedDict(
    "_RequiredCreatePolicyInputRequestTypeDef",
    {
        "policyStoreId": str,
        "definition": PolicyDefinitionTypeDef,
    },
)
_OptionalCreatePolicyInputRequestTypeDef = TypedDict(
    "_OptionalCreatePolicyInputRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)

class CreatePolicyInputRequestTypeDef(
    _RequiredCreatePolicyInputRequestTypeDef, _OptionalCreatePolicyInputRequestTypeDef
):
    pass

ListPoliciesOutputTypeDef = TypedDict(
    "ListPoliciesOutputTypeDef",
    {
        "nextToken": str,
        "policies": List[PolicyItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
