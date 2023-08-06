import nox

nox.options.sessions = ["format", "tests"]


@nox.session
def format(session):
    session.install("isort", "black")
    session.run("isort", ".")
    session.run("black", ".")


@nox.session
def tests(session):
    session.install("--editable", ".")
    session.install("pytest")
    session.run("pytest")


@nox.session
def build(session):
    session.install("build")
    session.run("python", "-m", "build")
