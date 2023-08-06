# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: 2023 Thomas Mahé <contact@tmahe.dev>

from typing import Optional


class ArgumentGroup:
    def __init__(self,
                 title: Optional[str] = None,
                 description: Optional[str] = None):
        self.title = title
        self.description = description


class MutuallyExclusiveGroup:
    def __init__(self, required: bool = False,
                 parent: Optional[ArgumentGroup] = None):
        self.parent = parent
        self.required = required
