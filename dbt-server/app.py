from typing import Union

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse

from dbt.cli.main import dbtRunner, dbtRunnerResult

import os

app = FastAPI()

DBT_PROJECTS = [d for d in os.listdir('./dbt/') if d not in [".DS_Store"]]
ACCEPTED_COMMANDS = ["debug", "list", "parse", "compile", "build", "clean", "docs"]


for proj in DBT_PROJECTS:
    app.mount(f"/project/{proj}/d/", StaticFiles(directory=f"./dbt/{proj}/target/", html=True, check_dir=False), name=f"{proj} Documentation site.")


# initialize
dbt = dbtRunner()

@app.get("/")
def root():
    return RedirectResponse("/projects", status_code=303)


@app.get("/projects")
def list_projects():

    html = f"""
<html>
<body><ul>
    """
    
    for proj in DBT_PROJECTS:
        html = html + f"""
        <li>
            <a href="/project/{proj}/d/">{proj} Documentation (may need to run /docs endpoint first)</a>
            <ul>
        """

        for c in ACCEPTED_COMMANDS:
            html = html + f"""
            <li><a href="/project/{proj}/{c}">{c}</a></li>
            """

        html = html + f"""
            </ul>
        </li>
        """
    
    html = html + f"""
    </ul>
    </body>
    </html>
    """

    return HTMLResponse(html, 200)


@app.get("/project/{item_id}/{dbt_command}")
def project(item_id: str, dbt_command: str = list, q: Union[str, None] = None):
    if dbt_command not in ACCEPTED_COMMANDS:
        raise ValueError(f"{dbt_command} should be one of {ACCEPTED_COMMANDS}.")
    cmd = [dbt_command] 
    if dbt_command == "docs":
        cmd = ["docs", "generate"]
    
    cmd = cmd + ["--project-dir", f"./dbt/{item_id}", "--profiles-dir", f"./dbt-profiles/{item_id}"]
    
    res: dbtRunnerResult = dbt.invoke(cmd)
    print(res)
    return {"item_id": item_id, "q": q, "result": str(res)}
