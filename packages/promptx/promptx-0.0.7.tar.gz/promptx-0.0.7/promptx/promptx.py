#!/usr/bin/env python3
# Copyright (C) 2022 John Dovern
#
# This file is part of PromptX <https://codeberg.org/johndovern/promptx>.
#
# PromptX is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation version 3 of the License
#
# PromptX is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# PromptX.  If not, see <http://www.gnu.org/licenses/>.

import shlex
import subprocess
from typing import List

__all__ = [
    "PromptXError",
    "PromptXCmdError",
    "PromptXSelectError",
    "PromptX",
]


class PromptXError(Exception):
    """
    Raised if OS error when trying to execute constructed prompt command
    or if prompt command returns non-zero value and stderr is not empty.
    """

    def __init__(self, cmd, err):
        self.cmd = cmd
        self.err = err
        self.message = (
            f"Failed to execute constructed command: {self.cmd}\nError: {self.err}"
        )
        super().__init__(self.message)


class PromptXCmdError(Exception):
    """
    Raised if PromptX is given a prompt command that is not fzf, dmenu, or rofi.
    """

    def __init__(self, prompt):
        self.prompt = prompt
        self.message = (
            f"PromptX does not yet handle the given prompt command: {self.prompt}"
        )
        super().__init__(self.message)


class PromptXSelectError(Exception):
    """
    Raised if select value is not "first", "last", or "all"
    """

    def __init__(self, select):
        self.select = select
        self.message = f"Invalid select option given: {self.select}"
        self.message = "\n".join(
            [self.message, 'Valid options are "first", "last", and "all"']
        )
        super().__init__(self.message)


class PromptX:
    """
    Prompt wrapper for dmenu, fzf, and rofi.
    """

    def __init__(
        self,
        prompt_cmd: str,
        default_args: str = "",
    ):
        # Check that we can handle the given command
        valid_prompt_cmds = ["dmenu", "fzf", "rofi"]
        if not prompt_cmd in valid_prompt_cmds:
            raise PromptXCmdError(prompt=prompt_cmd)
        # As PromptX works through stdin rofi needs the -dmenu flag to work
        if prompt_cmd == "rofi":
            default_args = " ".join((default_args, "-dmenu"))
        self.prompt_cmd = prompt_cmd
        self.default_args = default_args
        # Create a basic list of command args
        self.base_cmd = shlex.split(" ".join((prompt_cmd, default_args)))
        self.temp_args = []
        # fzf uses stderr to show prompt so we need to check for that
        self.stderr_file = None if self.prompt_cmd == "fzf" else subprocess.PIPE

    def ask(
        self,
        options: List,
        prompt: str | None = None,
        additional_args: str | None = None,
        deliminator: str = "\n",
    ) -> List[str]:
        """
        Ask the user to make a selection from the given options
        """
        cmd = []
        cmd.extend(self.base_cmd)
        cmd.extend(self.temp_args)
        if additional_args is not None:
            cmd.extend(shlex.split(additional_args))
        if self.prompt_cmd == "fzf" and prompt is not None:
            cmd.append(f"--prompt={prompt}")
        elif prompt is not None:
            cmd.extend(["-p", prompt])

        # Start prompt_cmd with given args
        try:
            proc = subprocess.Popen(
                cmd,
                universal_newlines=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=self.stderr_file,
            )
        # Failed to execute constructed command
        except OSError as err:
            raise PromptXError(cmd=cmd, err=err)

        # Reset temp_args
        self.temp_args = []
        # Create one long string similar to choice=$(printf '%s\n' "$@" | dmenu) in bash
        opts_str = deliminator.join(map(str, options))
        # Open stdin and populate choices
        outs, errs = proc.communicate(input=opts_str)
        ret_list = outs.rstrip().splitlines()
        if proc.wait() != 0:
            # If no err return None as user hit escape
            if errs == "":
                return ret_list
            # Otherwise some error occured
            raise PromptXError(cmd, errs)

        return ret_list

    def add_args(
        self,
        additional_args: List,
        default_args: bool = False,
    ):
        """
        Add args that are in a list. These are temporary by default but can be
        appended to the base_cmd if desired.
        """
        if default_args:
            for arg in additional_args:
                self.base_cmd.extend(shlex.split(arg))
        else:
            for arg in additional_args:
                self.temp_args.extend(shlex.split(arg))
