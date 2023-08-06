# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: 2023 Thomas Mahé <contact@tmahe.dev>

import argparse
import inspect
from typing import Callable


def get_callback_arguments(func: Callable, arguments: argparse.Namespace):
    return {p: getattr(arguments, p) for p in inspect.signature(func).parameters.keys()}
