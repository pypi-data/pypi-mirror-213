from pathlib import Path
from typing import List

import typer
import yaml
from alteia import SDK
from alteia.core.errors import ResponseError
from alteia.core.resources.resource import Resource
from alteia_cli.sdk import alteia_sdk
from tabulate import tabulate
from yaml import FullLoader

from alteia_cli import AppDesc, utils  # type: ignore
from alteia_cli.plugins.dataflow_management.color_manager import (
    UniqueColor,
    get_colored_field_exists,
)

app = typer.Typer()
app_desc = AppDesc(
    app, name="datastreamtemplates", help="Interact with datastream templates."
)


def has_contextualisation(dst):
    result = False
    test = getattr(dst, "contextualisation", False)
    if test:
        result = True
    return result


def has_transformation(dst):
    result = False
    test = getattr(dst, "transform", False)
    if test:
        result = True
    return result


@app.command(name="list")
def list_datastreamtemplates(
    company: str = typer.Option(default=None, help="Company ID."),
    limit: int = typer.Option(default=10, help="Limit number of results."),
    asset_schema_repository: str = typer.Option(
        default=None, help="Asset schema repository name."
    ),
    asset_schema: str = typer.Option(default=None, help="Asset schema name."),
):
    """List datastream templates."""
    sdk: SDK = alteia_sdk()
    datastreamtemplates: List[Resource] = []
    with utils.spinner():
        try:
            filter_data = {}
            if company:
                filter_data = {"company": {"$eq": company}}
            if asset_schema_repository:
                filter_data = {
                    "contextualisation.parameters.assets_schema_repository": {
                        "$eq": asset_schema_repository
                    }
                }
            if asset_schema:
                filter_data = {
                    "contextualisation.parameters.schemas.assets_schema": {
                        "$eq": asset_schema
                    }
                }
            if company:
                filter_data = {"company": {"$eq": company}}
            search_results = sdk.datastreamtemplates.search(
                filter=filter_data, limit=limit
            )
            if isinstance(search_results, list):
                datastreamtemplates = search_results
            else:
                typer.secho("✖ Unexpected return results")
                raise typer.Exit(2)

        except ResponseError as e:
            typer.secho("✖ Failed to retrieve datastream templates")
            typer.secho(f"details: {e}", fg=typer.colors.RED)
            raise typer.Exit(2)

    asset_schema_repository_lst = []
    asset_schema_lst = []
    for dst in datastreamtemplates:
        if getattr(dst, "contextualisation", False):
            asset_schema_repository_lst.append(
                dst.contextualisation["parameters"]["assets_schema_repository"]
            )
            asset_schema_lst.append(
                ",".join(
                    s["assets_schema"]
                    for s in dst.contextualisation["parameters"]["schemas"]
                )
            )
        else:
            asset_schema_repository_lst.append("")
            asset_schema_lst.append("")
    color_company = UniqueColor()
    table = {
        "Id": [dst.id for dst in datastreamtemplates],
        "Name": [
            typer.style(dst.name, fg=typer.colors.GREEN, bold=True)
            for dst in datastreamtemplates
        ],
        "Company": [
            color_company.get_colored(dst.company) for dst in datastreamtemplates
        ],
        "Source": [dst.source["type"] for dst in datastreamtemplates],
        "Asset schema repository": asset_schema_repository_lst,
        "Asset schemas": asset_schema_lst,
        "Contextualisation": [
            get_colored_field_exists(has_contextualisation(ds))
            for ds in datastreamtemplates
        ],
        "Transformation": [
            get_colored_field_exists(has_transformation(ds))
            for ds in datastreamtemplates
        ],
    }

    print(
        tabulate(
            table,
            headers="keys",
            tablefmt="pretty",
        )
    )


@app.command()
def create(
    description: Path = typer.Option(
        ...,  # '...' in typer.Option() makes the option required
        exists=True,
        readable=True,
        help="Path of the datastream template description (YAML file).",
    ),
    company: str = typer.Option(..., help="Company identifier."),
):
    """Create a datastream template."""
    datastream_template = yaml.load(description.read_text(), Loader=FullLoader)
    datastream_template["company"] = company

    sdk: SDK = alteia_sdk()
    with utils.spinner():
        template = sdk.datastreamtemplates.create(**datastream_template)

    typer.secho(
        f"✓ Datastream template created with id {template.id}", fg=typer.colors.GREEN
    )


@app.command()
def delete(
    datastreamstemplate: str = typer.Argument(..., help="Datastream template ID"),
):
    """Delete a datastream template."""
    sdk: SDK = alteia_sdk()
    with utils.spinner():
        sdk.datastreamtemplates.delete(template=datastreamstemplate)

    typer.secho(
        f"✓ Datastream template {datastreamstemplate} deleted", fg=typer.colors.GREEN
    )
