from typing import List, Optional, Any
import benchexec.util as util
import benchexec.result as result
from benchexec.tools.template import BaseTool2
import sys, re
import os


class SMTCompTool(BaseTool2):  # type: ignore
    """
    Generic tool for smtcomp execution
    """

    REQUIRED_PATHS = ["."]
    EXECUTABLE = "./false"
    NAME = "SMT-COMP generic tool"

    def determine_result(self, run: BaseTool2.Run) -> Any:  # type: ignore
        """Adaptation of Jochen Hoenicke process script

        A simple post-processor for SMT.
        The logic is:
         - remove success outputs (they're ignored for now)
         - take the first line
         - all other lines after it ignored
         - if the line is sat, unsat, or unknown this is the status
         - if no such line exists, the status is unknown.
         - all lines after the result are ignored.
        """

        returncode: int = run.exit_code.value
        returnsignal: int = run.exit_code.signal
        output: List[str] = run.output
        isTimeout: bool = run.was_timeout

        if returnsignal is None:
            status = None
            for line in output:
                line = line.strip()
                # ignore
                if re.compile(r"^\s*(success|;.*)?\s*$").match(line):
                    continue
                if line == "unsat":
                    return result.RESULT_FALSE_PROP
                elif line == "sat":
                    return result.RESULT_TRUE_PROP
                else:
                    return result.RESULT_UNKNOWN
            return result.RESULT_UNKNOWN

        elif ((returnsignal == 9) or (returnsignal == 15)) and isTimeout:
            status = result.RESULT_TIMEOUT

        elif returnsignal == 9:
            status = "KILLED BY SIGNAL 9"
        elif returnsignal == 6:
            status = "ABORTED"
        elif returnsignal == 15:
            status = "KILLED"
        else:
            status = f"ERROR ({returncode})"

        return status

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
            return [*options, *tasks]
        else:
            # using default executable
            return [executable, *tasks]

    def program_files(self, executable: str) -> Any:
        files = [executable] + self._program_files_from_executable(executable, self.REQUIRED_PATHS)
        return files

    @staticmethod
    def _program_files_from_executable(executable: str, required_paths: list[str]) -> Any:
        scriptdir = os.path.dirname(os.path.abspath(__file__))
        basedir = os.path.join(scriptdir, os.path.pardir)

        return util.flatten(util.expand_filename_pattern(path, basedir) for path in required_paths)
