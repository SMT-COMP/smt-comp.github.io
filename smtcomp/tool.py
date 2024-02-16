from typing import List, Optional, Any
import benchexec.util as util
import benchexec.result as result
from benchexec.tools.template import BaseTool2
import sys, re

fallback_name = "./false"


class Tool(BaseTool2):  # type: ignore
    """
    Generic tool for smtcomp execution
    """

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
                if re.compile("^\s*(success|;.*)?\s*$").match(line):
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
        return util.find_executable("smtlib2_trace_executor", fallback=fallback_name, exitOnError=False)

    def version(self, executable: str) -> str:
        return ""

    def name(self) -> str:
        return "SC"

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
        assert len(options) >= 2, "options give the mode and command to run"
        cmd = options[0]
        options = options[1:]
        if cmd == "direct":
            return [*options, *tasks]
        elif cmd == "trace":
            if executable == fallback_name:
                sys.exit("benchexec smtcomp tool needs 'smtlib2_trace_executor' for tracing")
            else:
                return [executable, *options, *tasks]
        else:
            sys.exit("benchexec smtcomp executor accept only mode direct or trace")
