import time
from dataclasses import asdict, dataclass, field, fields
from enum import Enum
from functools import wraps
from typing import Any, Callable, Protocol, Self, Tuple, Type, TypeVar, cast

from dacite import Config, from_dict


class KastDataFrameBackend(Enum):
    NOTSET = "notset"
    PANDAS = "pandas"
    PYSPARK = "pyspark"

    @staticmethod
    def from_string(s: str) -> "KastDataFrameBackend":
        try:
            return KastDataFrameBackend(s)
        except KeyError:
            raise KastInvalidDataFrameBackend(
                message=[
                    ["Error", "Unsupported DataFrame backend"],
                    ["Given", s],
                ],
                errors=None,
            )


T = TypeVar("T")


def kast_unmarshal(clazz: T) -> T:
    """Type ignore is necessary due to typechecker not supporting alias of dataclass
    see: https://github.com/python/mypy/issues/9875
    """
    return dataclass(clazz, frozen=True, slots=True, kw_only=True, eq=True)  # type: ignore


class KastDataFrame(Protocol):
    @property
    def parents_id(self: Self) -> list[str]:
        ...

    @property
    def id(self: Self) -> str:
        ...

    @property
    def backend(self: Self) -> KastDataFrameBackend:
        ...

    @property
    def schema(self: Self) -> Any:
        ...

    def createOrReplaceTempView(self: Self, name: str = "") -> "KastDataFrame":
        ...

    def map(self: Self, fn: Any, schema: str | dict[str, Any]) -> "KastDataFrame":
        ...

    def show(
        self: Self, id: list[str] = [], truncate: bool = False, vertical: bool = False
    ) -> None:
        ...

    def sql(self: Self, query: str) -> "KastDataFrame":
        ...

    def table_sql(self: Self, query: str) -> None:
        ...

    def to_df(self: Self) -> Any:
        ...

    @property
    def table_engine(self: Self) -> Any:
        ...


@dataclass(frozen=True, slots=True, kw_only=True, eq=True)
class SideOutValue:
    out: str
    schema: str


KastNodeList = Tuple["KastNode", ...]
KastOuts = Tuple[str, ...]
SideOutKey = str
SideOut = dict[SideOutKey, SideOutValue]


def make_side_out() -> SideOut:
    return cast(SideOut, dict[SideOutKey, SideOutValue])


def make_outs() -> KastOuts:
    return field(default_factory=lambda: cast(KastOuts, tuple()))


@dataclass(frozen=True, slots=True, kw_only=True, eq=True)
class KastTable:
    sql: str
    type: str = "table"


class KastTool(Protocol):
    def newKastDataFrame(
        self: Self,
        df: Any,
    ) -> KastDataFrame:
        ...

    def emptyKastDataFrame(self: Self) -> KastDataFrame:
        ...


@dataclass(frozen=True, slots=True, kw_only=True, eq=True)
class KastFunction(Protocol):
    id: str
    backend: KastDataFrameBackend = KastDataFrameBackend.NOTSET
    outs: KastOuts = field(default_factory=make_outs)

    def compute(
        self: Self,
        tool: KastTool,
        tables: list[KastDataFrame],
    ) -> KastDataFrame:
        ...


@dataclass(frozen=True, slots=True, kw_only=True, eq=True)
class Internal:
    modules: set[str]


def make_internal() -> Internal:
    """load python module files
    By default, load __name__
    """
    return Internal(modules={__name__})


@dataclass(frozen=True, slots=True, kw_only=True, eq=True)
class PredefinedAttributesMixin:
    id: str
    type: str
    name: str = ""
    schema: str = ""
    sideOut: SideOut = field(default_factory=make_side_out)
    out: KastOuts = make_outs()
    settings: dict[str, Any] = field(default_factory=dict)
    internal: Internal = field(default_factory=make_internal)

    def clazz_settings_name(self: Self) -> str:
        names: list[str] = self.type.split("-")
        if len(names) == 2:
            return f"{names[0].capitalize()}{names[1].capitalize()}"
        return f"{names[0].capitalize()}"


class KastNode(PredefinedAttributesMixin):
    def __init__(self: Self, **kwargs: Any) -> None:
        return super().__init__(**kwargs)

    @property
    def fn(self: Self) -> KastFunction:
        target: str = self.clazz_settings_name()
        modules: set[str] = self.internal.modules
        import importlib

        for mod in modules:
            try:
                clazz = getattr(importlib.import_module(mod), target)
                compute: KastFunction = clazz(
                    **self.settings, outs=self.out, id=self.id
                )
                return from_dict(  # type: ignore
                    data_class=clazz,
                    data=asdict(compute),
                    config=Config(check_types=True),
                )
            except AttributeError:
                continue
            except Exception as e:
                raise KastFunctionInvalidArgumentsException(
                    message=[
                        ["Origin", str(e)],
                        ["Function", mod],
                        ["ID", self.id],
                    ],
                    errors=e,
                )
        raise KastNodeNotFoundException(
            message=[
                ["Origin", f"{target} is an unknown function implementation"],
                ["ID", self.id],
            ],
            errors=None,
        )

    @classmethod
    def from_dict(cls: Type[Self], modules: set[str], **kwargs: dict[str, Any]) -> Self:
        clazz_attrs = {f.name for f in fields(cls)}
        known_fields: dict[str, Any] = {
            k: v for k, v in kwargs.items() if k in clazz_attrs
        }
        known_fields["out"] = tuple(known_fields.get("out", tuple()))
        unknown_fields: dict[str, Any] = {
            **{k: v for k, v in kwargs.items() if k not in clazz_attrs},
        }
        unknown_fields["schema"] = known_fields.get("schema", "")
        return cls(
            **{
                **known_fields,
                "settings": unknown_fields,
                "internal": Internal(modules=modules),
            }
        )


Fn = TypeVar("Fn", bound=Callable[..., Any])


def timeit(wrapped_func: Fn) -> Fn:
    @wraps(wrapped_func)
    def duration(*args: list[Any], **kwargs: dict[str, Any]) -> Any:
        start_time = time.perf_counter()
        result = wrapped_func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time

        print(
            f"Function {wrapped_func.__name__}{args} {kwargs} Took {total_time:.4f} seconds to compute"
        )
        return result

    return cast(Fn, duration)


class KastManifest:
    __nodes: KastNodeList
    __backend: KastDataFrameBackend

    def __init__(
        self: Self, nodes: KastNodeList, backend: KastDataFrameBackend
    ) -> None:
        self.__nodes = nodes
        self.__backend = backend

    def deser(self: Self, *add_modules: str) -> KastNodeList:
        nodesRaw: list[KastNode] = []
        for node in self.__nodes:
            node_dict: dict[str, Any] = cast(dict[str, Any], node)
            node_dict["backend"] = self.__backend
            nodesRaw.append(
                KastNode.from_dict(
                    modules={__name__, *add_modules},
                    **node_dict,
                )
            )
        return cast(KastNodeList, nodesRaw)


class KastBaseException(Exception):
    """base exception for errors requiring better feedback"""

    def __init__(self: Self, message: list[list[str]] = [], errors: Any = None) -> None:
        super().__init__(message)
        self._message = message
        self.errors = errors

    def __str__(self: Self) -> str:
        from tabulate import tabulate

        return f"\n\n{tabulate(tabular_data=self._message, tablefmt='grid')}"


class KastNodeNotFoundException(KastBaseException):
    "When node is missing from the dag, this exception is raised"


class KastUnsupportedDAGOperation(KastBaseException):
    "when unsupported operation happens on the graph dag pub/sub, this exception is raised"


class KastFunctionInvalidArgumentsException(KastBaseException):
    """when required, unknown or invalid arguments are passed as input to a function,
    this exception is raised"""


class KastConfigDeserializationException(KastBaseException):
    "When invalid configuration file is passed, this exception is raised"


class KastInvalidDataFrameBackend(KastBaseException):
    "When invalid backend is requested, this exception is raised"
