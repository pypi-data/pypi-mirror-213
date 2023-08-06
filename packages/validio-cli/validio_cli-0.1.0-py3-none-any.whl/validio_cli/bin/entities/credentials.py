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

app = AsyncTyper(help="Credentials used for sources and destinations")


@app.async_command(help="Get credentials")
async def get(
    config_dir: str = ConfigDir,
    output_format: OutputFormat = OutputFormatOption,
    identifier: str = Identifier,
):
    vc, _ = await get_client_and_config(config_dir)

    # TODO: Get a single resource by id/name to not have to list.
    credentials = await vc.list_credentials()
    credentials = _single_resource_if_specified(credentials, identifier)

    if output_format == OutputFormat.JSON:
        return output_json(credentials)

    return output_text(
        credentials,
        fields={
            "name": OutputSettings(attribute_name="resource_name"),
            "type": OutputSettings.trimmed_upper_snake("typename__", "Credential"),
            "age": OutputSettings(attribute_name="created_at"),
        },
    )


if __name__ == "__main__":
    typer.run(app())
