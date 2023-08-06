import typer
from camel_converter import to_snake
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

app = AsyncTyper(help="Windows used to group data for calculations")


@app.async_command(help="Get windows")
async def get(
    config_dir: str = ConfigDir,
    output_format: OutputFormat = OutputFormatOption,
    namespace: str = Namespace,
    identifier: str = Identifier,
    source: str = typer.Option(None, help="List Windows for this source (ID or name)"),
):
    vc, cfg = await get_client_and_config(config_dir)

    # TODO: Get a single resource by id/name to not have to list.
    windows = await vc.list_windows(
        filter=ResourceFilter(resourceNamespace=get_namespace(namespace, cfg))
    )
    windows = [
        window
        for window in windows
        if window is not None
        and validio_cli._resource_filter(window, ["source"], source)
    ]
    windows = _single_resource_if_specified(windows, identifier)

    if output_format == OutputFormat.JSON:
        return output_json(windows)

    return output_text(
        windows,
        fields={
            "name": OutputSettings(attribute_name="resource_name"),
            "source": OutputSettings(reformat=lambda source: source.resource_name),
            "type": OutputSettings(
                attribute_name="typename__",
                reformat=lambda x: to_snake(
                    x.removesuffix("Window").removesuffix("Batch")
                ).upper(),
            ),
            "age": OutputSettings(attribute_name="created_at"),
        },
    )


if __name__ == "__main__":
    typer.run(app())
