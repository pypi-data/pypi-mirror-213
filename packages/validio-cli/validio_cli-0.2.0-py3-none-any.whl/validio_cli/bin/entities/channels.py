import typer
from camel_converter import to_snake
from validio_sdk.graphql_client.input_types import ResourceFilter

from validio_cli import (
    AsyncTyper,
    ConfigDir,
    Identifier,
    Namespace,
    OutputFormat,
    OutputFormatOption,
    OutputSettings,
    get_client_and_config,
    output_json,
    output_text,
)
from validio_cli.namespace import get_namespace

app = AsyncTyper(help="Channels used for notifications")


@app.async_command(help="Get channels")
async def get(
    config_dir: str = ConfigDir,
    output_format: OutputFormat = OutputFormatOption,
    namespace: str = Namespace,
    identifier: str = Identifier,
):
    vc, cfg = await get_client_and_config(config_dir)
    ns = get_namespace(namespace, cfg)

    if identifier is not None:
        channels = await vc.get_channel_by_resource_name(
            resource_name=identifier, resource_namespace=ns
        )
    else:
        channels = await vc.get_channels(filter=ResourceFilter(resourceNamespace=ns))

    if output_format == OutputFormat.JSON:
        return output_json(channels)

    return output_text(
        channels,
        fields={
            "name": OutputSettings(attribute_name="resource_name"),
            "type": OutputSettings(
                attribute_name="typename__",
                reformat=lambda x: to_snake(x.removesuffix("Channel")).upper(),
            ),
            "age": OutputSettings(attribute_name="created_at"),
        },
    )


if __name__ == "__main__":
    typer.run(app())
