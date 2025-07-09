from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Header,
)

from untils.helper import GreateHelper, GreateService
from .dependencies.func_deps import (
    get_x_foo_bar,
    get_header_dependency,
    get_greate_helper,
)
from .dependencies.cls_deps import (
    path_reader,
    PathReaderDependency,
    TokenIntrospectResult,
    access_required,
)

router = APIRouter(tags=["Dependencies Examples"])


@router.get("/single-direct-dependency")
def single_direct_dependency(
    foobar: Annotated[
        str,
        Header(),
    ],
):
    return {
        "foobar": foobar,
        "message": "single direct dependency foobar",
    }


@router.get("/single-via-func")
def single_via_func(
    foobar: Annotated[str, Depends(get_x_foo_bar)],
):
    return {
        "x-foobar": foobar,
        "message": "single via-func dependency foobar",
    }


@router.get("/multy-direct-and-via-func")
def multi_direct_and_via_func(
    fizzbuzz: Annotated[
        str,
        Header(alias="x-fizz-buzz"),
    ],
    foobar: Annotated[
        str,
        Depends(get_x_foo_bar),
    ],
):
    return {
        "x-fizz-buzz": fizzbuzz,
        "x-foobar": foobar,
        "message": "multi-direct and-via-func dependency foobar",
    }


@router.get("multy-indirect")
def multi_indirect_dependency(
    foobar: Annotated[
        str,
        Depends(get_header_dependency("x-foobar")),
    ],
    fizzbuss: Annotated[
        str,
        Depends(
            get_header_dependency(
                "x-fizz-buzz",
                default_value="FizzBuzz",
            ),
        ),
    ],
):
    return {
        "x-fizz-buzz": fizzbuss,
        "x-foobar": foobar,
        "message": "multi-indirect dependency foobar",
    }


@router.get("/top-level-helper-creation")
def top_level_helper_creation(
    helper_name: Annotated[
        str,
        Depends(
            get_header_dependency(
                "x-helper_name",
                default_value="HelperOne",
            ),
        ),
    ],
    helper_default: Annotated[
        str,
        Depends(
            get_header_dependency(
                "x-helper_default",
                default_value="",
            ),
        ),
    ],
):
    helper = GreateHelper(
        name=helper_name,
        default=helper_default,
    )
    return {
        "helper": helper.as_dict(),
        "message": "Top level helper creation",
    }


@router.get("/helper-as-dependency")
def helper_as_dependency(
    helper: Annotated[
        GreateHelper,
        Depends(get_greate_helper),
    ],
):
    return {
        "helper": helper.as_dict(),
        "message": "helper-as-dependency",
    }


@router.get("/greate-service-as-dependency")
def get_greate_service_as_dependency(
    service: Annotated[
        GreateService,
        Depends(GreateService),
    ],
):
    return {
        "service": service.as_dict(),
        "message": "greate-service-as-dependency",
    }


@router.get("/path-reader-dependency-from-method")
def path_reader_dependency(
    reader: Annotated[
        PathReaderDependency,
        Depends(path_reader.as_dependency),
    ],
):
    return {
        "reader": reader.read(foo="bar"),
        "message": "path-reader-dependency-from-method",
    }


@router.get("/direct-cls-dependency")
def direct_cls_dependency(
    token_data: Annotated[
        TokenIntrospectResult,
        Depends(access_required),
    ],
):
    return {
        "token_data": token_data.model_dump(),
        "message": "direct-cls-dependency",
    }
