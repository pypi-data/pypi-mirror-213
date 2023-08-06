from dataclasses import dataclass

import typer
from validio_sdk.graphql_client import input_types

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
from validio_cli.bin.entities import sources

app = AsyncTyper(help="Recommended validators for your sources")

APPLY_RESULT_SUCCEEDED = "SUCCEEDED"
APPLY_RESULT_FAILED = "FAILED"


@dataclass
class ApplyResult:
    """Result from applying recommendation"""

    id: str
    state: str


@app.async_command(help="List all recommendations")
async def get(
    config_dir: str = ConfigDir,
    output_format: OutputFormat = OutputFormatOption,
    identifier: str = Identifier,
    source: str = typer.Option(
        ..., help="List recommendations for this source (id or name)"
    ),
):
    vc, _ = await get_client_and_config(config_dir)

    source_id = await sources._get_source_id(vc, source)
    if source_id is None:
        return None

    recommendations = await vc.get_source_recommended_validators(id=source_id)

    # TODO: Add endpoint to get a single recommendation by id
    if recommendations is not None:
        recommendations = _single_resource_if_specified(
            recommendations.recommended_validators, identifier
        )

    if output_format == OutputFormat.JSON:
        return output_json(recommendations)

    return output_text(
        recommendations,
        fields={
            "id": None,
            "name": None,
            "type": OutputSettings.trimmed_upper_snake(
                attribute_name="typename__", trim="Validator"
            ),
            "age": OutputSettings(attribute_name="created_at"),
        },
    )


@app.async_command(help="Apply recommendations")
async def apply(
    config_dir: str = ConfigDir,
    output_format: OutputFormat = OutputFormatOption,
    ids: list[str] = typer.Option(
        ..., "--id", help="Recommendations to apply (ids), can supports multiple values"
    ),
):
    vc, _ = await get_client_and_config(config_dir)

    api_result = await vc.apply_validator_recommendation(
        input=input_types.ValidatorRecommendationApplyInput(ids=ids)
    )

    result = []
    seen_ids = set()

    for r, state in [
        (api_result.failed_ids, APPLY_RESULT_FAILED),
        (api_result.success_ids, APPLY_RESULT_SUCCEEDED),
    ]:
        for id in r:
            seen_ids.add(id)
            result.append(ApplyResult(id=id, state=state))

    # TODO: The API silently accepts unknown ids but we want to add them as
    # failed in the output so the caller know they've not been applied.
    for id in ids:
        if id in seen_ids:
            continue

        result.append(ApplyResult(id=id, state=APPLY_RESULT_FAILED))

    if output_format == OutputFormat.JSON:
        return output_json(result)

    return output_text(
        result,
        fields={
            "id": None,
            "state": None,
        },
    )


if __name__ == "__main__":
    typer.run(app())
