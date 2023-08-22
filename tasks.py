import subprocess

from invoke import task


@task
def clean_build(c):
    """
    Remove build artifacts
    """
    c.run("rm -fr build/")
    c.run("rm -fr dist/")
    c.run("rm -fr *.egg-info")


@task
def clean_pyc(c):
    """
    Remove python file artifacts
    """
    c.run("find . -name '*.pyc' -exec rm -f {} +")
    c.run("find . -name '*.pyo' -exec rm -f {} +")
    c.run("find . -name '*~' -exec rm -f {} +")


@task
def test_all(c):
    """
    Run tests on every python version with tox
    """
    c.run("tox")


@task
def clean(c):
    """
    Remove python file and build artifacts
    """
    clean_build(c)
    clean_pyc(c)


@task
def unittest(c):
    """
    Run unittests
    """
    c.run("python setup.py test")


@task
def lint(c):
    """
    Check style with flake8
    """
    c.run("flake8 jmespathutils tests")


class PublishError(Exception):
    pass


@task(help={'bumpsize': 'Bump either for a "feature" or "breaking" change'})
def release(c, bumpsize=''):
    """
    Package and upload a release
    """
    branch_response = subprocess.check_output('git branch', shell=True)
    if '* develop'.encode('utf-8') not in branch_response:
        raise PublishError("You are not in branch develop")
    print("You are in branch develop")

    clean(c)
    if bumpsize:
        bumpsize = '--' + bumpsize

    c.run("bumpversion {bump} --no-input".format(bump=bumpsize))

    import jmespathutils
    c.run("python setup.py sdist bdist_wheel")
    c.run("twine upload dist/*")

    c.run('git tag -a {version} -m "New version: {version}"'.format(version=jmespathutils.__version__))
    c.run("git push --tags")
    c.run("git push origin master")
