__all__ = ["read_config", "read_configs"]

from .types import Config, FileLike, Variable

from dataclasses import dataclass
import dataclasses

import ast
import re


@dataclass
class Regexes:
    section: re.Pattern[str]
    comment: re.Pattern[str]
    variable: re.Pattern[str]


regexes = Regexes(
    section=re.compile(r"^\[(?P<section>.*)\](#.*)?$"),
    comment=re.compile(r"^[#;]\s?(?P<comment>.*)$"),
    variable=re.compile(
        r"^(?P<name>\w+)\s*(:\s*(?P<type>\w+))?\s*((?P<not_required>=)\s*(?P<value>.*))?\s*([#;].*)?$"
    ),
)


def read_config(config: FileLike, preconfig: Config | None = None) -> Config:
    if isinstance(config, str):
        with open(config) as file:
            return read_config(file, preconfig)
    result: Config = dict(**(preconfig or {}))
    result.setdefault("DEFAULT", {})

    @dataclass
    class Current:
        section: str
        description: list[str]

    current = Current(section="DEFAULT", description=[])
    for i in config:
        match i.strip():
            case "":
                current.description = []

            case i if m := regexes.section.match(i):
                current.section = m.group("section")
                result[current.section] = result.get(current.section, {})
                current.description = []

            case i if m := regexes.comment.match(i):
                current.description += [m.group("comment")]

            case i if m := regexes.variable.match(i):
                variable_name = m.group("name").strip()
                variable_value = ast.literal_eval(m.group("value") or "None")
                variable_exact_type = m.group("type")
                variable_inferred_type = variable_exact_type or (
                    typename
                    if (typename := type(variable_value).__name__) != "NoneType"
                    else None
                )
                current_variable = result[current.section].get(
                    variable_name, Variable()
                )

                result[current.section][variable_name] = dataclasses.replace(
                    current_variable,
                    value=variable_value,
                    required=m.group("not_required") is None,
                    **(
                        (
                            dict(description="\n".join(current.description))
                            if current.description
                            else {}
                        )
                        | (
                            dict(type=variable_inferred_type)
                            if (current_variable.type is None or variable_exact_type)
                            and variable_inferred_type
                            else {}
                        )
                    ),
                )

                current.description = []

            case i:
                raise ValueError(f"Could not parse line: {i}")

    return result


def read_configs(
    filenames: FileLike | list[FileLike], preconfig: Config | None = None
) -> Config:
    result = dict(**(preconfig or {}))
    if not isinstance(filenames, list):
        filenames = [filenames]

    for file in filenames:
        result = read_config(file, result)

    return result
