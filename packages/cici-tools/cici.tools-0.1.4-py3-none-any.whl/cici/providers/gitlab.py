import functools
import io
import json
import typing

import jsonschema
import ruamel.yaml
from jinja2 import Environment

from ..constants import SCHEMA_DIR
from ..utils import make_scalar_list, make_scalar_string
from . import brettops


@functools.cache
def load_gitlab_ci_schema() -> typing.Any:
    schema_file = SCHEMA_DIR / "gitlab-ci.json"
    return json.load(open(schema_file))


def validate_gitlab_ci(data: typing.Any):
    schema = load_gitlab_ci_schema()
    jsonschema.validate(data, schema=schema)


def dump_gitlab_ci_image(
    environment: typing.Optional[brettops.Environment],
) -> typing.Optional[typing.Any]:
    if environment is None:
        return None
    if environment.entrypoint:
        return dict(
            name=environment.image,
            entrypoint=environment.entrypoint,
        )
    return environment.image


def get_inputs(pipeline: brettops.Job, job: brettops.Job):
    return pipeline.inputs + job.inputs


def get_gitlab_ci_variable_name(pipeline: brettops.Pipeline, input: brettops.Input):
    return f"{pipeline.name}_{input.name}".upper()


def get_template_context(pipeline: brettops.Job, job: brettops.Job):
    context = {}
    # context["platform"] = {
    #     "machine": platform.machine(),
    #     "node": platform.node(),
    #     "release": platform.release(),
    #     "system": platform.system(),
    # }
    context["input"] = {
        input.name: f"{get_gitlab_ci_variable_name(pipeline=pipeline, input=input)}"
        for input in get_inputs(pipeline=pipeline, job=job)
    }
    return context


def dump_gitlab_ci_script(pipeline: brettops.Job, job: brettops.Job) -> typing.Any:
    env = Environment()
    context = get_template_context(pipeline=pipeline, job=job)
    lines = [line for script in job.scripts for line in script.script]
    lines = [env.from_string(line).render(context) for line in lines]
    return make_scalar_list(lines)


def dump_gitlab_ci_variable(
    pipeline: brettops.Pipeline, input: brettops.Input
) -> dict[str, str]:
    variables: dict[str, str] = {}
    if input.type not in (brettops.ARTIFACT_VARIABLE,):
        return variables
    variable_name = get_gitlab_ci_variable_name(pipeline=pipeline, input=input)
    variables[variable_name] = make_scalar_string(input.default, quote=True)
    return variables


def dump_gitlab_ci_variables(
    pipeline: brettops.Pipeline, inputs: list[brettops.Input]
) -> typing.Any:
    variables = {}
    for input in inputs:
        variables.update(dump_gitlab_ci_variable(pipeline=pipeline, input=input))
    return variables


def dump_gitlab_ci_artifacts_paths(
    outputs: list[brettops.Output],
) -> typing.Any:
    artifacts = {}
    paths = [output.value for output in outputs]
    if paths:
        artifacts["paths"] = paths
    return artifacts


def dump_gitlab_ci_artifacts(job: brettops.Job) -> typing.Any:
    artifacts = {}
    artifacts.update(dump_gitlab_ci_artifacts_paths(outputs=job.outputs))
    return artifacts


def dump_gitlab_ci_job(pipeline: brettops.Pipeline, job: brettops.Job) -> typing.Any:
    data = dict(
        stage=job.stage,
        image=dump_gitlab_ci_image(environment=job.environment),
        script=dump_gitlab_ci_script(pipeline=pipeline, job=job),
    )

    variables = dump_gitlab_ci_variables(pipeline=pipeline, inputs=job.inputs)
    if variables:
        data["variables"] = variables
    artifacts = dump_gitlab_ci_artifacts(job=job)
    if artifacts:
        data["artifacts"] = artifacts
    return data


def dump_gitlab_ci_workflow() -> typing.Any:
    return dict(
        rules=[
            {
                "if": """$CI_PIPELINE_SOURCE == "push" && $CI_OPEN_MERGE_REQUESTS""",
                "when": "never",
            },
            {
                "when": "always",
            },
        ]
    )


def dump_gitlab_ci_file(pipeline: brettops.Pipeline) -> typing.Any:
    data = {}
    data["stages"] = [stage.name for stage in pipeline.stages]
    data["workflow"] = dump_gitlab_ci_workflow()

    variables = dump_gitlab_ci_variables(pipeline=pipeline, inputs=pipeline.inputs)
    if variables:
        data["variables"] = variables

    for job in pipeline.jobs:
        job_name = f"{pipeline.name}-{job.name}"
        data[job_name] = dump_gitlab_ci_job(pipeline=pipeline, job=job)
    return data


def dumps(pipeline: brettops.Pipeline) -> str:
    output = io.StringIO()
    dump(pipeline, output)
    return output.getvalue()


def dump(pipeline: brettops.Pipeline, stream: typing.IO):
    data = dump_gitlab_ci_file(pipeline)
    validate_gitlab_ci(data)
    yaml = ruamel.yaml.YAML()
    yaml.default_flow_style = False
    yaml.explicit_start = False
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)

    for key, value in data.items():
        yaml.dump({key: value}, stream)
        stream.write("\n")
