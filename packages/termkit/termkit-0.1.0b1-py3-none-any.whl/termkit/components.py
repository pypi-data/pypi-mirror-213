# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: 2023 Thomas Mahé <contact@tmahe.dev>

import argparse
import inspect
import os
import sys
import typing
from abc import ABC
from typing import Optional, Callable, Union, Dict, Any

from helpers import get_callback_arguments
from termkit.groups import ArgumentGroup, MutuallyExclusiveGroup

from termkit.formatters import TermkitDefaultFormatter
from termkit.arguments import Argument
from termkit.exceptions import TermkitError, InconsistentTypingError


class Component(ABC):
    name: Optional[str]
    help: Optional[str]
    description: Optional[str]


class Termkit(Component):
    _callback: Optional[Callable]
    _childs: typing.List[Component]

    def __init__(self,
                 name: Optional[str] = None,
                 callback: Optional[Callable] = None,
                 description: Optional[str] = None):

        # Legacy argparse default for prog name
        if name is None:
            name = os.path.basename(sys.argv[0])

        if callback is not None and not inspect.isfunction(callback):
            raise TermkitError("termkit.Command callback must be a function")

        self.description = description

        if description is None:
            self.help = None
        else:
            self.help = description.splitlines()[0]

        self.name = name

        self._callback = callback
        self._childs = list()

    def add(self, app_or_command: typing.Union[Component, Callable]):
        # Adding sub-app
        if isinstance(app_or_command, Termkit):
            if app_or_command.name == os.path.basename(sys.argv[0]):
                raise TermkitError('cannot add unnamed Termkit application')
            self._childs.append(app_or_command)

        # Adding command
        elif isinstance(app_or_command, Command):
            self._childs.append(app_or_command)

        # Adding function
        elif inspect.isfunction(app_or_command):
            self._childs.append(Command(name=app_or_command.__name__,
                                        callback=app_or_command))

        # Raise error on incompatible type
        else:
            raise TermkitError(f'cannot add object of type {type(app_or_command)} to Termkit application')

        child_names = [e.name for e in self._childs]
        duplicates = set([e for e in child_names if child_names.count(e) > 1])
        if len(duplicates) > 0:
            self._childs.pop()
            raise TermkitError(f"duplicated command or sub-app name {duplicates} in application '{self.name}'")

    def command(self, name: Optional[str] = None):
        def _decorated_callable(callback: Callable, _name=name):
            if _name is None:
                _name = callback.__name__
            self._childs.append(Command(name=_name,
                                        callback=callback))
            return callback

        return _decorated_callable

    def callback(self):
        def _decorated_callable(callback: Callable):
            if inspect.isfunction(callback):
                self._callback = callback
            else:
                raise TermkitError(f"cannot set object of type '{type(callback).__name__}' as callback for Termkit application")
            return callback
        return _decorated_callable

    def __call__(self, *args, **kwargs):
        parser = TermkitParser(self)
        args = parser.parse_args()

        callbacks = [f for k, f in args.__dict__.items() if "__TERMKIT_CALLBACK_" in k]

        for callback in callbacks:
            callback(**get_callback_arguments(callback, args))

        sys.exit(0)


class Command(Component):
    def __init__(self,
                 name: str,
                 callback: Callable):
        if not inspect.isfunction(callback):
            raise TermkitError("termkit.Command callback must be a function")

        self.name = str(name)
        self._callback = callback

        doc = inspect.getdoc(callback)
        if doc is None:
            self.help = ""
            self.description = ""
        else:
            self.help = doc.splitlines()[0]
            self.description = doc


class TermkitParser(argparse.ArgumentParser):
    _argument_groups: Dict[Union[ArgumentGroup, MutuallyExclusiveGroup], Any]

    def __init__(self, app: Termkit, *args, **kwargs):
        if not isinstance(app, Component):
            raise TermkitError(f"TermkitParser.app expected object of type [Termkit | Command], {type(app)} provided")

        super().__init__(prog=kwargs.get('prog', app.name), formatter_class=TermkitDefaultFormatter)
        self._positionals.title = "Positional arguments"
        self._optionals.title = "Optional arguments"
        self._required = super(TermkitParser, self).add_argument_group("Required arguments")

        self.description = app.description
        self.help = app.help

        # Re-order groups
        positional_group = self._action_groups.pop()
        self._action_groups.insert(1, positional_group)

        self._depth = kwargs.get("depth", 0)
        self._app = app
        self._argument_groups = dict()
        self._populate()

    @property
    def positionals(self):
        return self._positionals

    @property
    def required(self):
        return self._required

    @property
    def optionals(self):
        return self._optionals

    def _populate(self):
        if isinstance(self._app, Termkit):
            self._populate_termkit_app(app=self._app)
        else:
            self._populate_command(command=self._app)

    def _populate_termkit_app(self, app: Termkit):

        if app._callback is not None:
            command = Command(name=app._callback.__name__, callback=app._callback)
            if self.description is None:
                self.description = command.description
            else:
                self.description += f"\n\n{command.description}"
            self._populate_command(command)

        if len(app._childs) > 0:
            p = self.add_subparsers(title="Commands")

            for child in app._childs:
                p.add_parser(app=child, name=child.name, help=child.help, description=child.description, depth=self._depth+1)

    def _populate_command(self, command: Command):
        self.add_argument(f'__TERMKIT_CALLBACK_{self._depth}', action="store_const", const=command._callback,
                          help=argparse.SUPPRESS)
        if sys.version_info >= (3, 9):
            type_hints = typing.get_type_hints(command._callback, include_extras=True)
        else:
            type_hints = typing.get_type_hints(command._callback)  # pragma: nocover

        for arg_name, arg_spec in inspect.signature(command._callback).parameters.items():

            if sys.version_info >= (3, 9) and isinstance(typing.get_origin(type_hints.get(arg_name, None)), typing.Annotated.__class__):
                annotated_type, argument = typing.get_args(type_hints.get(arg_name, None))
                if issubclass(type(argument), Argument):
                    if argument.type is not None and annotated_type != argument.type:
                        raise InconsistentTypingError(arg_name, command._callback, annotated_type, argument.type)
                    argument._populate(self, arg_name, annotated_type)
                else:
                    raise TermkitError(f"incompatible object for Termkit command: "
                                       f"'{arg_name}: Annotated[{annotated_type.__name__}, {argument.__class__.__name__}]'")

            elif isinstance(type_hints.get(arg_name, None), Argument):
                type_hints.get(arg_name)._populate(self, arg_name, None)

            elif isinstance(arg_spec.default, Argument):
                type_hint = type_hints.get(arg_name, None)
                if None not in [type_hint, arg_spec.default.type] and arg_spec.default.type != type_hint:
                    raise InconsistentTypingError(arg_name, command._callback, type_hint, arg_spec.default.type)
                arg_spec.default._populate(self, arg_name, type_hints.get(arg_name, None))

            elif arg_spec.default is inspect.Parameter.empty:
                # implicit positional
                _type = type_hints.get(arg_name, str)
                self.positionals.add_argument(arg_name, metavar=arg_name.upper(), type=_type, help="(%(type)s)")
            else:
                # implicit option
                _type = type(arg_spec.default)
                if type_hints.get(arg_name, _type) != _type:
                    raise TermkitError(
                        f"default type mismatch with type hint ({_type.__name__} != {type_hints.get(arg_name).__name__}) for argument '{arg_name}'")
                self.optionals.add_argument(f"--{arg_name}", type=_type, default=arg_spec.default,
                                            metavar=_type.__name__.upper(), help="(default: %(default)s)")

    def add_argument_group(self,
                           title: Optional[str] = None,
                           description: Optional[str] = None,
                           group: Optional[Union[ArgumentGroup, MutuallyExclusiveGroup]] = None):

        if group is None:
            return super(self.__class__, self).add_argument_group(title=title, description=description)

        if group in self._argument_groups.keys():
            return self._argument_groups.get(group)

        parent_group = self

        if isinstance(group, MutuallyExclusiveGroup) and group.parent is not None:
            parent_group = self.add_argument_group(group=group.parent)

        if isinstance(group, MutuallyExclusiveGroup):
            self._argument_groups[group] = parent_group.add_mutually_exclusive_group(required=group.required)

        if isinstance(group, ArgumentGroup):
            self._argument_groups[group] = super(self.__class__, self).add_argument_group(title=group.title, description=group.description)

        return self._argument_groups[group]


def run(func_or_app: Union[Callable, Termkit]):
    if inspect.isfunction(func_or_app):
        Termkit(name=func_or_app.__name__, callback=func_or_app)()
    elif isinstance(func_or_app, Termkit):
        func_or_app()
    else:
        raise TermkitError(f"cannot run object of type '{type(func_or_app).__name__}'")
