from enum import Enum
from typing import Any, Dict, List

import typer
import yaml
from alteia import SDK
from alteia.core.errors import ResponseError
from alteia.core.resources.resource import Resource
from alteia_cli.sdk import alteia_sdk
from dateutil import parser
from pydantic import BaseModel
from tabulate import tabulate

from alteia_cli import AppDesc, utils  # type: ignore
from alteia_cli.plugins.dataflow_management.color_manager import (
    UniqueColor,
    get_colored_field_exists,
)

app = typer.Typer()
app_desc = AppDesc(app, name="datastreams", help="Interact with datastream.")


class DatastreamStatusEnum(str, Enum):
    pending = "pending"
    listing = "listing"
    listing_error = "listing_error"
    running = "running"
    running_error = "running_error"
    waiting_for_completion = "waiting_for_completion"
    completion = "completion"
    completion_error = "completion_error"
    completed = "completed"
    error = "error"


def get_datastream_colored_status(status: str) -> str:
    if status == DatastreamStatusEnum.completed:
        colored_status = typer.style(status, fg=typer.colors.GREEN, bold=True)
    elif status in (
        DatastreamStatusEnum.listing_error,
        DatastreamStatusEnum.running_error,
        DatastreamStatusEnum.completion_error,
        DatastreamStatusEnum.error,
    ):
        colored_status = typer.style(status, fg=typer.colors.RED, bold=True)
    elif status in (DatastreamStatusEnum.waiting_for_completion):
        colored_status = typer.style(status, fg=typer.colors.BLUE, bold=True)
    else:
        colored_status = typer.style(status, fg=typer.colors.YELLOW, bold=True)
    return colored_status


def has_contextualisation(ds):
    result = False
    test = getattr(ds, "contextualisation", False)
    if test:
        result = True
    return result


def has_transformation(ds):
    return "transform" in ds.template


class DatastreamFileStatusEnum(str, Enum):
    pending = "pending"
    importing = "importing"
    importing_error = "importing_error"
    imported = "imported"
    transforming = "transforming"
    transforming_error = "transforming_error"
    complete = "complete"
    error = "error"


class DatastreamFileContextualisationStatusEnum(str, Enum):
    not_applicable = "not_applicable"
    pending = "pending"
    contextualising = "contextualising"
    contextualising_error = "contextualising_error"
    contextualised = "contextualised"


def get_datastream_file_colored_status(
    status: str, contextualisation_status: str
) -> str:
    if status == DatastreamFileStatusEnum.complete:
        colored_status = typer.style(status, fg=typer.colors.GREEN, bold=True)
    elif status in (
        DatastreamFileStatusEnum.importing_error,
        DatastreamFileStatusEnum.transforming_error,
        DatastreamFileStatusEnum.error,
    ):
        colored_status = typer.style(status, fg=typer.colors.RED, bold=True)
    elif (
        status == DatastreamFileStatusEnum.imported
        and contextualisation_status
        == DatastreamFileContextualisationStatusEnum.pending
    ):
        colored_status = typer.style(status, fg=typer.colors.BLUE, bold=True)
    elif (
        status == DatastreamFileStatusEnum.imported
        and contextualisation_status
        == DatastreamFileContextualisationStatusEnum.contextualised
    ):
        colored_status = typer.style(
            contextualisation_status, fg=typer.colors.BLUE, bold=True
        )
    elif status == DatastreamFileStatusEnum.imported and contextualisation_status in (
        DatastreamFileContextualisationStatusEnum.not_applicable,
        DatastreamFileContextualisationStatusEnum.contextualising_error,
    ):
        colored_status = typer.style(
            contextualisation_status, fg=typer.colors.RED, bold=True
        )
    elif (
        status == DatastreamFileStatusEnum.imported
        and contextualisation_status
        == DatastreamFileContextualisationStatusEnum.contextualising
    ):
        colored_status = typer.style(
            contextualisation_status, fg=typer.colors.YELLOW, bold=True
        )
    else:
        colored_status = typer.style(status, fg=typer.colors.YELLOW, bold=True)
    return colored_status


@app.command(name="list")
def list_datastreams(
    company: str = typer.Option(default=None, help="Company ID."),
    limit: int = typer.Option(default=10, help="Limit number of results."),
    asset_schema_repository: str = typer.Option(
        default=None, help="Asset schema repository name."
    ),
    asset_schema: str = typer.Option(default=None, help="Asset schema name."),
    asset_schema_repository_id: str = typer.Option(
        default=None, help="Asset schema repository id."
    ),
    asset_schema_id: str = typer.Option(default=None, help="Asset schema id."),
):
    """List datastreams."""
    sdk: SDK = alteia_sdk()
    datastreams = []
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
            if asset_schema_repository_id:
                filter_data = {
                    "contextualisation.parameters.assets_schema_repository_id": {
                        "$eq": asset_schema_repository_id
                    }
                }
            if asset_schema_id:
                filter_data = {
                    "contextualisation.parameters.schemas.assets_schema_id": {
                        "$eq": asset_schema_id
                    }
                }
            results = sdk.datastreamtemplates._provider.post(
                "/search-datastreams", data={"filter": filter_data, "limit": limit}
            )
            datastreams = [Resource(**r) for r in results["results"]]

        except ResponseError as e:
            typer.secho("✖ Failed to retrieve datastream")
            typer.secho(f"details: {e}", fg=typer.colors.RED)
            raise typer.Exit(2)

    color_company = UniqueColor()
    color_project = UniqueColor()
    table = {
        "Id": [dst.id for dst in datastreams],
        "Name": [
            typer.style(dst.name, fg=typer.colors.GREEN, bold=True)
            for dst in datastreams
        ],
        "Company": [color_company.get_colored(dst.company) for dst in datastreams],
        "Project": [color_project.get_colored(dst.project) for dst in datastreams],
        "Template": [dst.template["name"] for dst in datastreams],
        "Status": [
            get_datastream_colored_status(dst._desc.get("status", ""))
            for dst in datastreams
            if dst
        ],
        "Contextualisation": [
            get_colored_field_exists(has_contextualisation(ds)) for ds in datastreams
        ],
        "Transformation": [
            get_colored_field_exists(has_transformation(ds)) for ds in datastreams
        ],
    }

    print(
        tabulate(
            table,
            headers="keys",
            tablefmt="pretty",
        )
    )


@app.command(name="get")
def get_datastream(datastream_id: str = typer.Argument(..., help="Datastream ID")):
    """Get datastream description in yaml format."""
    sdk: SDK = alteia_sdk()
    with utils.spinner():
        try:
            datastream_dict = sdk.datastreamtemplates._provider.post(
                "/describe-datastream", data={"datastream": datastream_id}
            )
            datastream = Resource(**datastream_dict)

        except ResponseError as e:
            typer.secho("✖ Failed to retrieve datastream")
            typer.secho(f"details: {e}", fg=typer.colors.RED)
            raise typer.Exit(2)

    print(yaml.dump(datastream._desc))


def print_file(prestring: str, file: Resource):
    colored_status = get_datastream_file_colored_status(
        file._desc.get("status", ""), file._desc.get("contextualisation_status", "")
    )
    source = file._desc.get("import", {}).get("source", "")
    print(f"{prestring}{source} - {colored_status}")


@app.command(name="describe")
def describe_datastream(datastream_id: str = typer.Argument(..., help="Datastream ID")):
    """Describe datastream and its datastream files status."""
    sdk: SDK = alteia_sdk()
    datastream = None
    datastream_files = []
    with utils.spinner():
        try:
            datastream_dict = sdk.datastreamtemplates._provider.post(
                "/describe-datastream", data={"datastream": datastream_id}
            )
            datastream = Resource(**datastream_dict)

            data = {"filter": {"datastream": {"$eq": datastream.id}}}
            search_results = sdk.datastreamtemplates._provider.post(
                "/search-datastreams-files", data=data
            )
            datastream_files = [Resource(**f) for f in search_results["results"]]

        except ResponseError as e:
            typer.secho("✖ Failed to retrieve datastream")
            typer.secho(f"details: {e}", fg=typer.colors.RED)
            raise typer.Exit(2)

    branch = "│   "
    tee = "├── "
    last = "└── "

    status_val = get_datastream_colored_status(datastream._desc.get("status", ""))
    print(f"{datastream.name} - {status_val}")
    if len(datastream_files):
        print(branch)
        for file in datastream_files[:-1]:
            print_file(tee, file)
        print_file(last, datastream_files[-1])


@app.command(name="monitor-assets")
def monitor_datastream_assets(
    datastream_id: str = typer.Argument(..., help="Datastream ID")
):
    """Monitor datastream assets monitored."""
    sdk: SDK = alteia_sdk()
    datastream = None
    asset_monitoring = []
    with utils.spinner():
        try:
            datastream_dict = sdk.datastreamtemplates._provider.post(
                "/describe-datastream", data={"datastream": datastream_id}
            )
            datastream = Resource(**datastream_dict)

            data = {"filter": {"datastream": {"$eq": datastream.id}}}
            search_results = sdk.datastreamtemplates._provider.post(
                "/search-datastreams-assets-monitoring", data=data
            )
            asset_monitoring = [Resource(**f) for f in search_results["results"]]

        except ResponseError as e:
            typer.secho("✖ Failed to retrieve datastream")
            typer.secho(f"details: {e}", fg=typer.colors.RED)
            raise typer.Exit(2)

    def print_perc(perc):
        return f"{perc:.1f}%"

    def print_distance(distance):
        return f"{distance / 1000:.2f} Km"

    table = {
        "Asset": [ass.asset for ass in asset_monitoring],
        "Assets schema": [ass.assets_schema for ass in asset_monitoring],
        "Coveraged length": [
            print_distance(ass.coveraged_length) for ass in asset_monitoring
        ],
        "Total length": [print_distance(ass.total_length) for ass in asset_monitoring],
        "Coverage percentage": [
            print_perc(ass.coverage_percentage) for ass in asset_monitoring
        ],
        "Context length": [
            print_distance(
                ass._desc.get("contextualized", {}).get(
                    "asset_contextualized_length", 0
                )
            )
            for ass in asset_monitoring
        ],
        "Context perc": [
            print_perc(
                ass._desc.get("contextualized", {}).get(
                    "asset_contextualized_percentage", 0
                )
            )
            for ass in asset_monitoring
        ],
        "Transf length": [
            print_distance(
                ass._desc.get("transforming", {}).get("asset_transforming_length", 0)
            )
            for ass in asset_monitoring
        ],
        "Transf perc": [
            print_perc(
                ass._desc.get("transforming", {}).get(
                    "asset_transforming_percentage", 0
                )
            )
            for ass in asset_monitoring
        ],
        "Completed length": [
            print_distance(
                ass._desc.get("completed", {}).get("asset_completed_length", 0)
            )
            for ass in asset_monitoring
        ],
        "Completed perc": [
            print_perc(
                ass._desc.get("completed", {}).get("asset_completed_percentage", 0)
            )
            for ass in asset_monitoring
        ],
    }

    print(
        tabulate(
            table,
            headers="keys",
            tablefmt="pretty",
        )
    )


@app.command(name="create")
def create_datastream(
    name: str = typer.Option(..., help="Datastream name."),
    template: str = typer.Option(..., help="Datastream Template identifier."),
    source: str = typer.Option(..., help="Source url."),
    synchronisation: str = typer.Option(
        default="automatic", help="Source synchronisation."
    ),
    start_date: str = typer.Option(
        ..., help="Start date in format 2023-01-01T01:01:01Z."
    ),
    end_date: str = typer.Option(..., help="End date in format 2023-02-01T01:01:01Z."),
    description: str = typer.Option(default="", help="Description."),
    regex: str = typer.Option(default=".*las$", help="Regex."),
    project: str = typer.Option(
        default=None,
        help="Project identifier, used in order to describe a project target.",
    ),
):
    """Create a datastream from a datastream template."""
    start_date_dt = parser.isoparse(start_date)
    end_date_dt = parser.isoparse(end_date)
    sdk: SDK = alteia_sdk()
    data = {
        "name": name,
        "start_date": start_date_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "end_date": end_date_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": {
            "url": source,
            "regex": regex,
            "synchronisation": {"type": synchronisation},
        },
        "description": description,
        "template": template,
    }
    if project:
        data.update({"target": {"project": project}})

    datastream_dict = sdk.datastreamtemplates._provider.post(
        "/create-datastream", data=data
    )
    return Resource(**datastream_dict)


@app.command(name="complete")
def complete_datastream(datastream_id: str = typer.Argument(..., help="Datastream ID")):
    """Complete a datastream."""
    sdk: SDK = alteia_sdk()
    datastream_dict = sdk.datastreamtemplates._provider.post(
        "/complete-datastream", data={"datastream": datastream_id}
    )
    datastream = Resource(**datastream_dict)

    typer.secho(
        f"✓ Datastream completion started {datastream.id}", fg=typer.colors.GREEN
    )


@app.command(name="trigger")
def trigger_datastream(
    datastream_id: str = typer.Argument(..., help="Datastream ID"),
    max_nb_files_sync: int = typer.Option(
        default=20, help="Maximum number of files to synchronize."
    ),
    fill_runnings_files: bool = typer.Option(
        default=False,
        help="Synchronize files in order to reach the maximum number of files.",
    ),
):
    """Trigger a datastream in order to synchronise
    the datastream files with its source."""
    sdk: SDK = alteia_sdk()
    if fill_runnings_files:
        data = {
            "filter": {
                "datastream": {"$eq": datastream_id},
                "status": {
                    "$in": [
                        "importing",
                        "imported",
                        "contextualising",
                        "contextualised",
                        "transforming",
                    ]
                },
            },
            "limit": 1,
        }
        search_results = sdk.datastreamtemplates._provider.post(
            "/search-datastreams-files", data=data
        )
        if max_nb_files_sync <= search_results["total"]:
            typer.secho(
                f"✓ Datastream not triggered {datastream_id} maximum files asked "
                f"allready reached ({search_results['total']}/{max_nb_files_sync}) ",
                fg=typer.colors.YELLOW,
            )
            exit(0)
        max_nb_files_sync = max_nb_files_sync - search_results["total"]

    data = {"datastream": datastream_id, "max_nb_files_sync": max_nb_files_sync}
    datastream_dict = sdk.datastreamtemplates._provider.post(
        "/trigger-datastream", data=data
    )
    datastream = Resource(**datastream_dict)

    typer.secho(f"✓ Datastream triggered {datastream.id}", fg=typer.colors.GREEN)


class PartialEnumerationDataType(Enum):
    command_partial_aggregation = "command_partial_aggregation"
    partial_aggregation_started = "partial_aggregation_started"
    partial_aggregation_running = "partial_aggregation_running"
    partial_aggregation_completed = "partial_aggregation_completed"
    partial_aggregation_completed_with_errors = (
        "partial_aggregation_completed_with_errors"
    )

    def __lt__(self, other: "PartialEnumerationDataType"):
        order = {
            "command_partial_aggregation": 1,
            "partial_aggregation_started": 2,
            "partial_aggregation_running": 3,
            "partial_aggregation_completed": 4,
            "partial_aggregation_completed_with_errors": 5,
        }
        return order[self.value] < order[other.value]

    def printable(self):
        string_printable = {
            "command_partial_aggregation": ("commanded", typer.colors.YELLOW),
            "partial_aggregation_started": ("started", typer.colors.BLUE),
            "partial_aggregation_running": ("running", typer.colors.BLUE),
            "partial_aggregation_completed": ("completed", typer.colors.GREEN),
            "partial_aggregation_completed_with_errors": ("errors", typer.colors.RED),
        }
        status, color = string_printable[self.value]
        return typer.style(status, fg=color, bold=True)


class PartialAggregation(BaseModel):
    current_status: PartialEnumerationDataType
    events: List[Dict[str, Any]]
    aggregation_id: str
    outputs: List[str]

    @classmethod
    def from_event_list(cls, events: List[Dict[str, Any]]):
        aggregation_id = events[0]["data"]["tracking_oid"]
        events = sorted(
            events,
            key=lambda item: PartialEnumerationDataType(item["data"].get("type")),
        )
        current_status = PartialEnumerationDataType(events[-1]["data"].get("type"))
        outputs = events[-1]["data"].get("datasets", [])

        return cls(
            current_status=current_status,
            events=events,
            aggregation_id=aggregation_id,
            outputs=outputs,
        )


def list_partial_aggregations(sdk, datastream_id) -> List[PartialAggregation]:
    try:
        datastream_dict = sdk.datastreamtemplates._provider.post(
            "/describe-datastream", data={"datastream": datastream_id}
        )
        datastream = Resource(**datastream_dict)

        partial_aggregations_events = [
            e
            for e in datastream.events
            if e["data"].get("type") in [t.value for t in PartialEnumerationDataType]
        ]

        aggregations: Dict[str, List[Any]] = {}
        for e in partial_aggregations_events:
            if e["data"]["tracking_oid"] not in aggregations:
                aggregations[e["data"]["tracking_oid"]] = []
            aggregations[e["data"]["tracking_oid"]].append(e)

        return [
            PartialAggregation.from_event_list(events=a)
            for _, a in aggregations.items()
        ]

    except ResponseError as e:
        typer.secho("✖ Failed to retrieve datastream")
        typer.secho(f"details: {e}", fg=typer.colors.RED)
        raise typer.Exit(2)


@app.command(name="aggregate-partial-results")
def aggregate_datastream(
    datastream_id: str = typer.Argument(..., help="Datastream ID"),
    force_command: bool = typer.Option(
        default=False,
        help="Force partial aggregation command even if another one is running.",
    ),
):
    """Aggregate a datastream outputs using its aggregation parameters."""
    sdk: SDK = alteia_sdk()

    if not force_command:
        with utils.spinner():
            partial_aggregations = list_partial_aggregations(sdk, datastream_id)
        for p in partial_aggregations:
            if p.current_status in [
                PartialEnumerationDataType.command_partial_aggregation,
                PartialEnumerationDataType.partial_aggregation_started,
                PartialEnumerationDataType.partial_aggregation_running,
            ]:
                typer.secho(
                    "✖ Partial aggregation allready "
                    f"running for this datastream : {p.aggregation_id}",
                    fg=typer.colors.YELLOW,
                )
                raise typer.Exit(0)
    data = {"datastream": datastream_id}
    datastream_dict = sdk.datastreamtemplates._provider.post(
        "/aggregate-datastream-partial-results", data=data
    )
    datastream = Resource(**datastream_dict)

    typer.secho(
        f"✓ Datastream {datastream.id} partial results aggregation requested",
        fg=typer.colors.GREEN,
    )


@app.command(name="list-partial-aggregations")
def list_partial_aggregations_command(
    datastream_id: str = typer.Argument(..., help="Datastream ID"),
):
    """List ongoing aggregation for a datastream."""
    sdk: SDK = alteia_sdk()

    partial_aggregations: List[PartialAggregation] = []
    with utils.spinner():
        partial_aggregations = list_partial_aggregations(sdk, datastream_id)

    table = {
        "Aggregation id": [pa.aggregation_id for pa in partial_aggregations],
        "Status": [pa.current_status.printable() for pa in partial_aggregations],
        "Outputs": [pa.outputs for pa in partial_aggregations],
    }

    print(
        tabulate(
            table,
            headers="keys",
            tablefmt="pretty",
        )
    )
