import json
from enum import Enum
from textwrap import indent

from typing import Optional, Union, List

from janis_core.translations.nfgen.common import NFBase, filter_null
from janis_core.translations.nfgen.directives import ProcessDirective


class ProcessScriptType(Enum):
    script = "script"
    shell = "shell"
    exec = "exec"


class InputProcessQualifier(Enum):
    val = "val"
    env = "env"
    file = "file"
    path = "path"
    stdin = "stdin"
    tuple = "tuple"
    each = "each"


class OutputProcessQualifier(Enum):
    val = "val"
    file = "file"
    path = "path"
    env = "env"
    stdout = "stdout"
    tuple = "tuple"


class ProcessInput(NFBase):
    def __init__(
        self,
        qualifier: InputProcessQualifier,
        name: str,
        from_: Optional[str] = None,
        attributes: Optional[Union[str, List[str]]] = None,
        as_param: Optional[str] = None,
    ):
        self.qualifier = qualifier
        self.name = name
        self.from_ = from_
        self.attributes = attributes
        self.as_param = as_param

    def get_string(self):
        els = [self.qualifier.value, self.name]

        if self.from_:
            els.append(f"from {self.from_}")
        if self.attributes:
            if isinstance(self.attributes, list):
                els.extend(str(a) for a in self.attributes)
            else:
                els.append(str(self.attributes))

        return " ".join(str(e) for e in els).strip()


class ProcessOutput(NFBase):
    def __init__(
        self,
        qualifier: OutputProcessQualifier,
        name: str,
        expression: str,
        is_optional=False,
        into: Optional[Union[str, List[str]]] = None,
        attributes: Optional[Union[str, List[str]]] = None,
    ):

        self.qualifier = qualifier
        self.name = name
        self.expression = expression
        self.into = into
        self.optional = is_optional
        self.attributes = attributes

    def get_string(self):
        if self.qualifier != OutputProcessQualifier.tuple:
            self.expression = f'"${{{self.expression}}}"'

        els = [self.qualifier.value, f"{self.expression}"]

        if self.optional is True:
            els.extend(["optional", "true"])

        if self.into:
            intochannels = (
                ", ".join(str(i) for i in self.into)
                if isinstance(self.into, list)
                else str(self.into)
            )
            els.extend(["into", intochannels])
        if self.attributes:
            if isinstance(self.attributes, list):
                els.extend(str(a) for a in self.attributes)
            else:
                els.append(str(self.attributes))

        els.append(f", emit: {self.name}")

        return " ".join(str(e) for e in els).strip()


class TupleElementForOutput(NFBase):
    def __init__(
        self,
        qualifier: OutputProcessQualifier,
        expression: str,
    ):

        self.qualifier = qualifier
        self.expression = expression

    def get_string(self):
        return f'{self.qualifier.value}("${{{self.expression}}}")'


class Process(NFBase):
    def __init__(
        self,
        name: Optional[str],
        script: str,
        script_type: Optional[ProcessScriptType] = None,
        script_quote: Optional[str] = '"',
        inputs: List[ProcessInput] = None,
        outputs: List[ProcessOutput] = None,
        when: Optional[str] = None,
        directives: List[ProcessDirective] = None,
        pre_script: Optional[str] = None,
    ):

        self.name = name

        self.script = script
        self.script_type = script_type
        self.script_quote = script_quote

        self.inputs: List[ProcessInput] = inputs or []
        self.outputs: List[ProcessOutput] = outputs or []
        self.directives: List[ProcessDirective] = directives or []
        self.pre_script = pre_script

    def prepare_script(self, prefix="  "):
        script = str(self.script).strip()
        if self.script_quote:
            q = 3 * self.script_quote
            script = q + "\n" + script + "\n" + q

        script = indent(script, prefix)

        if self.pre_script:
            pre_script = indent(self.pre_script, prefix)
        else:
            pre_script = ""

        if self.script_type:
            script = indent(f"{self.script_type.value}:\n{pre_script}" + script, "  ")

        return script

    def prepare_inputs(self, prefix="  "):
        if not self.inputs:
            return None
        return indent(
            "input:\n" + "\n".join("  " + i.get_string() for i in self.inputs), "  "
        )

    def prepare_outputs(self, prefix="  "):
        if not self.outputs:
            return None
        return indent(
            "output:\n" + "\n".join(prefix + o.get_string() for o in self.outputs),
            "  ",
        )

    def prepare_directives(self, prefix="  "):
        if not self.directives:
            return None
        return "\n".join(prefix + d.get_string() for d in self.directives)

    def get_string(self):
        nl = "\n"
        components = filter_null(
            [
                self.prepare_inputs(),
                self.prepare_outputs(),
                self.prepare_directives(),
                self.prepare_script(),
            ]
        )
        name = self.name or ""
        tool_definition = (2 * nl).join(components)

        return f"""\

process {name}
{{
{tool_definition}
}}


"""
