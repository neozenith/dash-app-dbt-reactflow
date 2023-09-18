from invoke import task
import shutil


@task
def format(c):
    """Autoformat code for code style."""
    c.run("black .")
    c.run("isort .")


@task
def lint(c):
    """Linting and style checking."""
    c.run("black --check .")
    c.run("isort --check .")
    c.run("flake8 .")


@task
def typecheck(c):
    """Run typechecking tooling."""
    c.run("mypy .")


@task
def test(c):
    """Run test suite."""
    c.run("python3 -m pytest")


@task
def build(c):
    """Build wheel."""
    shutil.rmtree("dist/", ignore_errors=True)
    c.run("poetry build -f wheel")


@task(pre=[lint, typecheck, test])
def ci(c):
    """Run linting and test suite for Continuous Integration."""
    ...

@task
def serve(c):
    """Start Dash server."""
    c.run("gunicorn dash.app:server")

@task
def dev(c):
    """Start Dash server."""
    c.run("python3 dash_app_dbt_reactflow/app.py")

@task
def dev_dbt(c):
    """Start Dash server."""
    c.run("hypercorn dbt-server.app:app --reload")

@task
def dev_db(c):
    """Start test postgreSQL database."""
    c.run(f"""
docker run -d \
	--name dbt-postgres \
    -p 5432:5432 \
    -e POSTGRES_DB=jaffle_shop \
	-e POSTGRES_PASSWORD=mysecretpassword \
	-e PGDATA=/var/lib/postgresql/data/pgdata \
	-v ./dbt-data/:/var/lib/postgresql/data \
	postgres
          """)
    