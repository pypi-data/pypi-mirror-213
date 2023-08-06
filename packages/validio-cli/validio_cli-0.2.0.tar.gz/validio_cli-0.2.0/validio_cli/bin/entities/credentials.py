import typer
from validio_sdk.graphql_client.input_types import ResourceFilter

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

app = AsyncTyper(help="Credentials used for Sources and Destinations")


@app.async_command(help="Get credentials")
async def get(
    config_dir: str = ConfigDir,
    output_format: OutputFormat = OutputFormatOption,
    namespace: str = Namespace,
    identifier: str = Identifier,
):
    vc, cfg = await get_client_and_config(config_dir)

    # TODO: Get a single resource by id/name to not have to list.
    credentials = await vc.list_credentials(
        filter=ResourceFilter(resourceNamespace=get_namespace(namespace, cfg))
    )
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
