from typing import List, Optional, Any
import benchexec.util as util
import benchexec.result as result
from benchexec.tools.template import BaseTool2
import sys, re
import os

TRACE_EXECUTOR = "./smtlib2_trace_executor"


class IncrementalSMTCompTool(BaseTool2):  # type: ignore
    """
    Generic incremental tool for smtcomp execution
    """

    REQUIRED_PATHS = ["."]
    EXECUTABLE = "./false"
    NAME = "SMT-COMP generic incremental tool"

    def determine_result(self, run: BaseTool2.Run) -> Any:  # type: ignore
        returncode: int = run.exit_code.value
        returnsignal: int = run.exit_code.signal
        output: List[str] = run.output
        isTimeout: bool = run.was_timeout

        correct = 0
        status = None

        for line in output:
            line = line.strip()
            if line in ("sat", "unsat"):
                correct += 1
            if line.startswith("WRONG"):
                return "WRONG"

        if returnsignal is None:
            status = "DONE"
        elif ((returnsignal == 9) or (returnsignal == 15)) and isTimeout:
            status = "TIMEOUT"
        elif returnsignal == 9:
            status = "KILLED BY SIGNAL 9"
        elif returnsignal == 6:
            status = "ABORTED"
        elif returnsignal == 15:
            status = "KILLED"
        else:
            status = "ERROR"

        return f"{status} ({correct} correct)"

    def executable(self, _: Any) -> str | Any | None:
        return util.find_executable(self.EXECUTABLE, exitOnError=True)

    def version(self, executable: str) -> str:
        return ""

    def name(self) -> str:
        return self.NAME

    def cmdline(  # type: ignore
        self,
        executable: str,
        options: List[str],
        task: BaseTool2.Task,
        rlimits: BaseTool2.ResourceLimits,
    ) -> Any:
        tasks = task.input_files
        options = options + ([] if task.options is None else task.options)
        assert len(tasks) <= 1, "only one inputfile supported"
        if options:
            # executable and options were overridden by the task definition
            return [TRACE_EXECUTOR, *options, *tasks]
        else:
            # using default executable
            return [TRACE_EXECUTOR, executable, *tasks]

    def program_files(self, executable: str) -> list[str]:
        files = [TRACE_EXECUTOR, executable] + self._program_files_from_executable(executable, self.REQUIRED_PATHS)
        return files

    @staticmethod
    def _program_files_from_executable(executable: str, required_paths: list[str]) -> list[str]:
        scriptdir = os.path.dirname(os.path.abspath(__file__))
        basedir = os.path.join(scriptdir, os.path.pardir)

        return util.flatten(util.expand_filename_pattern(path, basedir) for path in required_paths)
