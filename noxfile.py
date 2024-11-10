from __future__ import annotations

import os

import nox


ROOT = os.path.dirname(os.path.abspath(__file__))


@nox.session
def build(session: nox.Session) -> None:
    """Build sdist and wheel dists."""
    session.install("pip", "build")
    session.install("setuptools")
    session.run("python", "--version")
    session.run("pip", "--version")
    session.run("python", "-m", "build")


@nox.session
def install(session: nox.Session) -> None:
    first_arg = session.posargs[0] if session.posargs else None

    if first_arg:
        if os.path.isfile(first_arg):
            session.install(first_arg)
        elif os.path.isdir(first_arg):
            session.install(
                "bmi_map", f"--find-links={first_arg}", "--no-deps", "--no-index"
            )
        else:
            session.error("path must be a source distribution or folder")
    else:
        session.install(".")


@nox.session
def test(session: nox.Session) -> None:
    """Run the tests."""
    session.install("-r", "requirements-testing.in")
    install(session)

    args = ["--cov", "bmi_map", "-vvv"]

    if "CI" in os.environ:
        args.append(f"--cov-report=xml:{ROOT}/coverage.xml")
    session.run("pytest", *args)

    if "CI" not in os.environ:
        session.run("coverage", "report", "--ignore-errors", "--show-missing")


@nox.session
def lint(session: nox.Session) -> None:
    """Look for lint."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files")