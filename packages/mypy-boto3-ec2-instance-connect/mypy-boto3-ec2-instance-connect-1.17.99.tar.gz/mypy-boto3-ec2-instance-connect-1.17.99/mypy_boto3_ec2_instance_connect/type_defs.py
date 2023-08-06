"""
Type annotations for ec2-instance-connect service type definitions.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ec2_instance_connect/type_defs.html)

Usage::

    ```python
    from mypy_boto3_ec2_instance_connect.type_defs import SendSSHPublicKeyResponseTypeDef

    data: SendSSHPublicKeyResponseTypeDef = {...}
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = ("SendSSHPublicKeyResponseTypeDef", "SendSerialConsoleSSHPublicKeyResponseTypeDef")

SendSSHPublicKeyResponseTypeDef = TypedDict(
    "SendSSHPublicKeyResponseTypeDef",
    {
        "RequestId": str,
        "Success": bool,
    },
    total=False,
)

SendSerialConsoleSSHPublicKeyResponseTypeDef = TypedDict(
    "SendSerialConsoleSSHPublicKeyResponseTypeDef",
    {
        "RequestId": str,
        "Success": bool,
    },
    total=False,
)
