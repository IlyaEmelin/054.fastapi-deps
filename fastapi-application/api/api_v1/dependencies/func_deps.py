from typing import Annotated

from fastapi import Header, Depends

from untils.helper import GreateHelper


def get_x_foo_bar(
    foobar: Annotated[
        str,
        Header(alias="x-foo-bar"),
    ] = "",
) -> str:
    return foobar


def get_header_dependency(
    header_name: str,
    default_value: str = "",
):
    def dependency(
        header: Annotated[
            str,
            Header(alias=header_name),
        ] = default_value,
    ) -> str:
        return header

    return dependency


def get_greate_helper(
    helper_name: Annotated[
        str,
        Depends(
            get_header_dependency(
                "x-helper_name",
            ),
        ),
    ],
    helper_default: Annotated[
        str,
        Depends(
            get_header_dependency(
                "x-helper_default",
            ),
        ),
    ],
) -> GreateHelper:
    helper = GreateHelper(
        name=helper_name,
        default=helper_default,
    )
    return helper
