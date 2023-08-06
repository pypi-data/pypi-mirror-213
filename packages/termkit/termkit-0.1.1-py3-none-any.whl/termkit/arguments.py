# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: 2023 Thomas Mahé <contact@tmahe.dev>

from __future__ import annotations

import typing
from abc import ABC, abstractmethod
from typing import Optional, Type, Any, TYPE_CHECKING, Union

if TYPE_CHECKING:  # pragma: nocover
    from termkit.components import TermkitParser

from termkit.groups import ArgumentGroup, MutuallyExclusiveGroup


class Argument(ABC):
    type: Optional[Type]

    @abstractmethod
    def _populate(self,
                  parser: TermkitParser,
                  argument_name: str,
                  type_hint: typing.Any):
        ...  # pragma: nocover


class Positional(Argument):

    def __init__(self,
                 type: Optional[Type] = None,
                 help: Optional[str] = None,
                 metavar: Optional[str] = None,
                 choices: Optional[typing.Iterable[Any]] = None,
                 group: Optional[Union[ArgumentGroup, MutuallyExclusiveGroup]] = None
                 ):
        self.type = type
        self.help = help
        self.metavar = metavar
        self.choices = choices
        self.group = group

    def _populate(self, parser: TermkitParser, argument_name: str, type_hint: typing.Any):
        if self.metavar is None and self.choices is None:
            self.metavar = argument_name.upper()

        if self.type is None:
            self.type = type_hint

        if self.type is None and type_hint is None:
            self.type = str

        if self.help is None:
            self.help = ""

        self.help = f"{self.help} (%(type)s) ".strip()

        args = self.__dict__.copy()
        del args['group']

        parser.positionals.add_argument(argument_name, **args)


class Option(Argument):
    def __init__(self,
                 *flags: Optional[str],
                 type: Optional[Type] = None,
                 help: Optional[str] = None,
                 metavar: Optional[str] = None,
                 default: Optional[Any] = None,
                 required: Optional[bool] = False,
                 nargs: Optional[str] = None,
                 choices: Optional[typing.Iterable[Any]] = None,
                 group: Optional[Union[ArgumentGroup, MutuallyExclusiveGroup]] = None):
        self.flags = None
        if flags:
            self.flags = sorted(map(str, flags), key=len, reverse=True)
        self.type = type
        self.help = help
        self.metavar = metavar
        self.default = default
        self.required = required
        self.nargs = nargs
        self.choices = choices
        self.group = group

    def _populate(self, parser: TermkitParser, argument_name: str, type_hint: typing.Any):
        if self.flags is None:
            self.flags = (f"--{argument_name}",)

        if self.type is None:
            self.type = type_hint

        if self.type is None and type_hint is None:
            if self.default is not None:
                self.type = type(self.default)
            else:
                self.type = str

        if self.metavar is None and self.choices is None:
            self.metavar = self.type.__name__.upper()

        if self.help is None:
            self.help = ""

        if self.default is not None:
            self.required = False
            self.help = f"{self.help} (default: %(default)s)".strip()

        if isinstance(self.group, ArgumentGroup) or isinstance(self.group, MutuallyExclusiveGroup):
            parser = parser.add_argument_group(group=self.group)
        else:
            parser = parser.required if self.required else parser.optionals

        args = self.__dict__.copy()
        del args['flags']
        del args['group']

        parser.add_argument(*self.flags, dest=argument_name, **args)
