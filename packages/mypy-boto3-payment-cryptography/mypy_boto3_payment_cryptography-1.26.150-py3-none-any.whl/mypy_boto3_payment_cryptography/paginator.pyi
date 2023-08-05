"""
Type annotations for payment-cryptography service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_payment_cryptography.client import PaymentCryptographyControlPlaneClient
    from mypy_boto3_payment_cryptography.paginator import (
        ListAliasesPaginator,
        ListKeysPaginator,
        ListTagsForResourcePaginator,
    )

    session = Session()
    client: PaymentCryptographyControlPlaneClient = session.client("payment-cryptography")

    list_aliases_paginator: ListAliasesPaginator = client.get_paginator("list_aliases")
    list_keys_paginator: ListKeysPaginator = client.get_paginator("list_keys")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .literals import KeyStateType
from .type_defs import (
    ListAliasesOutputTypeDef,
    ListKeysOutputTypeDef,
    ListTagsForResourceOutputTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = ("ListAliasesPaginator", "ListKeysPaginator", "ListTagsForResourcePaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListAliasesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography.html#PaymentCryptographyControlPlane.Paginator.ListAliases)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/paginators/#listaliasespaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAliasesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography.html#PaymentCryptographyControlPlane.Paginator.ListAliases.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/paginators/#listaliasespaginator)
        """

class ListKeysPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography.html#PaymentCryptographyControlPlane.Paginator.ListKeys)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/paginators/#listkeyspaginator)
    """

    def paginate(
        self, *, KeyState: KeyStateType = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListKeysOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography.html#PaymentCryptographyControlPlane.Paginator.ListKeys.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/paginators/#listkeyspaginator)
        """

class ListTagsForResourcePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography.html#PaymentCryptographyControlPlane.Paginator.ListTagsForResource)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/paginators/#listtagsforresourcepaginator)
    """

    def paginate(
        self, *, ResourceArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTagsForResourceOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography.html#PaymentCryptographyControlPlane.Paginator.ListTagsForResource.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography/paginators/#listtagsforresourcepaginator)
        """
