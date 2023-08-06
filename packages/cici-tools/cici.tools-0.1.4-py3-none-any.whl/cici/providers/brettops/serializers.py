import functools
import io
import typing

import cattrs
import ruamel.yaml
from cattrs.gen import make_dict_unstructure_fn, override

from ...utils import make_quoted_scalar_string, make_scalar_list
from .models import Input, Pipeline, Script


@functools.cache
def get_converter():
    converter = cattrs.Converter(omit_if_default=True, forbid_extra_keys=True)
    converter.register_unstructure_hook(
        Script,
        make_dict_unstructure_fn(
            Script,
            converter,
            script=override(unstruct_hook=make_scalar_list),
            _cattrs_omit_if_default=True,
        ),
    )
    converter.register_unstructure_hook(
        Input,
        make_dict_unstructure_fn(
            Input,
            converter,
            default=override(unstruct_hook=make_quoted_scalar_string),
            _cattrs_omit_if_default=True,
        ),
    )
    return converter


def loads(text: str) -> Pipeline:
    yaml = ruamel.yaml.YAML()
    data = yaml.load(text)
    converter = cattrs.Converter(omit_if_default=True, forbid_extra_keys=True)
    return converter.structure(data, Pipeline)


def load(file: typing.IO) -> Pipeline:
    return loads(open(file).read())


def dumps(pipeline: Pipeline) -> str:
    output = io.StringIO()
    dump(pipeline, output)
    return output.getvalue()


def dump(pipeline: Pipeline, stream: typing.IO):
    converter = get_converter()
    data = converter.unstructure(pipeline)
    yaml = ruamel.yaml.YAML()
    yaml.dump(data, stream)
