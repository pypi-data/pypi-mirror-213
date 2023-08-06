'''
# newrelic-observability-ainotificationschannel

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `NewRelic::Observability::AINotificationsChannel` v1.0.0.

## Description

CRUD operations for New Relic AI Notifications Channels via the NerdGraph API

## References

* [Source](https://github.com/newrelic/newrelic-cloudformation-resource-providers-ainotificationschannel.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name NewRelic::Observability::AINotificationsChannel \
  --publisher-id 759f81f13de188bad7cafc8a2d50910f7d5e2bcc \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/759f81f13de188bad7cafc8a2d50910f7d5e2bcc/NewRelic-Observability-AINotificationsChannel \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `NewRelic::Observability::AINotificationsChannel`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fnewrelic-observability-ainotificationschannel+v1.0.0).
* Issues related to `NewRelic::Observability::AINotificationsChannel` should be reported to the [publisher](https://github.com/newrelic/newrelic-cloudformation-resource-providers-ainotificationschannel.git).

## License

Distributed under the Apache-2.0 License.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import constructs as _constructs_77d1e7e8


class CfnAiNotificationsChannel(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/newrelic-observability-ainotificationschannel.CfnAiNotificationsChannel",
):
    '''A CloudFormation ``NewRelic::Observability::AINotificationsChannel``.

    :cloudformationResource: NewRelic::Observability::AINotificationsChannel
    :link: https://github.com/newrelic/newrelic-cloudformation-resource-providers-ainotificationschannel.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        channel: builtins.str,
        list_query_filter: typing.Optional[builtins.str] = None,
        list_query_sorter: typing.Optional[builtins.str] = None,
        variables: typing.Any = None,
    ) -> None:
        '''Create a new ``NewRelic::Observability::AINotificationsChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param channel: 
        :param list_query_filter: 
        :param list_query_sorter: 
        :param variables: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__773d8654ac4bac61b88cc66315a70cca777acf2b7efc7e0b50cdcf9d15aaff05)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAiNotificationsChannelProps(
            channel=channel,
            list_query_filter=list_query_filter,
            list_query_sorter=list_query_sorter,
            variables=variables,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''Attribute ``NewRelic::Observability::AINotificationsChannel.Id``.

        :link: https://github.com/newrelic/newrelic-cloudformation-resource-providers-ainotificationschannel.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnAiNotificationsChannelProps":
        '''Resource props.'''
        return typing.cast("CfnAiNotificationsChannelProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/newrelic-observability-ainotificationschannel.CfnAiNotificationsChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "channel": "channel",
        "list_query_filter": "listQueryFilter",
        "list_query_sorter": "listQuerySorter",
        "variables": "variables",
    },
)
class CfnAiNotificationsChannelProps:
    def __init__(
        self,
        *,
        channel: builtins.str,
        list_query_filter: typing.Optional[builtins.str] = None,
        list_query_sorter: typing.Optional[builtins.str] = None,
        variables: typing.Any = None,
    ) -> None:
        '''CRUD operations for New Relic AI Notifications Channels via the NerdGraph API.

        :param channel: 
        :param list_query_filter: 
        :param list_query_sorter: 
        :param variables: 

        :schema: CfnAiNotificationsChannelProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c4c7d8df36c3bf811bb62df65e86bfcc3d24908f23356bf838ee33fb388b662)
            check_type(argname="argument channel", value=channel, expected_type=type_hints["channel"])
            check_type(argname="argument list_query_filter", value=list_query_filter, expected_type=type_hints["list_query_filter"])
            check_type(argname="argument list_query_sorter", value=list_query_sorter, expected_type=type_hints["list_query_sorter"])
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "channel": channel,
        }
        if list_query_filter is not None:
            self._values["list_query_filter"] = list_query_filter
        if list_query_sorter is not None:
            self._values["list_query_sorter"] = list_query_sorter
        if variables is not None:
            self._values["variables"] = variables

    @builtins.property
    def channel(self) -> builtins.str:
        '''
        :schema: CfnAiNotificationsChannelProps#Channel
        '''
        result = self._values.get("channel")
        assert result is not None, "Required property 'channel' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def list_query_filter(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnAiNotificationsChannelProps#ListQueryFilter
        '''
        result = self._values.get("list_query_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def list_query_sorter(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnAiNotificationsChannelProps#ListQuerySorter
        '''
        result = self._values.get("list_query_sorter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def variables(self) -> typing.Any:
        '''
        :schema: CfnAiNotificationsChannelProps#Variables
        '''
        result = self._values.get("variables")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAiNotificationsChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAiNotificationsChannel",
    "CfnAiNotificationsChannelProps",
]

publication.publish()

def _typecheckingstub__773d8654ac4bac61b88cc66315a70cca777acf2b7efc7e0b50cdcf9d15aaff05(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    channel: builtins.str,
    list_query_filter: typing.Optional[builtins.str] = None,
    list_query_sorter: typing.Optional[builtins.str] = None,
    variables: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c4c7d8df36c3bf811bb62df65e86bfcc3d24908f23356bf838ee33fb388b662(
    *,
    channel: builtins.str,
    list_query_filter: typing.Optional[builtins.str] = None,
    list_query_sorter: typing.Optional[builtins.str] = None,
    variables: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass
