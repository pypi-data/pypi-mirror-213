# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: 2023 Thomas Mahé <contact@tmahe.dev>

from __future__ import annotations
import contextlib
import inspect
import io
import os
import pathlib

import sys


def capture_output(update_sample=False):
    def _decorator(f):
        def wrapper(self, *args):
            file_path = inspect.getfile(self.__class__)
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            output_files_path = os.path.join(os.path.dirname(inspect.getfile(self.__class__)),
                                             f'captured_output/{file_name}_{self.__class__.__name__}_{self._testMethodName}.log')

            captured = io.StringIO()
            with contextlib.redirect_stdout(captured):
                with contextlib.redirect_stderr(captured):
                    run = f(self, *args)

            if os.path.exists(output_files_path) and not update_sample:
                with open(output_files_path, 'r') as out:
                    self.assertEqual(out.read(), captured.getvalue())

            else:  # pragma: nocover
                pathlib.Path(os.path.dirname(output_files_path)).mkdir(parents=True, exist_ok=True)
                with open(output_files_path, 'w') as out:
                    out.write(captured.getvalue())
            return run

        return wrapper

    return _decorator


def with_exit_code(code):
    def test_decorator(fn):
        def test_decorated(self, *args, **kwargs):
            with self.assertRaises(SystemExit) as ctx:
                fn(self, *args)

            print(f">>> Exited with code: {ctx.exception.code}")
            self.assertEqual(code, ctx.exception.code)

        return test_decorated

    return test_decorator


def with_arguments(*argv: str):
    def decorator(fn):
        def wrapper(self, *args):
            print(f">>> Running with arguments: {list(argv)}")
            sys.argv = list(('<patched argv[0]>',) + argv)
            return fn(self, *args)

        return wrapper

    return decorator
