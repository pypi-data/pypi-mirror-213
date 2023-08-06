import typer

from validio_cli import (
    AsyncTyper,
    ConfigDir,
    Identifier,
    OutputFormat,
    OutputFormatOption,
    OutputSettings,
    _single_resource_if_specified,
    get_client_and_config,
    output_json,
    output_text,
)

app = AsyncTyper(help="Destinations where anomalies are sent")


@app.async_command(help="List all destinations")
async def get(
    config_dir: str = ConfigDir,
    output_format: OutputFormat = OutputFormatOption,
    identifier: str = Identifier,
):
    vc, _ = await get_client_and_config(config_dir)

    # TODO: Get a single resource by id/name to not have to list.
    destinations = await vc.list_destinations()
    destinations = _single_resource_if_specified(destinations, identifier)

    if output_format == OutputFormat.JSON:
        return output_json(destinations)

    return output_text(
        destinations,
        fields={
            "name": OutputSettings(attribute_name="resource_name"),
            "type": OutputSettings.trimmed_upper_snake("typename__", "Destination"),
            "age": OutputSettings(attribute_name="created_at"),
        },
    )


if __name__ == "__main__":
    typer.run(app())
