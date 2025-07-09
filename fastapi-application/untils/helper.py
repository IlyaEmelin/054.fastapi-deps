from typing import Annotated

from fastapi import Header


class BaseGreate:
    name: str
    default: str

    def as_dict(self) -> dict[str, str]:
        return {
            "name": self.name,
            "default": self.default,
        }


class GreateHelper(BaseGreate):
    def __init__(self, name: str, default: str) -> None:
        self.name = name
        self.default = default


class GreateService(BaseGreate):
    def __init__(
        self,
        name: Annotated[
            str,
            Header(alias="x-greate-service-name"),
        ],
        default: Annotated[
            str,
            Header(alias="x-greate-service-default-value"),
        ],
    ) -> None:
        self.name = name
        self.default = default
