# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: 2023 Thomas Mahé <contact@tmahe.dev>

import typing


class TermkitError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class InconsistentTypingError(TermkitError):
    def __init__(self,
                 argument_name: str,
                 function: typing.Callable,
                 hinted_type: typing.Type,
                 argument_type: typing.Type):
        self.message = f"inconsistent typing for argument '{argument_name}' of function '{function.__name__}' ({hinted_type.__name__} != {argument_type.__name__})"
        super().__init__(self.message)
