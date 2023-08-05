import inspect
import json
import shutil
import sys
from argparse import ArgumentParser
from contextlib import contextmanager
from functools import partial
from math import ceil, floor
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    NamedTuple,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)

from necessary import necessary
from typing_extensions import ParamSpec, TypeAlias

# parameter spec
PS = ParamSpec("PS")

# return type
RT = TypeVar("RT")

# generic type
T = TypeVar("T")

# type alias for a requirement
RequirementType: TypeAlias = Union[str, Tuple[str, str], "NamedRequirement"]


# sentinel value for missing arguments
class _M:
    ...  # noqa: E701


M = _M()  # noqa: E305


class ShadowModuleNotFoundError(ModuleNotFoundError):
    # make easier to track when this error is raised
    ...


class Argument:
    """Holds parameters for argparse.ArgumentParser.add_argument."""

    args: Tuple[str, ...]
    kwargs: Dict[str, Any]

    def __init__(
        self,
        *name_or_flags: str,
        action: Optional[str] = M,  # type: ignore
        nargs: Optional[str] = M,  # type: ignore
        const: Optional[str] = M,  # type: ignore
        default: Optional[T] = M,  # type: ignore
        type: Union[Type[T], Callable[..., T], None] = _M,  # type: ignore
        choices: Optional[List[str]] = M,  # type: ignore
        required: Optional[bool] = M,  # type: ignore
        help: Optional[str] = M,  # type: ignore
        metavar: Optional[str] = M,  # type: ignore
        dest: Optional[str] = M,  # type: ignore
    ):
        self.args = name_or_flags
        self.kwargs = {
            **({"action": action} if action is not M else {}),
            **({"nargs": nargs} if nargs is not M else {}),
            **({"const": const} if const is not M else {}),
            **({"default": default} if default is not M else {}),
            **({"type": type} if type is not _M else {}),
            **({"choices": choices} if choices is not M else {}),
            **({"required": required} if required is not M else {}),
            **({"help": help} if help is not M else {}),
            **({"metavar": metavar} if metavar is not M else {}),
            **({"dest": dest} if dest is not M else {}),
        }


class SpecTuple(NamedTuple):
    name: str
    func: str
    module: str


class NamedRequirement(NamedTuple):
    name: str
    package: str

    @classmethod
    def parse(cls, elem: RequirementType) -> "NamedRequirement":
        if isinstance(elem, cls):
            return elem
        if isinstance(elem, str):
            return cls(elem, elem)
        elif isinstance(elem, tuple):
            return cls(*elem)
        else:
            raise TypeError(f"Expected str or 2-tuple, got {type(elem)}")

    @classmethod
    def from_list(
        cls, elems: List[Union[str, Tuple[str, str]]]
    ) -> List["NamedRequirement"]:
        return [cls.parse(elem) for elem in elems]


class EntryPoint(Generic[PS, RT]):
    def __init__(
        self,
        name: str,
        func: Callable[PS, RT],
        args: List[Argument],
        reqs: List[RequirementType],
    ):
        self.name = name
        self.func = func
        self.args = args

        # if receiving a tuple, the first element is the name of the
        # package and the second is the name of the module to import
        self.reqs = NamedRequirement.from_list(reqs)

        # check that all requirements are met (error raised later if not)
        self.missing_reqs = [
            r.name for r in self.reqs if not necessary(r.package, soft=True)
        ]

    @property
    def spec(self) -> SpecTuple:
        """Returns a triple that identifies this entry point.

        The first argument of the triple is the name of the entry point,
        the second is the name of the function, and the third is the path
        to the function.
        """
        return SpecTuple(self.name, self.func.__name__, self.func.__module__)

    def __call__(self, *args: PS.args, **kwargs: PS.kwargs) -> RT:
        """Run the function."""

        if self.missing_reqs:
            raise ShadowModuleNotFoundError(
                f"Missing requirements: {' '.join(self.missing_reqs)}"
            )
        return self.func(*args, **kwargs)

    def cli(
        self,
        args: Optional[List[str]] = None,
        file_config: Optional[Dict[str, Any]] = None,
    ) -> RT:
        """Run the function from the command line."""

        file_config = file_config or {}

        ap = ArgumentParser(f"shadow-scholar {self.name}")
        for arg in self.args:
            ap.add_argument(*arg.args, **arg.kwargs)

        # parse command line arguments, merge them with json config
        # if one is provided.
        opts, *_ = ap.parse_known_args(args)
        cli_config = vars(opts)

        # only override with file options that are not already set
        # by the command line or that have a value that is equal to defaults
        config = {
            **cli_config,
            **{
                k: v
                for k, v in file_config.items()
                if k not in cli_config or ap.get_default(k) == cli_config[k]
            },
        }

        # actually bind the arguments to the to function args and run the cli
        parsed_args = inspect.signature(self.func).bind(**config).arguments
        return self(**parsed_args)  # pyright: ignore

    @classmethod
    def decorate(
        cls,
        func: Callable[PS, RT],
        name: Optional[str] = None,
        arguments: Optional[List[Argument]] = None,
        requirements: Optional[List[RequirementType]] = None,
        registry: Optional["Registry"] = None,
    ) -> "EntryPoint[PS, RT]":
        """Decorator designed to add function to a registry alongside
        all its arguments and requirements.

        We add the requirement for future parsing, rather than
        building a ArgumentParser here, for two reasons:
        1. We want to be able for all decorated functions to be able to
            use overlapping arguments, and
        2. Creating a single parser here might lead to a lot of unintended
            side effects.

        Args:
            func (Callable): The function to be decorated.
            name (str, optional): Name to use for the function when it is
                called from the command line. If none is provided, the
                function name is used. Defaults to None.
            arguments (List[Argument], optional): A list of Argument objects
                to be passed to the ArgumentParser. The available options
                are the same as those for argparse.ArgumentParser.add_argument.
                Defaults to None.
            requirements (Optional[List[str]], optional): A list of required
                packages for the function to run. Defaults to None.
            registry (Registry, optional): The registry to add the function
                to. If none is provided, the entrypoint is not registered.
        """

        name = name or func.__name__
        arguments = arguments or []
        func_requirements = requirements or []

        # create the entry point by wrapping the function
        entry_point = cls(
            name=name,
            func=func,
            args=arguments,
            reqs=func_requirements,
        )

        # add the function to the registry
        registry.add(entry_point) if registry else None

        return entry_point


class Registry:
    """A registry to hold all the functions decorated with @cli."""

    __instance__: "Registry"
    _registry: Dict[str, "EntryPoint"]

    def __new__(cls):
        """Singleton pattern for the registry."""
        if not hasattr(cls, "__instance__"):
            cls.__instance__ = super(Registry, cls).__new__(cls)
        return cls.__instance__

    def __init__(self) -> None:
        if not hasattr(self, "_registry"):
            self._registry = {}

    def add(self, entry_point: EntryPoint) -> None:
        """Add an entry point to the registry."""
        _, _, module = entry_point.spec

        # we raise an error if the function is already in the registry
        # and the user is not using a different entry point
        if entry_point.name in self._registry and module != "__main__":
            raise KeyError(f"Func {entry_point.name} already in the registry")

        self._registry[entry_point.name] = entry_point

    def cli(
        self,
        name: Optional[str] = None,
        arguments: Optional[List[Argument]] = None,
        requirements: Optional[List[RequirementType]] = None,
    ) -> Callable[[Callable[PS, RT]], "EntryPoint[PS, RT]"]:
        """A decorator to add a function to the registry.

        Args:
            name (str, optional): Name to use for the function
                when it is called from the command line. If none is provided,
                the function name is used. Defaults to None.
            arguments (List[Argument], optional): A list of Argument objects
                to be passed to the ArgumentParser. The available options
                are the same as those for argparse.ArgumentParser.add_argument.
                Defaults to None.
            requirements: A list of requirements for the function. Can
                be either a list of strings (e.g., ["spacy"]), a list that
                includes the minimum versions (e.g., ["spacy>=3.0.0"]), or a
                list of tuples (e.g., [("scikit-learn>=0.24.0", "sklearn"),
                "spacy"]) for cases where the package name is different from
                the import name.
        """
        decorated = partial(
            # need to make types more permissive here because otherwise
            # mypy complains about the partial not being a callable
            cast(Callable[..., EntryPoint[PS, RT]], EntryPoint.decorate),
            name=name,
            arguments=arguments,
            requirements=requirements,
            registry=self,
        )
        return decorated  # pyright: ignore

    def _formatted_entrypoints(self, sep="   ") -> str:
        term_width = shutil.get_terminal_size().columns

        l_col, r_col = zip(
            *(
                (e.spec.name, f"{e.spec.module}.{e.spec.func}")
                for e in sorted(self._registry.values(), key=lambda e: e.name)
            )
        )

        # pad the left column to the longest name, trim if too long
        longest_left = max(len(name) for name in l_col)
        l_col = tuple(
            name.ljust(longest_left)
            if len(name) < term_width
            else (name[: term_width - 3] + "...")
            for name in l_col
        )

        # trim the right column if too long
        max_length_right = term_width - longest_left - len(sep)
        r_col = tuple(
            name
            if len(name) <= max_length_right
            else (name[: max_length_right - 3] + "...")
            for name in r_col
        )
        longest_right = max(len(name) for name in r_col)

        # this is the total width of the entire table
        format_width = longest_left + len(sep) + longest_right

        title = "Available Entrypoints"
        title_pad_width = (format_width - len(title) - 2) / 2

        return (
            "=" * format_width
            + "\n"
            + " " * floor(title_pad_width)
            + "Available Entrypoints"
            + " " * ceil(title_pad_width)
            + "\n"
            + "-" * format_width
            + "\n"
            + "\n".join(f"{lc}   {rc}" for lc, rc in zip(l_col, r_col))
            + "\n"
            + "=" * format_width
        )

    def run(self):
        """Creates a click command group for all registered functions."""
        parser = ArgumentParser("shadow-scholar")
        parser.add_argument(
            "-r",
            "--list-requirements",
            action="store_true",
            help="List the requirements for all entrypoints.",
        )
        parser.add_argument(
            "-l",
            "--list-entrypoints",
            action="store_true",
            help="List the requirements for all entrypoints.",
        )
        parser.add_argument(
            "-c",
            "--config-path",
            help="Path to the config file. Complements cli options.",
        )

        # command line arguments; excluding the first one, which is the
        # name of the script
        args_ = sys.argv[1:]

        # the entrypoint could be any of the arguments that is not an option
        entrypoint_positions = [
            i
            for i in range(len(args_))
            if not (
                args_[i].startswith("-")  # ... is an option
                or args_[i - 1] == "-c"  # ... its the path for config
                or args_[i - 1] == "--config-path"  # ... same as above
            )
        ]
        if len(entrypoint_positions) > 0:
            # separate between the global arguments and the any
            # argument that comes after the mention of the first entrypoint
            pre_args, entry_name, post_args = (
                args_[: (ep := entrypoint_positions[0])],
                args_[ep],
                args_[ep + 1 :],
            )
        else:
            pre_args, entry_name, post_args = args_, None, []

        # get any options for shadow-scholar cli itself
        opts = parser.parse_args(pre_args)

        if opts.list_entrypoints:
            print(self._formatted_entrypoints())
            sys.exit(1)

        entrypoint = self._registry.get(entry_name, None)  # pyright: ignore
        if entrypoint is None:
            msg = (
                "No entrypoint "
                + (f"with name `{entry_name}`." if entry_name else "provided.")
                + " Please run again with one of the following names: "
                + ", ".join(sorted(self._registry))
            )
            print(msg, file=sys.stderr)
            sys.exit(1)

        if opts.list_requirements:
            print(" ".join(r.name for r in entrypoint.reqs))
            sys.exit(0)

        config = {}
        if opts.config_path:
            with open(opts.config_path) as f:
                config = json.load(f)

        try:
            entrypoint.cli(args=post_args, file_config=config)
        except ShadowModuleNotFoundError as e:
            e.msg += (
                f"; run `shadow -r {entry_name}` to list all requirements "
                "for this entrypoint."
            )
            raise e

    def require(
        self, requirements: List[RequirementType]
    ) -> Callable[[Callable[PS, RT]], EntryPoint[PS, RT]]:
        """Specifies a list of requirements for a function.

        Args:
            requirements: A list of requirements for the function. Can
                be either a list of strings (e.g., ["spacy"]), a list that
                includes the minimum versions (e.g., ["spacy>=3.0.0"]), or a
                list of tuples (e.g., [("scikit-learn>=0.24.0", "sklearn"),
                "spacy"]) for cases where the package name is different from
                the import name.
        """

        decorated = partial(
            cast(Callable[..., EntryPoint[PS, RT]], EntryPoint.decorate),
            requirements=requirements,
        )
        return decorated  # type: ignore


@contextmanager
def safe_import():
    """Context manager to safely import a package."""
    try:
        yield
    except (ModuleNotFoundError, ImportError):
        pass


def load_kwargs(path_or_json: str) -> Dict[str, Any]:
    """Load a json file containing a config, or a json string."""

    if Path(path_or_json).exists():
        with open(path_or_json) as f:
            path_or_json = f.read()

    try:
        return json.loads(path_or_json)
    except json.JSONDecodeError as e:
        err = ValueError(f"Could not parse json {path_or_json}.")
        raise err from e


run = Registry().run
cli = Registry().cli
require = Registry().require

__all__ = ["run", "cli", "Argument", "safe_import", "load_kwargs", "require"]
