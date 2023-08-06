#
# _filter_models.py - DeGirum Python SDK: common models filtering
# Copyright DeGirum Corp. 2022
#
# Contains DeGirum common models filtering implementation
#

import pdb
import re
from pathlib import Path

from .exceptions import DegirumException


def _filter_models(
    model_family=None,
    *,
    models,
    device=None,
    precision=None,
    pruned=None,
    runtime=None,
):
    """List all available model matching to specified filter values.

    - `models`: callback to acquire models info using model identifier
    - `model_family`: model family: a string to match any part of the model name; for example, "yolo", "mobilenet1"
    - `device`: target inference device(s): a string or a string list of device labels; possible labels: "orca", "orca1", "cpu", "edgetpu", "myriad"
    - `precision`: model calculation precision: a string or a string list of precision labels; possible labels: "quant", "float"
    - `pruned`: model density: a string or a string list of density labels; possible labels: "dense", "pruned"
    - `runtime`: type of inference runtime(s): a string or a string list of runtime labels; possible labels: "n2x", "tflite", "openvino"

    Returns list of matching model names
    """

    def _to_list(value):
        """Convert value to the list containing this value if it is not list already.
        Returns empty list if value is None
        """
        if not value:
            return []
        elif not isinstance(value, list):
            return [value]
        else:
            return value

    model_family = (
        [model_family]
        if isinstance(model_family, re.Pattern)
        else _to_list(model_family)
    )
    device = _to_list(device)
    precision = _to_list(precision)
    pruned = _to_list(pruned)
    runtime = _to_list(runtime)

    for (value, description, supported_values, check) in [
        (
            model_family,
            "model_family",
            ["yolo", "mobilenet", "..."],
            lambda f, l: not isinstance(f, str) and not isinstance(f, re.Pattern),
        ),
        (
            device,
            "device",
            ["ORCA", "ORCA1", "CPU", "EDGETPU", "MYRIAD"],
            lambda f, l: not isinstance(f, str) or f.upper() not in l,
        ),
        (
            precision,
            "precision",
            ["QUANT", "FLOAT"],
            lambda f, l: not isinstance(f, str) or f.upper() not in l,
        ),
        (
            pruned,
            "pruned",
            ["PRUNED", "DENSE"],
            lambda f, l: not isinstance(f, str) or f.upper() not in l,
        ),
        (
            runtime,
            "runtime",
            ["N2X", "TFLITE", "OPENVINO"],
            lambda f, l: not isinstance(f, str) or f.upper() not in l,
        ),
    ]:
        for f in value:
            if check(f, supported_values):
                raise DegirumException(
                    f"Filter {description} has unsupported value {f}. Possible values are {supported_values}"
                )

    def re_filter(mparams, l):
        return l[0].match(Path(mparams.ModelPath).stem)

    def str_filter(mparams, l):
        return any(n in Path(mparams.ModelPath).stem for n in l)

    def density_filter(mparams):
        name = Path(mparams.ModelPath).stem
        p = name.split("--")[-1].split("_")[::-1]
        return "PRUNED" if len(p) >= 5 and p[4].upper() == "PRUNED" else "DENSE"

    filters_configuration = [
        (
            model_family,
            re_filter
            if model_family and isinstance(model_family[0], re.Pattern)
            else str_filter,
        ),
        (
            [s.upper() for s in device],
            lambda mparams, l: mparams.DeviceType in l,
        ),
        (
            [s.upper() for s in runtime],
            lambda mparams, l: mparams.RuntimeAgent in l,
        ),
        (
            [True if s.upper() == "QUANT" else False for s in precision],
            lambda mparams, l: mparams.ModelQuantEn in l,
        ),
        ([s.upper() for s in pruned], lambda mparams, l: density_filter(mparams) in l),
    ]

    current = models()
    for filter_to_check, check_function in filters_configuration:
        if filter_to_check:
            current = [v for v in current if check_function(models(v), filter_to_check)]

    return current
