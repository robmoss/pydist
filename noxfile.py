import nox


@nox.session(reuse_venv=True)
def tests(session):
    """Run test cases and record the test coverage."""
    session.install('.[tests]')
    # Run the test cases and report the test coverage.
    package = 'pydist'
    session.run(
        'pytest',
        f'--cov={package}',
        '--pyargs',
        package,
        './tests',
        # './doc',
        *session.posargs,
    )


@nox.session(reuse_venv=True)
def ruff(session):
    """Check code for linter warnings and formatting issues."""
    # check_files = ['src', 'tests', 'doc', 'noxfile.py']
    check_files = ['src', 'tests', 'noxfile.py']
    session.install('ruff ~= 0.5')
    session.run('ruff', 'check', *check_files)
    session.run('ruff', 'format', '--diff', *check_files)
