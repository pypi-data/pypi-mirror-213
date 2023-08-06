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

app = AsyncTyper(help="Validators monitor data from your Source")


@app.async_command(help="Get Validators")
async def get(
    config_dir: str = ConfigDir,
    output_format: OutputFormat = OutputFormatOption,
    namespace: str = Namespace,
    identifier: str = Identifier,
    source: str = typer.Option(
        None, help="List Validators for this Source (name or ID)"
    ),
    destination: str = typer.Option(
        None, help="List Validators for this Destination (name or ID)"
    ),
    window: str = typer.Option(
        None, help="List Validators for this Window (name or ID)"
    ),
    segmentation: str = typer.Option(
        None, help="List Validators for this Segmentation (name or ID)"
    ),
):
    vc, cfg = await get_client_and_config(config_dir)

    validators: list[Any] = []

    # TODO: UI-1957
    # We don't want to get all resources if identifier is not id.
    # TODO: Add support for namespace
    if identifier is not None and identifier.startswith("MTR_"):
        validators.append(await vc.get_validator(id=identifier))
    elif source is None or not source.startswith("SRC_"):
        for s in await vc.list_sources(
            filter=ResourceFilter(resourceNamespace=get_namespace(namespace, cfg))
        ):
            validators.extend(await vc.list_validators(s.id))
    else:
        validators = await vc.list_validators(
            id=source,
            filter=ResourceFilter(resourceNamespace=get_namespace(namespace, cfg)),
        )

    validators = [
        validator
        for validator in validators
        if validio_cli._resource_filter(validator, ["source_config", "source"], source)
        and validio_cli._resource_filter(validator, ["source_config", "window"], window)
        and validio_cli._resource_filter(
            validator, ["source_config", "segmentation"], segmentation
        )
        and validio_cli._resource_filter(validator, ["destination"], destination)
    ]
    validators = _single_resource_if_specified(validators, identifier)

    if output_format == OutputFormat.JSON:
        return output_json(validators)

    return output_text(
        validators,
        fields={
            "name": OutputSettings(attribute_name="resource_name"),
            "type": OutputSettings.trimmed_upper_snake("typename__", "Validator"),
            "age": OutputSettings(attribute_name="created_at"),
        },
    )


if __name__ == "__main__":
    app()
