import typing

import attrs
from attrs import define, field

from .constants import ARTIFACT_TYPES, ARTIFACT_VARIABLE


@define(frozen=True, kw_only=True, slots=True)
class Input:
    name: str
    type: str = field(
        default=ARTIFACT_VARIABLE, validator=attrs.validators.in_(ARTIFACT_TYPES)
    )

    default: str = ""
    description: str = ""


@define(frozen=True, kw_only=True, slots=True)
class Output:
    name: str
    type: str = field(validator=attrs.validators.in_(ARTIFACT_TYPES))
    value: str

    description: str = ""


@define(frozen=True, kw_only=True, slots=True)
class Environment:
    image: str
    entrypoint: list[str] = field(factory=list)
    variables: dict[str, str] = field(factory=dict)


@define(frozen=True, kw_only=True, slots=True)
class Script:
    script: list[str]
    name: str = ""
    description: str = ""


@define(frozen=True, kw_only=True, slots=True)
class ScriptInclude:
    name: str


@define(frozen=True, kw_only=True, slots=True)
class Job:
    name: str
    stage: str
    scripts: list[Script]
    environment: typing.Optional[Environment] = None
    inputs: list[Input] = field(factory=list)
    outputs: list[Output] = field(factory=list)
    description: str = ""


@define(frozen=True, kw_only=True, slots=True)
class Include:
    repository: str
    ref: str = ""
    jobs: list[str]


@define(frozen=True, kw_only=True, slots=True)
class Stage:
    name: str


@define(frozen=True, kw_only=True, slots=True)
class Pipeline:
    name: str
    stages: list[Stage]
    includes: list[Include] = field(factory=list)
    inputs: list[Input] = field(factory=list)
    jobs: list[Job]
