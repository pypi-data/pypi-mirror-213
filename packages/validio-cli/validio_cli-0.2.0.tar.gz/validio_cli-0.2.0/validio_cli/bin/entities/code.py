import pathlib
import re
import sys
from collections.abc import Mapping
from enum import Enum
from typing import Any

import classdiff  # type: ignore
import prompt_toolkit
import typer
from validio_sdk.code import apply as code_apply
from validio_sdk.code import plan as code_plan
from validio_sdk.code import scaffold
from validio_sdk.resource._diff import DiffContext, GraphDiff, ResourceUpdate
from validio_sdk.resource._resource import Resource
from validio_sdk.resource._util import SourceSchemaReinference
from validio_sdk.validio_client import ValidioAPIClient

from validio_cli import AsyncTyper, ConfigDir, get_client_and_config

app = AsyncTyper(help="Plan or apply your configuration")


class DiffOutput(str, Enum):
    """Available output formats for the CLI"""

    FULL = "full"
    CHANGES = "changes"
    NONE = "none"


directory_option = typer.Option(
    "",
    help=(
        "The location to place the generated project; "
        "Defaults to the current directory if not specified"
    ),
)

no_capture_option: bool = typer.Option(
    False,
    help=(
        "By default, the code program's stdout output is hidden; "
        "enable this parameter to recover the output"
    ),
)

show_schema_option = typer.Option(
    False, help="Show the JTD schema in the plan output for Sources"
)

diff_option = typer.Option(
    DiffOutput.CHANGES.value,
    "--diff",
    help="Show only the changed lines (added, removed, or modified)",
)

destroy_option = typer.Option(
    False, help="Deletes all resources associated with the project"
)

show_secrets_option = typer.Option(
    False,
    help=(
        "By default, secret values within credentials are not shown; "
        "enable this parameter to show the values"
    ),
)

update_schema_option = typer.Option(
    None,
    help=(
        "Specify a Source name to update its schema. This checks the upstream data"
        " source for any schema changes before planning. You can use"
        " --update-schema src1 --update-schema src2 to specify multiple Sources."
    ),
)

update_all_schemas_option = typer.Option(
    False,
    help=(
        "Similar to --update-schema. Checks for schema "
        "updates for all Sources before planning"
    ),
)


@app.command()
def init(
    directory: str = directory_option,
    force: bool = typer.Option(
        False, help="Forces project files to be generated in a non-empty directory"
    ),
    namespace: str = typer.Option(
        "dev", help="A unique name to associate resources managed by the project"
    ),
):
    dir_path = directory_or_default(directory)

    scaffold._new_project(namespace, dir_path, force)


@app.async_command()
async def plan(
    directory: str = directory_option,
    no_capture: bool = no_capture_option,
    config_dir: str = ConfigDir,
    update_schema: list[str] = update_schema_option,
    update_all_schemas: bool = update_all_schemas_option,
    show_schema: bool = show_schema_option,
    diff_output: DiffOutput = diff_option,
    destroy: bool = destroy_option,
    show_secrets: bool = show_secrets_option,
):
    dir_path = directory_or_default(directory)
    client, _ = await get_client_and_config(config_dir)

    schema_reinference = create_source_schema_reinference(
        update_schema, update_all_schemas
    )

    namespace = get_namespace(dir_path)
    await _plan(
        namespace=namespace,
        client=client,
        directory=dir_path,
        schema_reinference=schema_reinference,
        destroy=destroy,
        no_capture=no_capture,
        show_schema=show_schema,
        diff_output=diff_output,
        show_secrets=show_secrets,
    )


@app.async_command()
async def apply(
    directory: str = directory_option,
    no_capture: bool = no_capture_option,
    auto_approve: bool = typer.Option(
        False, help="Automatically approve and perform plan operations"
    ),
    config_dir: str = ConfigDir,
    update_schema: list[str] = update_schema_option,
    update_all_schemas: bool = update_all_schemas_option,
    show_schema: bool = show_schema_option,
    diff_output: DiffOutput = diff_option,
    destroy: bool = destroy_option,
    show_secrets: bool = show_secrets_option,
):
    dir_path = directory_or_default(directory)
    client, _ = await get_client_and_config(config_dir)

    schema_reinference = create_source_schema_reinference(
        update_schema, update_all_schemas
    )

    namespace = get_namespace(dir_path)
    diff, manifest_ctx = await _plan(
        namespace=namespace,
        client=client,
        directory=dir_path,
        schema_reinference=schema_reinference,
        destroy=destroy,
        no_capture=no_capture,
        show_schema=show_schema,
        diff_output=diff_output,
        show_secrets=show_secrets,
    )

    if diff.num_operations() == 0:
        return

    print()
    print("Do you want to perform these operations?")
    print("\tOnly 'yes' is accepted to approve")

    if not auto_approve:
        session: prompt_toolkit.PromptSession = prompt_toolkit.PromptSession()
        p = await session.prompt_async("Enter a value: ")
        if p != "yes":
            print("Cancelled")
            return

    print()
    print("Applying...")

    await code_apply.apply(
        namespace=namespace,
        client=client,
        ctx=manifest_ctx,
        diff=diff,
        show_secrets=show_secrets,
    )

    print(
        f"Apply complete! Resources: {diff.num_creates()} created, "
        f"{diff.num_updates()} updated, {diff.num_deletes()} deleted"
    )


def get_namespace(directory: pathlib.Path) -> str:
    settings = scaffold._read_project_settings(directory)
    return settings.namespace


def directory_or_default(directory: str) -> pathlib.Path:
    return (pathlib.Path(directory) if directory else pathlib.Path.cwd()).absolute()


async def _plan(
    namespace: str,
    client: ValidioAPIClient,
    directory: pathlib.Path,
    schema_reinference: SourceSchemaReinference,
    destroy: bool,
    no_capture: bool,
    show_schema: bool = False,
    diff_output: DiffOutput = DiffOutput.FULL,
    show_secrets: bool = False,
) -> tuple[GraphDiff, DiffContext]:
    (diff, manifest_ctx) = await code_plan.plan(
        namespace=namespace,
        client=client,
        directory=directory,
        schema_reinference=schema_reinference,
        destroy=destroy,
        no_capture=no_capture,
        show_secrets=show_secrets,
    )

    if diff.num_operations() == 0:
        print("No changes. The configuration is up-to-date!")
        return diff, manifest_ctx

    _show_resources_diff(
        diff=diff,
        show_schema=show_schema,
        show_secrets=show_secrets,
        escape=sys.stdout.isatty(),
        diff_output=diff_output,
    )

    return diff, manifest_ctx


# https://stackoverflow.com/a/14693789/2274551
ansi_escape = re.compile(
    r"""
   \x1B  # ESC
   (?:   # 7-bit C1 Fe (except CSI)
       [@-Z\\-_]
   |     # or [ for CSI, followed by a control sequence
       \[
       [0-?]*  # Parameter bytes
       [ -/]*  # Intermediate bytes
       [@-~]   # Final byte
   )
""",
    re.VERBOSE,
)


def _show_resources_diff(
    diff: GraphDiff,
    show_schema: bool,
    show_secrets: bool,
    escape: bool,
    diff_output: DiffOutput,
):
    resource_types = DiffContext.fields()
    if diff.num_creates() > 0:
        for t in resource_types:
            _show_create_resource_diff(
                getattr(diff.to_create, t),
                show_schema,
                show_secrets,
                escape,
                diff_output,
            )

    if diff.num_deletes() > 0:
        for t in resource_types:
            _show_delete_resource_diff(
                getattr(diff.to_delete, t),
                show_schema,
                show_secrets,
                escape,
                diff_output,
            )

    if diff.num_updates() > 0:
        for t in resource_types:
            _show_update_resource_diff(
                resources=getattr(diff.to_update, t),
                show_schema=show_schema,
                show_secrets=show_secrets,
                color=escape,
                diff_output=diff_output,
            )

    print(
        "\n"
        f"Plan: {diff.num_creates()} to create, {diff.num_updates()} to update, "
        f"{diff.num_deletes()} to delete."
    )


def _show_create_resource_diff(
    resources: Mapping[str, Resource],
    show_schema: bool,
    show_secrets: bool,
    color: bool,
    diff_output: DiffOutput,
):
    for r in resources.values():
        class_key = r.__class__.__name__

        print(f"{class_key} '{r.name}' will be created")

        rewrites = _diff_field_rewrites(show_schema)
        value = code_plan._create_resource_diff_object(
            r, rewrites=rewrites, show_secrets=show_secrets
        )
        diff = classdiff.diff(a=value, b=None, class_key=class_key)

        _show_diff(diff, color, diff_output)


def _show_delete_resource_diff(
    resources: Mapping[str, Resource],
    show_schema: bool,
    show_secrets: bool,
    color: bool,
    diff_output: DiffOutput,
):
    for r in resources.values():
        class_key = r.__class__.__name__

        print(f"{class_key} '{r.name}' will be deleted")

        rewrites = _diff_field_rewrites(show_schema)
        value = code_plan._create_resource_diff_object(
            r, rewrites=rewrites, show_secrets=show_secrets
        )
        diff = classdiff.diff(a=None, b=value, class_key=class_key)

        _show_diff(diff, color, diff_output)


def _show_update_resource_diff(
    resources: Mapping[str, ResourceUpdate],
    show_schema: bool,
    show_secrets: bool,
    color: bool,
    diff_output: DiffOutput,
):
    for r in resources.values():
        class_key = r.manifest.resource.__class__.__name__

        print(f"{class_key} '{r.manifest.resource.name}' will be updated")

        rewrites = _diff_field_rewrites(show_schema)
        a_value = code_plan._create_resource_diff_object(
            r.manifest.resource, show_secrets=show_secrets, rewrites=rewrites
        )
        b_value = code_plan._create_resource_diff_object(
            r.server.resource, show_secrets=show_secrets, rewrites=rewrites
        )
        diff = classdiff.diff(a=a_value, b=b_value, class_key=class_key)

        _show_diff(diff, color, diff_output)


def _show_diff(diff: Any, color: bool, diff_output: DiffOutput):
    if diff_output == DiffOutput.NONE:
        return

    # We keep track if any lines were printed at all (any changes or full
    # output) and if not we don't add a newline. This is to make it more
    # condensed and consistent with the DiffOutput.NONE output.
    any_lines_printed = False

    for diff_info in diff:
        if (
            diff_output == DiffOutput.CHANGES
            and diff_info.diff_type == classdiff.DiffType.UNCHANGED
        ):
            continue

        any_lines_printed = True
        line = str(diff_info)
        if not color:
            line = ansi_escape.sub("", line)
        print(f"{line}")

    if any_lines_printed:
        print()


def _diff_field_rewrites(show_schema: bool) -> dict[str, Any]:
    return {} if show_schema else {"jtd_schema": "[NOT SHOWN]"}


def create_source_schema_reinference(
    schemas_to_update: list[str], update_all_schemas: bool
) -> SourceSchemaReinference:
    source_names = None
    if update_all_schemas:
        source_names = []
    elif len(schemas_to_update) > 0:
        source_names = schemas_to_update

    return SourceSchemaReinference(set(source_names) if source_names else None)


if __name__ == "__main__":
    app()
