import tempfile

import nox

locations = "src", "noxfile.py"
nox.options.sessions = ("black", "isort", "lint")


def install_with_constraints(session, *args, **kwargs):
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--without-hashes",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session(python="3.8")
def lint(session):
    args = session.posargs or locations
    install_with_constraints(session, "flake8", "flake8-bandit")
    session.run("flake8", *args)


@nox.session(python="3.8")
def black(session):
    args = session.posargs or locations
    install_with_constraints(session, "black")
    session.run("black", *args)


@nox.session(python="3.8")
def isort(session):
    args = session.posargs or locations
    install_with_constraints(session, "isort")
    session.run("isort", *args)
