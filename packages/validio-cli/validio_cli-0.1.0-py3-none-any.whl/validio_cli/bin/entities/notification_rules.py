import typer
from camel_converter import to_snake

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

app = AsyncTyper(help="Notification rules for incidents")


@app.async_command(help="Get notification rules")
async def get(
    config_dir: str = ConfigDir,
    output_format: OutputFormat = OutputFormatOption,
    identifier: str = Identifier,
    source: str = typer.Option(
        None, help="List notification rules for this source (id)"
    ),
):
    vc, _ = await get_client_and_config(config_dir)

    # TODO: Get a single resource by id/name to not have to list.
    notification_rules = await vc.get_notification_rules_v2()
    notification_rules = [
        nr
        for nr in notification_rules
        if source is None or (nr is not None and source in nr.sources)
    ]
    notification_rules = _single_resource_if_specified(notification_rules, identifier)

    if output_format == OutputFormat.JSON:
        return output_json(notification_rules)

    return output_text(
        notification_rules,
        fields={
            "name": OutputSettings(attribute_name="resource_name"),
            "channel": OutputSettings(reformat=lambda x: x.resource_name),
            "type": OutputSettings(
                attribute_name="channel",
                reformat=lambda x: to_snake(
                    x.typename__.removesuffix("Channel")
                ).upper(),
            ),
            "age": OutputSettings(attribute_name="created_at"),
        },
    )


if __name__ == "__main__":
    typer.run(app())
