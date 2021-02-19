from curricula_grade.shortcuts import *
from curricula_grade.setup.common import check_file_exists
from curricula_grade_cpp.setup.common.gpp import gpp_compile_object
from curricula.library.files import delete_file

from pathlib import Path

root = Path(__file__).absolute().parent
grader = Grader()

GPP_OPTIONS = ("-std=c++14", "-Wall")


@grader.register(tags={"sanity"}, graded=False)
def check_submission(submission: Submission, resources: dict) -> SetupResult:
    """Check submission.cpp is present."""

    header_path = resources["source"] = submission.problem_path.joinpath("submission.cpp")
    return check_file_exists(header_path)


@grader.register(passing={"check_submission"}, tags={"sanity"}, graded=False)
def build_submission(source: Path, resources: dict) -> SetupResult:
    """Compile the submission."""

    result, resources["binary"] = gpp_compile_object(
        source,
        destination_path=source.parent.joinpath("binary"),
        gpp_options=GPP_OPTIONS)
    return result


@grader.register(passing={"build_submission"})
def test_simple_addition(binary: ExecutableFile) -> CorrectnessResult:
    """Check 1 + 1."""

    runtime = binary.execute("1", "1")
    if runtime.stdout.strip() != b"2":
        return CorrectnessResult(
            passing=False,
            actual=runtime.stdout.strip().decode(),
            expected="2",
            error=Error(description="incorrect result"),
            details=dict(runtime=runtime.dump()))
    return CorrectnessResult(passing=True)


@grader.register[CleanupResult](passing={"build_submission"}, tags={"sanity"}, graded=False)
def cleanup_submission(binary: ExecutableFile):
    """Delete the binary."""

    delete_file(binary.path)


# Ignore this, added so that example can be tested.
if __name__ == '__main__':
    import json
    from pathlib import Path
    from curricula_grade.models import GradingProblem

    root = Path(__file__).absolute().parent
    grader.problem = GradingProblem(short="test", title="Test")
    report = grader.run(context=Context(), submission=Submission(problem_path=root, assignment_path=root))

    print(json.dumps(report.dump(), indent=2))
