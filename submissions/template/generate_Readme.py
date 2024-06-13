from pathlib import Path
from string import Template
from urllib.parse import quote

import rich
import typer

app = typer.Typer()


def substitute():
    tdir = Path("submissions").joinpath("template")

    json = tdir.joinpath("template.json").read_text()
    json = quote(json, safe="")

    src = tdir.joinpath("template.md")
    src = Template(src.read_text())

    result = '[//]: # "Generated from submissions/template/template.md"\n\n'
    result += src.safe_substitute({"value": json})
    return result


dst = Path("submissions").joinpath("Readme.md")


@app.command()
def generate():
    dst.write_text(substitute())


@app.command()
def check():
    current = dst.read_text()
    oracle = substitute()
    if current == oracle:
        rich.print(":white_check_mark: submissions/Readme.md is up to date")
        exit(0)
    else:
        rich.print(":heavy_exclamation_mark: submissions/Readme.md is obsolete!")
        exit(1)


app()
