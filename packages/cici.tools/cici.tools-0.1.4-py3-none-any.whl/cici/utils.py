import typing

from ruamel.yaml.scalarstring import (
    DoubleQuotedScalarString,
    FoldedScalarString,
    PreservedScalarString,
)


def merge_dict(orig: dict, new: dict) -> dict:
    final = {}

    all_keys = sorted(list(set(orig.keys()) | set(new.keys())))
    for key in all_keys:
        if key in orig and key in new:
            if isinstance(orig[key], dict):
                if not isinstance(new[key], dict):
                    raise NotImplementedError("Can't merge dict and non-dict keys")
                final[key] = merge_dict(orig[key], new[key])
            else:
                final[key] = new[key]  # new takes precedence
        elif key in orig:
            final[key] = orig[key]
        elif key in new:
            final[key] = new[key]
        else:
            raise NotImplementedError("This should not possible")
    return final


def make_scalar_string(line, quote=False):
    if "\n" in line.strip():
        return PreservedScalarString(line)
    elif len(line) >= 80:
        return FoldedScalarString(line)
    elif quote:
        return DoubleQuotedScalarString(line)
    return line


def make_quoted_scalar_string(line):
    return make_scalar_string(line, quote=True)


def make_scalar_list(value: list[str]) -> list[typing.Any]:
    return [make_scalar_string(line) for line in value]
