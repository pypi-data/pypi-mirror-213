from typing import Any

import typer
from validio_sdk.graphql_client.input_types import ResourceFilter

import validio_cli
from validio_cli import (
    AsyncTyper,
    ConfigDir,
    Identifier,
    Namespace,
    OutputFormat,
    OutputFormatOption,
    OutputSettings,
    _single_resource_if_specified,
    get_client_and_config,
    output_json,
    output_text,
)
from validio_cli.namespace import get_namespace

app = AsyncTyper(help="Segmentation to group data")


@app.async_command(help="List all Segmentations")
async def get(
    config_dir: str = ConfigDir,
    output_format: OutputFormat = OutputFormatOption,
    namespace: str = Namespace,
    identifier: str = Identifier,
    source: str = typer.Option(
        None, help="List Segmentations for this Source (ID or name)"
    ),
):
    vc, cfg = await get_client_and_config(config_dir)

    segmentations: list[Any] = []

    # TODO: UI-1957
    # We don't want to get all resources if identifier is not id.
    # TODO: Add namespace support in API
    if identifier is not None and identifier.startswith("SGM_"):
        segmentations = [await vc.get_segmentation(id=identifier)]
    else:
        segmentations = await vc.list_segmentations(
            filter=ResourceFilter(resourceNamespace=get_namespace(namespace, cfg))
        )

    segmentations = [
        segmentation
        for segmentation in segmentations
        if segmentation is not None
        and validio_cli._resource_filter(segmentation, ["source"], source)
    ]
    segmentations = _single_resource_if_specified(segmentations, identifier)

    if output_format == OutputFormat.JSON:
        return output_json(segmentations)

    return output_text(
        segmentations,
        fields={
            "name": OutputSettings(attribute_name="resource_name"),
            "source": OutputSettings(reformat=lambda source: source.resource_name),
            "age": OutputSettings(attribute_name="created_at"),
        },
    )


if __name__ == "__main__":
    typer.run(app())
